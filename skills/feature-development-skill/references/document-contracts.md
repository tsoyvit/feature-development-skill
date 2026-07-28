# Document contracts

## Contents

1. General rules
2. ROADMAP.md
3. HANDOFF.md
4. PLAN.md
5. RESULT.md
6. Stable IDs and links

## 1. General rules

- Preserve the project's documentation language unless requested otherwise.
- Use exact dates when dates matter.
- Use repository-relative links where practical.
- Separate confirmed facts, decisions, assumptions, and proposals.
- Do not paste secrets, credentials, full provider payloads, or sensitive production data.
- Do not append chat transcripts or unbounded logs.
- In a coordination workspace, initiative documents live only in the coordination repository.
- Current technical documentation remains next to the code that owns the behavior.

## 2. ROADMAP.md

Required sections:

- Project topology
- Feature summary
- Confirmed scope
- Non-scope
- Stage registry
- Active stage
- Confirmed decisions
- Deferred requirements
- Known blockers
- Implementation references
- Recent changes

The project topology table records the coordination root and every application repository.

A stage row contains:

- stage number/name;
- status;
- one-sentence objective or implemented result;
- plan link;
- result link.

### Confirmed decisions

Each durable decision includes:

- stable ID;
- decision;
- rationale;
- date;
- source;
- status (`Active` or `Superseded`).

### Deferred requirements

Each row includes:

- stable ID;
- requirement;
- source stage;
- target stage/initiative;
- status;
- acceptance condition;
- source/result link.

## 3. HANDOFF.md

Required sections:

- Current position
- Last implemented result
- Active repositories
- Active constraints and decisions
- Open blockers
- Deferred requirements due now
- Read next
- Next concrete action

Rewrite after plan approval, implementation, stage closure, or a material scope change. Keep it below 150 lines when possible and never append detailed history.

## 4. PLAN.md

Required sections:

- Status and approval metadata
- Objective
- Current confirmed behavior
- Affected repositories
- Current docs to read or update
- Scope
- Non-scope
- Invariants and acceptance criteria
- Implementation plan
- Data/schema/API implications
- Failure and recovery behavior
- Migration and rollout
- Test/check plan
- Deferred requirements consumed
- Deferred requirements created
- Completion criteria

Before approval, revise normally. After explicit approval, preserve the plan. Material scope changes require an amendment or a new plan version.

## 5. RESULT.md

Required sections:

- Status
- Repository references
- Actual changes
- Changed files and migrations
- Checks run
- Current documentation
- Deviations from approved plan
- Remaining work and limitations
- Deferred requirements
- Next stage handoff

Write factual information from actual Git state and command output. For a coordination workspace, report every touched repository separately. Do not claim a check passed if it was not run or supported by CI output.

## 6. Stable IDs and links

Do not reuse or renumber IDs.

Recommended formats:

```text
<FEATURE>-REQ-001
<FEATURE>-ADM-001
<FEATURE>-DEC-001
<FEATURE>-BLOCK-001
```

The ID remains stable even if the target stage changes.
