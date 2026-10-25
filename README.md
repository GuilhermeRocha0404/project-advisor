# Project Advisor

**English** · [Português (Brasil)](.github/readme/README.pt-BR.md)

A model-independent project advisory method with workspace adapters for Codex, Claude Code and OpenCode.

Long coding-agent conversations can lose decisions and leave completion claims unsupported. Project Advisor aims to keep decisions, continuity and evidence review in an advisor workspace; a separate worker investigates, implements and verifies inside the project. You retain control of goals and priorities.

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

## Quick start

For an existing project at `../sample-app`, run from this repository root (or replace the script path with your installed copy):

```sh
python skills/project-advisor/scripts/workspace.py --workspace ../sample-advisor --project ../sample-app --harness codex
python skills/project-advisor/scripts/workspace.py --workspace ../sample-advisor --project ../sample-app --harness codex --apply
```

Review the preview before the second command. Open a fresh advisor chat in `../sample-advisor` and ask: "Identify your role, bound project and next step. I want staff to import customer CSV files; repeated emails should be reported for review. Help me choose the first useful delivery."

The generated `ADVISOR_STATE.md` starts with unknown facts. As decisions are made, the advisor maintains a handoff such as this synthetic excerpt; keep the other generated sections and record remaining unknowns:

```md
## Active objective and authorization
CSV customer import; planning authorized, implementation not yet authorized.

## Active decisions and constraints
Repeated emails go to review; existing customers must not be overwritten.

## Latest worker task and evidence
No worker task sent and no execution evidence received.

## Next step
Clarify which staff roles may import, then prepare a bounded worker prompt.
```

## Activate and use

Open a fresh chat in the prepared advisor folder. Loading its local instructions starts the advisor for its bound project; installing the skill alone does not activate other chats. Ask the agent to identify its role, project, state and next step to verify loading. Explicit deactivation applies to the current chat; a new chat in the dedicated folder starts as advisor again. Responses follow your preferred language. To resume explicitly, load the workspace AGENTS.md, binding and state.

## What the advisor does

- Connects the next task to a useful project outcome.
- Raises concrete concerns before preparing the worker prompt, recommends an alternative, and respects your informed decision.
- Asks about preferences, priorities, intent, and facts you can clarify.
- Asks before acting on unresolved choices with materially different consequences, including how to undo published work. Requesting an outcome does not automatically select the method or authorize publication; routine details and already settled choices remain autonomous.
- Uses directed investigation for technical or specialist questions.
- Adjusts planning, delegation, and verification to risk and uncertainty.
- Evaluates worker evidence and stops when the task is sufficiently complete.
- Respects informed decisions and authorization boundaries.
- Maintains a concise, current handoff rather than an accumulating activity log.

## Evidence and supported environments

This is a proposed working method, not a demonstrated productivity improvement. There is no controlled comparison of quality, time or cost against a single-agent workflow. Installer tests verify filesystem behavior; behavioral observations are limited scenarios.

Filesystem adapters are supplied for Codex, Claude Code and OpenCode. Runtime validation status is recorded in [HARNESSES.md](skills/project-advisor/references/HARNESSES.md); adapter generation is not proof of runtime loading. For chats without filesystem access, provide the method and current handoff manually and save updates yourself. Automatic binding checks and persistence are unavailable there.

## Installer checks and releases

[GitHub Actions](https://github.com/GuilhermeRocha0404/project-advisor/actions/workflows/installer-tests.yml) runs `python -m unittest discover -s tests -v` on Windows and Linux with Python 3.10 and 3.12, plus macOS with Python 3.12, for pushes and pull requests. The workflow adds no Python dependencies. Run `python <skill-dir>/scripts/workspace.py --version` to identify the method version; use the release or commit to identify subsequent installer changes.

[Releases](https://github.com/GuilhermeRocha0404/project-advisor/releases) provide versioned checkpoints and user-facing notes; the audit retains evidence and decisions. No separate changelog is maintained.

## State, privacy, and limits

The installed `AGENTS.md` contains the method; `CLAUDE.md` imports it only when needed. `.advisor-workspace.json` records the project, harness, method version and managed-file hashes. `ADVISOR_STATE.md` holds private decisions and progress; legacy `CONSULTOR_STATE.md` can be retained. Keep custom preferences in `ADVISOR_LOCAL.md`. State maintenance is model-driven, without hooks or a background service.

Updates use the same preview/apply command and refuse changed managed files. Existing state is never replaced; inspect it before using `--adopt-existing-state`. New POSIX state files request owner-only permissions (`0600`); existing state permissions remain unchanged. Windows uses ACLs. If setup stops before the manifest is written, follow [interrupted-install recovery](skills/project-advisor/references/HARNESSES.md#interrupted-first-install) to preserve state and review orphaned instructions before retrying.

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

## Maintenance and feedback

This is a personal, maintainer-led project shared for others to use. The maintainer decides direction, architecture and implementation. [Issues](https://github.com/GuilhermeRocha0404/project-advisor/issues) are welcome for bugs, incompatibilities and real usage experiences. Use small synthetic examples and redact private information. Pull requests are not requested or required and may not be accepted.

Maintain README documentation in English and Brazilian Portuguese only. The Portuguese version lives in `.github/readme/README.pt-BR.md`. Update both versions together so examples, commands, links and limitations remain aligned.

## License

[MIT](LICENSE) — Copyright (c) 2026 Guilherme Rocha.

## Audit revision 2.1

State reconciliation now protects open verification and active constraints, records evidence provenance, and removes superseded directions at closure or replacement. The installer shares one state schema, preserves legacy state names on update, validates manifests, explains stale-lock recovery and rejects overlapping skill/workspace trees. Existing state is never reset.

See [audit decisions and verification](docs/AUDIT_2_1.md) and [examples](skills/project-advisor/references/EXAMPLES.md). English is the technical reference; the Portuguese wording has not received independent native-speaker review.
