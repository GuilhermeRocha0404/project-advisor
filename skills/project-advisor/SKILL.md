---
name: project-advisor
description: "Set up or resume a dedicated project-advisor workspace, prepare focused prompts for a separate worker, and evaluate its results. One advisor folder per target project."
license: MIT
---

# Project Advisor

This skill prepares and resumes advisory workspaces. The method's single distribution source is [templates/AGENTS.md](templates/AGENTS.md); its installed copy is the workspace's `AGENTS.md`. There is no separate CORE. Installation alone does not activate an advisor in arbitrary chats or the worker's repository.

## Prepare a workspace

When the user asks to set up an advisor, establish the target project, a separate advisor directory, and the harness. Reuse confirmed paths; ask only for missing choices. One advisor folder belongs to one project. Do not put the advisor inside the target's directory tree or inside the installed skill, and do not install these instructions globally. Inspect existing local and ancestor instructions for conflicts.

Read an existing state before migration and confirm its project association; do not reset it. Preserve `CONSULTOR_STATE.md` for a legacy workspace rather than creating a competing state. If both state names exist, resolve which is authoritative with the user before writing. An existing external template takes precedence for creating state: initialize it with confirmed facts or unknown values, preserving the template. [references/STATE_SCHEMA.md](references/STATE_SCHEMA.md) is the fallback only.

Use Python 3.10+ and [scripts/workspace.py](scripts/workspace.py) to preview setup or update:

```sh
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex
```

Review the diff and apply within the user's authorization by repeating with `--apply`. Supported harness values are `codex`, `claude`, and `opencode`. For confirmed legacy state, add `--state-file CONSULTOR_STATE.md --adopt-existing-state`. The adoption flag confirms the association already checked by the advisor; the script cannot interpret arbitrary project history.

The script preserves existing state, writes a version/hash manifest and refuses unmanaged or locally modified instruction files. Updates use the same command and preview; an omitted --state-file retains the name in the manifest. When a refusal reveals custom rules, show the concrete diff and preserve them in `ADVISOR_LOCAL.md` or perform an explicitly authorized merge; never silently force an overwrite. Failed/interrupted multi-file setup requires inspecting the reported files before retrying. The manifest is written last, but the whole setup is not one filesystem transaction.

Codex and OpenCode use the workspace `AGENTS.md`. Claude Code additionally gets a `CLAUDE.md` containing `@AGENTS.md`. No global configuration, hooks, target code or automatic worker messaging is installed. For another harness, consult its actual local-instruction mechanism before adding an adapter; do not promise unsupported loading.

## Resume and deactivate

Open a new advisor chat in the prepared workspace. Loading its local instructions activates its advisor role for that project; read the installed `AGENTS.md`, manifest and state. Do not recreate them or copy the template into every prompt. If the harness has not loaded local instructions, explicitly read those files and disclose the limitation. Keep the same method available across model changes; do not claim they guarantee continuity.

The user may deactivate the advisor for the current chat; preserve state and stop routine advisory maintenance until reactivation. New chats in the dedicated folder start as advisors again. Outside a prepared workspace, explicit activation requires reading the method template and establishing the external project/state binding; do not write workspace instructions merely because the skill was read for review.

Verify setup with a fresh session: ask it to identify its role, bound project, state and next step without suggesting their values. Confirm relevant file reads, state preservation, and that it does not modify target code. Distinguish this runtime observation from installer tests and documentation checks. See [references/HARNESSES.md](references/HARNESSES.md) for documented loading and verification limits.

## Examples and evaluation

Use [references/EXAMPLES.md](references/EXAMPLES.md) for focused prompt/report examples and bounded behavioral checks. These examples are optional references, not a mandatory workflow.

The method is reusable across models; the supplied filesystem setup supports Codex, Claude Code and OpenCode adapters. In a chat without filesystem access, the user must supply the method and current handoff and save updates manually. Disclose that automatic loading, binding validation and persistent writes are unavailable. Do not claim that installing a package configures such a chat.
