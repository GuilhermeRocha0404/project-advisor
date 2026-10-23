# Project Advisor

**English** · [Português (Brasil)](.github/readme/README.pt-BR.md)

A model-independent project advisory method with workspace adapters for Codex, Claude Code and OpenCode.

Use one chat to decide what is worth doing next and another agent to investigate, implement, and verify. The advisor challenges weak assumptions, recommends a proportionate process, and evaluates results. You retain decisions about goals, priorities, and preferences.

The methodology has no required model, vendor, plugin, or external service. It is intended for development projects across agent environments that can load its instructions and supporting files.

## Example workflow

You want to add CSV customer imports to an existing application.

| Step | Who | Example |
|---|---|---|
| Explain the goal | You → advisor | "I want staff to import customer CSV files without creating duplicate records." |
| Clarify a real ambiguity | Advisor ↔ you | "Should a repeated email update the existing customer or be reported for review?" You choose review. |
| Prepare execution | Advisor → you | A worker prompt defining the import behavior, duplicate handling, existing authorization constraints, and evidence needed for completion. |
| Execute | You → worker | You pass the prompt to the worker in the project workspace. It investigates, implements, and verifies. |
| Bring the result back | You → advisor | The worker reports successful imports and checks for malformed rows and duplicates within a file. |
| Assess the evidence | Advisor → you | It notices that importing the same file twice was not checked and requests that specific verification. |
| Close or correct | Worker → you → advisor | The result demonstrates the expected behavior, or a defect is corrected. The advisor closes the task when evidence is sufficient. |

This is an example, not a mandatory sequence. Clear tasks can proceed directly; unnecessary planning and repeated verification are discouraged. The skill does not automatically connect or send messages between chats.

## Recommended setup

Use one dedicated advisor folder and chat per target project, outside its directory tree. Another project gets another folder and a clean state. The worker stays in the target repository. Global and ancestor instructions can still apply; this is not complete isolation.

## Install

Copy the complete `skills/project-advisor` folder to your harness’s personal skill directory. Keep `templates/`, `scripts/`, `references/`, and `agents/`. Codex: `~/.agents/skills/project-advisor`; Claude Code: `~/.claude/skills/project-advisor`; OpenCode: `~/.config/opencode/skills/project-advisor`. Use Python 3.10+ to preview workspace setup, then repeat with `--apply` after reviewing the diff. Replace the example paths and choose `codex`, `claude`, or `opencode`.

```sh
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex
python <skill-dir>/scripts/workspace.py --workspace <advisor-dir> --project <target-dir> --harness codex --apply
```

Codex: `$project-advisor` · Claude Code: `/project-advisor` · OpenCode: `project-advisor`

[Codex / Claude Code / OpenCode — setup, updates, migration](skills/project-advisor/references/HARNESSES.md)

## Activate and use

Open a fresh chat in the prepared advisor folder. Loading its local instructions starts the advisor for its bound project; installing the skill alone does not activate other chats. Ask the agent to identify its role, project, state and next step to verify loading. Explicit deactivation applies to the current chat; a new chat in the dedicated folder starts as advisor again. Responses follow your preferred language. To resume explicitly, load the workspace AGENTS.md, binding and state.

## What the advisor does

- Connects the next task to a useful project outcome.
- Challenges decisions when it identifies a concrete problem and proposes alternatives.
- Asks about preferences, priorities, intent, and facts you can clarify.
- Uses directed investigation for technical or specialist questions.
- Adjusts planning, delegation, and verification to risk and uncertainty.
- Evaluates worker evidence and stops when the task is sufficiently complete.
- Respects informed decisions and authorization boundaries.
- Maintains a concise, current handoff rather than an accumulating activity log.

## Evidence and supported environments

This is a proposed working method, not a demonstrated productivity improvement. There is no controlled comparison of quality, time or cost against a single-agent workflow. Installer tests verify filesystem behavior; behavioral observations are limited scenarios.

Filesystem adapters are supplied for Codex, Claude Code and OpenCode. Runtime validation status is recorded in [HARNESSES.md](skills/project-advisor/references/HARNESSES.md); adapter generation is not proof of runtime loading. For chats without filesystem access, provide the method and current handoff manually and save updates yourself. Automatic binding checks and persistence are unavailable there.

## State, privacy, and limits

The installed `AGENTS.md` contains the method; `CLAUDE.md` imports it only when needed. `.advisor-workspace.json` records the project, harness, method version and managed-file hashes. `ADVISOR_STATE.md` holds private decisions and progress; legacy `CONSULTOR_STATE.md` can be retained. Inspect existing state before using `--adopt-existing-state`. Keep custom preferences in `ADVISOR_LOCAL.md`. Updates use the same preview/apply command and refuse changed managed files; review and merge personal changes explicitly. Existing state is never replaced by the installer. State maintenance remains model-driven, without hooks or a background service. Documentation and installer tests do not certify runtime behavior in every harness.

## Repository layout

The template is the single release source; each workspace receives a versioned copy. There is no separate CORE. Updating the skill does not silently update workspaces. Keep private state, bindings and local preferences outside the public repository.

```text
skills/project-advisor/
├── SKILL.md
├── templates/AGENTS.md
├── scripts/workspace.py
├── agents/openai.yaml
└── references/
    ├── HARNESSES.md
    ├── EXAMPLES.md
    └── STATE_SCHEMA.md
```

## Contributing

Describe a real problem, the expected behavior, and why the proposed change helps without adding unnecessary process. Use synthetic examples, remove private information, and report the environment and limitations of any behavioral checks. Improvements should preserve the distinction between reusable guidance and personal or project-specific preferences.

Maintain README documentation in English and Brazilian Portuguese only. The Portuguese version lives in `.github/readme/README.pt-BR.md`. Update both versions together so examples, commands, links and limitations remain aligned.

## License

[MIT](LICENSE) — Copyright (c) 2026 Guilherme Rocha.

## Audit revision 2.1

State reconciliation now protects open verification and active constraints, records evidence provenance, and removes superseded directions at closure or replacement. The installer shares one state schema, preserves legacy state names on update, validates manifests, explains stale-lock recovery and rejects overlapping skill/workspace trees. Existing state is never reset.

See [audit decisions and verification](docs/AUDIT_2_1.md) and [examples](skills/project-advisor/references/EXAMPLES.md). English and Brazilian Portuguese are the maintained README languages; English is the technical reference. Translation wording has not received independent native-speaker review.
