# 1 · Install and start

[Guide home](README.md) · [Next: modes and prompts →](02-modes-and-prompts.md)

## What you need

Use a host that can load local skills, with its normal account and model access already working. These instructions cover local Codex, Claude Code, Cursor, Antigravity App/IDE and Gemini CLI projects. They do not establish installation support in every web chat, mobile app or remote worker.

Create a separate folder for your fictional BA project, for example `pottery-booking-practice`. Keep it separate from the downloaded BA-MATE-SKILL project. The skill is the reusable instructions; your BA project holds the work produced using them.

## The simplest installation: copy one folder

1. Open the [BA-MATE-SKILL repository](https://github.com/NimnadaUGC/BA-MATE-SKILL). Select the branch or published package you intend to test, then download and extract it. For this guide, check that its `VERSION` file says `1.0.5`. A downloaded development branch can change; record its commit if available.
2. Inside the download, find `skills/ba-mate`. Copy the **whole `ba-mate` folder**, including its subfolders.
3. Place it inside your fictional project using the appropriate path below. Create the parent folders if needed. If a `ba-mate` folder already exists, save and inspect that installation before replacing it.

| Your host | Final location inside your BA project |
|---|---|
| Codex | `.agents/skills/ba-mate/` |
| Claude Code | `.claude/skills/ba-mate/` |
| Cursor | `.cursor/skills/ba-mate/` |
| Antigravity App / IDE | `.agents/skills/ba-mate/` |
| Gemini CLI | `.gemini/skills/ba-mate/` |

For example, Cursor should be able to find `pottery-booking-practice/.cursor/skills/ba-mate/SKILL.md`. The `references`, `assets` and `scripts` folders belong beside that file. Dot-prefixed folders may be hidden by your file browser; use its option to show hidden files.

Codex and Antigravity use the same project path. If you use both in one project, keep one copy there. Avoid duplicate installations in different discovery folders.

This folder-copy route needs no Python. If you prefer the optional installer, run this from the downloaded package's root, replacing the quoted path with your actual project:

```sh
python3 scripts/install_skill.py --host cursor --project "/path/to/pottery-booking-practice"
```

Choose `cursor`, `codex`, `claude`, `antigravity` or `gemini`. On Windows, use `py -3` instead of `python3` and a quoted Windows project path. The installer refuses to overwrite an existing skill. Global installation, plugin options and removal instructions are in the [full installation guide](../INSTALLATION.md).

## Open the right project and select the skill

Open **your fictional BA project** in the host and start a fresh conversation. Use its skill selector or the explicit invocation below when available.

| Host | How to request BA Mate |
|---|---|
| Codex | Select BA Mate in the available skill picker. CLI/IDE surfaces support `$ba-mate`; selection differs by surface. |
| Claude Code | For a direct folder installation, type `/ba-mate` followed by the task. The optional plugin uses `/ba-mate:ba-mate`. |
| Cursor | Type `/ba-mate`, or attach/select the installed skill using `@`. |
| Antigravity App / IDE | Ask to use BA Mate; the App documents `/ba-mate`. Use the IDE's available skill/customization controls. |
| Gemini CLI | Ask to use `ba-mate`. `/skills list` and `/skills reload` help inspect discovery; the optional extension supplies a `/ba-mate` wrapper. |

These are host-specific shortcuts to the **same skill**. For any mode, plain language is the fallback: “Use BA Mate to review this specification.” Confirm that the installed skill is available and, where the host exposes it, that its actual `SKILL.md` was loaded. A sensible answer alone does not prove skill activation.

The host mechanisms are described in the official [Codex/ChatGPT skills](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills), [Cursor](https://cursor.com/help/customization/skills), [Antigravity](https://antigravity.google/docs/skills) and [Gemini CLI](https://geminicli.com/docs/cli/skills/) documentation. These mechanisms and account requirements can change. Consult [our observed compatibility](../COMPATIBILITY.md) for what was actually tested.

## Try your first brief

Select the skill, then paste:

```text
Use BA Mate. This is a fictional practice project for a pottery studio.
We want customers to reserve workshop seats. Unpaid reservations should
be released quickly, but we have not decided the deadline or when it starts.

Start with scope and clarification. Separate facts, assumptions and unknowns.
Ask the most important business questions first. Do not invent a deadline,
payment method or notification policy. Keep everything as a draft.
```

Expect questions about the deadline, its starting event, payment confirmation, exceptions, stakeholders and decision authority. Questions can appear in a native question control or a numbered conversation. The skill should not supply made-up numerical defaults to fill a gap.

Answer with decisions for your fictional case, or say an answer is unknown and name who must decide. You can continue useful work on unaffected areas while a question remains open. You should not be asked to approve an affected item while its blocker remains unresolved.

Before you stop, ask it to save a session record or produce a ledger you can save. [Saving and resuming](05-save-and-resume.md) explains both options.

---

**Next:** [Find the right mode and prompt →](02-modes-and-prompts.md)
