# Compatibility and capability limits

Documentation checked 13 October 2026. **Documented** means official support exists. **Structurally checked** means local bundle/resource/helper tests passed. **Runtime verified** requires a real installed host/session, recorded host/model version and observable behavioural evidence. One status never implies another.

| Target | Format | Current qualification |
|---|---|---|
| Codex | Portable plugin + direct skill | Documented; structural bundle checks. Runtime pending: local CLI wrapper cannot find its platform executable (ENOENT). No unrelated installation repair performed. |
| Claude Code | Plugin/marketplace + direct skill | Documented; structural bundle checks. Runtime pending; CLI unavailable on this machine. |
| Gemini CLI | Extension + direct skill | Documented; structural bundle checks. Runtime pending; CLI unavailable on this machine. |
| Antigravity IDE / 2.0 | Direct skill | Documented; structural bundle checks. Runtime pending; no host session used. |

No target is advertised as live-host verified. The scripts run locally without provider/model access. Behavioural host qualification procedures are in the source repository's evaluation material. Global/context paths and invocation differ by surface; see INSTALLATION.md.

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
