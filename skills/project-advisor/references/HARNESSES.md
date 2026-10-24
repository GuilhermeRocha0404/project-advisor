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

## Historical verification of 2.0.0

Nine synthetic installer tests passed with Python 3.12 on Windows (`python -m unittest discover -s tests -v`). They cover setup, updates, state preservation, missing-state refusal, independent projects, adapters and instruction conflicts. The package passed the skill metadata validator; relative Markdown links were checked.

A fresh, ephemeral Codex CLI session in read-only mode correctly identified its advisor role, synthetic project binding, state file and recorded next action. Its tool trace showed reads of the local manifest and state, without implementing the next action. This is one observed session, not a compaction reliability benchmark. Claude Code and OpenCode runtime loading have not been exercised for this revision.

## Updates and recovery (2.1.0)

Updates infer the state filename from an existing valid manifest. Explicit conflicting names are refused. Both ADVISOR_STATE_TEMPLATE.md and CONSULTOR_STATE_TEMPLATE.md are recognized for recovery; STATE_SCHEMA.md is the single initial-state source used by the installer. Existing state bytes are preserved. Generated instruction files use UTF-8/LF regardless of template CRLF.

A malformed or missing manifest is not permission to initialize over existing instructions. Preserve files and recover a trusted binding; ask for clarification if project identity is uncertain. Absolute project paths are local binding data. Moving only the advisor folder does not change the project path. When the project itself moves, verify it is the same project and explicitly review the manifest path change; do not bypass managed-file hashes or rebind to a different project.

For a setup lock, check whether its PID belongs to an active setup. A PID alone is insufficient because it may be reused. Only after confirming the lock is stale, inspect partial writes and remove that lock. Never delete it automatically or delete state to make setup pass. Multi-file installation is not a single transaction.

For an existing personal skill alias, preserve its name/frontmatter and invocation metadata during migration; the distributed package remains project-advisor.

### Interrupted first install

An interruption can leave instructions and state without a manifest. Refusal on retry protects those files; it does not mean the state should be reset.

1. Confirm no setup process is active. If a lock remains, follow the stale-lock guidance above. Preserve a backup of the entire workspace outside that workspace.
2. If a trusted manifest backup exists, recover it and review its binding and managed-file hashes. A mismatch still needs a manual merge; do not change hashes to force acceptance.
3. Without a recoverable manifest, confirm the target project and intended harness. Read the existing state, including its final sections, to check for incomplete content. Recover damaged state from a trusted source before proceeding; the installer cannot determine its correctness.
4. Compare orphaned `AGENTS.md` with `templates/AGENTS.md`, substituting the intended state filename for `{{STATE_FILE}}`. For Claude, also compare `CLAUDE.md` with the adapter `# Project Advisor workspace` followed by a blank line and `@AGENTS.md`. Preserve custom instructions and resolve any differences explicitly. Move only reviewed orphaned instruction files to the external backup; do not delete state or blindly remove instructions.
5. Preview setup with the confirmed `--workspace`, `--project`, `--harness` and `--state-file`; add `--adopt-existing-state` when retaining state. Inspect the proposed changes, then repeat with `--apply`. Verify the recovered binding and that state bytes remain unchanged.

The script never performs automatic repair or deletes these files. This procedure also applies to a missing manifest in an existing workspace, but absence of a manifest is not evidence that its instructions are disposable.

Run installer checks with Python unittest. If the platform's default temporary directory is restricted, set ADVISOR_TEST_TMPDIR to an existing writable scratch directory; this does not require disabling the sandbox. Running on one OS does not establish cross-platform execution.

Before release, verify current harness documentation and actual loading separately. Codex's documented default project_doc_max_bytes is 32 KiB; inspect the effective instruction chain, including global rules, rather than measuring only this template. A fresh-session response should cover the final sections as well as role/binding, and its reads should be inspected. This is a scenario check, not a guarantee after arbitrary compactions.

Claude Code/OpenCode adapter-file tests are not runtime tests in those products. In clients without filesystem access, supply the method and current handoff manually and save the returned state yourself; no automatic persistence is provided.

## File permissions

The installer is intended for a private, single-user advisor workspace. On POSIX, mkstemp creates replacement instruction/manifest files with owner-only permissions (0600); replacement keeps that mode, including when updating a previously more permissive file. New state files are created with a requested mode of 0600 (the process umask may restrict it further). Existing state permissions and bytes are untouched, including on adoption and update. Folder permissions, local preferences and files subsequently written by the agent require an appropriate local privacy policy.

Shared/container/WSL access across users requires an explicit local permission decision. Do not broaden access automatically. Windows access is governed by its ACLs. No cross-user runtime validation is claimed.
