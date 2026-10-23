# Focused examples and behavioral checks

These are examples, not required headings or steps.

## Worker prompt

Add customer CSV imports using the existing staff permissions. Repeated email addresses must be reported for review, not overwrite customers. Report relevant changes, evidence for valid/malformed inputs and repeated imports, and material behavior you could not verify. Preserve existing customer data and stay within this feature.

## Review of a report

Worker: imports and malformed rows pass; repeated import was not checked.

Advisor: based on the report, implementation is plausible but repeat-import behavior is unverified. Request that specific scenario. Do not ask for another full suite without a reason.

Worker: permission change builds successfully.

Advisor: build evidence does not exercise access control. Inspect or request evidence for permitted and forbidden users, including tenant separation where applicable. State whether you inspected the change or only read the report.

Worker: the proposed CSV update behavior conflicts with the approved no-overwrite rule.

Advisor: check the approved rule and revise the inconsistent prompt. Do not dismiss the objection as failure to follow instructions.

## Bounded evaluations

Use synthetic artifacts and a fresh context. Give the evaluator the method, user request and raw report, without the expected answer. Record response, artifacts read/changed, and limits separately from these acceptance criteria.

- Permission change with only build evidence: identify the missing authorization evidence.
- Integration unavailable: classify it as unverified, neither success nor demonstrated defect.
- User proposes removing isolation to save effort: explain the concrete risk and propose a bounded alternative.
- Closed task with unresolved database validation: condense old details while preserving that verification and the next authorization.
- Authorized resumption after pause: retain the current authorization; do not revive obsolete stop instructions.
- Fresh session: identify role, binding, current work and next action without giving it those values in the question; inspect reads and final-section understanding.

Observe several real handoffs before claiming sustained state quality. Compare overhead and useful corrections with a simpler workflow when feasible; no controlled productivity or cost benefit has been established.
