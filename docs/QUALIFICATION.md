# Host qualification for v1.0.5

Test installation and observed agent behaviour separately. A copied folder, valid manifest, available model selector or plausible answer alone is not a runtime pass.

## Repeatable fictional smoke test

1. Record the exact package/commit, host version/surface, model if exposed, date and tools. Unknown model/provider values remain null.
2. Make a new empty project outside real BA work. Install with the beta quickstart. Verify every installed resource matches the canonical skill, then open that project in the intended host.
3. Use a fresh chat for each task in [smoke-cases.json](../evaluation/smoke-cases.json). Give the model only the prompt, not the acceptance text or earlier answers. S01/S04/S05 explicitly request the skill; S02 tests natural selection; S03 is unrelated.
4. Observe actual discovery/read events and the response. Assess the acceptance text afterwards. Record pass, fail, blocked or not-run separately for every attempted task. If the model cannot be reached, record the failure, leave its model unknown if not exposed and do not mark behaviour passed.
5. Preserve the first attempt. Record evaluator assistance, retries, environment repairs and intervention. A corrected run does not erase the original failure. Repeat the affected journey if instructions/helpers change.
6. Retain permitted raw outputs locally. Publish only sanitised fictional observations. Summaries in [results](../evaluation/results) record host/model/task/result/assistance/failure; they are author-led smoke evidence, not independent participant outcomes.

Installation by a script is structural evidence until the host actually discovers the skill. UI-selected skills versus natural-language matching are distinct. A request to use an explicit path is assisted loading and does not qualify implicit discovery. Account/sign-in/network failures are environment blockers rather than invented model failures. Never disable security controls or create credentials to turn a blocked test into a pass.

## Claims

- **Documented:** the vendor describes the target path and invocation.
- **Structurally checked:** isolated installer, installed links, canonical resources and helper tests passed.
- **Observed beta behaviour:** identified tasks ran in an actual host, with concrete evidence and recorded limitations. This is not all-host or all-workflow qualification.
- **Unverified:** no successful observed runtime test for that surface/model/task, including blocked runs.
- **Supported:** reserve broad runtime support for successful B01–B15 and all three journeys on the identified host/model; any critical known failure prevents this claim.

Keep [COMPATIBILITY.md](COMPATIBILITY.md), release metadata and actual result records consistent. The five smoke tasks supplement [B01–B15](../evaluation/BEHAVIOURAL_CASES.md); they do not replace change, baseline, recovery or export qualification. Missing measurements remain missing. The application-based A/B/C research protocol remains separate.
