# 4 · Review, approve and handle changes

[Guide home](README.md) · [← Example](03-worked-example.md) · [Next: save and resume →](05-save-and-resume.md)

## Three different human decisions

![Three distinct human decisions: adopt selected proposals into a draft; verify the meaning against evidence; approve an exact revision manifest to create a baseline. A changed input triggers impact review and revised drafts while the earlier baseline is retained.](images/human-decisions.png)

**Adopt:** “Keep this proposal, with these edits.” BA Mate retains the original proposal and records your selection, edits or rejection. Adopted content is a working draft.

**Verify:** “I checked this passage, and it supports this specific claim.” Check the actual source wording and context. A correct file name or citation can still point to contradictory or irrelevant content.

**Approve:** An authorised person agrees to identified revisions within an explicit scope. A baseline retains that selection and its content. Approval is not automatically carried forward to later edits.

These decisions may happen at different times and involve different people. A host permission to read a file, run a helper or continue generating text is not business approval. Recorded authority and identity are assertions, not authenticated signatures.

## Review before approving

| Check | Ask yourself |
|---|---|
| Clarity | Can the intended reader understand the requirement in one way? |
| Completeness | Are necessary actors, conditions and exceptions covered? What remains missing? |
| Consistency | Do the evidence, answers and requirements agree? |
| Testability | Could someone observe whether the requirement is satisfied? |
| Relevance | Does it belong in the agreed scope and serve a business need? |
| Transparency | Are assumptions, inferences, omissions and limits visible? |
| Stakeholders | Have the relevant people and decision owners been represented? |
| Traceability | Does the actual supporting passage justify this exact revision? |
| Ethical risks | Are privacy, access, exclusion or other harms considered where relevant? |

AI review can help find issues, but it does not establish stakeholder agreement. Call a review independent only when another reviewer actually performed it. Helper validation checks structure and references; it cannot certify that a requirement is true or that evidence supports its meaning.

## Make approval scope visible

Ask BA Mate to present:

- Selected artifacts with their **actual IDs and revisions**, and the exact content to be retained.
- The decision owner and stated basis for their authority.
- Human evidence checks, resolved findings and readiness results.
- Explicit exclusions and any accepted nonblocking uncertainty, with its human disposition.
- Remaining blockers and the items they affect.

You can approve an unaffected subset while excluding blocked items, provided its prerequisites are satisfied. The baseline must not imply that the excluded items were approved.

Use your own actual decision. A statement can take this form after all placeholders are replaced:

```text
As [role], authorised on the basis of [actual authority basis], I approve
[actual manifest identifier or explicit IDs and revisions] for [scope].
I exclude [actual items]. I accept [identified nonblocking issues and reasons].
Record this decision and retain exactly the content I reviewed.
```

This is a template, not evidence of an approval. “Looks good,” silence, or asking to create a baseline must not be expanded into an invented decision. Existing clear authorisation does not need to be repeatedly requested, but missing authority or ambiguous scope must be resolved.

## When something changes

Source → requirement → acceptance criterion/model/document is the direction of impact. A citation list points back to evidence; a recorded `supports` trace points from the evidence toward the requirement.

When a source, answer or requirement changes, ask BA Mate to identify potentially affected dependencies. Review which are affected and why. A helper's impact list is a prompt for human investigation, not a verdict on business consequences.

Keep the earlier baseline. Create revised working drafts, update supporting links and revalidate affected items before any new approval. If a source contradicts an approved requirement, record the discrepancy and its consequences; the historical approval does not make the new source disappear.

For a small change you may need only an addendum and an impact report. For a larger change, revisit scope, stakeholders, evidence and process as needed.

---

**Next:** [Keep the work and resume safely →](05-save-and-resume.md)
