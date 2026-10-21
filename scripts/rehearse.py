#!/usr/bin/env python3
"""Execute three fictional local journeys; never participant or live-host evidence."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'skills' / 'ba-mate' / 'scripts' / 'bamate.py'
spec = importlib.util.spec_from_file_location('rehearsal_helper', HELPER)
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)


def rehearse(output):
    if output.exists():
        raise ValueError('Rehearsal output must be a new directory')
    output.mkdir(parents=True)
    patch = json.loads((ROOT / 'skills/ba-mate/assets/example-patch.json').read_text())
    records = patch['records']
    source = next(r for r in records if r['type'] == 'source')
    state = ba.apply_patch(ba.blank(), patch)
    review = {'actor': 'Synthetic BA', 'at': '2026-10-13T10:00:00+05:30', 'basis': 'Fictional rehearsal semantic review; no actual stakeholder confirmation'}
    authority = next(r for r in records if r['type'] == 'authority')
    approval = {'id': 'AP-1', 'revision': 1, 'type': 'approval', 'status': 'confirmed', 'scope': {'id': 'S-1', 'revision': 1},
                'origin': {'kind': 'human', 'actor': 'Synthetic BA'}, 'at': review['at'], 'review': None, 'references': [],
                'content': {'decision': 'approved', 'authority': ba.pointer(authority),
                            'manifest': [ba.pointer(r) for r in records if r['type'] in ba.ARTIFACTS],
                            'excluded': [], 'accepted_issues': [], 'human_decision': {**review, 'actor': 'Synthetic Owner'}}}
    state = ba.apply_patch(state, {'records': [approval]})
    state, old_id = ba.capture(state, 'baselines', ba.pointer(approval))
    (output / 'new-project-baseline.md').write_text(ba.render(state, old_id), encoding='utf-8')
    # Actual CLI path in an isolated temporary workspace, not only in-memory calls.
    workspace = output / 'ba-mate-workspace'
    subprocess.run([sys.executable, str(HELPER), '--workspace', str(workspace), 'initialise'], check=True, capture_output=True)
    subprocess.run([sys.executable, str(HELPER), '--workspace', str(workspace), 'apply', '--patch', str(ROOT / 'skills/ba-mate/assets/example-patch.json'), '--expected-revision', '1'], check=True, capture_output=True)
    subprocess.run([sys.executable, str(HELPER), '--workspace', str(workspace), 'validate'], check=True, capture_output=True)
    # Existing specification: imported approval wording is not an approval record.
    imported = json.loads((ROOT / 'examples/existing-specification/patch.json').read_text())
    existing = ba.apply_patch(ba.blank(), imported)
    (output / 'existing-specification-draft.md').write_text(ba.render(existing), encoding='utf-8')
    # Change: old baseline remains byte-for-byte faithful; old approval becomes ineligible.
    original = ba.render(state, old_id)
    new_source = copy.deepcopy(source)
    new_source['revision'] = 2
    new_source['content']['text'] = new_source['content']['text'].replace('36', '60')
    changed = ba.apply_patch(state, {'records': [new_source]})
    try:
        ba.approval_issues(changed, ba.pointer(approval))
        raise AssertionError('Old approval incorrectly remained eligible')
    except ba.IntegrityError:
        pass
    assert ba.render(changed, old_id) == original
    (output / 'change-before-revalidation.md').write_text(ba.render(changed), encoding='utf-8')
    updates = []
    for r in records:
        if r['type'] in ba.ARTIFACTS:
            item = copy.deepcopy(r)
            item['revision'] = 2
            item['content']['text'] = item['content']['text'].replace('36', '60').replace('35 hours 59', '59 hours 59')
            item['references'] = [{'id': p['id'], 'revision': 2} for p in item['references']]
            updates.append(item)
    traces = []
    for t in patch['traces']:
        item = copy.deepcopy(t)
        item['revision'] = 2
        item['from']['revision'] = item['to']['revision'] = 2
        traces.append(item)
    revalidation = [{'target': ba.pointer(r), 'human_review': review} for r in [new_source] + updates]
    changed = ba.apply_patch(changed, {'records': updates, 'traces': traces, 'revalidated': revalidation})
    new_approval = copy.deepcopy(approval)
    new_approval['id'] = 'AP-2'
    new_approval['content']['manifest'] = [ba.pointer(r) for r in updates]
    changed = ba.apply_patch(changed, {'records': [new_approval]})
    changed, new_id = ba.capture(changed, 'baselines', ba.pointer(new_approval))
    (output / 'change-new-baseline.md').write_text(ba.render(changed, new_id), encoding='utf-8')
    (output / 'change-historical-baseline.md').write_text(ba.render(changed, old_id), encoding='utf-8')
    assert ba.render(changed, old_id) == original
    report = {'kind': 'author-led synthetic helper rehearsal', 'host_activation': 'not tested', 'participant_evidence': False,
              'python': sys.version.split()[0], 'journeys': {'new-project': 'passed', 'existing-specification': 'passed', 'approved-change': 'passed'},
              'old_baseline_preserved': True, 'old_working_approval_rejected_after_change': True}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output:
        print(json.dumps(rehearse(args.output), indent=2))
    else:
        with tempfile.TemporaryDirectory() as temporary:
            print(json.dumps(rehearse(Path(temporary) / 'rehearsal'), indent=2))
