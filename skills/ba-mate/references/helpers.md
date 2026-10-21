# Optional local helper

Python 3.10+ and standard library only. Locate `../scripts/bamate.py` relative to this reference; use its absolute installed path when invoking outside the skill folder. Examples below assume the repository root and a chosen project working directory. Replace paths with the actual installation/project paths; do not copy the research author's path.

```sh
python3 skills/ba-mate/scripts/bamate.py --version
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace initialise
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace status
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace validate
```

On Windows use `py -3` if appropriate. Do not install Python or change settings silently. `initialise` refuses to overwrite a state file. Every write takes an exclusive workspace lock and atomically replaces one state file; scope all commands to the user-chosen workspace.

## Record transactions

Prepare a patch JSON in the project containing the proposed record/trace additions. For human selections, confirmation, review or approval, include only decisions actually given. Keep private patches outside the public skill repo. Read `status`; use its current revision:

```sh
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace apply --patch /path/to/project/patch.json --expected-revision 1
```

See [records.md](records.md) for patch fields. Stale-write, malformed-record or unsupported-reference failure leaves the authoritative file unchanged. Reload and reconcile before retrying; do not bypass validation with direct edits. Proposal adoption and confirmed approval receive additional checks. A helper does not decide what business facts are true.

## Impact, review and baseline

```sh
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace impact --ids E-1
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace validate --approval-id AP-1
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace baseline --approval-id AP-1 --expected-revision 3
```

Impact returns potential dependants for human review. Validation with an approval ID checks current manifest/dependencies, authority assertion, required artifact reviews, criteria, support paths, blockers and nonblocking dispositions. It neither authenticates authority nor certifies semantic support. Baseline requires an already recorded explicit approval and rejects duplicate capture of that approval. Record the returned baseline ID.

## Checkpoint and recovery

```sh
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace checkpoint --expected-revision 4
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace restore --checkpoint-id CP-returned-id --human-review /path/to/project/restore-decision.json --expected-revision 5
```

The restore-decision file contains a human attestation of the requested recovery. Restore saves the previous working state in a recovery checkpoint inside the same transaction. It appends recovered drafts and removes current semantic verification; review restored sources, authority, traces and artifacts before approval. It never deletes baseline history. Keep ordinary filesystem backups separately; a checkpoint is not protection from deletion of the entire workspace file.

If a process dies leaving `.write.lock`, ensure no writer is active before manually removing that lock. Do not auto-break locks. Filesystem access controls and backups remain the project's responsibility; local JSON is not encrypted.

## Faithful exports

```sh
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace export --ids R-1 AC-1 --output /path/to/project/draft.md
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace export --baseline-id BL-returned-id --output /path/to/project/baseline.md
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace export --baseline-id BL-returned-id --handover
```

Without `--output`, Markdown goes to standard output. Output paths refuse existing files. Working exports always say draft. Baseline exports reproduce the snapshot's manifest, content, authority decision, exclusions, accepted issues, referenced records and trace status. Selecting an artifact outside the baseline manifest fails. Exact record JSON accompanies prose so no detail is silently lost. The artifact text may itself contain imported status claims; authoritative status is the export header/manifest, not embedded claims. Handover adds no technical architecture.

Exit codes: 0 success, 2 invalid input/conflict/tool failure. No network calls, secrets, automatic telemetry, model downloads or cloud API calls. If runtime/filesystem is absent, update the manual session ledger and disclose that helper checks did not run.
