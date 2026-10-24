# Installation and removal

Install into a chosen project first. The canonical source is `skills/ba-mate`; copy the whole folder, including references/assets/scripts. Do not install a lone SKILL.md or flatten nested resources. Existing installations must be preserved/reconciled before replacement. The installer copies only this skill and refuses overwrites; it does not change settings.

For a first fictional test, use [the beta quickstart](BETA_QUICKSTART.md). Exact observed qualification and failures are in [COMPATIBILITY.md](COMPATIBILITY.md).

## Direct installation (all five hosts)

From an extracted source or host distribution root:

```sh
python3 scripts/install_skill.py --host codex --scope workspace --project /path/to/your/project
```

Choose host `codex`, `claude`, `gemini`, `antigravity` or `cursor`. For a global install use `--scope user` instead; inspect the target below. On Windows use `py -3` and a Windows path. Without Python copy the folder manually to a target that does not already exist. No model/key installation is needed; actual host generation requires the host's normal account/model access.

| Host | Workspace folder | User folder | Invocation |
|---|---|---|---|
| Codex | `.agents/skills/ba-mate` | `~/.agents/skills/ba-mate` | `$ba-mate` or natural-language selection; selectors vary by surface. |
| Claude Code | `.claude/skills/ba-mate` | `~/.claude/skills/ba-mate` | `/ba-mate clarify this brief` for direct skill; plugin invocation is namespaced. |
| Gemini CLI | `.gemini/skills/ba-mate` | `~/.gemini/skills/ba-mate` | Ask to use ba-mate; `/skills list` and `/skills reload` inspect discovery. Workspace trust/activation consent applies. |
| Antigravity IDE / 2.0 | `.agents/skills/ba-mate` | `~/.gemini/config/skills/ba-mate` | Ask to use ba-mate; 2.0 documents `/ba-mate`. Inspect active skills in the IDE Customizations panel. |
| Cursor | `.cursor/skills/ba-mate` | `~/.cursor/skills/ba-mate` | `/ba-mate`, attach with `@`, or ask to use BA Mate. Natural selection must be observed on the installed version. |

Codex and Antigravity share the workspace `.agents/skills` convention: one installation there can serve both; do not attempt to overwrite it for the second host. Antigravity IDE also documents the legacy `~/.gemini/antigravity/skills` path. CLI global paths differ; use its documented workspace path for this direct bundle.

Examples: `Use BA Mate to clarify this business brief`; `Use BA Mate to review an existing specification and identify unsupported commitments`; `Use BA Mate to assess this change against baseline BL-…`. A mode name is an argument, not a promise that eleven native slash commands exist.

Official locations/invocation (checked 24 October 2026): [ChatGPT/Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude skills](https://code.claude.com/docs/en/skills), [Gemini skills](https://geminicli.com/docs/cli/skills/), [Antigravity skills](https://antigravity.google/docs/skills?tab=ide), [Cursor skills](https://cursor.com/help/customization/skills). Availability varies by host/version/account; consult the compatibility record instead of treating documentation as a runtime pass.

## Cursor direct bundle

Extract `ba-mate-cursor-1.0.5.zip`. From its root run `python3 scripts/install_skill.py --host cursor --project /path/to/project`. The archive contains the identical canonical skill under `skills/ba-mate`; the installer places it in `.cursor/skills/ba-mate` in the chosen project. Open that project in Cursor and start a fresh chat. Do not install duplicate copies under both `.cursor/skills` and `.agents/skills`.

This is a direct skill bundle, not a Cursor marketplace plugin. Cursor's From GitHub Repository plugin import requires its marketplace metadata; use this local-folder beta route for this repository. The ordinary repo download alone does not install the skill. Project-local installation does not enable personal skill sync, change permissions or send project records anywhere. Cloud/remote workers and their project context need separate qualification; no local smoke result qualifies them. See [Cursor's full reference](https://cursor.com/docs/skills).

## Codex portable plugin

Extract the Codex archive. Its root `plugin.json` and `skills/` follow the [portable packaging format](https://developers.openai.com/plugins/build/plugins). Add this package through the host's supported local plugin/marketplace interface, or use direct installation above. Building this archive does not publish a directory listing or grant account capabilities. ChatGPT Work/plugin surfaces require their supported installation process; regular chat should not be assumed to accept a repository folder. Helpers need a filesystem/Python-capable environment.

## Claude Code plugin / marketplace

Extract the Claude archive; its root includes `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` and `skills/`. In Claude Code:

```text
/plugin marketplace add /absolute/path/to/ba-mate-claude
/plugin install ba-mate@ba-mate-research
```

Invoke `/ba-mate:ba-mate clarify this brief`. For local authoring Claude also supports `claude --plugin-dir /absolute/path/to/ba-mate-claude`. Do not install both direct and plugin copies unless intentionally testing collision behaviour. After GitHub publication, users can add the actual repository through its documented marketplace mechanism; no repository URL is invented here. See [marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) and [manifest reference](https://code.claude.com/docs/en/plugins-reference).

## Gemini CLI extension

Extract the Gemini archive. Its root `gemini-extension.json`, `skills/` and `commands/ba-mate.toml` are self-contained. For local development use:

```sh
gemini extensions link /absolute/path/to/ba-mate-gemini
```

Ask to use ba-mate, or invoke the extension's `/ba-mate` wrapper with the task as its arguments. The wrapper routes to the canonical skill; it is not a separate governance copy. Users can install the actual Git repository after publication because the source root also includes the extension manifest. Discovery/activation and workspace trust follow Gemini's normal controls. See [extension reference](https://geminicli.com/docs/extensions/reference/).

## Antigravity direct bundle

Extract the Antigravity archive and copy/install its skill into the documented workspace/global folder above. This release targets direct skills on IDE/2.0; no untested CLI plugin manifest is invented. Use natural-language fallback if the surface lacks a selector/slash invocation. See [current surface-specific documentation](https://antigravity.google/docs/skills?tab=ide).

## Removal and updates

For a direct installation, back up local modifications and remove only the copied `ba-mate` skill folder listed above; BA project records live separately and should remain. Do not remove the whole skills directory. For Claude use the host's plugin uninstall action (`/plugin uninstall ba-mate@ba-mate-research`) and remove the marketplace only if no longer wanted. For Gemini use `gemini extensions uninstall ba-mate`; direct skills can instead be uninstalled through its skills manager or the exact copied folder. For Codex use its plugin removal interface. No uninstall automatically deletes private workspaces.

For updates preserve the old installation, inspect the new release, replace only the intended skill/package, and resume from local state after validation. Schema 1 is fixed in v1; unsupported future schemas fail explicitly rather than being silently migrated.
