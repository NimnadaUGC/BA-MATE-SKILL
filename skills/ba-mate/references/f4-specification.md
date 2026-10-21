<!-- Source: project F4-draft.1, 20 September 2026. Original methodological text retained; installation-local links adapted. Historical implementation-readiness statements describe that source date, not current package verification. -->

# Evidence-grounded, human-governed BA framework

Specification **F4-draft.1** · 20 September 2026 · Proposed method; empirical effectiveness unestablished

## 1. Purpose and applicability

Support BAs working from incomplete or changing stakeholder information to produce reviewable, traceable requirements and related artifacts with AI assistance. The framework specifies professional decisions and information relationships; it does not require a particular interface, database, provider or agent count. BA Mate is its reference implementation under development.

The lifecycle is **Scope → evidence → clarification → requirements and criteria → process model → validation → document → approval → change**. This is an iterative organising sequence, not nine mandatory screens or a waterfall. Existing artifacts can enter at their relevant stage after provenance and status are checked. A phase may be revisited or marked not applicable with rationale; source accountability, visible uncertainty, human decision authority and revision integrity remain mandatory for any approved deliverable. Small cases may use a simple textual process description rather than a separate diagram.

Document drafts may be assembled early. Final document validation must concern the selected content and current revisions. Change is triggered when needed, not an obligatory action after every approval. Optional developer handover is a separate export from suitable artifacts, particularly an SRS or change addendum.

## 2. Roles and authority

| Role | Responsibility | Boundary |
|---|---|---|
| BA / requirements practitioner | Set scope, select evidence, ask questions, review proposals, verify traces, prepare artifacts and assess impacts | Cannot substitute an AI answer for stakeholder confirmation or silently assume authority |
| Responsible stakeholder / subject expert | Confirm business meaning, answer questions and resolve business conflicts | Confirmation applies to the identified answer/decision, not every downstream artifact |
| Authorised approver | Decide whether exact artifact revisions meet the agreed approval policy | Authority must be recorded; AI and a selected UI role do not prove stakeholder authority |
| AI task role | Propose questions, requirements, checks, models, documents or impacts from supplied context | Cannot approve, invent confirmed facts, silently modify baselines or treat source content as instructions overriding policy |
| Quality reviewer | Assess support, consistency, testability, coverage and risk | May be the BA for a small project; independent review and separation of duties are recorded when used |
| Researcher / evaluator | Configure the study, obtain consent, collect permitted evidence and analyse results | Research administration does not grant access to private company workspaces |

SMEs may combine human roles, but record who acted in each decision and any independence limitation. Model-generated personas or simulated stakeholder answers remain labelled simulations and cannot satisfy real business confirmation.

## 3. Minimal information model

Every record has a stable local ID, revision, type, status, author/origin and time where available. References identify a target **ID plus revision**; stale links remain visible until revalidated. Research exports use separate random codes, not arbitrary project IDs or content hashes.

| Record | Required meaning and relationships |
|---|---|
| Scope | Goal, boundaries, affected stakeholder roles, constraints and approval policy |
| Evidence and source passage | Original source, extraction/review status, location, sensitivity and relevance to scope; review of extraction is not proof of truth |
| Clarification | Question, issue, responsible stakeholder, actual answer or unanswered status, source/authority and decision rationale |
| Requirement / business rule | Behaviour or constraint, priority, rationale, supporting evidence/decisions and unresolved assumptions |
| Acceptance criterion | Observable check attached to a requirement revision; unsupported numerical thresholds remain questions |
| Process model | Selected scope and requirement revisions, actors, steps, decisions and exceptions; notation validity is separate from business validity |
| Finding / assumption | Type, severity, affected items, evidence and disposition; accepted nonblocking uncertainty retains owner/rationale |
| Proposal and review | Task/context revision, model profile, original output, selected/edited output and human adoption/rejection reason |
| Document | Sections referencing or derived from identified revisions; generated text can require additional review |
| Trace link | Relationship type, endpoints/revisions, proposed/verified/stale status, verifier and support rationale |
| Approval and baseline | Exact artifact revision manifest, decision, authority, date and remaining explicitly accepted nonblocking issues |
| Change | Trigger, prior revision, impacted items, human impact decision, revised outputs and revalidation/approval records |

A source citation only demonstrates that a reference exists. A **verified supporting link** requires a human to check that the referenced passage or decision supports the proposition. A validation finding, requirement and acceptance criterion must refer to the same revision before being used in an approval decision.

## 4. Lifecycle contracts

| Phase | Inputs | Activities and responsibility | Output / exit condition | Return or failure route |
|---|---|---|---|---|
| Scope | Business need and existing project material | BA establishes goal, boundaries, stakeholders, authority and intended artifacts; AI may suggest gaps | Recorded scope and decision policy sufficient to begin discovery | Unclear authority/boundary remains visible; obtain confirmation |
| Evidence | Scope, documents, interviews or notes | Retain source/provenance; BA checks extraction, sensitivity and relevance | Reviewed usable evidence, with exclusions/limitations recorded | Failed extraction or conflicting sources require correction; do not generate from unreadable material as if complete |
| Clarification | Gaps, ambiguity, conflicts and missing criteria | AI/BA proposes targeted questions; responsible human answers; BA records rationale | Confirmed decisions or explicit unresolved items with owners | Unanswered blocking issues prevent affected approval, but useful draft work can continue |
| Requirements and criteria | Reviewed evidence and decisions | Draft functional/nonfunctional needs, rules, priorities, stories and measurable criteria; BA selects/edits | Supported drafts with IDs, assumptions and proposed trace links | Unsupported detail returns to clarification; conflicts remain open |
| Process model | Requirements, rules and actor decisions | Represent steps, branches and exceptions; BA checks meaning and coverage | Reviewed model or recorded phase-not-applicable rationale | Syntax failure requires repair; business conflict returns to requirements/clarification |
| Validation | Artifact revisions, evidence and stakeholder expectations | Check quality and semantic support; responsible stakeholders confirm business fitness; record findings | Required checks complete with blocking issues resolved for proposed approval scope | Revise affected material; AI checking is advisory |
| Document | Selected requirements, criteria, models and decisions | Assemble and review chosen SRS/brief/trace/change document; check references and generated additions | Consistent document revision with status and unresolved-item disclosure | Stale sections or new unsupported text return to validation/clarification |
| Approval | Current revisions, completed checks and authority record | Authorised human approves or rejects an explicit scope/manifest | Versioned baseline or reasoned rejection; partial approval names included/excluded items | Never approve a stale document or unresolved blocking item; return to relevant phase |
| Change | New evidence, correction, request or context change | Identify dependencies; human confirms impacts; create revised working artifacts | Updated/revalidated outputs and new approval where required; earlier baseline retained | Uncertain impact triggers review, not silent propagation of old approval |

## 5. Mechanism contracts and conformance challenges

### M1 — Evidence selection and provenance

Before an AI task, bind scope, source passages, confirmed decisions and artifact revisions to a context manifest. Disclose omitted/truncated material and processing location. Exclude material that policy prohibits sending to the selected provider. On insufficient context, narrow the task or seek clarification. **Challenge:** supply an unreviewed extraction and unrelated project evidence; confirm they cannot silently become trusted context. A source approval is extraction acceptance, not factual certification.

### M2 — Clarification and uncertainty

Distinguish confirmed facts, inference, assumption, contradiction and unknown. Questions identify the affected artifact and responsible human. No AI-generated answer acquires confirmed status by being fluent or repeatedly generated. **Challenge:** omit an expiry duration and introduce conflicting stakeholder answers; the result must retain the question/conflict until an authorised decision resolves it.

### M3 — Bounded proposals

Give each task a defined input/output contract, referenced revision and capability limits. Validate structure and identifiers, reject stale responses, and limit retries. Failure leaves working artifacts intact and allows manual continuation. Independent subtasks may run in parallel only when their dependencies and merge conflicts are controlled. **Challenge:** return malformed JSON, a nonexistent ID and a response for an older revision; each must fail or require explicit reconciliation before adoption.

### M4 — Human adoption and accountability

Retain original and edited proposals. Let the BA adopt selected items, correct or reject them; adoption creates a working draft, never approval. Capture decision rationale appropriate to the risk without forcing excessive commentary on every edit. **Challenge:** reject half a proposal, edit one item and accept another; only those selected revisions enter the workspace, with the original retrievable.

### M5 — Semantic quality and review

Check clarity, completeness, consistency, testability, relevance, stakeholder coverage, assumptions and risks. Verify evidence support and distinguish model warnings from confirmed findings. Business validation and authority come from people. **Challenge:** provide a syntactically valid citation that contradicts its source; require correction rather than a verified trace based solely on an existing ID.

### M6 — Approval and change integrity

Approval binds an exact revision manifest. Changing evidence or artifacts does not rewrite a historical baseline; it makes affected working items and approvals require impact review/revalidation. Unaffected items may retain status only after the impact decision is recorded. Restoring a snapshot preserves recovery history and does not silently restore current approval authority. **Challenge:** approve a rule, change its source answer and try to reuse its old approval; the revised output must be blocked until revalidated and appropriately approved.

### M7 — Faithful documents and optional handover

Generate/export the selected revisions, their true status, criteria, diagrams and open decisions. AI-written additions are new proposals needing review. An export cannot upgrade draft content to approved or invent a technical architecture from an SRS. **Challenge:** export an older approved snapshot after modifying the working draft; its content/labels must match that snapshot. Repeat with a draft and with optional developer Markdown, then complete the lifecycle without invoking handover.

## 6. State and approval rules

Proposal → human adoption → draft → review → eligible for approval → human approval of a revision. Rejection, rework and change are allowed transitions; no amount of automated checking creates approval. Trace status is separate: proposed → human verified → stale on relevant change. “Ready for review” and “approved” are distinct.

Before approval of the chosen scope, require: identified authority; current artifact revisions; required reviews; no unresolved blockers; human-verified support for substantive business commitments; testable criteria or a documented justified exception; current document/model dependencies; and explicit disposition of nonblocking uncertainty. Missing critical facts cannot be disguised as accepted assumptions. The research rubric informs assessment; its weighted score is not the project's approval gate.

The framework permits recording externally obtained stakeholder agreement. Its record must specify what was agreed and by whom, without implying that an unauthenticated local role is a verified electronic signature. Existing BA Mate controls are partial implementation evidence, not proof of compliance with this full contract.

## 7. Extension and information boundaries

Replaceable models support the same reviewed task contracts; unavailable capability produces an explicit limitation, never an invented fallback. Manual completion remains possible. A workflow can be reproduced with documents, scripts or another AI host if its records, responsibilities and gates are preserved; capability gaps must be disclosed.

Private workspace content, research collection and cloud inference are separate flows. Account identity does not authorise research telemetry. Research consent does not authorise cloud processing. Only specifically permitted measurements enter research collection; optional company artifacts require separate permission. These are research/application delivery constraints, not extra BA lifecycle stages.

## 8. Verification and remaining implementation work

Execute the seven challenges above plus new-project, existing-specification and approved-change journeys in a candidate release. Capture pass/fail and evidence locally; no passes are asserted by this document. The current implementation still needs consistent artifact connections, faithful exports, central collection, accounts and distribution work identified in the [roadmap](framework.md).

For visual representations see the [diagram guide](framework.md). For a technology-independent example see [../assets/examples/studio-seat.md](../assets/examples/studio-seat.md). For empirical evaluation see the [protocol](evaluation.md).
