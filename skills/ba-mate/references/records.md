# Record contract — schema 1

Authoritative workspace: `ba-mate-workspace/state.json`. Use the helper `apply` transaction instead of editing this file. Previous record/trace revisions, baseline contents and proposal originals are retained. The Python runtime is optional; manual ledgers cannot reproduce atomic-write enforcement.

## Workspace

Fields: `schema_version` (1), `package_version` (1.0.0), `framework_version` (F4-draft.1), `workspace_revision` (starts at 1), and arrays `records`, `traces`, `pending_reviews`, `baselines`, `checkpoints`, `events`. Each mutation increments `workspace_revision` once. Do not use this number as an artifact revision. No application database, account, telemetry or native BA Mate ZIP import is implied.

## Record

Every record has exactly these fields:

```json
{
  "id": "R-1", "revision": 1, "type": "requirement", "status": "draft",
  "scope": {"id": "S-1", "revision": 1},
  "origin": {"kind": "ai", "actor": null}, "at": null,
  "content": {"text": "Proposed business behaviour awaiting review"},
  "references": [{"id": "E-1", "revision": 1}], "review": null
}
```

IDs begin with a letter and contain letters/digits/underscore/hyphen, maximum 80 characters. The same ID retains its type. Revisions are contiguous integers from 1. `scope` is null only for a scope record; other records refer to its ID/revision. A reference contains exactly `id` and `revision`. Use ISO 8601 timestamps with timezone; unknown record time/actor/model is null, never fabricated.

Types: scope, stakeholder, authority, source, context, clarification, requirement, business-rule, story, criterion, process, finding, assumption, risk, issue, decision, proposal, document, approval, change.

Statuses: draft, in-review, confirmed, rejected, open, resolved, deferred, excluded, not-applicable. **Artifact approval is represented by the approval decision and baseline manifest, not an arbitrary `approved` status on an artifact.** Origin kind: human, ai, source or unknown. Content carries type-specific business information; references carry actual record dependencies.

A human attestation is `{ "actor": "actual recorded human", "at": "2026-10-13T10:00:00+05:30", "basis": "actual decision or check" }`. Illustrative fields in documentation are not authority. Attestations are unauthenticated assertions; neither JSON nor a helper establishes identity or truth.

## Content by type

| Type | Content to record |
|---|---|
| scope | Goal, boundaries, constraints, affected stakeholders, intended deliverables, approval policy and processing restrictions. |
| stakeholder | Role, involvement, responsibilities and relevant inclusion concerns; avoid unnecessary personal details. |
| authority | For confirmed status require `person`, `role`, `basis`, human origin, and the correct scope. |
| source | Reviewed excerpt `text`, `provenance`, `locator`, `classification`, `extraction_reviewed`, `relevant`, limitations and original location when known. Support requires text/provenance, true review/relevance flags and human `review`. |
| context | Task, included references, omissions, partial material, processing location/provider, model when exposed, capability limits and output contract. Use `references` for included records. |
| clarification | `question`, rationale, `priority` blocking/important/optional, owner; confirmed answers require `answer`, `respondent`, `authority_basis` and identified human origin. `references` name affected items/evidence. |
| requirement / business-rule / story | `text`, rationale, priority, business value, assumptions and actor/behaviour/constraint. Criteria are separate criterion records; any `criteria_exception` is a justified human attestation. |
| criterion | Observable `text`, requirement/story revision references and boundary cases; no invented quantitative targets. |
| process | `text` containing process description or Mermaid source, notation, syntax-check result/limitation and business-review evidence. |
| finding / risk / issue / assumption | `text`, owner, severity (including `blocking`), affected references, disposition and rationale. Open nonblocking items accepted at approval require a human `disposition` attestation. Confirmed means recognised, not resolved. |
| decision | Actual decision, actor/authority basis, rationale and supporting/affected references. Human origin and review are needed for confirmed supporting decisions. |
| proposal | Immutable `original` text and `context` reference array; `disposition` pending/adopted/rejected/failed; task/model/limitations; `edited`, rejected items and reason when relevant. Adoption requires human `adoption` attestation and nonempty `selected` current draft artifact refs. A new input context needs a new proposal ID. |
| document | `text`, deliverable type, section dependencies and unresolved decisions; references name all included BA artifacts. |
| approval | `decision` approved/rejected, `authority` ref, `human_decision` attestation, `manifest`, `excluded`, `accepted_issues` ref arrays. Confirmed approval needs human origin. |
| change | Trigger, old baseline ID, prior/current refs, potential impact, human impact decision, revised outputs and revalidation/approval refs. |

Record confirmed stakeholders/decisions only from actual people, not AI personas. Source extraction review is not factual certification. Existing documents' embedded approval labels are imported claims until actual authority and revision scope are recorded.

Clarifications, findings, assumptions, risks and issues marked resolved, rejected, excluded or not-applicable require an explicit human `content.disposition` attestation. Deferred blockers still prevent affected approval. Accepted uncertainty must be a current nonblocking record in the approval's scope; excluded artifacts must belong to that scope. A confirmed clarification has an actual answer; confirmation of a risk or finding does not remove its unresolved effect.

## Trace

```json
{
  "id": "T-1", "revision": 1,
  "from": {"id": "E-1", "revision": 1},
  "to": {"id": "R-1", "revision": 1},
  "relation": "supports", "status": "proposed", "verification": null
}
```

Relation is supports or depends-on, directed from upstream input to downstream output. Status is proposed, verified or stale. Verified requires a human semantic `verification` attestation. Trace endpoints must share a scope. Append a new trace revision for changes; historical verification remains retrievable. A verified label on an old endpoint is not current verification.

## Apply and revalidation

A patch accepts only `records`, `traces`, `revalidated` arrays. Include only new IDs or the next revision. All referenced records must exist after the transaction. Revalidation entries are `{ "target": {"id":"R-1","revision":2}, "human_review": {"actor":"…","at":"…","basis":"…"} }`. The review is an explicit human dependency/meaning decision, not an AI-generated annotation.

On any existing record revision, direct/transitive dependants enter `pending_reviews`; scope revision conservatively affects its scope. Adding or revising a trace to an existing record also marks its target and downstream dependants for review, even when artifact text has not changed. Redirecting a trace marks both its former and new targets. Rejected, excluded or not-applicable records cannot establish a support path. New evidence may require a separately recorded impact assessment even if it has no previous dependency. Revalidation removes a pending item only for the current revision. It does not fix old references or confer approval. Update stale dependencies/traces and reviews separately.

## Snapshots and trust boundary

Baselines store an approval ref, exact snapshot contents, workspace revision, capture time and local SHA-256 integrity digest. Checkpoints preserve working contents for recovery. Digests detect accidental content changes; they are not signatures and never enter public analytics. Helpers cannot protect against a user deliberately rewriting the entire state and recomputing digests; direct state-file editing is unsupported.

Restore retains pre-restore work, appends recovered revisions as drafts, clears human review and source extraction-review flags, and proposes recovered traces. Later work absent from the checkpoint is retained as excluded working revisions with consistent remapped scopes/references; later traces are stale. Recovery records the human exclusion disposition for later uncertainty. It does not reinstate past authority/approval. Original proposal/approval history and baselines remain. Revalidate before any new approval.
