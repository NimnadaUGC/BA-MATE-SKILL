# Framework alignment

Methodological source: the research specification **F4-draft.1**, dated 20 September 2026, "Evidence-grounded, human-governed BA framework". Read the bundled [full source specification](f4-specification.md) when resolving methodological details. This self-contained adaptation preserves its roles, iterative lifecycle, record relationships and M1–M7 contracts. It is not a final validated framework. Original research: SME software-delivery requirements work, MRQ and SQ1–SQ3; O1 adaptive elicitation, O2 ethics/transparency, O3 integrated prototype, O4 repeatable measures, O5 comparative evaluation, O6 adoption guidance.

MRQ: How can a human-in-the-loop AI-enhanced workflow improve Business Analysis requirements work while preserving ethical safeguards and the Business Analyst's responsibility for final decisions?

| Mechanism | Instructions | Records / helper checks | Behavioural challenges | Limits |
|---|---|---|---|---|
| M1 evidence selection/provenance | Evidence mode; reviewed relevant context, omissions, privacy boundary | Sources/context/revision refs; support rejects unreviewed/irrelevant/empty evidence | B03, B04 | Host extraction/context/cloud controls differ; helper cannot observe provider routing. |
| M2 clarification/uncertainty | Clarify mode; actual answers, visible conflict, no invented thresholds | Clarifications/decisions; AI-origin confirmation and unresolved blockers rejected | B01, B02, B05 | Human identity and answer truth are asserted, not authenticated. |
| M3 bounded proposals | Draft task/input/output contract; limited repairs | Immutable original/context; referential/schema checks; stale adoption/write rejection | B06, B07 | No universal interception of host outputs; user/agent must use transactions. |
| M4 human adoption/accountability | Preserve selection, editing and rejection; adoption is draft | Proposal history, selected draft refs, human adoption; no AI approval | B08 | Recording review does not prove it occurred; conversation-only enforcement weaker. |
| M5 semantic quality/review | Review dimensions; human passage-to-proposition check | Verified trace attestations/reviews; structural support path checks | B09, B10 | Scripts cannot detect every contradiction or certify business fitness. |
| M6 approval/change integrity | Exact manifest, authority, blockers, partial scope, impact/revalidation | Append-only revisions; immutable snapshots; conservative dependency impact; atomic writes/recovery | B11, B12, B13 | Local JSON is editable outside helpers; no authenticated signature or encrypted storage. |
| M7 faithful document/handover | Selected revisions and real status; optional handover | Snapshot exports preserve exact records, manifest, open decisions and dependencies | B14, B15 | Markdown/Mermaid source guaranteed; host rendering/conversion qualified separately. |

The behavioural IDs refer to the public qualification cases supplied with the repository. Helper tests cover structural invariants; host tests cover observed agent behaviour. No table entry is an empirical participant result.

## Relationship to BA Mate

The application provides interface gates, source review, bounded proposals, local persistence, traceability, approval history and controlled changes. This package implements the method using host capabilities and JSON transactions rather than reproducing its screens or provider gateways. App Setup/Discover/Clarify/Define/Validate/Approve navigation is not the framework's mandatory stage sequence. Do not require artificial questions/answers, a separate diagram, or developer handover in every case.

Native BA Mate project packages are not compatible with this schema in v1. Import documents as reviewed evidence; do not silently translate application statuses or authority. Model replacement does not remove human review. Capability gaps must be disclosed, and private work, cloud inference and research collection remain separate flows.
