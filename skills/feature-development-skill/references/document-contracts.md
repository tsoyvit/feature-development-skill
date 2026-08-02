# Document contracts

## Contents

1. General rules
2. ROADMAP.md
3. HANDOFF.md
4. RESULT.md
5. Stable IDs and links

## 1. General rules

- Preserve the project's documentation language unless requested otherwise.
- Use exact dates when dates matter.
- Use repository-relative links where practical.
- Separate confirmed facts, durable decisions, assumptions, and proposals.
- Do not paste secrets, credentials, full provider payloads, or sensitive production data.
- Do not append chat transcripts, full Codex plans, or unbounded logs.
- In a coordination workspace, initiative documents live only in the coordination repository.
- Current technical documentation remains next to the code that owns the behavior.
- Keep initiative documents compact enough for a new Codex session to read before touching code.

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
- result link when the stage has started.

### Confirmed decisions

Each durable decision includes:

- stable ID;
- decision;
- rationale;
- date;
- source;
- status (`Active` or `Superseded`).

Record only decisions that constrain future work. Do not record the full discussion that produced them.

### Deferred requirements

Each row includes:

- stable ID;
- requirement;
- source stage;
- target stage/initiative;
- status;
- acceptance condition;
- source/result link.

Future obligations must remain visible even when their source stage is already implemented.

## 3. HANDOFF.md

Required sections:

- Current position
- Active stage intent
- Last implemented result
- Current progress
- Active repositories
- Active constraints and decisions
- Open blockers
- Deferred requirements due now
- Read next
- Next concrete action

Rewrite at the start of implementation, after meaningful checkpoints, before ending an incomplete run, after stage completion, or after a material scope change.

The active-stage intent should preserve only the concise objective and approved boundaries needed to continue safely. Current progress should say what is already complete, what remains, and where work should resume.

Keep the file below 150 lines when possible and never append detailed history.

## 4. RESULT.md

A stage receives one `RESULT.md` when implementation begins.

Required sections:

- Status and timestamps
- Stage objective and approved boundaries
- Repository references
- Actual changes
- Changed files and migrations
- Checks run
- Current documentation
- Deviations from approved scope
- Remaining work and limitations
- Deferred requirements
- Next stage handoff

While the stage is `In progress`, the file may contain a concise factual checkpoint. After implementation, complete it from actual Git state and command output.

For a coordination workspace, report every touched repository separately. Do not claim a check passed if it was not run or supported by CI output.

`Stage objective and approved boundaries` is a compact implementation record, not a copy of the Codex plan. It should preserve the goal, important non-scope, and key constraints needed to understand the result later.

`Deviations from approved scope` records material differences between the approved Codex plan and actual implementation. Minor implementation details do not need to be listed as deviations.

## 5. Stable IDs and links

Do not reuse or renumber IDs.

Recommended formats:

```text
<FEATURE>-REQ-001
<FEATURE>-ADM-001
<FEATURE>-DEC-001
<FEATURE>-BLOCK-001
```

The ID remains stable even if the target stage changes.
