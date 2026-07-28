# Review rules

## Contents

1. Review integrity
2. Evidence hierarchy
3. Review procedure
4. Severity
5. Complete-first-pass rule
6. Verification after fixes

## 1. Review integrity

Review the implementation, not the author's confidence. Implementation reports and plan checklists are navigation aids, not proof.

When the same agent implemented and reviews the work, label the result as self-review. It may find defects but should not alone establish independent verification unless the user explicitly accepts that reduced assurance.

## 2. Evidence hierarchy

Prefer evidence in this order:

1. current repository code and schema;
2. version-control diff and commit history;
3. deterministic tests and build output;
4. runtime or controlled production checks;
5. implementation report;
6. plan statements;
7. chat claims.

When evidence conflicts, investigate rather than averaging the claims.

## 3. Review procedure

1. Read the approved plan and stage invariants.
2. Identify the implementation reference and actual changed files.
3. Trace the critical runtime and data paths.
4. Check migration forward/rollback behavior and compatibility boundaries.
5. Inspect idempotency, concurrency, failure recovery, security, observability, and operator behavior where relevant.
6. Compare actual tests with required scenarios.
7. Check deferred requirements for omissions or premature implementation.
8. Record all actionable findings in one pass when possible.
9. State what was not inspected or could not be verified.

## 4. Severity

- `P0`: likely data loss, security breach, financial corruption, or unrecoverable production failure.
- `P1`: correctness or availability defect that blocks rollout or stage completion.
- `P2`: meaningful reliability, maintainability, observability, or test gap that should be fixed in scope.
- `P3`: non-blocking cleanup or documentation issue. Avoid inflating stylistic preferences into findings.

Every finding should include:

- affected invariant or requirement;
- concrete evidence/location;
- failure scenario;
- required correction;
- whether it blocks stage closure.

## 5. Complete-first-pass rule

Do not drip-feed obvious findings across repeated plan revisions. Inspect the whole available scope before responding and list all currently identified actionable issues. New findings after revisions should arise from changed content or deeper evidence, not from an intentionally partial first pass.

Do not add praise filler when the user asks only for issues.

## 6. Verification after fixes

After fixes:

- inspect the corrected diff;
- rerun or verify relevant checks;
- confirm the fix did not violate another invariant;
- close each finding explicitly;
- leave unresolved findings visible;
- update the disposition only after evidence supports it.
