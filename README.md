# BA-MATE-SKILL

**A portable, evidence-grounded, human-governed Business Analysis workflow.**

Use BA Mate inside Codex, Claude Code, Cursor, Gemini CLI or Antigravity to work from stakeholder evidence through clarification, requirements, review, documents, approval records and controlled change. It supports ordinary BA projects and synthetic research practice. AI proposes; people decide business meaning, verify support and approve exact revisions.

Package **1.0.5 beta** · framework **F4-draft.1** · record schema **1**. This is an implementation of a proposed research method, not evidence of proven improvement, authenticated approvals or enterprise readiness. Host runtime qualification and practitioner pilot results remain separate from package/structural checks; see [verification](docs/VERIFICATION.md).

Runtime evidence: Codex passed five smoke cases on the final core. Cursor has actual activation/review evidence with a retained manual-trace defect; its correction is not runtime verified. Antigravity has a retained clarification failure; Claude Code is blocked by login. See [the exact compatibility claims](docs/COMPATIBILITY.md) and [qualification results](evaluation/results/README.md). No host is fully qualified across every workflow.

## Start

1. Follow the [beta quickstart](docs/BETA_QUICKSTART.md) to install only this skill into a chosen fictional project. Full platform options are in [installation instructions](docs/INSTALLATION.md).
2. Open your chosen BA project and invoke the skill, for example: **Use BA Mate to review this brief, identify missing business decisions and draft requirements after clarification.**
3. Review actual evidence and answer/route questions. Select/edit/reject proposals. Adoption creates drafts; final approval is separate.

Modes: start, evidence, clarify, draft, model, review, document, baseline, change, status/resume and optional handover. Existing specifications can enter at review/change. Small cases can use textual processes.

The optional Python 3.10+ helper has no third-party dependencies:

```sh
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace initialise
python3 skills/ba-mate/scripts/bamate.py --workspace /path/to/project/ba-mate-workspace status
```

Use an actual project path and installed helper path. On Windows use `py -3` where appropriate. Follow [workspace operations](skills/ba-mate/references/helpers.md) and [record contract](skills/ba-mate/references/records.md); do not edit the authoritative state directly. Without filesystem/Python access, use the [manual session ledger](skills/ba-mate/assets/session-ledger.md) with disclosed integrity limitations.

## What is included

- One canonical skill with focused references and artifact templates.
- Versioned local JSON, proposal history, source/decision references, human review assertions and exact baseline snapshots.
- Optional validation, impact, checkpoint/recovery and faithful Markdown export.
- Five distribution targets (including Cursor), installation/removal guidance and host qualification cases.
- Three new fictional journeys, mechanism mapping, tests, release tooling and GitHub issue forms.

Markdown and Mermaid source are portable. Word/PDF and diagram rendering use available host tools and require checking actual results. No telemetry, accounts, MCP server, model downloads, provider integration or paid credentials are bundled. Ordinary project content remains in the chosen workspace; do not commit it to this repository. A cloud host may process supplied content externally: use only material that project policy allows, or local/manual work.

## Research and contribution

The framework, BA Mate application and this skills implementation are distinct artifacts. The primary application-based A/B/C study is preserved; skills use is a separate portability/formative stream. Public feedback is not a controlled effectiveness sample. See [research boundaries](docs/RESEARCH.md), [framework mapping](skills/ba-mate/references/framework.md), [project plan](docs/PROJECT_PLAN.md) and [contributor guide](CONTRIBUTING.md).

Try [the synthetic journeys](examples/README.md). Report sanitised, reproducible feedback through the issue forms in this repository. Do not include private workspaces, unseen assessment cases, participant records, API keys or confidential evidence.

## Maintainer checks

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_project.py
python3 scripts/build_release.py --version 1.0.5
```

Build tooling packages only allowlisted project content, verifies canonical skill consistency, and writes distribution archives/checksums under `dist/`. The [v1.0.5 code CI run](https://github.com/NimnadaUGC/BA-MATE-SKILL/actions/runs/40076794392) passed all six Linux/macOS/Windows and Python 3.10/3.13 jobs (56 tests each). This does not qualify model behaviour. No host settings or public services are changed by building. Publishing a release and marketplace submission remain separate actions.

Licensed Apache-2.0. Attribution: BA Mate research project. See [citation metadata](CITATION.cff) and [release checklist](docs/RELEASE_CHECKLIST.md).
