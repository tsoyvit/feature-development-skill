# Workflow reference

## Contents

1. Topology detection
2. Operating modes
3. Lifecycle transitions
4. File-update matrix
5. Plan approval
6. Context handoff
7. Recovery from drift

## 1. Topology detection

Initialization begins by detecting:

- SkillCue coordination workspace;
- another coordination workspace with independent child repositories;
- a single repository.

The agent should inspect the root README, AGENTS instructions, Git remote, and immediate child Git repositories. Use `scripts/detect_project.py`.

Do not ask the user to classify a clearly detectable project.

## 2. Operating modes

### Initialize

Detect topology and create the minimum initiative structure. Do not create project files during skill installation.

### Discover

Capture confirmed behavior, scope, constraints, stages, and open questions.

### Plan

Create one implementable stage plan. Keep it proposed until explicit user approval.

### Implement

Execute an approved plan, run checks, update current docs, write `RESULT.md`, and update roadmap/handoff.

### Close stage

Finish missing initiative bookkeeping after implementation. This is not a review.

### Resume

Read bounded initiative context and continue from the next action.

## 3. Lifecycle transitions

```text
Backlog → Discovery → Planned → In progress → Implemented
Any non-terminal state → Blocked
Blocked → prior valid state
Backlog/Planned → Deferred
Backlog/Planned → Cancelled
```

There is no mandatory review, verification, or post-implementation audit transition.

## 4. File-update matrix

| Mode | ROADMAP | HANDOFF | PLAN | RESULT |
|---|---|---|---|---|
| Initialize | Create | Create | Optional | No |
| Discover | Update | Update | Draft if ready | No |
| Plan | Update status | Update next action | Create/revise before approval | No |
| Implement | Set In progress then Implemented | Rewrite | Read only after approval | Create/update |
| Close stage | Record implemented result | Rewrite | Frozen | Finish |
| Resume | Correct stale state when factual | Rewrite if stale | Read active | Read active |

## 5. Plan approval

Only explicit user approval or another authority explicitly defined by the project may mark a plan approved. Silence is not approval.

After approval, preserve `PLAN.md`. Record deviations in `RESULT.md`.

## 6. Context handoff

`HANDOFF.md` should include:

- initiative and active stage;
- last implemented result;
- active repositories;
- decisions constraining the next step;
- blockers;
- deferred IDs due now;
- files to read;
- exact next action.

Do not include full plans, diffs, logs, or historical discussions.

## 7. Recovery from drift

When documents and repositories disagree:

1. inspect actual Git state and current code;
2. identify which document is stale;
3. correct roadmap, result, or handoff explicitly;
4. preserve approved plan history;
5. create a repair stage if the discrepancy affects planned work.
