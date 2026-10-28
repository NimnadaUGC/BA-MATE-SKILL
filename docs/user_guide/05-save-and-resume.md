# 5 · Save, resume and export

[Guide home](README.md) · [← Review](04-review-and-change.md) · [Next: help and feedback →](06-help-and-feedback.md)

## Choose the record option your host can actually use

| Available capability | How to keep your work |
|---|---|
| Project file access and Python 3.10+ | Ask BA Mate to use the optional helper and a dedicated `ba-mate-workspace` folder inside your BA project. JSON records are authoritative; Markdown is for readers. |
| Project files but no Python | Save a manual ledger and artifacts. Automated integrity checks have not run; do not directly edit an existing helper-managed state file. |
| Conversation only | Ask for a complete exportable ledger, copy it into a local file and supply it in the next session. The AI must not claim it saved files it cannot write. |

The helper is optional and uses Python's standard library. You can do BA work without it. Its atomic writes, stale-write checks and snapshots apply only when those helper operations actually run successfully. They do not authenticate approvals or verify source meaning.

## Save before ending a session

```text
Use BA Mate to prepare for stopping. Save through the helper if it is
available, or give me a complete manual ledger I can save. Include scope,
sources and limitations, actual answers, proposal history, current revisions,
trace links, reviews, approval boundaries, open issues and next steps.
Tell me exactly where work was saved and which checks actually ran.
```

For a manual session, use the [session ledger template](../../skills/ba-mate/assets/session-ledger.md). Save it with the actual evidence and artifacts needed to understand its references. A short chat summary alone may omit source passages, rejected proposals or the exact content previously approved.

Keep ordinary project records outside the public skill repository. A suitable separation is:

```text
BA-MATE-SKILL/                reusable downloaded package
pottery-booking-practice/     your chosen fictional BA project
  .cursor/skills/ba-mate/     installed reusable skill (example host)
  ba-mate-workspace/          project records, when using the helper
  artifacts/                 reader-facing exports, if you choose this folder
```

The workspace path does not determine where the host processes prompts. Check your host and project policy before supplying sensitive content; a local helper does not make a cloud model local.

## Resume from records

Open the same project, make the saved workspace or ledger available, and ask:

```text
Use BA Mate to resume from these records. Confirm what you can actually read.
Show the current scope, selected revisions, retained baselines, open decisions,
stale dependencies and next useful action. Reconcile conflicts before claiming
that anything is current or approved.
```

If the records are unavailable, supply what you have and ask for a provisional reconstruction. Missing history stays missing; the AI should not pretend to remember an earlier conversation it cannot access. Importing an existing specification also does not establish its claimed approval status.

## Export for the right audience

Ask for the output you need: SRS (Software Requirements Specification), BRD (Business Requirements Document), workshop summary, requirements addendum, traceability report, change-impact report or optional developer handover.

```text
Use BA Mate to export the selected current working revisions as a draft
requirements document in Markdown. Show status, scope, exact references and
unresolved items. Tell me which selected items could not be exported.
```

For historical work:

```text
Use BA Mate to export the retained baseline I select below. Reproduce its
approved snapshot content and revision scope, rather than substituting newer
working text. Disclose later changes separately from that historical content.
```

Use the real baseline reference from your records. Draft exports and historical baseline exports serve different purposes; check the label and content before sharing.

Markdown and Mermaid source are the portable formats. Word/PDF conversion and rendered diagrams depend on tools actually available in the host. Ask it to check the produced file; do not accept a claim that an unavailable converter or renderer ran.

## Recover after a failed operation

If a helper rejects a stale update, stop that write, reload the current records and reconcile your intended change. Do not force an old patch over newer work. If generation fails, retain the original/failed proposal and continue manually from the last trustworthy records.

Request a checkpoint before substantial revisions. A checkpoint is a recoverable working snapshot, not a business baseline. Restoring one through the helper creates working drafts requiring review; it does not restore approval automatically. Back up the whole workspace before recovery and preserve the earlier baselines.

For precise helper operations, use the [helper guide](../../skills/ba-mate/references/helpers.md). Ask the host to perform them only when it has the required access; the manual ledger remains the fallback.

---

**Next:** [Troubleshoot or report your test →](06-help-and-feedback.md)
