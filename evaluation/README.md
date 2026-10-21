# Public conformance qualification

Use [BEHAVIOURAL_CASES.md](BEHAVIOURAL_CASES.md) and the blank [qualification record](qualification-record.json). These are public synthetic challenges, not unseen assessment cases or private study keys. Test actual installed-host behaviour; automated helper/package tests do not establish activation reliability, semantic correctness or independent review.

For each host/version/model: install into an isolated synthetic project, confirm resource access, start a fresh session, run the stated request with only the stated material, and retain permitted output/decisions locally. Record observed behaviour, failure, assistance and limitations. Do not provide the acceptance checklist as instructions during the first forward test; use it afterwards to assess the output. Use separate fresh sessions for explicit, implicit and unrelated-request activation tests to avoid teaching the answer through prior context.

The evaluator supplies labelled fictional human answers/approval only when the case calls for them. They are not real stakeholder decisions. On failure, preserve the first attempt, repair a narrow cause, rerun that challenge and its affected journey, and record old/new versions. A critical known failure prevents runtime-supported claims for that host. Report missing runs honestly.

Synthetic rehearsals can be repeated without credentials using `python3 scripts/rehearse.py`. Live host calls may depend on user access; no new paid credentials/models or telemetry are created by this repository.
