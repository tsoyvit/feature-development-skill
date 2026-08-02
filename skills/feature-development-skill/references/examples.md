# Examples

## Prepare a SkillCue Billing stage in Plan Mode

Prompt:

```text
Use $feature-development-skill.
Prepare the next Billing stage from the SkillCue workspace root.
Inspect the actual repositories and current documentation, ask me for material product decisions, and do not implement until I approve the Codex plan.
```

Expected behavior:

- detect `skillcue-workspace`;
- use root `docs/initiatives/billing/` when it exists;
- read roadmap, handoff, active result, project instructions, current docs, and relevant code;
- identify affected backend/web/windows/landing repositories;
- ask the user for decisions that affect product behavior or scope;
- refine the implementation plan in Codex Plan Mode;
- make no project-file changes before execution approval.

## Execute an approved SkillCue stage

The user approves the current Codex plan.

Expected behavior:

- treat that approval as the implementation gate;
- initialize the initiative automatically if it does not exist;
- create the stage `RESULT.md` and mark the stage `In progress`;
- record concise active intent, boundaries, repositories, decisions, deferred requirements, and next action in roadmap/handoff/result;
- continue directly into implementation without another approval stop;
- target each affected child repository explicitly;
- run affected checks;
- update canonical current docs;
- complete one factual `RESULT.md`;
- record branch/commit/PR per touched repository;
- set the stage to `Implemented`;
- update roadmap and handoff.

## Generic single repository

Prompt in Codex Plan Mode:

```text
Use $feature-development-skill.
Prepare a staged authentication migration in this repository and ask me for any material decisions before implementation.
```

Expected behavior:

- detect one Git repository;
- use it as both coordination and implementation repository;
- refine the next-stage plan in Codex Plan Mode;
- after approval, create `docs/initiatives/auth-migration/` if needed;
- use the same roadmap/handoff/result lifecycle.

## Resume after context loss

Prompt:

```text
Use $feature-development-skill.
Resume the current Billing initiative and continue from the next concrete action.
```

Expected behavior:

- read roadmap, handoff, and the active stage result;
- inspect referenced repositories and actual Git state only when needed;
- report implemented stages, current progress, blockers, deferred requirements, and next action;
- continue an `In progress` stage from the recorded checkpoint;
- avoid redoing completed discovery.

## Interrupted implementation

Before ending an incomplete implementation run, the agent should rewrite `HANDOFF.md` with:

- what was completed;
- what remains;
- current branches/worktrees;
- unresolved blocker or decision;
- exact next file/command/action.

The active `RESULT.md` remains `In progress` and contains only factual progress.

## Non-trigger examples

Do not initialize an initiative for ordinary isolated work such as:

```text
Increase button spacing and update the snapshot.
```

```text
Fix one null check and add a regression test.
```

Use the ordinary project workflow unless the user explicitly invokes the skill.

## Example statuses

```text
Stage 1 — Payment integrity: Implemented
Stage 2 — Public billing contract: Discovery
Stage 3 — Refund and package revocation: Backlog
Billing admin redesign: Deferred
```

After the Stage 2 Codex plan is approved, its status moves directly from `Discovery` to `In progress`.

## Example deferred requirement

```text
BILL-ADM-003 | Show fulfillment worker state for a paid checkout | Stage 1 | Billing admin redesign | Deferred | Admin can see scheduled/running/retrying/exhausted state and the related checkout
```
