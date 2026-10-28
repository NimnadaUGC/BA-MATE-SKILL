# 6 · Help, glossary and beta feedback

[Guide home](README.md) · [← Save and resume](05-save-and-resume.md)

## Common questions

| What happened? | What to do |
|---|---|
| BA Mate does not appear | Check that the whole folder is installed inside the project you opened, at the [correct host path](01-start-here.md). Start a fresh chat or use the host's refresh controls. Confirm `SKILL.md` and its resource folders are present. |
| A slash command does not work | Check the [host-specific invocation](01-start-here.md#open-the-right-project-and-select-the-skill). Select the skill or ask “Use BA Mate…” and inspect actual loading. A mode such as Clarify is not universally `/clarify`. |
| Cursor's GitHub plugin import rejects this repo | Use the folder-copy or optional local installer route. This package is a direct Cursor skill bundle; it is not a Cursor marketplace plugin. |
| Login or model access stops the run | Resolve the host's normal account access if you choose to. Record the blocked attempt accurately; it is not a completed behaviour test. Claude Code runtime remains unverified in this beta. |
| The AI invents a deadline, stakeholder answer or policy | Do not accept the affected proposal. Preserve the failure, ask it to mark the gap and obtain an actual answer. Review dependent items and report a fictional reproduction. |
| A citation exists but contradicts the requirement | Record a semantic support finding. Revise/reject the proposal, verify the actual passage and keep affected approval blocked until resolved. |
| A PDF/image cannot be read | Supply a readable extract or use an available extraction tool. Retain the original and disclose omissions. Do not treat an invented transcript as evidence. |
| Python is unavailable | Continue with the [manual ledger](../../skills/ba-mate/assets/session-ledger.md). Clearly record that automated validation/persistence did not run. |
| A diagram is only code | Mermaid source is a valid portable output. Ask for a textual explanation or render it using an available tool; business review is still needed. |
| It asks too many questions | Request only questions affecting the current task first. Route others to the responsible person and continue unaffected draft work. |
| It calls its own review independent | Correct the record to self-review unless another reviewer actually performed it. |
| The installer says the skill already exists | Back up and compare the existing installation. Do not delete the entire host skills directory; replace only BA Mate after preserving local changes. |
| Can I import a native BA Mate application workspace ZIP? | Native application workspace interoperability is deferred. Provide readable material for reviewed import instead of claiming the formats are interchangeable. |

For observed host results, including retained failures and blocked repeats, see [compatibility](../COMPATIBILITY.md). Your chosen model and the host application are separate: record both when available. A different model in the same host may behave differently.

## A small BA glossary

| Term | In everyday language |
|---|---|
| Evidence | A source and the actual passages used to support a claim. |
| Requirement | A needed behaviour or quality that can be understood and checked. |
| Functional / nonfunctional | What the solution does / qualities or constraints it must satisfy. Neither justifies inventing targets. |
| Business rule | A policy or condition decided by the business. |
| User story | A short statement of who needs something, what they need and why. |
| Acceptance criterion | An observable condition for deciding whether a requirement is met. |
| Traceability | A recorded connection between exact source and artifact revisions, checked for meaning. |
| Proposal / draft | AI-generated candidate / working content selected or edited by a human. |
| Baseline | Retained selected revisions with an explicit authorised human approval record. |
| Impact / revalidation | What a change might affect / checking affected work again. |
| Blocker | An unresolved issue preventing approval of the items it affects. |

## A useful first public test

Use the [fictional journey](03-worked-example.md), or create your own fictional brief. Try clarification, proposal selection and a review. If you can, save/resume and introduce a source change. An unrelated question should not trigger an unnecessary BA workflow.

Record what actually happened. A repaired result does not erase the initial failure; record the assistance, rerun the failed case and its affected journey, and keep both outcomes. Unavailable host/model details and measurements stay **unknown/missing**, not zero or passed. The [qualification procedure](../QUALIFICATION.md) provides the fuller test set.

## Send feedback that others can reproduce

Open a [GitHub feedback issue](https://github.com/NimnadaUGC/BA-MATE-SKILL/issues/new/choose) and choose installation failure, workflow defect, unsupported AI commitment or suggestion. Use fictional, sanitised content. A compact report includes:

```text
Package version and source commit (if available):
Host / host version / surface (desktop, IDE or CLI):
Model name/version shown by the host, or unknown:
Installation route and skill activation observed:
Mode and fictional task:
Expected behaviour:
Actual result, including the failure or blocked step:
Assistance (edits, retries, extra prompts, manual repairs):
Sanitised reproduction and relevant output:
Repeat outcome, if actually rerun:
```

Use the [local run-record template](../../skills/ba-mate/assets/run-record.md) for fuller notes. Inspect attachments and screenshots for private names, paths, credentials and source material before posting. Do not attach private workspaces, participant records or unseen assessment material.

This package includes no telemetry or automatic research submission. Public issues are voluntary feedback, not consented study records. Skills testing is a portability/formative stream separate from the application-based controlled A/B/C evaluation.

## Updating or removing BA Mate

Save your project records and any local skill edits. Follow the [update/removal instructions](../INSTALLATION.md#removal-and-updates) for the installation route you used. Remove only the intended `ba-mate` skill or plugin; your BA workspace is separate and should remain available.

---

[Return to guide home](README.md) · [Copy a prompt](02-modes-and-prompts.md) · [Start a fictional test](03-worked-example.md)
