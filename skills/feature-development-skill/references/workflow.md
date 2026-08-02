# Workflow reference

## Contents

1. Topology detection
2. Working pipeline
3. Operating modes
4. Lifecycle transitions
5. File-update matrix
6. Execution approval
7. Context handoff
8. Recovery from drift

## 1. Topology detection

Detect:

- the SkillCue coordination workspace;
- another coordination workspace with independent child repositories;
- a single repository.

Inspect the root README, AGENTS instructions, Git remote, and immediate child Git repositories. Use `scripts/detect_project.py`.

Do not ask the user to classify a clearly detectable project.

## 2. Working pipeline

The normal pipeline is:

```text
idea and product discussion
→ Codex Plan Mode discovery
→ plan refinement and user decisions
→ explicit approval to execute
→ durable stage checkpoint
→ implementation
→ factual RESULT.md
→ ROADMAP.md and HANDOFF.md update
→ next stage
```

Idea discussion may happen outside Codex and does not need to be copied into initiative documents. The Codex plan is the working implementation plan. Repository documents preserve only durable decisions, active context, actual results, and future obligations.

When the user approves execution, implementation begins immediately. The first writable actions create any missing initiative/stage structure and checkpoint the active stage. They do not create another approval boundary.

## 3. Operating modes

### Discover / Plan

Run in Codex Plan Mode. Inspect current behavior, ask for missing product decisions, identify repositories and risks, and refine an implementable plan. No project-file changes are required.

### Implement

After explicit approval, checkpoint durable context and execute the approved Codex plan in the same run. Run checks, update current docs, complete `RESULT.md`, and update roadmap/handoff.

### Close stage

Finish missing initiative bookkeeping after implementation. This is not a review or a new approval step.

### Resume

Read bounded initiative context plus actual Git state and continue from the next action.

### Initialize

Create the initiative in a writable run when useful. Initialization may instead happen automatically at the beginning of the first implementation run.

## 4. Lifecycle transitions

```text
Backlog → Discovery → In progress → Implemented
Any non-terminal state → Blocked
Blocked → prior valid state
Backlog/Discovery → Deferred
Backlog/Discovery → Cancelled
```

Plan refinement happens inside Codex Plan Mode and is not represented by a separate repository status.

There is no mandatory review, verification, or post-implementation audit transition.

## 5. File-update matrix

| Mode | ROADMAP | HANDOFF | RESULT |
|---|---|---|---|
| Initialize | Create | Create | No |
| Discover / Plan | Read when present | Read when present | Read active result when needed |
| Implement start | Set active stage `In progress`; record concise objective/decisions | Record active intent, boundaries, repositories, progress, next action | Create active stage checkpoint |
| Implement progress | Update only for durable scope/decision/blocker changes | Rewrite at meaningful checkpoints | Update factual progress when useful |
| Implement completion | Record implemented result, references, decisions, deferred requirements | Rewrite for next stage | Complete |
| Close stage | Correct implemented state | Rewrite | Finish |
| Resume | Correct stale state when factual | Rewrite if stale | Read/update active result |

## 6. Execution approval

Only explicit user approval or another authority explicitly defined by the project authorizes implementation. Silence is not approval.

Approval of the current Codex plan authorizes the agent to:

1. create missing initiative/stage documents;
2. mark the stage `In progress`;
3. persist concise durable context;
4. execute the approved plan;
5. finish the stage documents.

Do not ask for a second approval between context checkpointing and application changes.

If implementation discovers a new product decision, destructive action, material scope expansion, or changed public behavior that was not covered by the approved plan, ask the user before proceeding with that decision.

## 7. Context handoff

`HANDOFF.md` should include:

- initiative and active stage;
- concise active-stage intent and approved boundaries;
- last implemented result;
- current implementation progress;
- active repositories;
- decisions constraining the next step;
- blockers;
- deferred IDs due now;
- files to read;
- exact next action.

Do not include full plans, diffs, logs, chat transcripts, or historical discussion.

During an active stage, rewrite the handoff after meaningful checkpoints and before ending an incomplete run. This is the primary continuation point for a new Codex session.

## 8. Recovery from drift

When documents and repositories disagree:

1. inspect actual Git state and current code;
2. identify which document is stale;
3. correct roadmap, result, or handoff explicitly;
4. preserve confirmed decisions and stable deferred IDs;
5. ask one targeted question if a material approved boundary cannot be reconstructed;
6. create a repair stage if the discrepancy requires new implementation work.
