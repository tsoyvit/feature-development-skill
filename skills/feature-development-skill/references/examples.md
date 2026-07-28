# Examples

## SkillCue Billing initiative

Prompt:

```text
Use $feature-development-skill.
Initialize the Billing initiative from the SkillCue workspace root.
Detect the repositories automatically and prepare the first stage plan.
```

Expected behavior:

- detect `skillcue-workspace`;
- use root `docs/initiatives/billing/`;
- populate workspace/backend/web/windows/landing topology;
- read root AGENTS and relevant billing current docs;
- create `ROADMAP.md`, `HANDOFF.md`, and the first `PLAN.md`;
- preserve future admin requirements with stable IDs;
- do not create review documents.

## Implement an approved SkillCue stage

Prompt:

```text
Use $feature-development-skill.
Implement the approved active Billing stage and update initiative state.
```

Expected behavior:

- work from the workspace root;
- target each affected child repository explicitly;
- run affected checks;
- update canonical current docs;
- write one `RESULT.md`;
- record branch/commit/PR per touched repository;
- set the stage to `Implemented`;
- update roadmap and handoff;
- do not start a review phase.

## Generic single repository

Prompt:

```text
Use $feature-development-skill.
Initialize a multi-stage authentication migration in this repository.
```

Expected behavior:

- detect one Git repository;
- use it as both coordination and implementation repository;
- create `docs/initiatives/auth-migration/`;
- use the same PLAN/RESULT lifecycle.

## Resume after context loss

Prompt:

```text
Use $feature-development-skill.
Resume the current Billing initiative and tell me the next concrete action.
```

Expected behavior:

- read roadmap, handoff, and active stage files;
- inspect referenced repositories only when needed;
- report implemented stages, blockers, deferred requirements, and next action;
- avoid redoing completed discovery.

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
Stage 2 — Public billing contract: Planned
Stage 3 — Refund and package revocation: Backlog
Billing admin redesign: Deferred
```

## Example deferred requirement

```text
BILL-ADM-003 | Show fulfillment worker state for a paid checkout | Stage 1 | Billing admin redesign | Deferred | Admin can see scheduled/running/retrying/exhausted state and the related checkout
```
