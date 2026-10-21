# Operating modes

Read only the requested mode and its dependencies. Deliver a concise artifact appropriate to the case. An explicit request to draft authorises drafting; it is not adoption, stakeholder confirmation or final approval. Record human decisions when actually supplied, without repeatedly asking for permissions already given.

## Start

Input: business need or existing project material. Establish goal, boundaries, affected roles, constraints, responsible stakeholders, authorised approver, intended artifacts and processing restrictions. Use a scope record and stakeholder/authority records. Unknown authority does not prevent discovery but prevents final approval. Do not equate the user controlling a chat with an authorised company approver. Choose new-project, existing-specification or change entry; disclose imported provenance and claimed statuses. State the next useful activity.

## Evidence

Input: scoped documents, interviews, messages or existing artifacts. Register source text, original location/provenance, extraction limitations, classification and relevant passages. Keep originals in the user's project when permitted; source text in records is the reviewed excerpt, not necessarily the whole original. Human extraction review checks fidelity; it does not certify the stakeholder's assertion as true. Mark unrelated or unreadable material excluded/limited. Create a context record with included ID/revision references, omissions, partial passages, task, host/provider location and limitations. Never convert PDF/image/audio failure into invented text. Use host extraction tools only if available and authorised.

## Clarify

Input: gaps, contradictions, missing criteria and unresolved assumptions. Questions include rationale, priority (blocking/important/optional), responsible human and affected record references. Ask the smallest useful batch; use choices only when they do not bias the answer or conceal uncertainty. Record the question even if another stakeholder must answer later. Actual answers include respondent and authority basis. Retain conflicting versions/answers and a reasoned authorised resolution; recency alone does not settle conflicting authorities. Simulated answers are illustrations with draft status. Defer nonblocking work with an owner/rationale; a deferred blocker still prevents affected approval.

## Draft

Input: reviewed evidence, confirmed decisions and a context manifest. Define a bounded task contract, e.g. requirements and criteria only, with the exact input revisions. Propose functional/nonfunctional requirements, rules or stories with rationale, priorities, source refs, assumptions and observable criteria. Do not add implementation choices, configuration screens, permissions, notifications or thresholds unless supported. Preserve the original proposal verbatim; use an `edited` field and explicit selected/rejected references for human changes. On adoption create only the selected records as drafts and proposed trace links. Draft acceptance is separate from final approval. Cite clarification answers where they determine meaning. Reject stale context or nonexistent references and regenerate/reconcile before adoption.

## Model

Input: selected scope, requirements/rules and actor decisions. Produce a textual process or Mermaid source covering normal steps, branches and exceptions. Link the process record to those revisions. Render/parse only with an available tool, and report the actual result. Human business review is separate from syntax checking. Return unsupported business steps to clarification. A textual process or justified not-applicable decision can satisfy a small case; do not require a diagram for every approval.

## Review

Input: selected artifact revisions and their evidence. Use [review.md](review.md). Record advisory findings and affected references; human disposition confirms or rejects findings. A human examines supporting passages/decisions before a proposed trace becomes verified. Keep false alarms, corrections and open risks visible. Mark an artifact in-review only after actual human review is recorded. Record revalidation against the current revision after change; do not infer it from passing structural checks.

## Document

Input: selected current revisions and intended deliverable. Use [../assets/artifact-templates.md](../assets/artifact-templates.md) for SRS, BRD, workshop summary, traceability report, addendum or impact report. Sections reference their source artifact revisions. New AI prose containing business commitments is a new proposal requiring support/review. Include open decisions and actual status. Do not copy obsolete wording while updating only a revision label. Markdown is guaranteed; Word/PDF requires a working host converter and checked output. Review any converted document against the canonical content.

## Baseline

Input: selected artifacts, current dependencies, required reviews, verified support and a human authority record. Present the exact manifest, exclusions, blockers and accepted nonblocking uncertainty. Use [review.md](review.md) for readiness. Human decides; record their actual statement, date, authority and decision scope. If approval is absent, report ready-for-human-review or draft. If supplied approval already clearly identifies revisions/authority, record it without asking for the same approval again. Use helper validation and baseline capture only for the recorded decision. A snapshot is a local workflow record, not an authenticated signature.

## Change

Input: new evidence, correction, request or changed business context. Retain the old baseline. Record trigger, prior revisions, potential dependencies and proposed impact. Helper impact is an over-approximation for human examination, not a certified complete business assessment. Human confirms affected/unaffected items and reasons. Append changed revisions; update dependent requirements, criteria, models and documents. Reverify traces and revalidate current revisions. New approval creates a new baseline; previous exports retain their original content/status. Do not silently propagate old approval or auto-clear pending reviews.

## Status / resume

Input: persistent state or user-supplied session ledger. Summarise scope, selected deliverables, current revisions, missing sources, open blockers, pending revalidation and available baseline/checkpoint IDs. Choose the next action based on the user's request. If records conflict with conversation, disclose the discrepancy and reconcile; do not overwrite them from memory. Distinguish missing information from zero events. For helper operations use the observed workspace revision.

## Handover

Input: a selected draft or baseline, requested developer-facing format. Export requirements, criteria, business process, provenance, constraints, open questions and exact status. Technical architecture, database schema or endpoint design is unspecified unless present in selected reviewed BA records; suggestions must be clearly separate proposals. Handover is optional and its non-use is not lifecycle failure.

## Failure and manual continuation

Keep original malformed/failed model output in a failed proposal when it can be safely represented; never adopt it. Two targeted repair attempts maximum per bounded task, then explain and continue manually or narrow the task. Do not fabricate capabilities, approvals, sources or successful exports. Without persistent tooling, update the [session ledger](../assets/session-ledger.md), disclose unchecked integrity and offer it for saving. Do not require a paid provider, new model download or automatic agent delegation.
