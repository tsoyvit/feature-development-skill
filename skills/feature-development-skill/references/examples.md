# Examples

## Qualifying examples

### Cross-system billing redesign

Prompt:

```text
Use $feature-development-skill. We need to redesign payment acceptance, fulfillment recovery, refunds, reconciliation, and the Billing admin experience over several stages.
```

Expected behavior:

- initialize or locate the feature workspace;
- preserve the business model and decisions;
- create a staged roadmap;
- assign stable IDs to future admin requirements;
- prepare only the active stage plan;
- require implementation and review reports before verification.

### Authentication migration

Prompt:

```text
Use $feature-development-skill. Plan and execute a migration from the old device authentication model across backend, web, and Windows clients.
```

Expected behavior:

- identify compatibility and rollout stages;
- record migration and rollback invariants;
- prevent the implementer from self-marking production verification;
- maintain a bounded handoff across sessions.

### Resume after context loss

Prompt:

```text
Use $feature-development-skill. Resume the current large feature from repository documents and tell me what is actually verified and what comes next.
```

Expected behavior:

- read roadmap/handoff and active-stage evidence;
- verify referenced repository state where possible;
- distinguish planned, implemented, and verified work;
- report the next concrete action without redoing completed discovery.

## Non-trigger examples

### Small visual adjustment

Prompt:

```text
Increase the spacing under this button and update its snapshot test.
```

Expected behavior: use ordinary repository workflow. Do not initialize a feature-development workspace.

### Isolated bug fix

Prompt:

```text
Fix this null check in one endpoint and add a regression test.
```

Expected behavior: do not apply the full process unless explicitly requested or the investigation reveals materially larger scope.

### Explicit invocation for a small task

Prompt:

```text
Use $feature-development-skill for this small task because I need an auditable handoff.
```

Expected behavior: honor explicit invocation, but keep the generated structure and process minimal.

## Example stage statuses

```text
Stage 1 — Payment integrity: Verified
Stage 2 — Public billing contract: Planned
Stage 3 — Refund and package revocation: Backlog
Billing admin redesign: Deferred
```

## Example deferred requirement

```text
BILL-ADM-003 | Show fulfillment worker state for a paid checkout | Stage 1 | Billing admin redesign | Deferred | Admin can see scheduled/running/retrying/exhausted state and the related checkout
```
