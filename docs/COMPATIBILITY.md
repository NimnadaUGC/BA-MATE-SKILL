# Compatibility and capability limits — v1.0.5 beta

Checked 24 October 2026. Installation targets and behavioural qualification are separate. **Documented** means the vendor describes the skills mechanism; **structurally checked** means isolated installation/resources/helpers passed; **observed** means a stated task actually ran. Neither documentation nor a successful folder copy proves model behaviour.

| Host / tested surface | Installation target | Actual beta runtime evidence | Claim |
|---|---|---|---|
| Codex CLI 0.163.0-alpha.11.1, desktop-bundled CLI | Portable plugin or `.agents/skills/ba-mate` | gpt-6.1-sol configured default; five fresh smoke cases passed initially and all five repeated successfully on the final core. Explicit/implicit skill reads observed; unrelated question did not load it. | Observed beta smoke behaviour; broader workflows unverified. Separate Homebrew launcher still fails ENOENT. |
| Cursor 3.19.13, local IDE Agent | Direct `.cursor/skills/ba-mate` bundle | Active model Cursor Grok 4.6 Medium. Initial S01/S02/S03/S05 passed; S04 caught the semantic contradiction but its manual trace direction/relationship violated the contract. Ledger guidance corrected; final-core repeat was blocked by computer-use input/control failures. | Beta installation available, partial runtime evidence; corrected ledger behaviour remains unverified. No full runtime support claim. |
| Claude Code 2.1.197, CLI | Direct `.claude/skills/ba-mate` or plugin | `ba-mate` appeared in startup skill commands. S01 returned “Not logged in”; no model generation. Actual model unknown; requested model reported as claude-opus-5-5. Owner chose to retain unverified status. | Discovery observed; BA behaviour unverified, login required. |
| Antigravity App 2.19.1, local project | Direct `.agents/skills/ba-mate` | Model label Gemini 3.8 Flash Medium. S01 asked relevant questions but offered invented numerical examples. Clarify guidance corrected; repeat blocked by computer-use controls. Reading SKILL.md was not independently observed. | Failed initial clarification check; corrected behaviour unverified. Do not advertise runtime supported. |
| Antigravity standalone IDE / CLI | Direct skill at the documented paths | No completed behavioural runs on these surfaces. App evidence does not qualify them. | Documented / structurally checked only; runtime unverified. |
| Gemini CLI | Extension or direct `.gemini/skills/ba-mate` | Retained distribution target; not included in this round of actual model tests. | Documented / structurally checked only; runtime unverified. |

All five distribution targets have isolated installer/resource/helper coverage, including refusal to overwrite an existing skill and independence from unrelated settings. **No host has full B01–B15 and complete installed-host journey qualification.** Broad “supported” claims are withheld. These author-led fictional smoke runs are not research effectiveness or participant evidence. Proposed manual ledgers require human review and must not be treated as helper-validated JSON.

Use [BETA_QUICKSTART.md](BETA_QUICKSTART.md) for the simple project-local install and [QUALIFICATION.md](QUALIFICATION.md) to repeat a test. Sanitised prompts, results, assistance, failures and tested-core fingerprints are in the bundled [evaluation results](../evaluation/results/README.md). Private raw logs remain local; screenshots containing unrelated project names/paths are not release evidence.

Official mechanisms: [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills), [Cursor](https://cursor.com/help/customization/skills), [Antigravity](https://antigravity.google/docs/skills), [Gemini CLI](https://geminicli.com/docs/cli/skills/). No identical slash syntax, cloud-worker behaviour, account entitlement or model availability is promised.

| Capability | Behaviour |
|---|---|
| Filesystem + Python 3.10+ | Local helper transactions, histories, structural checks, snapshots and Markdown export. |
| Filesystem without Python | Host can prepare drafts/patches and manual records; helper checks cannot be claimed. Do not directly edit authoritative helper state. |
| No filesystem | Exportable manual ledger; no persistent or atomic-write assurance. |
| Native question UI absent | Conversational targeted questions. |
| PDF/image/audio extraction absent | Preserve supplied original/limitations; request readable content or use manual/local extraction when appropriate. No invented transcript/OCR. |
| Mermaid renderer absent | Deliver Mermaid source/textual process; syntax rendering unverified. |
| Word/PDF converter absent | Deliver Markdown; conversion unsupported rather than fabricated. |
| Independent reviewer absent | Self-review labelled as such; human review remains required. |
| Host processing location unknown/unsuitable | Use shareable context or local/manual work consistent with project policy. No helper routes around host privacy controls. |

Human review/authority fields are assertions, not authenticated signatures. Structural checks cannot certify semantics or regulatory compliance. Direct editing of state, recomputation of digests or an agent bypassing the helper is outside integrity guarantees. Native BA Mate project archives are not schema-1 imports. No telemetry/API/network transport exists in the helper.
