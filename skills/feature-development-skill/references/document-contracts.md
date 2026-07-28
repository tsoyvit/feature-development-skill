# Document contracts

## Contents

1. General rules
2. ROADMAP.md
3. HANDOFF.md
4. PLAN.md
5. IMPLEMENTATION.md
6. REVIEW.md
7. Stable IDs and links

## 1. General rules

- Preserve the repository's documentation language unless the user requests another language.
- Use exact dates in ISO format when dates matter.
- Use repository-relative links.
- Keep confirmed facts, decisions, assumptions, and proposals visibly separate.
- Do not paste secrets, full provider payloads, credentials, or sensitive production data.
- Do not append unbounded logs or chat transcripts.

## 2. ROADMAP.md

Required sections:

- Feature summary
- Confirmed scope and non-scope
- Stage registry
- Active stage
- Confirmed decisions
- Deferred requirements
- Known risks and blockers
- Evidence index
- Recent changes

The roadmap is compact. A stage row should contain:

- stage number/name;
- status;
- one-sentence result or objective;
- plan/report/review links;
- implementation reference when available.

### Confirmed decisions

Each durable decision should have:

- ID;
- decision;
- rationale;
- date;
- source;
- status (`Active` or `Superseded`);
- superseding decision when applicable.

### Deferred requirements

Each row should include:

- stable ID;
- requirement;
- source stage;
- target stage/initiative;
- status;
- acceptance condition;
- evidence link.

## 3. HANDOFF.md

Required sections:

- Current position
- Last verified result
- Active constraints and decisions
- Open blockers
- Deferred requirements due now
- Read next
- Next concrete action

Rewrite the file after stage approval, implementation, review, closure, or a material scope change.

## 4. PLAN.md

Required sections:

- Metadata and approval state
- Objective
- Current confirmed behavior
- Scope
- Non-scope
- Invariants and acceptance criteria
- Implementation plan
- Data/schema/API implications
- Failure and recovery behavior
- Migration and rollout
- Test plan
- Documentation updates
- Deferred requirements created or consumed
- Completion criteria

Before approval, revise the plan normally. After approval, preserve it. If scope changes materially, add an amendment or create a new plan version while retaining the approved original.

## 5. IMPLEMENTATION.md

Required sections:

- Implementation status
- Implementation reference
- Actual changes
- Changed files and migrations
- Deviations from approved plan
- Tests and checks with exact outcomes
- Manual/production checks
- New risks or limitations
- Deferred-requirement candidates
- Reviewer entry points

Write facts from the actual repository. Do not claim a test passed without running it or citing existing CI evidence.

## 6. REVIEW.md

Required sections:

- Review scope and evidence
- Findings ordered by severity
- Plan and invariant compliance
- Test and migration assessment
- Deferred-requirement assessment
- Fix verification
- Unreviewed areas
- Disposition

Allowed disposition values:

- `Pending`
- `Needs changes`
- `Accepted — verification incomplete`
- `Verified`

A `Verified` disposition must state the evidence and any remaining non-blocking limitations.

## 7. Stable IDs and links

Use stable IDs for requirements and decisions. Do not reuse or renumber retired IDs.

Recommended formats:

```text
<FEATURE>-REQ-001
<FEATURE>-ADM-001
<FEATURE>-DEC-001
<FEATURE>-RISK-001
```

Use a shorter domain prefix when the project already has one. The ID should remain stable even if the target stage changes.
