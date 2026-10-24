# Historical v1.0.0 implementation and qualification audit

For the v1.0.5 beta update, current host evidence and failures are in [COMPATIBILITY.md](COMPATIBILITY.md), [QUALIFICATION.md](QUALIFICATION.md) and [results](../evaluation/results/README.md). The following is retained as the original release audit.

Recorded 13 October 2026 against the approved v1.0.0 project plan. The local standalone implementation is delivered. Installed-host behaviour, practitioner pilots and cross-platform CI execution are pending; the project owner explicitly requested that unavailable results remain marked pending. Preparing the final archives does not grant a runtime-supported or research-validated label.

## Requirements and evidence

| Plan requirement | Implementation / evidence | State |
|---|---|---|
| Separate public-ready project; no application dependency | Standalone root, independent local Git repository, allowlisted source archive; isolated package tests | Implemented; no remote publication |
| F4-draft.1 authority and original objectives/instruments | Bundled full specification; references/framework.md and evaluation.md; docs/RESEARCH.md | Implemented |
| One canonical skill and all eleven operating modes | skills/ba-mate/SKILL.md; linked workflow/review references and templates | Implemented; activation qualification pending |
| Iterative entry from new brief, existing specification or approved change | Three new fictional journeys; scripts/rehearse.py; fixture tests | Local helper rehearsals passed |
| Evidence, passages, relevance, sensitivity, extraction omissions | Revisioned source excerpt records with provenance/locator; context manifest and evidence procedure | Implemented; actual host extraction behaviour pending |
| Actual human answers, uncertainty, prioritised questions | Clarification contract; native/conversational fallback; blocker/disposition checks | Structural tests passed; host behaviour pending |
| No invented facts, thresholds, IDs or source instructions | Workflow rules; missing-reference/AI-confirmation tests; B01–B09 cases | Structural coverage; semantic/activation tests pending |
| Bounded proposals, original output, human edits/adoption/rejection | Proposal contract, immutable original/context, selected draft refs, manual repair procedure | Local structural tests passed |
| Semantic support and review dimensions | Human trace/review attestations; all nine dimensions; B09–B10 | Implemented; helpers do not certify truth |
| Exact revision approval, partial scope and affected blockers | Manifest/authority/exclusion/accepted-issue checks; scope and blocker tests | Local structural tests passed |
| M1–M7 observable conformance mapping | references/framework.md linking procedures, records, checks, B01–B15 and limits | Implemented |
| Stable JSON IDs/revisions/status/origin/time; unknowns explicit | Schema-1 contract and validator; empty workspace/example patch | Implemented |
| Trace endpoint revisions, immutable baselines and retained contents | Versioned traces, full snapshot contents, digest checks and historical exports | Local tests passed |
| Change impacts and revalidation history | Record/trace changes invalidate dependants; human revalidation events; earlier baselines retained | Local tests passed, including redirected traces |
| Optional Python 3.10+ standard-library helper | Initialise, validate, checkpoint, impact, baseline, export; additional apply/status/restore | Implemented; local Python 3.13.2 tested |
| Atomic writes, stale conflicts and no partial failure | Exclusive lock, revision/content conflict checks, atomic replacement; failure injection tests | Local tests passed |
| Recovery creates drafts requiring review | Retained pre-restore checkpoint, coherent remapped refs, reset reviews, excluded later work | Local tests passed |
| Manual continuation without Python/filesystem/history | Session ledger, record/artifact templates, capability disclosures and supplied-state resume | Implemented; host fallback behaviour pending |
| Four self-contained distributions from one core | Codex portable plugin, Claude plugin/marketplace, Gemini extension, Antigravity direct skill | Structural extraction/resource tests passed |
| Host instructions/removal/invocation; no silent overwrite/settings edits | INSTALLATION.md, guarded local installer, host examples and natural-language fallback | Local isolation tests passed |
| Markdown/Mermaid and optional host conversion/handover | Templates, model guidance, accurate draft/baseline exports and optional handover | Markdown tested; renderer/converters unqualified |
| Documentation, contribution/release guidance | README, project plan, installation, compatibility, research, checklist, audit | Implemented |
| Apache-2.0, project attribution, citation/version/changelog | LICENSE, NOTICE, CITATION.cff, VERSION, manifests, schema version, CHANGELOG | Implemented; no invented identity/URL/DOI |
| Four structured GitHub feedback forms | Installation, workflow, unsupported commitment and suggestions; sanitised reproduction fields | Implemented; GitHub UI execution pending |
| Separate public feedback/consented study records and A/B/C | Research boundary, local run form, original five feedback items/instrument semantics | Implemented; no participant collection |
| Only synthetic public material, no telemetry/integrations | Newly fictional examples/tests; public archive filtering and bounded hygiene checks | Local checks passed; no confidential records included |
| Full required behavioural scenario coverage | B01–B15 cover activation, thresholds/conflicts, extraction/instructions, malformed/stale work, selection, contradiction, partial approval, change, export, resume/fallback | Procedures supplied; actual host outcomes pending |
| Linux/macOS/Windows repository CI | Six-job OS/Python 3.10/3.13 matrix runs tests, checks, rehearsal and packages | Configured; execution pending |
| rc.1, pilot findings and final archives | Candidate/final source plus four host ZIPs and checksums; defects retained in VERIFICATION.md | Archives prepared; practitioner pilot pending |
| Critical-defect release gate | Repaired approval, trace-change, recovery and export failures rerun; no known critical defect remaining in tested helper paths | Local gate passed; host/public circulation gate remains open |

Paths in the table are repository-relative locators. All installed skill references resolve inside the canonical skill, and package tests execute bundled helpers without this research parent directory. Automated helper tests assert structural integrity, not factual correctness or stakeholder agreement.

## Evidence still required before stronger claims

1. Run the configured repository CI on all three operating systems and retain job outcomes. The repository has no remote; publication remains a separate action. The local Docker engine is unavailable, so a Linux container outcome is not asserted either.
2. Qualify installed-host B01–B15 with actual host/model versions and retained observations. Codex's local CLI wrapper lacks its platform executable; the other target hosts have no usable local session. No target is advertised as runtime verified.
3. Conduct the permitted practitioner pilot, preserve actual findings and repeat repaired cases and affected journeys. No participant result or pilot acceptance is fabricated.

Use evaluation/qualification-record.json and the local run-record template. Update COMPATIBILITY.md, VERIFICATION.md and release metadata from actual evidence before public circulation claims. If a critical host failure is discovered, keep that host unqualified until repaired and retested. Public repository publication and marketplace submissions are outside this local delivery.
