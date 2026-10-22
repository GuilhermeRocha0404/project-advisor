# Workspace loading and migration

Checked against primary documentation on October 22, 2026:

| Harness | Workspace files | Evidence |
|---|---|---|
| Codex | `AGENTS.md` | [Instruction discovery, overrides and size limits](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Claude Code | `CLAUDE.md` imports `@AGENTS.md` | [Memory and imports](https://code.claude.com/docs/en/memory) |
| OpenCode | `AGENTS.md`; no additional config | [Project rules and precedence](https://opencode.ai/docs/rules/) |

Open the harness in the advisor folder. An ancestor/global instruction or local override may change effective behavior; setup does not disable those rules. Claude imports must be outside code fences. OpenCode uses AGENTS.md ahead of its CLAUDE.md fallback. Do not assume another harness recognizes these filenames.

Personal skill directories: Codex `~/.agents/skills/project-advisor`, Claude Code `~/.claude/skills/project-advisor`, OpenCode `~/.config/opencode/skills/project-advisor`. Copy the whole package. The included `agents/openai.yaml` disables implicit skill invocation in Codex; it does not prevent the prepared workspace's AGENTS.md from loading. Other clients have their own skill activation controls; do not assume this YAML controls them.

The workspace has one method copy, one project binding and one state. The distribution's template is the release source; installed files are versioned snapshots, not a second independently maintained method. Personal choices belong in ADVISOR_LOCAL.md; project facts and progress belong in state. Keep the skill installation outside advisor and target folders when possible.

Updating the package does not update existing workspaces. Run workspace.py without --apply, inspect the diff, then apply an authorized update. It rejects edited managed files rather than replacing personal content. Review and merge such changes explicitly. Do not edit manifest hashes to bypass review. Changing projects requires another folder; changing harness adapters requires explicit review.

Legacy migration: retain the existing state filename and bytes, inspect its binding, then use --adopt-existing-state with the matching --state-file. Replace old CORE references in active continuity records only after the workspace files exist; preserve historical evidence. Remove the obsolete CORE from the installed skill only after all active callers have migrated. Do not publish private manifests, state or local preferences.

Verification should include dry-run/no-write behavior, independent workspaces, refusal to switch projects, preservation of existing state and custom instructions, and the Claude import adapter. A fresh-session role/state check is separate from these deterministic checks. Neither file validation nor documentation review proves end-to-end behavior across all clients or perfect state maintenance after compaction. No hooks are included.

## Verification of this revision

Nine synthetic installer tests passed with Python 3.12 on Windows (`python -m unittest discover -s tests -v`). They cover setup, updates, state preservation, missing-state refusal, independent projects, adapters and instruction conflicts. The package passed the skill metadata validator; relative Markdown links were checked.

A fresh, ephemeral Codex CLI session in read-only mode correctly identified its advisor role, synthetic project binding, state file and recorded next action. Its tool trace showed reads of the local manifest and state, without implementing the next action. This is one observed session, not a compaction reliability benchmark. Claude Code and OpenCode runtime loading have not been exercised for this revision.
