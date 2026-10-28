# 3 · A fictional journey: pottery workshop reservations

[Guide home](README.md) · [← Modes](02-modes-and-prompts.md) · [Next: review and change →](04-review-and-change.md)

This is a newly written practice scenario, not a participant record or a fixed assessment key. All business facts and numbers below are **fictional scenario inputs**, not suggested defaults for real projects. Host outputs and IDs can differ; the checks describe the behaviour to look for, not a transcript of a completed host run.

## A · Begin with an incomplete brief

Use the [first brief](01-start-here.md#try-your-first-brief): customers reserve workshop seats; unpaid reservations should be released “quickly”; the deadline and starting event are undecided.

A useful response establishes boundaries and asks who can decide the rule. It should ask what “quickly” means rather than filling the gap with a convenient number. It should not silently add online payment, reminder messages or a particular database.

## B · Supply actual answers for the fictional case

After its questions, reply with these scenario decisions:

```text
For this fictional exercise I am role-playing the studio owner, authorised
to decide the reservation rules. Please record that as a practice assertion.

Use these answers as the owner's fictional interview note:
- This exercise covers workshops booked at least seven days before they start.
- Staff enter reservations and record confirmed payments manually.
- The hold begins when staff confirm the reservation.
- Release a still-unpaid seat 36 elapsed hours after that confirmation.
- A payment recorded by the deadline counts as paid; paid seats must not release.
- The release step runs automatically at the deadline in this scenario.
- Late bookings, refunds, reminders and customer self-service are outside scope.

Register the note and the relevant passages. Show me the extraction and
questions about any remaining ambiguity before drafting affected items.
```

You are providing the decision rather than accepting an invented one. Inspect the extracted note against your actual message. If you spot a mistake, correct it explicitly and keep the correction in the record.

## C · Draft and select

Ask for a small set first:

```text
Use BA Mate to propose the unpaid-reservation requirement and its acceptance
criteria from the reviewed note. Show the supporting passages, preserve the
original proposals and leave the output as draft for my selection.
```

An illustrative requirement could read:

> Within the agreed booking scope, the system shall release a reserved seat at 36 elapsed hours after staff confirm the reservation when no confirmed payment has been recorded by that deadline.

Its criteria should distinguish unpaid, paid and boundary cases. For example, a confirmed payment recorded exactly at the deadline must not cause the seat to release under the owner's note. If the evidence does not settle an implementation-level race condition, record that open detail for delivery rather than claiming a tested solution.

Ask to remove unsupported suggestions such as an email reminder:

```text
Adopt the proposal that follows the reviewed release rule as a working draft.
Reject any reminder proposal as outside scope. Preserve both the original
proposal and my selection/rejection decisions. This is not baseline approval.
```

Use the real proposal references shown in your session if several items match. An AI-created reference is usable only if its record actually exists.

## D · Review the meaning, not just the citation

Ask:

```text
Use BA Mate to review the selected draft against the owner's actual note.
Check the timer start, elapsed-hours wording, paid-seat exclusion, deadline
boundary and scope. Show upstream-to-downstream trace links and open issues.
```

A statement that “all seats release after 36 hours” conflicts with the paid-seat exclusion, even if it cites the correct note. Identify the mismatch, retain the finding and revise the affected draft. A valid source ID alone does not establish semantic support.

You can also ask for a textual process or Mermaid: staff confirm → hold begins → payment decision at deadline → retain paid seat or release unpaid seat. Any missing exception stays visible.

## E · Prepare a small, explicit baseline

Ask for readiness and an exact manifest. Check the selected requirement, criteria and supporting review records. Exclude anything still unresolved or outside scope. Then, only if you intend approval in this fictional role, provide a decision referring to the **actual manifest and revisions** shown in your session.

The recorded decision must say this is a fictional practice approval. It must not imply that a real studio or stakeholder signed off. After recording it, request a baseline export and compare the retained content with what you approved.

## F · Introduce a change

```text
Use BA Mate Change mode. In this fictional exercise the owner now requests
a 48-elapsed-hour unpaid hold instead of 36. This is a proposed change,
not approval. Preserve the earlier baseline. Identify affected requirements,
criteria, process and documents, and prepare revised drafts for revalidation.
```

Expect the old baseline to retain **36 hours**. New working drafts may propose **48 hours**, linked to the new source/decision. Review the impacts and revised evidence support, then decide separately whether to approve a new baseline. Exporting the historical baseline must not silently substitute the new wording.

## Two other ways to begin

**Already have a specification?** Supply it and ask BA Mate to register it as imported evidence, identify unknown origins and review unsupported commitments. An “Approved” heading is a claim until supported by actual human approval records. Do not silently convert it into an authenticated baseline.

**Only need a change review?** Supply the retained baseline, its approval scope and the new request. Ask for impact candidates and gaps before drafting. If the baseline or history is unavailable, continue with a clearly labelled provisional analysis and disclose that limitation.

Keep your actual result, assistance and failures in a [local run record](../../skills/ba-mate/assets/run-record.md). Do not mark this journey passed merely because you read the example.

---

**Next:** [Make human review and approval clear →](04-review-and-change.md)
