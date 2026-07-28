---
name: feature-development-skill
description: Run large, multi-stage feature or module development with a SkillCue-first workflow. Automatically detect the SkillCue coordination workspace with independent backend, web, windows, and landing repositories, or fall back to another coordination workspace or a single repository. Maintain central ROADMAP.md and HANDOFF.md files plus approved PLAN.md and factual RESULT.md files for each stage. Preserve deferred requirements and cross-repository implementation references without adding a mandatory post-implementation review phase. Use when the user explicitly invokes this skill or requests substantial work spanning stages, repositories, migrations, future obligations, or multiple Codex sessions. Do not use for routine isolated tasks unless explicitly requested.
license: MIT
metadata:
  author: tsoyvit
  version: "2.0.0"
---

# Feature Development

Run large feature work as a durable lifecycle stored in the project repository. Treat chat history as temporary and repository documents as the source of truth.

This skill is designed first for SkillCue. Reusability is secondary: preserve the SkillCue behavior below, then fall back cleanly for other projects.

## Core rules

1. **SkillCue first.** When the current root is `skillcue-workspace` or matches the documented SkillCue layout, use the SkillCue project model in [references/skillcue-workspace.md](references/skillcue-workspace.md).
2. **Detect topology automatically.** Inspect root instructions, Git boundaries, remotes, and child repositories. Do not ask the user to classify the project unless the evidence is genuinely ambiguous.
3. **Centralize initiative state.** In a coordination workspace, store roadmap, handoff, stage plans, and stage results only in the coordination repository.
4. **Keep current technical docs near code.** Update backend/web/windows/landing current documentation when their behavior changes, but do not duplicate initiative documents there.
5. **Freeze approved plans.** After explicit user approval, preserve `PLAN.md`. Record actual deviations in `RESULT.md`.
6. **No mandatory review phase.** The lifecycle ends implementation with a factual `RESULT.md` and roadmap/handoff updates. Do not create `REVIEW.md`, review statuses, or a separate verification stage.
7. **Preserve future obligations.** Give every deferred requirement a stable ID, target stage or initiative, and acceptance condition.
8. **Keep context bounded.** Rewrite `HANDOFF.md`; do not append transcripts or unlimited history.
9. **Stay proportional.** Do not use this workflow for a routine isolated task unless explicitly requested.

## Operating modes

Infer the mode from the user's request and current initiative state:

- **Initialize**: detect topology and create the initiative workspace.
- **Discover**: investigate current behavior and define scope, constraints, stages, and open questions.
- **Plan**: create or revise one stage plan before explicit approval.
- **Implement**: execute an approved stage, run relevant checks, write `RESULT.md`, and update initiative state.
- **Close stage**: complete missing roadmap/handoff bookkeeping after implementation when it was not finished in the implementation run.
- **Resume**: reconstruct current state from repository documents and continue from the next valid action.

Do not implement a proposed plan before explicit user approval. The implementing run may finish the stage and update its documents; no separate review run is required by this skill.

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

Installation must not create project files. Initialization happens only after the user invokes the skill for a specific project or initiative.

Default initiative location:

```text
docs/initiatives/<initiative-slug>/
```

Use `scripts/init_feature.py` when available. It detects the topology and pre-populates the project map. Never overwrite an existing initiative.

Required structure:

```text
<initiative-root>/
├── ROADMAP.md
├── HANDOFF.md
└── stages/
    └── NN-stage-slug/
        ├── PLAN.md
        └── RESULT.md
```

Before editing, read only the bounded context required for the current mode:

- always read `ROADMAP.md` and `HANDOFF.md`;
- read the active stage `PLAN.md` for planning or implementation;
- read the active stage `RESULT.md` when resuming or closing an implemented stage;
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

- `ROADMAP.md`: compact source of truth for project topology, scope, stages, decisions, deferred requirements, blockers, and implementation references.
- `HANDOFF.md`: bounded current state for a new chat.
- `PLAN.md`: proposed or approved plan for one stage. Preserve after approval.
- `RESULT.md`: factual account of actual changes, repository references, checks, docs, deviations, remaining work, and new deferred requirements.

Read [references/document-contracts.md](references/document-contracts.md) before creating or materially restructuring these files.

## Status model

Use only:

- `Backlog`
- `Discovery`
- `Planned`
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

### Initialize or discover

- Read project instructions before inventing structure.
- Detect and record project topology automatically.
- For SkillCue, create the initiative only in workspace `docs/initiatives/`.
- Separate confirmed facts, assumptions, and open questions.
- Define only useful stage boundaries.
- Set the next concrete action in `HANDOFF.md`.

### Plan

- Ground the plan in current code and canonical current docs.
- List affected repositories explicitly.
- State scope, non-scope, invariants, failure/recovery behavior, migrations, rollout, checks, documentation changes, and completion criteria.
- Link deferred requirements consumed or created.
- Keep the plan proposed until explicit user approval.

### Implement

- Require an approved plan unless the user explicitly changes scope.
- Mark the stage `In progress`.
- Work from the coordination root and target child repositories explicitly.
- Keep changes within stage scope; record deviations in `RESULT.md`.
- Run the checks relevant to every changed repository.
- Update canonical current docs when behavior changes.
- Write `RESULT.md` from actual Git state and command results.
- Record branch, commit, and PR for each touched repository when available.
- Mark the stage `Implemented`.
- Update `ROADMAP.md` and rewrite `HANDOFF.md` in the same run when possible.

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

- Read `ROADMAP.md`, `HANDOFF.md`, and only the active stage documents.
- Inspect referenced repositories/branches when necessary.
- Summarize current status, last implemented result, blockers, deferred requirements due now, and the next action.
- Do not redo completed discovery or reopen approved decisions without new evidence.

## Change control

When an approved requirement changes:

1. preserve the prior decision in the roadmap;
2. record the reason and date;
3. update affected scope and deferred requirements;
4. add an amendment or new plan version instead of rewriting the approved history;
5. identify work already implemented under the old decision.

Minor implementation details that do not alter scope or invariants belong in `RESULT.md`.

## Final response contract

At the end of a run, report:

- mode performed;
- initiative files created or updated;
- repositories and code files changed;
- migrations changed;
- current docs read/created/updated;
- checks run and outcomes;
- resulting stage status;
- blockers or deferred IDs;
- exact next action.

Do not claim work that was not performed.

## Validation

```bash
python scripts/validate_feature_docs.py <initiative-root>
```

The validator checks document structure, required headings, stage completeness, bounded handoff size, allowed statuses, project topology, and deferred-ID consistency. It does not inspect or review application code.

For lifecycle details and examples, read:

- [references/workflow.md](references/workflow.md)
- [references/examples.md](references/examples.md)
