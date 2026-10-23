# Audit revision 2.1.0

Status: local revision 2.1.1 after external review of 2.1.0; publication pending. No controlled evidence establishes productivity, quality or cost gains. This record distinguishes implemented changes from unperformed runtime checks.

## Decisions by finding

| ID | Disposition | Change or evidence |
|---|---|---|
| A1 | Applied | Method treats state as a handoff with concise domain pointers; local state consolidated. |
| A2 | Applied | State privacy/minimization rule; private paths distinguished from exportable data. |
| A3 | Applied | Installer reads STATE_SCHEMA.md; generated state tested against that source. |
| A4 | Adapted | Proportionate report and reported/inspected/executed provenance; risk-directed inspection, not mandatory full logs. |
| A5 | Adapted | Closure/replacement/resumption reconciliation, contradiction signals, explicit status, active versus completed references, brief closure disclosure; no arbitrary word target. |
| B1 | Applied | Location/isolation check in method; symmetric directory guards in installer. |
| B2 | Applied | Both legacy/current recovery template names recognized; legacy-template preservation test. |
| B3 | Applied | Missing/corrupt binding recovery instructions and validated manifest errors; no-write tests. |
| B4 | Applied | Worker objections assessed as evidence/clarification rather than presumed misunderstanding. |
| B5 | Applied | Omitted state argument inherits valid manifest name; legacy update preserves bytes. |
| B6 | Applied | Existing lock yields actionable recovery guidance and is never removed automatically. |
| B7 | Applied | Skill/workspace ancestor overlap rejected; no-write test. |
| B8 | Clarified | Public project-advisor name preserved; local consultor-codex documented as legacy alias. |
| B9 | Applied | Filesystem adapter scope and manual no-filesystem workflow distinguished. |
| B10 | Checked | Official documentation URLs opened during audit review; runtime support remains a separate question. |
| C1 | Corrected in 2.1.1 | Compression omitted the explicit warning against weakened checks. Restored it and the stalled-investigation guidance; task sizing remains in prose. |
| C2 | Applied | Optional examples and bounded evaluation cases in references/EXAMPLES.md. |
| C3 | Applied | Prompt language follows user preference unless worker needs differ. |
| C4 | Adapted | All eleven translations retained, with localized revision/limitations notes; English technical reference linked. No independent native-speaker review. |
| C5 | Preserved | Workspace activation and per-chat deactivation explained in method and entrypoint. |
| C6 | Reviewed | External package contains generic method, tests and synthetic evidence; no private state/logs included. No anonymity guarantee claimed. |
| I1 | Pending external review | Corrected revision prepared for a third party; self-review not presented as external acceptance. |
| I2 | Applied | README/method disclose no controlled benefit evidence; compare overhead proportionately during use. |
| I3 | Adapted | Critical judgment split into shorter paragraphs; existing impact criteria preserved; no fixed objection count. |
| I4 | Applied | Open verification and active safeguards survive closure; removal requires resolution or superseding decision. |
| I5 | Applied | Technical references allowed when useful; paths/URLs can still contain sensitive data. |
| M1 | Applied | Local C3 duplication and skill/domain history condensed without discarding open constraints. |
| M2 | Adapted | Absolute local binding retained; explicit verified relocation documented, never silent rebinding. |
| M3 | Applied | UTF-8/LF contract documented and tested with CRLF sources. |
| M4 | Adapted | Optional ADVISOR_TEST_TMPDIR; ACL restrictions documented as environment-specific, not a portability defect. |
| M5 | Not applicable | Obsolete manual Claude frontmatter instruction absent from examined current package. |
| M6 | Preserved | Fresh-session checks, concise skill entrypoint and useful negative constraints retained. |

## Verification

- Fifteen installer tests passed on Windows/Python 3.12. New cases cover malformed/missing manifest, existing lock, legacy update/template, ancestor overlap and CRLF/schema consistency.
- First sandbox run failed at temporary-directory access before exercising installer behavior, even with a workspace scratch location. The authorized execution outside that ACL restriction passed. This is not Linux execution evidence.
- Isolated behavioral evaluator read only the method and four synthetic scenarios, without the example answer/reference. It requested authorization evidence for a build-only report, treated unavailable integration as unverified, challenged removal of tenant isolation with an alternative, and preserved database verification while recognizing authorized resumption. These are bounded observations, not reliability statistics.
- Workspace update preserved existing state bytes; subsequent state maintenance is a separate operation.
- Claude Code/OpenCode adapter generation is tested; runtime loading in those products remains unverified. Long-term behavior over several real handoffs and final external review remain pending.

## Historical trace clarification

A directed local trace inspection resolved the disputed missing invocation text: the message received by the advisor contained “use  ou consulte /skills”, without the invocation token. The subsequent response supplied the missing token. The same turn contains actual configuration/context/plan reads and a targeted diff command. This supports the narrow claims about that turn, not all historical self-reports. Raw traces are private and excluded from this distribution.

## Reproduce installer checks

Run python -m unittest discover -s tests -v from the repository root. If needed, set ADVISOR_TEST_TMPDIR to an existing writable scratch folder. Do not weaken filesystem safeguards or delete state to obtain a passing result.

Method and installer tests do not replace real usage, native-language review, or per-harness runtime checks.

## Final local checks

An ephemeral Codex read-only session identified the advisor role, project binding, authorized C3 continuation, pending closure and PostgreSQL limitation. It explained the method's final environment/model section. Its trace showed reads of manifest, state and local preferences; it reported receiving AGENTS instructions through the harness rather than reading that file again. No target work or state writes were performed by that check. This is one resumption observation, not a long-term or cross-harness guarantee.

The initial CLI attempt was blocked by sandbox initialization permissions; the authorized retry retained the inner read-only mode and completed. Skill metadata validation passed for distribution and local alias. Relative Markdown links and git diff whitespace checks passed. The revised method is about 10.6 KB, below the previous 15,199-byte installed method; byte count alone does not measure instruction quality.

Publication, external acceptance, repeated real-world handoff evaluation and Claude/OpenCode runtime tests remain pending.

## External review and follow-up 2.1.1

The external reviewer reported all 15 installer tests passing on Linux/Python 3.12.3 against the 2.1.0 package (30321c1). This is externally reported execution, not a Linux run performed or raw test logs inspected by this maintainer. It adds Linux evidence without proving macOS or Claude Code/OpenCode runtime behavior.

The reviewer identified a genuinely omitted safeguard: success must not be accepted by hiding failures, weakening contracts or disabling checks. It is restored in the evaluation section, together with explicit attention to removed/relaxed checks. Guidance on investigating stalled hypotheses/context/environment is restored. Task difficulty remains covered in prose rather than duplicating a table.

The README introduction and all translations now describe a model-independent method with specific workspace adapters. State reconciliation is a short ordered sequence. POSIX owner-only replacement permissions are documented deliberately; no permission-broadening code was added.

Four one-shot synthetic behavioral cases are not out-of-sample validation or sustained reliability evidence. Repetition and additional cases unlike the published examples belong to the planned real-use evaluation. The external reviewer did not rerun those behavioral cases and had authored the original recommendations, so this review does not establish strong independent acceptance. A different reviewer or human review of the final version remains desirable before claiming that acceptance.

Publication remains pending the user's decision.
