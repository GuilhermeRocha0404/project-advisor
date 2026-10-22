# Project Advisor

**English** · [Português (Brasil)](.github/readme/README.pt-BR.md)

A platform-independent skill for critical project guidance, focused worker prompts, and evidence-based review.

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

Use a **separate advisor chat and workspace outside the target project's directory tree**. Keep the worker in the project workspace, following its applicable instructions. A second chat attached to the same project may still load that project's `AGENTS.md`, `CLAUDE.md`, or other local rules.

This reduces automatic loading of project-specific instructions into the advisor's context. Global instructions, parent-directory rules, integrations, and inherited session context may still apply; complete isolation is not guaranteed. Give the advisor the necessary context through goals, selected documents, and worker reports. The advisor can examine project rules as evidence while respecting the host's instruction hierarchy.

Keep each project's advisor state in its own external folder, outside the installed skill and preferably outside the target repository. Do not publish private project state with the skill.

## Install

Clone or download this repository, then copy the entire `skills/project-advisor` folder to the appropriate location. Preserve `references/` and `agents/` alongside `SKILL.md`. Do not overwrite an existing installation without reviewing your local changes.

| Environment | Personal installation folder | Explicit invocation |
|---|---|---|
| Codex | `~/.agents/skills/project-advisor/` | `$project-advisor` |
| Claude Code | `~/.claude/skills/project-advisor/` | `/project-advisor` |
| OpenCode | `~/.config/opencode/skills/project-advisor/` | Select/load the skill explicitly; see the optional command setting below. |

Here, `~` means your home directory, including on Windows. Installation directories refer to the local tools; hosted products can have different mechanisms. Use a new advisor session after installation if the skill has not appeared.

### Invocation controls

The core always requires an explicit activation request. Host controls are separate:

- **Codex:** the included `agents/openai.yaml` sets `policy.allow_implicit_invocation: false`.
- **Claude Code:** add `disable-model-invocation: true` to the YAML frontmatter of the installed `SKILL.md` to prevent model-initiated invocation. This field is a Claude Code adaptation, not part of the shared source.
- **OpenCode:** add the following string-valued metadata to the installed `SKILL.md` frontmatter to expose a command and remove automatic selection guidance:

  ```yaml
  metadata:
    opencode/slash: "true"
    opencode/autoinvoke: "false"
  ```

  Then invoke `/project-advisor` in versions supporting these settings. If your client differs, use its explicit skill-loading mechanism.

These are local installation adjustments; they do not require separate copies of the methodology in this repository. Before updating an installation, preserve any host-specific frontmatter settings.

Installation and invocation guidance was checked against the official [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills), and [OpenCode](https://opencode.ai/docs/skills/) documentation on October 21, 2026. **This release has not been exercised end to end in all three clients.** Documentation checks are not runtime compatibility certification. Existing use of the earlier Portuguese advisor informed this version; the English adaptation still needs broader field feedback.

## Activate and use

Invoke the skill using your environment's mechanism, then provide your objective and a state folder. For example:

```text
Activate Project Advisor.
Use this external state folder: /path/to/my-advisor-workspace.
The implementation worker is in a separate chat.
I want to add CSV customer imports to an existing application.
```

The advisor reads its core instructions and the external state, or creates state when needed. It remains active in the same chat until you explicitly deactivate it:

```text
Deactivate advisor.
```

For a new chat, explicitly activate the skill again and provide the same state folder to resume the project. Installation alone never activates the role. Instructions and examples are in English; **the advisor communicates in your preferred language**.

## What the advisor does

- Connects the next task to a useful project outcome.
- Challenges decisions when it identifies a concrete problem and proposes alternatives.
- Asks about preferences, priorities, intent, and facts you can clarify.
- Uses directed investigation for technical or specialist questions.
- Adjusts planning, delegation, and verification to risk and uncertainty.
- Evaluates worker evidence and stops when the task is sufficiently complete.
- Respects informed decisions and authorization boundaries.
- Maintains a concise, current handoff rather than an accumulating activity log.

## State, privacy, and limits

The advisor uses `ADVISOR_STATE.md` in your external workspace. An existing `ADVISOR_STATE_TEMPLATE.md` takes precedence over the bundled fallback schema when creating a new state file. The bundled `STATE_SCHEMA.md` contains only generic placeholders.

State may contain sensitive decisions, paths, or project facts. Store and share it deliberately. The repository's `.gitignore` excludes advisor state filenames, but that protection applies only within this checkout and does not remove already tracked files. Prefer keeping private state outside repositories you publish.

State is consolidated during active turns when information changes materially, when closing work, or when resuming after compaction as needed. There is no background process, session hook, or guaranteed recovery if the activation context is lost. Reactivate with the same state folder when necessary. If file access is unavailable, the advisor can provide a handoff for you to save instead of claiming persistence.

The skill supplies instructions, not access controls or a guarantee of correct decisions. Its behavior depends on the model, available evidence, host instructions, and tools. It does not implement the target project or independently contact the worker.

## Repository layout

```text
skills/project-advisor/
├── SKILL.md                   Activation, state, and continuity
├── agents/openai.yaml         Codex-specific invocation policy
└── references/
    ├── ADVISOR_CORE.md        Platform-independent method
    └── STATE_SCHEMA.md        Fallback state structure
```

## Contributing

Describe a real problem, the expected behavior, and why the proposed change helps without adding unnecessary process. Use synthetic examples, remove private information, and report the environment and limitations of any behavioral checks. Improvements should preserve the distinction between reusable guidance and personal or project-specific preferences.

README translations live in `.github/readme/`. Keep their examples, commands, links, and limitations aligned with the English README when updating documentation. Add language navigation links only for translations included in the repository.

## License

[MIT](LICENSE) — Copyright (c) 2026 Guilherme Rocha.
