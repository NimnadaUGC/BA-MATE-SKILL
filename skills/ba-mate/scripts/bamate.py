#!/usr/bin/env python3
"""BA Mate local integrity helper. Python 3.10+, standard library only.

Human attestations are recorded assertions, not authentication or semantic proof.
All workspace state changes use a single locked, atomic state-file replacement.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from datetime import datetime, timezone
from contextlib import contextmanager
import uuid

PACKAGE_VERSION = '1.0.0'
FRAMEWORK_VERSION = 'F4-draft.1'
SCHEMA_VERSION = 1
TYPES = {'scope', 'stakeholder', 'authority', 'source', 'context', 'clarification',
         'requirement', 'business-rule', 'story', 'criterion', 'process', 'finding',
         'assumption', 'risk', 'issue', 'decision', 'proposal', 'document', 'approval', 'change'}
STATUSES = {'draft', 'in-review', 'confirmed', 'rejected', 'open', 'resolved',
            'deferred', 'excluded', 'not-applicable'}
ARTIFACTS = {'requirement', 'business-rule', 'story', 'criterion', 'process', 'document'}
SUBSTANTIVE = {'requirement', 'business-rule', 'story', 'criterion'}
UNCERTAINTY = {'clarification', 'finding', 'assumption', 'risk', 'issue'}
DISPOSED = {'resolved', 'rejected', 'excluded', 'not-applicable'}
ID = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,79}$')


class IntegrityError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise IntegrityError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n'


def digest(value):
    return hashlib.sha256(encode(value).encode('utf-8')).hexdigest()


def read_json(path):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'Duplicate JSON key: ' + key)
            out[key] = value
        return out
    def bad_constant(value):
        raise IntegrityError('Non-finite JSON number: ' + value)
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=bad_constant)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def integer(value):
    return type(value) is int and value > 0


def ref(value):
    need(isinstance(value, dict) and set(value) == {'id', 'revision'}, 'Reference must contain id and revision only')
    need(isinstance(value['id'], str) and ID.fullmatch(value['id']) and integer(value['revision']), 'Invalid reference')
    return value['id'], value['revision']


def pointer(record):
    return {'id': record['id'], 'revision': record['revision']}


def attestation(value):
    need(isinstance(value, dict) and all(nonempty(value.get(k)) for k in ('actor', 'at', 'basis')),
         'Human attestation requires actor, at and basis')
    timestamp(value['at'])


def timestamp(value):
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        need(dt.tzinfo is not None, 'Timestamp requires a timezone')
    except ValueError as exc:
        raise IntegrityError('Invalid timestamp') from exc


def latest(items):
    out = {}
    for item in items:
        if item['id'] not in out or item['revision'] > out[item['id']]['revision']:
            out[item['id']] = item
    return out


def blank():
    return {'schema_version': SCHEMA_VERSION, 'package_version': PACKAGE_VERSION,
            'framework_version': FRAMEWORK_VERSION, 'workspace_revision': 1,
            'records': [], 'traces': [], 'pending_reviews': [],
            'baselines': [], 'checkpoints': [], 'events': []}


def snapshot(state):
    return {k: copy.deepcopy(state[k]) for k in ('records', 'traces', 'pending_reviews')}


def check_records(state):
    need(isinstance(state, dict), 'Workspace must be an object')
    need(set(state) == set(blank()), 'Unexpected or missing workspace fields')
    need(type(state['schema_version']) is int and state['schema_version'] == SCHEMA_VERSION, 'Unsupported record schema')
    need(state['framework_version'] == FRAMEWORK_VERSION, 'Unsupported framework version')
    need(nonempty(state['package_version']) and integer(state['workspace_revision']), 'Invalid workspace metadata')
    for k in ('records', 'traces', 'pending_reviews', 'baselines', 'checkpoints', 'events'):
        need(isinstance(state[k], list), k + ' must be an array')
    index = {}
    seen_types = {}
    for r in state['records']:
        need(isinstance(r, dict) and set(r) == {'id', 'revision', 'type', 'status', 'scope', 'origin', 'at', 'content', 'references', 'review'}, 'Invalid record fields')
        key = ref(pointer(r))
        need(key not in index, 'Duplicate record revision')
        need(r['type'] in TYPES and r['status'] in STATUSES, 'Invalid record type or status')
        need(r['id'] not in seen_types or seen_types[r['id']] == r['type'], 'Record type cannot change across revisions')
        seen_types[r['id']] = r['type']
        origin = r['origin']
        need(isinstance(origin, dict) and set(origin) == {'kind', 'actor'} and origin['kind'] in {'human', 'ai', 'source', 'unknown'} and
             (origin['actor'] is None or nonempty(origin['actor'])), 'Invalid record origin')
        need(r['at'] is None or nonempty(r['at']), 'Record time must be text or null')
        if r['at'] is not None:
            timestamp(r['at'])
        need(isinstance(r['content'], dict) and isinstance(r['references'], list), 'Invalid record content or references')
        if r['review'] is not None:
            attestation(r['review'])
        if r['type'] == 'scope':
            need(r['scope'] is None, 'Scope records cannot belong to another scope')
        else:
            ref(r['scope'])
        for p in r['references']:
            ref(p)
        if r['type'] in ARTIFACTS:
            need(nonempty(r['content'].get('text')), 'BA artifacts require nonempty text')
        if r['type'] == 'clarification':
            need(nonempty(r['content'].get('question')) and r['content'].get('priority') in {'blocking', 'important', 'optional'}, 'Clarification requires a question and explicit lowercase priority')
        if r['type'] in {'finding', 'risk', 'issue', 'assumption'}:
            need(nonempty(r['content'].get('text')) and r['content'].get('severity') in {'blocking', 'important', 'optional', 'low', 'medium', 'high'}, 'Uncertainty requires text and explicit lowercase severity')
        if r['type'] in UNCERTAINTY and r['status'] in DISPOSED:
            attestation(r['content'].get('disposition'))
        if r['type'] == 'source':
            for flag in ('extraction_reviewed', 'relevant'):
                need(type(r['content'].get(flag)) is bool, 'Source review/relevance flags must be booleans')
        if r['type'] in {'clarification', 'decision', 'authority', 'approval'} and r['status'] == 'confirmed':
            need(origin['kind'] == 'human' and nonempty(origin['actor']), 'Confirmed business decisions require an identified human origin')
        if r['type'] == 'clarification' and r['status'] == 'confirmed':
            need(all(nonempty(r['content'].get(k)) for k in ('answer', 'respondent', 'authority_basis')), 'Confirmed clarification requires actual answer, respondent and authority basis')
        if r['type'] == 'authority' and r['status'] == 'confirmed':
            need(all(nonempty(r['content'].get(k)) for k in ('person', 'role', 'basis')), 'Authority requires person, role and basis')
        if r['type'] == 'proposal':
            need(nonempty(r['content'].get('original')) and isinstance(r['content'].get('context'), list), 'Proposal requires original output and context manifest')
            for p in r['content']['context']:
                ref(p)
            need(r['content'].get('disposition') in {'pending', 'adopted', 'rejected', 'failed'}, 'Invalid proposal disposition')
            if r['content']['disposition'] == 'adopted':
                attestation(r['content'].get('adoption'))
                need(isinstance(r['content'].get('selected'), list) and r['content']['selected'], 'Adoption requires selected output references')
                for p in r['content']['selected']:
                    ref(p)
        if r['type'] == 'approval':
            c = r['content']
            need(c.get('decision') in {'approved', 'rejected'}, 'Invalid approval decision')
            ref(c.get('authority'))
            attestation(c.get('human_decision'))
            for field in ('manifest', 'excluded', 'accepted_issues'):
                need(isinstance(c.get(field), list), 'Approval requires ' + field)
                for p in c[field]:
                    ref(p)
            need(c['manifest'] and len({ref(p) for p in c['manifest']}) == len(c['manifest']), 'Approval manifest must be nonempty and unique')
            need(not ({ref(p) for p in c['manifest']} & {ref(p) for p in c['excluded']}), 'Approval scope cannot include excluded items')
        index[key] = r
    for record_id in seen_types:
        versions = sorted(r['revision'] for r in state['records'] if r['id'] == record_id)
        need(versions == list(range(1, len(versions) + 1)), 'Record revisions must be contiguous from 1')
    for r in index.values():
        if r['scope'] is not None:
            need(ref(r['scope']) in index and index[ref(r['scope'])]['type'] == 'scope', 'Missing scope reference')
        references = list(r['references'])
        if r['type'] == 'approval':
            references += [r['content']['authority']] + sum((r['content'][k] for k in ('manifest', 'excluded', 'accepted_issues')), [])
        if r['type'] == 'proposal':
            references += r['content']['context'] + r['content'].get('selected', [])
        need(all(ref(p) in index for p in references), 'Record cites unavailable evidence or artifacts')
    trace_index = {}
    for t in state['traces']:
        need(isinstance(t, dict) and set(t) == {'id', 'revision', 'from', 'to', 'relation', 'status', 'verification'}, 'Invalid trace fields')
        key = ref(pointer(t))
        need(key not in trace_index and t['id'] not in seen_types, 'Duplicate or conflicting trace ID')
        need(ref(t['from']) in index and ref(t['to']) in index and ref(t['from']) != ref(t['to']), 'Invalid trace endpoint')
        need(index[ref(t['from'])]['scope'] == index[ref(t['to'])]['scope'], 'Trace endpoints must belong to the same scope')
        need(t['relation'] in {'supports', 'depends-on'} and t['status'] in {'proposed', 'verified', 'stale'}, 'Invalid trace relationship or status')
        if t['status'] == 'verified':
            attestation(t['verification'])
        elif t['verification'] is not None:
            attestation(t['verification'])
        trace_index[key] = t
    for trace_id in {t['id'] for t in state['traces']}:
        versions = sorted(t['revision'] for t in state['traces'] if t['id'] == trace_id)
        need(versions == list(range(1, len(versions) + 1)), 'Trace revisions must be contiguous from 1')
    for p in state['pending_reviews']:
        need(ref(p) in index, 'Missing pending-review target')
    for collection in ('baselines', 'checkpoints'):
        ids = set()
        for item in state[collection]:
            need(isinstance(item, dict) and nonempty(item.get('id')) and item['id'] not in ids, 'Invalid snapshot identity')
            ids.add(item['id'])
            need(isinstance(item.get('snapshot'), dict) and set(item['snapshot']) == {'records', 'traces', 'pending_reviews'}, 'Invalid snapshot contents')
            need(item.get('sha256') == digest(item['snapshot']), 'Snapshot integrity mismatch')
            sub = blank()
            sub.update(item['snapshot'])
            check_records(sub)
            if collection == 'baselines':
                need(isinstance(item.get('approval'), dict), 'Baseline approval reference missing')
                approval_issues(sub, item['approval'], historical=True)
    return index


def affected(state, changed_ids):
    touched = set(changed_ids)
    current = latest(state['records'])
    while True:
        before = set(touched)
        for r in current.values():
            if any(p['id'] in touched for p in r['references']) or (r['scope'] and r['scope']['id'] in touched):
                touched.add(r['id'])
        for t in latest(state['traces']).values():
            if t['from']['id'] in touched:
                touched.add(t['to']['id'])
        if before == touched:
            return touched


def closure(index, seeds):
    result = set(seeds)
    while True:
        before = set(result)
        for key in before:
            r = index[key]
            result.update(ref(p) for p in r['references'])
            if r['scope']:
                result.add(ref(r['scope']))
        if result == before:
            return result


def approval_issues(state, approval_ref, historical=False):
    index = {(r['id'], r['revision']): r for r in state['records']}
    current = latest(state['records'])
    key = ref(approval_ref)
    need(key in index and index[key]['type'] == 'approval', 'Approval record not found')
    approval = index[key]
    need(approval['status'] == 'confirmed' and approval['origin']['kind'] == 'human' and approval['content']['decision'] == 'approved', 'An explicit confirmed human approval is required')
    need(historical or pointer(current[approval['id']]) == approval_ref, 'Approval was superseded')
    c = approval['content']
    authority = index[ref(c['authority'])]
    need(authority['type'] == 'authority' and authority['status'] == 'confirmed' and authority['scope'] == approval['scope'], 'Authority must be confirmed for this scope')
    need(authority['content']['person'] == c['human_decision']['actor'], 'Decision actor does not match the recorded authority')
    manifest = {ref(p) for p in c['manifest']}
    chosen = [index[k] for k in manifest]
    need(all(r['type'] in ARTIFACTS and r['scope'] == approval['scope'] for r in chosen), 'Approval manifest must select artifacts within one scope')
    need(any(r['type'] in SUBSTANTIVE for r in chosen), 'Baseline needs a substantive BA artifact')
    dependencies = closure(index, manifest | {ref(c['authority']), ref(approval['scope'])})
    need(all(k in manifest for k in dependencies if index[k]['type'] in ARTIFACTS), 'Include linked BA artifacts in the approval manifest')
    need(all(pointer(current[rid]) == {'id': rid, 'revision': rev} for rid, rev in dependencies), 'Approval depends on stale revisions')
    need(not (dependencies & {ref(p) for p in state['pending_reviews']}), 'Affected dependencies require human revalidation')
    for r in chosen:
        need(r['status'] == 'in-review' and r['review'] is not None, 'Selected artifacts require human review')
        if r['type'] in {'requirement', 'business-rule', 'story'}:
            criteria = [a for a in chosen if a['type'] == 'criterion' and pointer(r) in a['references'] and nonempty(a['content'].get('text'))]
            exception = r['content'].get('criteria_exception')
            if exception is not None:
                attestation(exception)
            need(criteria or exception is not None, 'Include current acceptance criteria or a human justified exception')
    def supported(k, visited=None):
        visited = set() if visited is None else visited
        if k in visited:
            return False
        visited = visited | {k}
        r = index[k]
        if r['status'] in {'excluded', 'rejected', 'not-applicable'} or pointer(current[r['id']]) != pointer(r):
            return False
        if r['type'] == 'source':
            return r['review'] is not None and r['content'].get('extraction_reviewed') is True and r['content'].get('relevant') is True and nonempty(r['content'].get('text')) and nonempty(r['content'].get('provenance'))
        if r['type'] in {'clarification', 'decision'}:
            return r['status'] == 'confirmed' and r['origin']['kind'] == 'human' and r['review'] is not None
        for t in latest(state['traces']).values():
            if t['status'] == 'verified' and t['relation'] == 'supports' and ref(t['to']) == k and supported(ref(t['from']), visited):
                return True
        return False
    for r in chosen:
        if r['type'] in SUBSTANTIVE:
            need(supported(ref(pointer(r))), 'Missing current human-verified supporting evidence path: ' + r['id'])
    # Include trace-only supporting ancestors in freshness and uncertainty checks.
    relevant = set(dependencies)
    while True:
        before = set(relevant)
        for t in latest(state['traces']).values():
            if ref(t['to']) in relevant and t['status'] == 'verified':
                relevant.add(ref(t['from']))
        relevant = closure(index, relevant)
        if relevant == before:
            break
    need(all(pointer(current[rid]) == {'id': rid, 'revision': rev} for rid, rev in relevant), 'Supporting trace refers to stale evidence')
    need(not (relevant & {ref(p) for p in state['pending_reviews']}), 'Supporting evidence requires revalidation')
    for t in latest(state['traces']).values():
        if ref(t['to']) in relevant:
            need(t['status'] == 'verified' and pointer(current[t['from']['id']]) == t['from'] and pointer(current[t['to']['id']]) == t['to'], 'Resolve proposed or stale supporting/dependency links')
    accepted = {ref(p) for p in c['accepted_issues']}
    for p in c['excluded']:
        excluded = index[ref(p)]
        need(excluded['type'] in ARTIFACTS and excluded['scope'] == approval['scope'], 'Excluded approval items must be BA artifacts within this scope')
    for k in accepted:
        issue = index[k]
        need(issue['type'] in UNCERTAINTY and issue['scope'] == approval['scope'] and pointer(current[issue['id']]) == pointer(issue), 'Accepted uncertainty must identify current items within this scope')
        need(issue['content'].get('priority') != 'blocking' and issue['content'].get('severity') != 'blocking', 'A blocker cannot be accepted as nonblocking uncertainty')
        attestation(issue['content'].get('disposition'))
    for r in current.values():
        if r['type'] not in UNCERTAINTY or r['scope'] != approval['scope'] or r['status'] in DISPOSED:
            continue
        if r['type'] == 'clarification' and r['status'] == 'confirmed':
            continue
        targets = {ref(p) for p in r['references']}
        if targets and not {rid for rid, _ in targets} & {rid for rid, _ in relevant} and ref(pointer(r)) not in relevant:
            continue
        blocking = r['content'].get('priority') == 'blocking' or r['content'].get('severity') == 'blocking'
        need(not blocking, 'Unresolved blocking item: ' + r['id'])
        need(ref(pointer(r)) in accepted, 'Explicitly dispose of nonblocking uncertainty: ' + r['id'])
        attestation(r['content'].get('disposition'))
    return {'eligible': True, 'manifest': c['manifest'], 'limitations': ['Structural checks only; human assertions are not authenticated or semantically certified.']}


def apply_patch(state, patch):
    need(isinstance(patch, dict) and set(patch) <= {'records', 'traces', 'revalidated'} and patch, 'Patch accepts records, traces and revalidated only')
    for k, v in patch.items():
        need(isinstance(v, list), k + ' must be an array')
    out = copy.deepcopy(state)
    prior_ids = set(latest(state['records']))
    changed = set()
    for r in patch.get('records', []):
        need(isinstance(r, dict) and 'id' in r and 'revision' in r, 'Invalid patch record')
        existing = latest(out['records']).get(r['id'])
        need(r['revision'] == (existing['revision'] + 1 if existing else 1), 'Record patch must append the next revision')
        if existing:
            changed.add(r['id'])
            if existing['type'] == 'proposal':
                need(r.get('content', {}).get('original') == existing['content']['original'] and
                     r.get('content', {}).get('context') == existing['content']['context'],
                     'Proposal original output and context are immutable; create a new proposal')
        out['records'].append(copy.deepcopy(r))
    for t in patch.get('traces', []):
        need(isinstance(t, dict) and 'id' in t and 'revision' in t, 'Invalid patch trace')
        existing = latest(out['traces']).get(t['id'])
        need(t['revision'] == (existing['revision'] + 1 if existing else 1), 'Trace patch must append the next revision')
        out['traces'].append(copy.deepcopy(t))
        if existing:
            changed.add(existing['to']['id'])
        if isinstance(t.get('to'), dict) and t['to'].get('id') in prior_ids:
            changed.add(t['to']['id'])
    check_records(out)
    touched = affected(out, changed)
    current = latest(out['records'])
    pending = {ref(p) for p in out['pending_reviews']}
    pending = {ref(pointer(current[rid])) for rid, _ in pending}
    pending |= {ref(pointer(current[rid])) for rid in touched}
    for item in patch.get('revalidated', []):
        need(isinstance(item, dict) and set(item) == {'target', 'human_review'}, 'Invalid revalidation')
        target = ref(item['target'])
        need(target[0] in current and pointer(current[target[0]]) == item['target'], 'Revalidation must identify a current revision')
        attestation(item['human_review'])
        pending.discard(target)
    out['pending_reviews'] = [{'id': rid, 'revision': rev} for rid, rev in sorted(pending)]
    # Context staleness is checked on adoption, including proposals first supplied as adopted.
    for r in patch.get('records', []):
        if r['type'] == 'proposal' and r['content']['disposition'] == 'adopted':
            need(all(pointer(current[p['id']]) == p for p in r['content']['context']), 'Cannot adopt a stale proposal')
            for p in r['content']['selected']:
                selected = current[p['id']]
                need(pointer(selected) == p and selected['type'] in ARTIFACTS and selected['status'] == 'draft', 'Adoption selects current draft artifacts only')
        if r['type'] == 'approval' and r['status'] == 'confirmed' and r['content']['decision'] == 'approved':
            approval_issues(out, pointer(r))
    out['events'].append({'action': 'apply', 'at': now(), 'changed_ids': sorted(touched),
                          'revalidated': copy.deepcopy(patch.get('revalidated', []))})
    check_records(out)
    return out


def capture(state, kind, approval=None):
    out = copy.deepcopy(state)
    item = {'id': ('BL-' if kind == 'baselines' else 'CP-') + uuid.uuid4().hex[:12],
            'at': now(), 'workspace_revision': state['workspace_revision'], 'snapshot': snapshot(state)}
    item['sha256'] = digest(item['snapshot'])
    if approval is not None:
        approval_issues(state, approval)
        need(not any(b['approval'] == approval for b in state['baselines']), 'This approval already has a baseline')
        item['approval'] = approval
    out[kind].append(item)
    out['events'].append({'action': kind, 'at': item['at'], 'snapshot_id': item['id']})
    return out, item['id']


def restore(state, checkpoint_id, human_review):
    attestation(human_review)
    matches = [c for c in state['checkpoints'] if c['id'] == checkpoint_id]
    need(len(matches) == 1, 'Checkpoint not found')
    saved = matches[0]['snapshot']
    # The pre-restore working state is retained in the same atomic transaction.
    out, recovery_id = capture(state, 'checkpoints')
    existing = latest(out['records'])
    saved_current = latest(saved['records'])
    restored = {rid: r for rid, r in saved_current.items() if r['type'] not in {'approval', 'proposal'}}
    # Both recovered and later excluded records need coherent recovered scope refs.
    refs = {rid: {'id': rid, 'revision': r['revision'] + 1}
            for rid, r in existing.items() if r['type'] not in {'approval', 'proposal'}}
    records = []
    for rid, r in restored.items():
        new = copy.deepcopy(r)
        new['revision'] = refs[rid]['revision']
        new['status'] = 'draft'
        new['review'] = None
        new['at'] = now()
        new['origin'] = {'kind': 'human', 'actor': human_review['actor']}
        if new['scope']:
            new['scope'] = refs[new['scope']['id']]
        new['references'] = [refs.get(p['id'], p) for p in new['references']]
        if new['type'] == 'source':
            new['content']['extraction_reviewed'] = False
        records.append(new)
    for rid, r in existing.items():
        if rid not in restored and r['type'] not in {'approval', 'proposal'}:
            new = copy.deepcopy(r)
            new.update(revision=r['revision'] + 1, status='excluded', review=None, at=now())
            if new['scope']:
                new['scope'] = refs[new['scope']['id']]
            new['references'] = [refs.get(p['id'], p) for p in new['references']]
            if new['type'] in UNCERTAINTY:
                new['content']['disposition'] = copy.deepcopy(human_review)
            records.append(new)
    traces = []
    saved_traces = latest(saved['traces'])
    current_traces = latest(out['traces'])
    for tid in set(saved_traces) | set(current_traces):
        t = copy.deepcopy(saved_traces.get(tid, current_traces[tid]))
        t['revision'] = current_traces[tid]['revision'] + 1
        t['from'] = refs.get(t['from']['id'], t['from'])
        t['to'] = refs.get(t['to']['id'], t['to'])
        t['status'] = 'proposed' if tid in saved_traces else 'stale'
        t['verification'] = None
        traces.append(t)
    out = apply_patch(out, {'records': records, 'traces': traces})
    out['events'].append({'action': 'restore', 'at': now(), 'checkpoint_id': checkpoint_id,
                          'recovery_id': recovery_id, 'human_review': human_review})
    return out


def render(state, baseline_id=None, ids=None, handover=False):
    check_records(state)
    manifest = None
    if baseline_id:
        matches = [b for b in state['baselines'] if b['id'] == baseline_id]
        need(len(matches) == 1, 'Baseline not found')
        base = matches[0]
        sub = blank()
        sub.update(base['snapshot'])
        approval_issues(sub, base['approval'], historical=True)
        state = sub
        approval = {(r['id'], r['revision']): r for r in state['records']}[ref(base['approval'])]
        manifest = {ref(p) for p in approval['content']['manifest']}
        label = 'Historical approved baseline ' + baseline_id + ' (decision recorded ' + approval['content']['human_decision']['at'] + ')'
    else:
        label = 'Working DRAFT — not a current approval certificate'
    current = latest(state['records'])
    if ids:
        need(set(ids) <= set(current), 'Export selection includes unknown IDs')
        chosen = [current[i] for i in ids]
        need(all(r['type'] in ARTIFACTS for r in chosen), 'Export selection must contain BA artifacts')
        if manifest is not None:
            need(all(ref(pointer(r)) in manifest for r in chosen), 'Cannot export an unapproved item as baseline content')
    else:
        chosen = [r for r in current.values() if r['type'] in ARTIFACTS and r['status'] != 'excluded' and
                  (manifest is None or ref(pointer(r)) in manifest)]
    chosen.sort(key=lambda r: r['id'])
    chosen_scopes = {ref(r['scope']) for r in chosen}
    lines = ['# BA Mate ' + ('developer handover' if handover else 'artifact export'), '', label, '',
             'Framework: ' + FRAMEWORK_VERSION + ' · record schema: 1', '',
             'Human decisions and semantic checks are recorded assertions; the helper does not authenticate them.', '']
    if manifest:
        lines += ['Approved revision manifest: ' + ', '.join(f'{rid} r{rev}' for rid, rev in sorted(manifest)), '']
        lines += ['Approval decision (including exclusions and accepted issues):', '```json', encode(approval).strip(), '```', '']
    if handover:
        lines += ['Technical architecture is unspecified unless explicitly present in the selected BA records.', '']
    for r in chosen:
        lines += [f"## {r['id']} r{r['revision']} · {r['type']}", '', 'Recorded working status: ' + r['status'], '']
        if nonempty(r['content'].get('text')):
            lines += [r['content']['text'], '']
        lines += ['Exact record:', '```json', encode(r).strip(), '```', '']
    index = {(r['id'], r['revision']): r for r in state['records']}
    dependencies = closure(index, {ref(pointer(r)) for r in chosen})
    # Trace-only ancestors are provenance too; include their exact revisions.
    while True:
        before = set(dependencies)
        for t in latest(state['traces']).values():
            if ref(t['to']) in dependencies:
                dependencies.add(ref(t['from']))
        dependencies = closure(index, dependencies)
        if before == dependencies:
            break
    provenance = [index[k] for k in sorted(dependencies) if k not in {ref(pointer(r)) for r in chosen}]
    if manifest:
        context_refs = [approval['content']['authority']] + approval['content']['excluded'] + approval['content']['accepted_issues']
        lines += ['## Approval context (excluded records are outside the approved manifest)', '', '```json',
                  encode([index[k] for k in sorted({ref(p) for p in context_refs})]).strip(), '```', '']
    lines += ['## Referenced records', '', '```json', encode(provenance).strip(), '```', '', '## Trace records', '', '```json',
              encode([t for t in latest(state['traces']).values() if ref(t['to']) in dependencies]).strip(), '```', '',
              '## Open decisions and uncertainty', '', '```json',
              encode([r for r in current.values() if r['scope'] is not None and ref(r['scope']) in chosen_scopes and r['type'] in UNCERTAINTY and
                      r['status'] not in DISPOSED and not (r['type'] == 'clarification' and r['status'] == 'confirmed')]).strip(), '```', '',
              '## Pending impact/revalidation', '', '```json', encode([p for p in state['pending_reviews'] if ref(p) in dependencies]).strip(), '```', '']
    return '\n'.join(lines)


def atomic_write(path, value):
    need(not path.is_symlink(), 'Refusing a symlinked state file')
    fd, tmp = tempfile.mkstemp(prefix='.state-', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(encode(value))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def locked(workspace):
    need(not workspace.is_symlink(), 'Refusing a symlinked workspace')
    lock = workspace / '.write.lock'
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise IntegrityError('Workspace is locked; do not remove the lock while a writer is active') from exc
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(str(os.getpid()))
        yield
    finally:
        lock.unlink()


def mutate(workspace, expected_revision, operation):
    with locked(workspace):
        path = workspace / 'state.json'
        need(not path.is_symlink(), 'Refusing a symlinked state file')
        state = read_json(path)
        check_records(state)
        need(state['workspace_revision'] == expected_revision, 'Stale workspace revision; reload and reconcile')
        before = digest(state)
        out = operation(copy.deepcopy(state))
        out['workspace_revision'] = state['workspace_revision'] + 1
        check_records(out)
        need(digest(read_json(path)) == before, 'State changed outside this transaction; nothing applied')
        atomic_write(path, out)
        return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=f'BA Mate {PACKAGE_VERSION}; {FRAMEWORK_VERSION}; schema {SCHEMA_VERSION}')
    parser.add_argument('--workspace', type=Path, default=Path('ba-mate-workspace'))
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('initialise', aliases=['init'])
    validation = commands.add_parser('validate')
    validation.add_argument('--approval-id')
    commands.add_parser('status')
    impact = commands.add_parser('impact')
    impact.add_argument('--ids', nargs='+', required=True)
    for cmd in ('apply', 'checkpoint', 'baseline', 'restore'):
        p = commands.add_parser(cmd)
        p.add_argument('--expected-revision', type=int, required=True)
        if cmd == 'apply':
            p.add_argument('--patch', type=Path, required=True)
        elif cmd == 'baseline':
            p.add_argument('--approval-id', required=True)
        elif cmd == 'restore':
            p.add_argument('--checkpoint-id', required=True)
            p.add_argument('--human-review', type=Path, required=True)
    export = commands.add_parser('export')
    export.add_argument('--baseline-id')
    export.add_argument('--ids', nargs='+')
    export.add_argument('--handover', action='store_true')
    export.add_argument('--output', type=Path)
    args = parser.parse_args(argv)
    try:
        workspace = args.workspace.absolute()
        path = workspace / 'state.json'
        if args.command in {'initialise', 'init'}:
            need(not workspace.is_symlink(), 'Refusing a symlinked workspace')
            workspace.mkdir(parents=True, exist_ok=True)
            with locked(workspace):
                need(not path.exists() and not path.is_symlink(), 'Existing workspace will not be overwritten')
                atomic_write(path, blank())
            result = {'workspace_revision': 1, 'created': True}
        elif args.command in {'apply', 'checkpoint', 'baseline', 'restore'}:
            ids = []
            def operation(state):
                if args.command == 'apply':
                    return apply_patch(state, read_json(args.patch))
                if args.command == 'restore':
                    return restore(state, args.checkpoint_id, read_json(args.human_review))
                approval = pointer(latest(state['records'])[args.approval_id]) if args.command == 'baseline' else None
                out, identity = capture(state, 'baselines' if approval else 'checkpoints', approval)
                ids.append(identity)
                return out
            result = mutate(workspace, args.expected_revision, operation)
            result = {'workspace_revision': result['workspace_revision'], 'snapshot_ids': ids}
        else:
            state = read_json(path)
            check_records(state)
            current = latest(state['records'])
            if args.command == 'export':
                output = render(state, args.baseline_id, args.ids, args.handover)
                if args.output:
                    with args.output.open('x', encoding='utf-8') as f:
                        f.write(output)
                    result = {'exported': True}
                else:
                    print(output)
                    return 0
            elif args.command == 'impact':
                need(set(args.ids) <= set(current), 'Unknown impact target')
                result = {'potentially_affected': sorted(affected(state, args.ids)), 'human_review_required': True}
            elif args.command == 'validate':
                result = {'structurally_valid': True, 'workspace_revision': state['workspace_revision'],
                          'pending_reviews': state['pending_reviews'], 'limitations': ['No authentication or semantic certification.']}
                if args.approval_id:
                    need(args.approval_id in current, 'Approval record not found')
                    result['approval'] = approval_issues(state, pointer(current[args.approval_id]))
            else:
                result = {'workspace_revision': state['workspace_revision'], 'records': len(current),
                          'pending_reviews': state['pending_reviews'], 'baselines': [b['id'] for b in state['baselines']],
                          'checkpoints': [c['id'] for c in state['checkpoints']],
                          'open_items': [pointer(r) for r in current.values() if r['status'] in {'open', 'deferred'}]}
        print(encode(result), end='')
        return 0
    except (IntegrityError, OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        print('BA Mate: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
