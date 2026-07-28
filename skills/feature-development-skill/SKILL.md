---
name: feature-development-skill
description: Manage large, multi-stage feature or module development with durable repository documentation, approved plans, implementation reports, independent reviews, deferred requirements, evidence-based completion, and bounded context handoffs. Use when the user explicitly invokes this skill or asks to develop, redesign, migrate, audit, or plan a substantial feature that spans multiple systems, stages, pull requests, migrations, future obligations, or Codex sessions. Do not use for routine isolated bug fixes, small UI changes, single-file refactors, or ordinary tasks unless explicitly requested.
license: MIT
metadata:
  author: tsoyvit
  version: "1.0.0"
---

# Feature Development

Run large feature work as a durable, evidence-based lifecycle stored in the target repository. Treat chat history as temporary and repository documents as the source of truth.

## Core rules

1. Keep the process proportional. Do not impose this workflow on a small isolated task unless the user explicitly invoked the skill.
2. Preserve approved decisions. Do not silently reopen or reinterpret them without a concrete contradiction, new evidence, or explicit user direction.
3. Freeze an approved `PLAN.md`. Record implementation deviations in `IMPLEMENTATION.md`; do not rewrite history to make the plan appear exact.
4. Separate implementation from verification. The implementing agent may report `Implemented — unverified` but must not mark its own work `Verified` without independent review evidence or explicit user approval.
5. Never mark work complete from a plan, checklist, or agent claim alone. Ground completion in the actual diff, migrations, tests, runtime checks, and deployment evidence relevant to the stage.
6. Give every deferred obligation a stable ID and target stage or initiative. Never leave future requirements only in prose or chat.
7. Keep handoff context bounded. Rewrite summaries instead of appending transcripts or unlimited history.
8. Prefer the simplest process that preserves correctness, traceability, and recovery. Do not create extra governance files or automation without a demonstrated need.

## Determine the operating mode

Infer the mode from the user's request. When ambiguous, inspect the existing feature documents before acting.

- **Initialize**: create a feature workspace and initial roadmap.
- **Discover**: investigate the current system and define confirmed scope, constraints, risks, and open questions.
- **Plan**: create or revise a stage plan before approval.
- **Implement**: execute an approved stage and write the factual implementation report.
- **Review**: inspect the actual implementation against the approved plan and project invariants.
- **Close stage**: update verified status, durable decisions, deferred requirements, and handoff.
- **Resume**: reconstruct current state from repository documents and continue from the next valid action.

Do not combine modes when that would bypass an approval or verification boundary. In particular, do not plan, approve, implement, and verify a high-risk stage as one unbroken self-certified action.

## Locate or initialize the feature workspace

1. Respect a path supplied by the user or repository conventions.
2. Otherwise search for `docs/feature-development/*/ROADMAP.md` and relevant references in `AGENTS.md`.
3. If no workspace exists and the task qualifies, initialize under:

```text
docs/feature-development/<feature-slug>/
```

Use `scripts/init_feature.py` and `scripts/init_stage.py` when available rather than recreating the structure manually.

Before editing, read only the bounded context needed for the current mode:

- always read `ROADMAP.md` and `HANDOFF.md`;
- read the active stage `PLAN.md` for planning, implementation, review, or closure;
- read `IMPLEMENTATION.md` and `REVIEW.md` only when reviewing, closing, or resuming after implementation;
- load detailed references from this skill only when the current mode requires them.

See [references/workflow.md](references/workflow.md) for the lifecycle and file-update matrix.

## Qualification rule

Use the full workflow when explicitly invoked or when several of these signals are present:

- multiple services, repositories, subsystems, or teams;
- schema migrations, rollout sequencing, or recovery requirements;
- more than one implementation stage or pull request;
- important decisions that must survive context loss;
- requirements intentionally deferred to future work;
- an implementation/review separation is necessary;
- the work is expected to span multiple Codex sessions.

For a small task, state that the full workflow is unnecessary and use the repository's ordinary planning conventions unless the user explicitly requires this skill.

## Required repository documents

Maintain the following contract:

```text
<feature-root>/
├── ROADMAP.md
├── HANDOFF.md
└── stages/
    └── NN-stage-slug/
        ├── PLAN.md
        ├── IMPLEMENTATION.md
        └── REVIEW.md
```

- `ROADMAP.md`: compact source of truth for scope, stage statuses, confirmed decisions, deferred requirements, risks, and links.
- `HANDOFF.md`: bounded current-state summary for a fresh agent or chat. Rewrite it after meaningful transitions.
- `PLAN.md`: proposed or approved technical plan for one stage. Freeze after approval.
- `IMPLEMENTATION.md`: factual report of what was changed, tested, omitted, and discovered.
- `REVIEW.md`: independent findings, fixes, verification evidence, and final disposition.

Read [references/document-contracts.md](references/document-contracts.md) before creating or materially restructuring these files.

## Status model

Use only explicit evidence states:

- `Backlog`
- `Discovery`
- `Planned`
- `In progress`
- `Implemented — unverified`
- `Needs changes`
- `Verified`
- `Deferred`
- `Blocked`
- `Cancelled`

A stage can become `Verified` only when:

1. the implementation exists in the repository;
2. relevant automated checks have passed or failures are documented;
3. the implementation was reviewed against the approved plan and invariants;
4. required manual, migration, rollout, or production checks are complete or explicitly marked as remaining;
5. the user or an independent reviewer accepts the result.

If production verification is required but not yet possible, keep the stage `Implemented — unverified` or state a narrower verified scope. Never hide that gap.

## Deferred requirements

Record each future obligation in the `ROADMAP.md` deferred-requirements registry with:

- stable ID;
- concise requirement;
- source stage;
- target stage or initiative;
- current status;
- acceptance condition;
- links to the originating plan or implementation evidence.

Use a feature-specific prefix when known, such as `BILL-ADM-001`. Otherwise use the initialized feature prefix. Do not renumber existing IDs.

At the start of every stage, collect all deferred requirements targeted to that stage. At closure, either satisfy each one with evidence or explicitly move it with a reason. Never silently drop it.

## Mode procedures

### Initialize or discover

- Inspect the current repository and existing documentation before inventing structure.
- Initialize the feature workspace without overwriting existing files.
- Record confirmed facts separately from assumptions and open questions.
- Define stages only as far as current evidence supports; avoid speculative micro-stages.
- Set the next concrete action in `HANDOFF.md`.

### Plan

- Ground the plan in current code and documentation.
- State scope, non-scope, invariants, failure modes, migration/rollout implications, tests, and completion criteria.
- Link deferred requirements created or consumed by the stage.
- Avoid implementation detail that adds no reliability or decision value.
- Mark the stage `Planned` only after explicit user approval. Before approval, keep the plan proposed and editable.

### Implement

- Require an approved plan unless the user explicitly changes the scope.
- Mark the stage `In progress` before making substantive changes.
- Follow repository instructions and inspect actual code paths before editing.
- Keep changes within stage scope. Record necessary deviations; do not silently expand the feature.
- Run relevant checks and capture exact commands and outcomes.
- Write `IMPLEMENTATION.md` from the actual diff and test evidence.
- Mark `Implemented — unverified`, never `Verified`.
- Update `HANDOFF.md` with the review entry point and known limitations.

### Review

- Review the actual diff, migrations, tests, and runtime behavior, not only the implementation report.
- Compare against the approved plan, repository invariants, and deferred-requirement registry.
- Report all actionable findings in one pass when possible, ordered by severity.
- Do not praise or restate correct sections unless needed to explain a finding.
- Record unresolved findings in `REVIEW.md` and set `Needs changes` when they block closure.
- After fixes, verify the corrected diff and rerun relevant checks.
- Follow [references/review-rules.md](references/review-rules.md).

### Close stage

- Confirm the review disposition and required evidence.
- Mark `Verified` only when the status criteria are satisfied.
- Update roadmap stage result with commit/PR, migrations, tests, rollout checks, and known limitations.
- Add or update deferred requirements and durable decisions.
- Rewrite `HANDOFF.md` to the next stage or remaining blocker.
- Keep detailed implementation history in stage files, not in the roadmap.
- Run `scripts/validate_feature_docs.py` and resolve structural errors.

### Resume

- Read `ROADMAP.md`, `HANDOFF.md`, and only the relevant active-stage files.
- Confirm repository state and referenced commits when possible.
- Distinguish confirmed implementation from planned or reported work.
- Summarize: current status, last verified result, unresolved blockers, deferred obligations due now, and the next concrete action.
- Do not reopen completed decisions without new evidence.

## Change control

When the user changes an approved requirement or new evidence invalidates a decision:

1. preserve the previous decision in the roadmap decision log;
2. record the reason and date of supersession;
3. update affected stage scope and deferred requirements;
4. create a revised plan or amendment rather than silently rewriting an approved plan;
5. identify implementation already made under the old decision.

For minor implementation details that do not alter scope or invariants, record the deviation in `IMPLEMENTATION.md`; do not create unnecessary ceremony.

## Final response contract

At the end of a run, report only what is useful to continue:

- mode performed;
- files created or updated;
- resulting status;
- evidence or checks completed;
- unresolved blockers or deferred IDs;
- exact next action.

Do not claim asynchronous follow-up. Do not claim verification that was not performed.

## Validation

Use:

```bash
python scripts/validate_feature_docs.py <feature-root>
```

The validator checks structure, required headings, stage-file completeness, bounded handoff size, allowed statuses, and basic deferred-ID consistency. It does not prove that code is correct; independent implementation review remains required.

For examples and non-trigger cases, read [references/examples.md](references/examples.md).
