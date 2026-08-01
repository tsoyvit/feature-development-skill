---
name: feature-development-skill
description: Run large, multi-stage feature or module development without losing context between Codex sessions. Designed first for the SkillCue coordination workspace with independent backend, web, windows, and landing repositories, with fallback support for another coordination workspace or a single repository. Use Codex Plan Mode to investigate and refine the next stage, then execute immediately after explicit user approval. Keep durable initiative context in ROADMAP.md, HANDOFF.md, and factual per-stage RESULT.md files, including stable deferred requirements and cross-repository implementation references. Use for substantial work spanning stages, repositories, migrations, future obligations, or multiple Codex sessions. Do not use for routine isolated tasks unless explicitly requested.
license: MIT
metadata:
  author: tsoyvit
  version: "3.0.0"
---

# Feature Development

Run large feature work as a durable, staged initiative. Chat and Codex Plan Mode are the working space for investigation and plan refinement. Repository documents preserve only the context needed to continue implementation safely across sessions.

This skill is designed first for SkillCue. Reusability is secondary: preserve the SkillCue behavior below, then fall back cleanly for other projects.

## Core rules

1. **SkillCue first.** When the current root is `skillcue-workspace` or matches the documented SkillCue layout, use the SkillCue project model in [references/skillcue-workspace.md](references/skillcue-workspace.md).
2. **Detect topology automatically.** Inspect root instructions, Git boundaries, remotes, and child repositories. Do not ask the user to classify the project unless the evidence is genuinely ambiguous.
3. **Centralize initiative state.** In a coordination workspace, store `ROADMAP.md`, `HANDOFF.md`, and stage `RESULT.md` files only in the coordination repository.
4. **Keep current technical docs near code.** Update backend/web/windows/landing current documentation when behavior changes, but do not duplicate initiative documents there.
5. **Plan in Codex Plan Mode.** Investigate, ask for product decisions, and refine the stage plan in the Codex interface. Do not require a stage plan file.
6. **One approval starts execution.** Explicit approval of the current Codex plan is the implementation gate. After approval, begin implementation without a second approval checkpoint.
7. **Checkpoint durable context before code.** At the start of execution, create any missing initiative/stage files, mark the stage `In progress`, and capture the concise stage intent, approved boundaries, decisions, repositories, and next action in `ROADMAP.md`, `HANDOFF.md`, and the active `RESULT.md`. Then continue implementation in the same run.
8. **Record facts, not transcripts.** `RESULT.md` records actual changes, checks, deviations, limitations, and future obligations. Do not copy chat history or the full Codex plan into repository documents.
9. **Preserve future obligations.** Give every deferred requirement a stable ID, target stage or initiative, and acceptance condition.
10. **Keep context bounded.** Rewrite `HANDOFF.md`; do not append unlimited history. Update it at meaningful implementation checkpoints and before ending an incomplete run.
11. **Stay proportional.** Do not use this workflow for a routine isolated task unless explicitly requested.

## Operating modes

Infer the mode from the user's request, Codex mode, and current initiative state:

- **Discover / Plan**: inspect current behavior, ask for missing decisions, and refine the next stage in Codex Plan Mode. Project files are not required to change.
- **Implement**: after explicit approval, initialize missing initiative state, checkpoint the active stage, execute the approved plan, run checks, write the factual result, and update the initiative.
- **Close stage**: complete missing result/roadmap/handoff bookkeeping when implementation finished but the implementation run ended early.
- **Resume**: reconstruct current state from bounded repository documents and actual Git state, then continue from the next valid action.
- **Initialize**: create the initiative explicitly in a writable run when useful. Initialization may also happen automatically as the first action after plan approval.

Do not implement before explicit user approval. Do not ask for another approval after the user has approved execution of the current Codex plan.

## Detect project topology

Run `scripts/detect_project.py` from the current project root when available. Also inspect:

- root `README.md`;
- root `AGENTS.md`;
- root Git remote;
- immediate child directories that are independent Git repositories;
- existing `docs/initiatives/*/ROADMAP.md`.

### SkillCue detection

Treat the project as SkillCue when one or more strong signals match:

- root remote is `tsoyvit/skillcue-workspace`;
- root README identifies `SkillCue Workspace`;
- the root coordinates `backend`, `web`, `windows`, and `landing`;
- those paths map to the known independent SkillCue repositories.

Use the root workspace as the coordination repository even though implementation occurs in child repositories.

### Generic coordination workspace

Treat the root as a coordination workspace when it owns shared docs/scripts/orchestration and contains multiple independent child Git repositories.

### Single repository

When there are no independent child application repositories and the root is the code repository, use the root as both coordination and implementation repository.

Ask one targeted question only if:

- multiple plausible coordination roots exist;
- the current directory is inside a child repository rather than the intended workspace and project instructions do not resolve it;
- destructive or conflicting existing initiative structures make automatic selection unsafe.

## Initialize the initiative

Installation must not create project files. Initialization happens only for a specific project/initiative, either in an explicit writable run or automatically after the user approves the first stage for execution.

Default initiative location:

```text
docs/initiatives/<initiative-slug>/
```

Use `scripts/init_feature.py` when available. It detects topology and pre-populates the project map. Never overwrite an existing initiative.

Required structure:

```text
<initiative-root>/
├── ROADMAP.md
├── HANDOFF.md
└── stages/
    └── NN-stage-slug/
        └── RESULT.md
```

Before work, read only the bounded context required for the current mode:

- always read `ROADMAP.md` and `HANDOFF.md` when they exist;
- read the active stage `RESULT.md` when resuming, implementing an already-started stage, or closing a stage;
- read relevant canonical current documentation and code for the repositories in scope;
- load detailed references from this skill only when needed.

## SkillCue repository model

For SkillCue, use:

| Component | Local path | Git repository | Responsibility |
|---|---|---|---|
| Workspace | `.` | `tsoyvit/skillcue-workspace` | Cross-repository initiatives, shared docs, orchestration, project agent rules |
| Backend | `backend/` | `tsoyvit/skillcue` | Backend, API, billing, auth, resources, providers |
| Web | `web/` | `tsoyvit/skillcue-web` | User cabinet and owner/admin web app |
| Windows | `windows/` | `tsoyvit/skillcue-windows` | Windows client |
| Landing | `landing/` | `tsoyvit/skillcue-landing` | Public marketing site |

Run root Git operations only for workspace files. Run application Git operations explicitly with `git -C backend`, `git -C web`, `git -C windows`, or `git -C landing`.

Read [references/skillcue-workspace.md](references/skillcue-workspace.md) before initializing or implementing a SkillCue initiative.

## Document contract

- `ROADMAP.md`: compact source of truth for project topology, feature scope, stage boundaries/status, durable decisions, deferred requirements, blockers, and implementation references.
- `HANDOFF.md`: bounded current state for a new Codex session, including active stage intent, progress, constraints, and exact next action.
- `RESULT.md`: one factual file per started stage. While work is active it is a compact checkpoint; after completion it records actual changes, repository references, checks, documentation, deviations from approved scope, limitations, deferred requirements, and next-stage handoff.

Read [references/document-contracts.md](references/document-contracts.md) before creating or materially restructuring these files.

## Status model

Use only:

- `Backlog`
- `Discovery`
- `In progress`
- `Implemented`
- `Deferred`
- `Blocked`
- `Cancelled`

`Implemented` means the stage implementation run is complete and `RESULT.md` records the checks and limitations. It does not claim an independent audit or external certification.

## Deferred requirements

Record every future obligation in `ROADMAP.md` with:

- stable ID;
- concise requirement;
- source stage;
- target stage or initiative;
- status;
- acceptance condition;
- source/result link.

Use a project/domain prefix such as `BILL-ADM-001`. Do not renumber existing IDs.

At the start of every stage, collect deferred requirements targeted to it. At completion, either mark them implemented with a result link or move them explicitly with a reason.

## Mode procedures

### Discover / Plan

- Work in Codex Plan Mode when the user is preparing a stage for approval.
- Read project instructions, initiative context, canonical current docs, and actual code before proposing changes.
- Separate confirmed facts, assumptions, product decisions, and open questions.
- Ask the user for decisions that affect product behavior, scope, public copy, data contracts, destructive changes, or rollout semantics. Do not decide them silently.
- Make affected repositories, scope, non-scope, invariants, failure/recovery behavior, migrations, rollout, checks, documentation changes, deferred obligations, and completion criteria explicit in the Codex plan.
- Refine the plan until the user approves execution.
- Do not require or create repository documents during Plan Mode.

### Implement

- Treat explicit approval of the current Codex plan as authorization to execute it.
- Do not insert a separate documentation approval step.
- If the initiative does not exist, initialize it as the first writable action.
- If the stage does not exist, create it with `scripts/init_stage.py`.
- Before application changes, update durable context:
  - set the roadmap stage to `In progress` and record its concise objective;
  - record active repositories, approved boundaries, durable decisions, deferred requirements due now, and the exact next action in `HANDOFF.md`;
  - initialize the active `RESULT.md` with the stage objective and approved boundaries.
- Continue directly into implementation in the same run.
- Work from the coordination root and target child repositories explicitly.
- Keep changes within the approved scope. Record material deviations in `RESULT.md`; ask the user before making a new product or scope decision.
- Update `HANDOFF.md` after meaningful checkpoints or before ending an incomplete run so another session can continue from actual state.
- Run the checks relevant to every changed repository.
- Update canonical current docs when behavior changes.
- Finish `RESULT.md` from actual Git state and command results.
- Record branch, commit, and PR for each touched repository when available.
- Mark the stage `Implemented`, update `ROADMAP.md`, and rewrite `HANDOFF.md` in the same run when possible.

### Close stage

Use only when implementation finished but initiative bookkeeping remains incomplete:

- finish `RESULT.md`;
- mark the stage `Implemented`;
- update decisions and deferred requirements;
- record repository references;
- rewrite `HANDOFF.md`;
- run `scripts/validate_feature_docs.py`.

Do not introduce a review or verification phase.

### Resume

- Read `ROADMAP.md`, `HANDOFF.md`, and the active stage `RESULT.md` when it exists.
- Inspect referenced repositories, branches, diffs, and current docs only as needed.
- Reconstruct current status, active stage intent, completed work, blockers, deferred requirements due now, and the next action.
- For an `In progress` stage, use `HANDOFF.md`, the active `RESULT.md`, and actual Git state as the continuation checkpoint.
- If a material approved boundary is missing, ask one targeted question rather than guessing or redoing all discovery.
- Do not reopen implemented stages or confirmed decisions without new evidence.

## Change control

When a durable requirement or decision changes:

1. record the new decision and rationale in `ROADMAP.md`;
2. mark the prior decision `Superseded` when applicable;
3. update affected scope, blockers, and deferred requirements;
4. identify work already implemented under the prior decision;
5. record any implementation impact in the active or completed `RESULT.md`.

Minor implementation details that do not alter scope, product behavior, or invariants belong only in `RESULT.md`.

## Final response contract

At the end of a writable run, report:

- mode performed;
- initiative files created or updated;
- repositories and code files changed;
- migrations changed;
- current docs read/created/updated;
- checks run and outcomes;
- resulting stage status;
- blockers or deferred IDs;
- exact next action.

In Plan Mode, return the current plan and unresolved decisions in the Codex interface without claiming repository changes.

Do not claim work that was not performed.

## Validation

```bash
python scripts/validate_feature_docs.py <initiative-root>
```

The validator checks document structure, required headings, stage completeness, bounded handoff size, allowed statuses, project topology, and deferred-ID consistency. It does not inspect or review application code.

For lifecycle details and examples, read:

- [references/workflow.md](references/workflow.md)
- [references/examples.md](references/examples.md)
