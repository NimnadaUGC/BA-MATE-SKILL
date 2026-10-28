# Try BA Mate v1.0.5 beta

Prefer a guided introduction? Open the [BA Mate User Guide](user_guide/README.md) for illustrated explanations, copyable prompts and a fictional BA journey.

Use a new fictional project first. This is a beta implementation of F4-draft.1; host qualification is limited to the observations in [COMPATIBILITY.md](COMPATIBILITY.md). Installation does not establish research effectiveness.

## Install in a project

Download and extract the v1.0.5 source/host archive, or check out the development branch:

```sh
git clone --branch dev/v1.0.5 --single-branch https://github.com/NimnadaUGC/BA-MATE-SKILL.git
cd BA-MATE-SKILL
python3 scripts/install_skill.py --host cursor --project /absolute/path/to/your-fictional-project
```

Choose `cursor`, `codex`, `claude`, `antigravity` or `gemini`. The default scope is just the chosen project. On Windows use `py -3` instead of `python3` and your actual Windows project path. The installer refuses an existing skill; it does not change account settings or enable cloud synchronisation. A development branch can move; use the package version and commit when recording a test.

Without Python, copy the complete `skills/ba-mate` directory into the chosen project: `.cursor/skills/ba-mate` for Cursor, `.agents/skills/ba-mate` for Codex/Antigravity, `.claude/skills/ba-mate` for Claude Code, or `.gemini/skills/ba-mate` for Gemini CLI. Do not copy only SKILL.md.

Open **that project** in the host, start a fresh chat and use:

> Use BA Mate to clarify this fictional brief: Our pottery studio should release unclaimed workshop seats quickly. We have not decided when the timer starts or how long it runs.

Cursor also documents `/ba-mate` or attaching the skill with `@`; Codex CLI supports `$ba-mate`; Claude Code direct installs support `/ba-mate`. Confirm the skill is visible and that its actual file is read. Natural-language matching is not guaranteed merely because the response looks sensible.

Expect targeted questions rather than an invented duration. Answer using fictional decisions. AI suggestions remain drafts until an actual human reviews/adopts them; approval binds exact revisions separately.

## Report a result

Record package/host/model, task, observed output, assistance and any failure using [the qualification procedure](QUALIFICATION.md). Public GitHub feedback must use a sanitised fictional reproduction. Private BA work and consented study material stay outside this repository.

For removal, delete only the copied `ba-mate` folder after saving local edits. Keep BA project records separately. Full platform/plugin/global instructions are in [INSTALLATION.md](INSTALLATION.md).
