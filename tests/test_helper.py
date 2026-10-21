"""Synthetic conformance tests; no participant records or private research cases."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills' / 'ba-mate' / 'scripts' / 'bamate.py'
spec = importlib.util.spec_from_file_location('bamate', SCRIPT)
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)
AT = '2026-10-13T10:00:00+05:30'


def human(actor='Synthetic BA', basis='Synthetic human review of this exact revision'):
    return {'actor': actor, 'at': AT, 'basis': basis}


def r(identity, kind, content, revision=1, status='draft', references=None, reviewed=False, origin='human', scope='S-1'):
    return {'id': identity, 'revision': revision, 'type': kind, 'status': status,
            'scope': None if kind == 'scope' else {'id': scope, 'revision': 1},
            'origin': {'kind': origin, 'actor': 'Synthetic AI' if origin == 'ai' else 'Synthetic BA'},
            'at': AT, 'content': content, 'references': references or [],
            'review': human() if reviewed else None}


def p(identity, revision=1):
    return {'id': identity, 'revision': revision}


def trace(identity, from_id, to_id, status='verified', from_revision=1, to_revision=1, revision=1):
    return {'id': identity, 'revision': revision, 'from': p(from_id, from_revision), 'to': p(to_id, to_revision),
            'relation': 'supports', 'status': status, 'verification': human() if status == 'verified' else None}


def fixture():
    records = [
        r('S-1', 'scope', {'text': 'Fictional craft studio: release unclaimed workshop seats; notifications excluded.'}),
        r('ST-1', 'stakeholder', {'text': 'Fictional studio coordinator'}),
        r('AU-1', 'authority', {'person': 'Synthetic Owner', 'role': 'Studio owner', 'basis': 'Fictional delegated project authority'}, status='confirmed', reviewed=True),
        r('E-1', 'source', {'text': 'Release unclaimed seats exactly 36 elapsed hours after booking confirmation. Do not release attended bookings.',
                          'provenance': 'New fictional studio interview, paragraph 1', 'locator': 'paragraph 1',
                          'extraction_reviewed': True, 'relevant': True, 'classification': 'public'}, reviewed=True),
        r('R-1', 'requirement', {'text': 'At 36 elapsed hours after confirmation, release an unclaimed seat. Attended bookings are excluded.'}, status='in-review', references=[p('E-1')], reviewed=True),
        r('AC-1', 'criterion', {'text': 'At 35 hours 59 minutes retain an unclaimed seat; at 36 hours release it. Retain attended bookings.'}, status='in-review', references=[p('R-1')], reviewed=True),
        r('D-1', 'document', {'text': 'Studio requirement: 36 elapsed hours, attended bookings excluded.'}, status='in-review', references=[p('R-1'), p('AC-1')], reviewed=True),
    ]
    state = ba.apply_patch(ba.blank(), {'records': records, 'traces': [trace('T-1', 'E-1', 'R-1'), trace('T-2', 'R-1', 'AC-1')]})
    approval = r('AP-1', 'approval', {'decision': 'approved', 'authority': p('AU-1'),
                 'manifest': [p('R-1'), p('AC-1'), p('D-1')], 'excluded': [], 'accepted_issues': [],
                 'human_decision': human('Synthetic Owner', 'Fictional approval of these exact revisions; no real business decision')}, status='confirmed')
    return ba.apply_patch(state, {'records': [approval]})


class RecordTests(unittest.TestCase):
    def test_redirected_trace_requires_review_of_both_targets(self):
        state = fixture()
        # Keep another supporting path so removal alone cannot mask the impact check.
        state = ba.apply_patch(state, {'traces': [trace('T-3', 'E-1', 'R-1')],
            'revalidated': [{'target': p(identity), 'human_review': human()}
                            for identity in ('R-1', 'AC-1', 'D-1')]})
        redirected = trace('T-1', 'E-1', 'AC-1', revision=2)
        state = ba.apply_patch(state, {'traces': [redirected]})
        self.assertIn(p('R-1'), state['pending_reviews'])
        self.assertIn(p('AC-1'), state['pending_reviews'])
        with self.assertRaisesRegex(ba.IntegrityError, 'revalidation'):
            ba.approval_issues(state, p('AP-1'))

    def test_rejected_source_cannot_support_approval(self):
        for status in ('rejected', 'excluded', 'not-applicable'):
            state = fixture()
            source = ba.latest(state['records'])['E-1']
            source['status'] = status
            with self.subTest(status=status), self.assertRaisesRegex(ba.IntegrityError, 'supporting evidence'):
                ba.approval_issues(state, p('AP-1'))

    def test_changed_trace_requires_revalidation_and_preserves_baseline(self):
        state, baseline = ba.capture(fixture(), 'baselines', p('AP-1'))
        original = ba.render(state, baseline)
        revised = copy.deepcopy(state['traces'][0])
        revised['revision'] = 2
        revised['verification'] = human(basis='Updated human check of the same support relation')
        state = ba.apply_patch(state, {'traces': [revised]})
        for identity in ('R-1', 'AC-1', 'D-1'):
            self.assertIn(p(identity), state['pending_reviews'])
        with self.assertRaisesRegex(ba.IntegrityError, 'revalidation'):
            ba.approval_issues(state, p('AP-1'))
        self.assertEqual(original, ba.render(state, baseline))
        state = ba.apply_patch(state, {'revalidated': [
            {'target': p(identity), 'human_review': human(basis='Same artifact meaning retained after trace review')}
            for identity in ('R-1', 'AC-1', 'D-1')]})
        self.assertTrue(ba.approval_issues(state, p('AP-1'))['eligible'])

    def test_added_trace_to_existing_work_requires_review(self):
        state = fixture()
        state = ba.apply_patch(state, {'traces': [trace('T-3', 'E-1', 'R-1')]})
        self.assertIn(p('R-1'), state['pending_reviews'])
        with self.assertRaises(ba.IntegrityError):
            ba.approval_issues(state, p('AP-1'))

    def test_confirmed_blocking_risk_is_not_resolved(self):
        state = fixture()
        risk = r('RK-1', 'risk', {'text': 'Fictional unresolved privacy risk', 'severity': 'blocking'}, status='confirmed')
        state = ba.apply_patch(state, {'records': [risk]})
        with self.assertRaisesRegex(ba.IntegrityError, 'blocking'):
            ba.approval_issues(state, p('AP-1'))
        self.assertIn('Fictional unresolved privacy risk', ba.render(state, ids=['R-1']))

    def test_disposing_blocker_requires_explicit_human_attestation(self):
        state = fixture()
        for status in ('resolved', 'rejected', 'excluded', 'not-applicable'):
            issue = r('I-1', 'issue', {'text': 'Fictional blocker', 'severity': 'blocking'}, status=status, origin='ai')
            with self.subTest(status=status), self.assertRaises(ba.IntegrityError):
                ba.apply_patch(state, {'records': [issue]})
        issue['content']['disposition'] = human(basis='Responsible human determines the finding is outside this scope')
        out = ba.apply_patch(state, {'records': [issue]})
        self.assertTrue(ba.approval_issues(out, p('AP-1'))['eligible'])

    def test_recovery_with_later_evidence_and_trace(self):
        state, checkpoint = ba.capture(fixture(), 'checkpoints')
        later = r('E-2', 'source', {'text': 'Later fictional evidence', 'provenance': 'Synthetic note 2', 'extraction_reviewed': True, 'relevant': True}, reviewed=True)
        state = ba.apply_patch(state, {'records': [later], 'traces': [trace('T-3', 'E-2', 'R-1')]})
        state = ba.restore(state, checkpoint, human(basis='Restore the earlier fictional checkpoint'))
        ba.check_records(state)
        current = ba.latest(state['records'])
        self.assertEqual(current['E-2']['status'], 'excluded')
        self.assertEqual(current['E-2']['scope'], current['R-1']['scope'])
        self.assertEqual(current['R-1']['status'], 'draft')
        self.assertEqual(ba.latest(state['traces'])['T-3']['status'], 'stale')
        self.assertEqual(len(state['checkpoints']), 2)

    def test_baseline_export_preserves_authority_and_accepted_issue_context(self):
        state = fixture()
        issue = r('AS-1', 'assumption', {'text': 'Fictional nonblocking reporting uncertainty', 'severity': 'optional',
                  'disposition': human(basis='Synthetic owner accepts reporting uncertainty outside the core commitment')}, status='open')
        state = ba.apply_patch(state, {'records': [issue]})
        approval = copy.deepcopy(ba.latest(state['records'])['AP-1'])
        approval.update(id='AP-2')
        approval['content']['accepted_issues'] = [p('AS-1')]
        state = ba.apply_patch(state, {'records': [approval]})
        state, baseline = ba.capture(state, 'baselines', p('AP-2'))
        output = ba.render(state, baseline)
        self.assertIn('Fictional delegated project authority', output)
        self.assertIn('Synthetic owner accepts reporting uncertainty', output)

    def test_accepted_issue_cannot_name_another_scope(self):
        state = fixture()
        state = ba.apply_patch(state, {'records': [r('S-2', 'scope', {'text': 'Other scope'}),
            r('AS-2', 'assumption', {'text': 'Other private uncertainty', 'severity': 'optional', 'disposition': human()}, status='open', scope='S-2')]})
        approval = copy.deepcopy(ba.latest(state['records'])['AP-1'])
        approval.update(id='AP-2')
        approval['content']['accepted_issues'] = [p('AS-2')]
        with self.assertRaisesRegex(ba.IntegrityError, 'this scope'):
            ba.apply_patch(state, {'records': [approval]})

    def test_new_project_approval_and_baseline(self):
        state = fixture()
        self.assertTrue(ba.approval_issues(state, p('AP-1'))['eligible'])
        state, identity = ba.capture(state, 'baselines', p('AP-1'))
        ba.check_records(state)
        self.assertIn('36 elapsed hours', ba.render(state, identity))
        self.assertIn('Historical approved baseline', ba.render(state, identity))

    def test_no_ai_approval(self):
        state = fixture()
        state['records'][-1]['origin']['kind'] = 'ai'
        with self.assertRaises(ba.IntegrityError):
            ba.check_records(state)

    def test_no_generated_stakeholder_confirmation(self):
        record = r('Q-1', 'clarification', {'answer': '12 hours', 'respondent': 'Simulated manager', 'authority_basis': 'Persona'}, status='confirmed', origin='ai')
        with self.assertRaises(ba.IntegrityError):
            ba.apply_patch(fixture(), {'records': [record]})

    def test_blocker_prevents_approval(self):
        state = fixture()
        state['records'].append(r('Q-1', 'clarification', {'question': 'Which notification is required?', 'priority': 'blocking'}, status='open', references=[p('R-1')]))
        with self.assertRaisesRegex(ba.IntegrityError, 'blocking'):
            ba.approval_issues(state, p('AP-1'))

    def test_deferred_blocker_still_blocks(self):
        state = fixture()
        state['records'].append(r('Q-1', 'clarification', {'question': 'Conflicting seat rules', 'priority': 'blocking'}, status='deferred'))
        with self.assertRaises(ba.IntegrityError):
            ba.approval_issues(state, p('AP-1'))

    def test_partial_approval_excludes_unrelated_work(self):
        state = fixture()
        state['records'].extend([r('R-2', 'requirement', {'text': 'Notification pending.'}), r('Q-2', 'clarification', {'question': 'Delivery channel?', 'priority': 'blocking'}, status='open', references=[p('R-2')])])
        state['records'][-3]['content']['excluded'] = [p('R-2')]
        self.assertTrue(ba.approval_issues(state, p('AP-1'))['eligible'])
        state, identity = ba.capture(state, 'baselines', p('AP-1'))
        with self.assertRaises(ba.IntegrityError):
            ba.render(state, identity, ['R-2'])

    def test_nonblocking_uncertainty_needs_disposition(self):
        state = fixture()
        uncertainty = r('AS-1', 'assumption', {'text': 'Future reporting unspecified', 'severity': 'important'}, status='open')
        state['records'].append(uncertainty)
        with self.assertRaises(ba.IntegrityError):
            ba.approval_issues(state, p('AP-1'))
        uncertainty['content']['disposition'] = human(basis='Outside expiry scope; owner retained for next review')
        state['records'][-2]['content']['accepted_issues'] = [p('AS-1')]
        self.assertTrue(ba.approval_issues(state, p('AP-1'))['eligible'])

    def test_unreviewed_or_irrelevant_source_not_support(self):
        for key in ('extraction_reviewed', 'relevant'):
            state = fixture()
            state['records'][3]['content'][key] = False
            with self.assertRaises(ba.IntegrityError):
                ba.approval_issues(state, p('AP-1'))

    def test_missing_evidence_and_duplicate_revision_rejected(self):
        state = fixture()
        with self.assertRaises(ba.IntegrityError):
            ba.apply_patch(state, {'records': [r('R-2', 'requirement', {'text': 'Unknown source'}, references=[p('NO-SOURCE')])]})
        with self.assertRaises(ba.IntegrityError):
            ba.apply_patch(state, {'records': [state['records'][4]]})

    def test_semantic_check_is_not_automatically_verified(self):
        state = fixture()
        state['traces'][0]['status'] = 'proposed'
        state['traces'][0]['verification'] = None
        with self.assertRaises(ba.IntegrityError):
            ba.approval_issues(state, p('AP-1'))
        # Human assertions cannot be authenticated or semantically proved by this helper.
        self.assertIn('Structural checks only', ba.approval_issues(fixture(), p('AP-1'))['limitations'][0])

    def test_criteria_and_authority_required(self):
        for modify in ('criteria', 'authority', 'actor'):
            state = fixture()
            approval = state['records'][-1]['content']
            if modify == 'criteria':
                approval['manifest'] = [p('R-1')]
            elif modify == 'authority':
                state['records'][2]['status'] = 'draft'
            else:
                approval['human_decision']['actor'] = 'Wrong person'
            with self.assertRaises(ba.IntegrityError):
                ba.approval_issues(state, p('AP-1'))

    def test_change_invalidates_working_approval_keeps_baseline(self):
        state, identity = ba.capture(fixture(), 'baselines', p('AP-1'))
        original = ba.render(state, identity)
        source = copy.deepcopy(state['records'][3])
        source['revision'] = 2
        source['content']['text'] = 'Release after 60 elapsed hours.'
        state = ba.apply_patch(state, {'records': [source]})
        self.assertIn(p('R-1'), state['pending_reviews'])
        self.assertIn(p('AC-1'), state['pending_reviews'])
        self.assertIn(p('D-1'), state['pending_reviews'])
        with self.assertRaises(ba.IntegrityError):
            ba.approval_issues(state, p('AP-1'))
        self.assertEqual(original, ba.render(state, identity))
        self.assertIn('Working DRAFT', ba.render(state))

    def test_approved_change_requires_new_revisions_and_review(self):
        state, identity = ba.capture(fixture(), 'baselines', p('AP-1'))
        updates = []
        for rid in ('E-1', 'R-1', 'AC-1', 'D-1'):
            record = copy.deepcopy(ba.latest(state['records'])[rid])
            record['revision'] = 2
            record['content']['text'] = record['content']['text'].replace('36', '60').replace('35 hours 59', '59 hours 59')
            record['references'] = [p(x['id'], 2) for x in record['references']]
            updates.append(record)
        traces = [trace('T-1', 'E-1', 'R-1', from_revision=2, to_revision=2, revision=2), trace('T-2', 'R-1', 'AC-1', from_revision=2, to_revision=2, revision=2)]
        revalidation = [{'target': p(rid, 2), 'human_review': human()} for rid in ('E-1', 'R-1', 'AC-1', 'D-1')]
        state = ba.apply_patch(state, {'records': updates, 'traces': traces, 'revalidated': revalidation})
        approval = copy.deepcopy(ba.latest(state['records'])['AP-1'])
        approval['id'] = 'AP-2'
        approval['content']['manifest'] = [p(rid, 2) for rid in ('R-1', 'AC-1', 'D-1')]
        # An unresolved question attached to r1 still affects the same item at r2.
        old_question = r('Q-1', 'clarification', {'question': 'Resolve an outstanding rule conflict', 'priority': 'blocking'}, status='open', references=[p('R-1')])
        state = ba.apply_patch(state, {'records': [old_question]})
        with self.assertRaisesRegex(ba.IntegrityError, 'blocking'):
            ba.apply_patch(state, {'records': [approval]})
        resolved = copy.deepcopy(old_question)
        resolved.update(revision=2, status='resolved')
        resolved['content']['resolution'] = 'Fictional human resolution; no outstanding conflict'
        resolved['content']['disposition'] = human(basis='Fictional responsible human resolves the conflicting rule')
        state = ba.apply_patch(state, {'records': [resolved]})
        state = ba.apply_patch(state, {'records': [approval]})
        state, new_id = ba.capture(state, 'baselines', p('AP-2'))
        self.assertIn('60 elapsed hours', ba.render(state, new_id))
        self.assertIn('36 elapsed hours', ba.render(state, identity))

    def test_trace_only_evidence_change_requires_review(self):
        state = fixture()
        state['records'][4]['references'] = []
        changed = copy.deepcopy(state['records'][3])
        changed['revision'] = 2
        state = ba.apply_patch(state, {'records': [changed]})
        with self.assertRaises(ba.IntegrityError):
            ba.approval_issues(state, p('AP-1'))

    def test_unknown_patch_fields_cannot_rewrite_baselines(self):
        state, _ = ba.capture(fixture(), 'baselines', p('AP-1'))
        with self.assertRaises(ba.IntegrityError):
            ba.apply_patch(state, {'baselines': []})

    def test_modified_snapshot_detected(self):
        state, _ = ba.capture(fixture(), 'baselines', p('AP-1'))
        state['baselines'][0]['snapshot']['records'][4]['content']['text'] = 'Changed'
        with self.assertRaisesRegex(ba.IntegrityError, 'integrity'):
            ba.check_records(state)

    def test_recovery_creates_drafts_and_retains_pre_restore(self):
        state, baseline_id = ba.capture(fixture(), 'baselines', p('AP-1'))
        state, checkpoint_id = ba.capture(state, 'checkpoints')
        before = ba.render(state, baseline_id)
        state = ba.restore(state, checkpoint_id, human())
        self.assertEqual(len(state['checkpoints']), 2)
        self.assertEqual(ba.latest(state['records'])['R-1']['status'], 'draft')
        self.assertTrue(all(t['status'] != 'verified' for t in ba.latest(state['traces']).values()))
        self.assertEqual(before, ba.render(state, baseline_id))
        with self.assertRaises(ba.IntegrityError):
            ba.approval_issues(state, p('AP-1'))

    def test_original_rejected_and_selected_edited_proposals_retained(self):
        state = fixture()
        proposal = r('P-1', 'proposal', {'original': 'Draft A and draft B', 'context': [p('E-1')], 'disposition': 'pending', 'model': None}, origin='ai')
        state = ba.apply_patch(state, {'records': [proposal]})
        selected = r('R-2', 'requirement', {'text': 'Human corrected draft A'}, references=[p('E-1')])
        adopted = copy.deepcopy(proposal)
        adopted['revision'] = 2
        adopted['content'].update(disposition='adopted', edited='Human corrected draft A; B rejected', selected=[p('R-2')], adoption=human())
        state = ba.apply_patch(state, {'records': [selected, adopted]})
        self.assertEqual(state['records'][-3]['content']['original'], 'Draft A and draft B')
        self.assertEqual(ba.latest(state['records'])['R-2']['status'], 'draft')
        self.assertNotIn('R-3', ba.latest(state['records']))

    def test_stale_proposal_rejected_without_working_change(self):
        state = fixture()
        changed = copy.deepcopy(state['records'][3])
        changed['revision'] = 2
        state = ba.apply_patch(state, {'records': [changed]})
        original = copy.deepcopy(state)
        proposal = r('P-1', 'proposal', {'original': 'Old context', 'context': [p('E-1')], 'disposition': 'adopted', 'selected': [p('R-2')], 'adoption': human()}, origin='ai')
        with self.assertRaisesRegex(ba.IntegrityError, 'stale'):
            ba.apply_patch(state, {'records': [r('R-2', 'requirement', {'text': 'Draft'}), proposal]})
        self.assertEqual(state, original)

    def test_cannot_rewrite_original_proposal(self):
        state = fixture()
        proposal = r('P-1', 'proposal', {'original': 'Preserve this', 'context': [p('E-1')], 'disposition': 'pending'}, origin='ai')
        state = ba.apply_patch(state, {'records': [proposal]})
        edited = copy.deepcopy(proposal)
        edited['revision'] = 2
        edited['content']['original'] = 'Replaced original'
        with self.assertRaisesRegex(ba.IntegrityError, 'immutable'):
            ba.apply_patch(state, {'records': [edited]})

    def test_document_cannot_approve_omitted_linked_artifact(self):
        state = fixture()
        extra = r('R-2', 'requirement', {'text': 'Unreviewed extra business behaviour'})
        state['records'].append(extra)
        state['records'][6]['references'].append(p('R-2'))
        with self.assertRaisesRegex(ba.IntegrityError, 'manifest'):
            ba.approval_issues(state, p('AP-1'))

    def test_invalid_timestamp_and_priority_rejected(self):
        record = r('Q-1', 'clarification', {'question': 'Which rule?', 'priority': 'Blocking'}, status='open')
        with self.assertRaises(ba.IntegrityError):
            ba.apply_patch(fixture(), {'records': [record]})
        record['content']['priority'] = 'blocking'
        record['at'] = 'yesterday'
        with self.assertRaises(ba.IntegrityError):
            ba.apply_patch(fixture(), {'records': [record]})

    def test_scope_export_does_not_include_other_scope_uncertainty(self):
        state = fixture()
        state['records'].extend([r('S-2', 'scope', {'text': 'Other private work'}), r('I-2', 'issue', {'text': 'Other scope confidential marker', 'severity': 'blocking'}, status='open', scope='S-2')])
        self.assertNotIn('Other scope confidential marker', ba.render(state, ids=['R-1']))

    def test_snapshot_cannot_be_captured_twice(self):
        state, _ = ba.capture(fixture(), 'baselines', p('AP-1'))
        with self.assertRaises(ba.IntegrityError):
            ba.capture(state, 'baselines', p('AP-1'))

    def test_export_exact_selection_and_handover(self):
        state = fixture()
        output = ba.render(state, ids=['R-1'], handover=True)
        self.assertIn('developer handover', output)
        self.assertIn('Technical architecture is unspecified', output)
        self.assertIn('New fictional studio interview', output)
        self.assertNotIn('## D-1', output)

    def test_existing_specification_is_draft_without_authority(self):
        state = ba.apply_patch(ba.blank(), {'records': [r('S-1', 'scope', {'text': 'Imported specification'}), r('D-1', 'document', {'text': 'Imported vendor document says approved'})]})
        self.assertIn('Working DRAFT', ba.render(state))

    def test_malformed_json_duplicate_keys_and_nan(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'
            for text in ('{"a":1,"a":2}', '{"a":NaN}', 'broken'):
                path.write_text(text, encoding='utf-8')
                with self.assertRaises((ba.IntegrityError, ValueError)):
                    ba.read_json(path)


class TransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name)
        ba.atomic_write(self.workspace / 'state.json', fixture())

    def tearDown(self):
        self.temp.cleanup()

    def test_revision_conflict_no_mutation(self):
        before = (self.workspace / 'state.json').read_bytes()
        with self.assertRaisesRegex(ba.IntegrityError, 'Stale'):
            ba.mutate(self.workspace, 7, lambda s: s)
        self.assertEqual(before, (self.workspace / 'state.json').read_bytes())
        self.assertFalse((self.workspace / '.write.lock').exists())

    def test_lock_prevents_second_writer(self):
        with ba.locked(self.workspace):
            with self.assertRaises(ba.IntegrityError):
                ba.mutate(self.workspace, 1, lambda s: s)

    def test_failed_validation_no_partial_write(self):
        before = (self.workspace / 'state.json').read_bytes()
        with self.assertRaises(ba.IntegrityError):
            ba.mutate(self.workspace, 1, lambda s: ba.apply_patch(s, {'records': [r('R-2', 'requirement', {}, references=[p('missing')])]}))
        self.assertEqual(before, (self.workspace / 'state.json').read_bytes())

    def test_atomic_replace_failure_retains_old_file(self):
        before = (self.workspace / 'state.json').read_bytes()
        with patch.object(ba.os, 'replace', side_effect=OSError('synthetic storage failure')):
            with self.assertRaises(OSError):
                ba.mutate(self.workspace, 1, lambda s: s)
        self.assertEqual(before, (self.workspace / 'state.json').read_bytes())
        self.assertFalse(list(self.workspace.glob('.state-*.tmp')))

    def test_external_change_detected(self):
        def interfere(state):
            external = copy.deepcopy(state)
            external['workspace_revision'] = 9
            ba.atomic_write(self.workspace / 'state.json', external)
            return state
        with self.assertRaisesRegex(ba.IntegrityError, 'outside'):
            ba.mutate(self.workspace, 1, interfere)
        self.assertEqual(ba.read_json(self.workspace / 'state.json')['workspace_revision'], 9)

    def test_cli_initialise_validate_status_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / 'ba-mate-workspace'
            def run(*args):
                return subprocess.run([sys.executable, str(SCRIPT), '--workspace', str(workspace), *args], capture_output=True, text=True)
            self.assertEqual(run('initialise').returncode, 0)
            self.assertEqual(run('initialise').returncode, 2)
            self.assertTrue(json.loads(run('validate').stdout)['structurally_valid'])
            self.assertEqual(json.loads(run('status').stdout)['workspace_revision'], 1)

    def test_export_refuses_overwrite(self):
        target = self.workspace / 'output.md'
        target.write_text('Retain this', encoding='utf-8')
        result = subprocess.run([sys.executable, str(SCRIPT), '--workspace', str(self.workspace), 'export', '--output', str(target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(target.read_text(encoding='utf-8'), 'Retain this')


if __name__ == '__main__':
    unittest.main()
