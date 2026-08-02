---
name: feature-development-skill
description: Run large, multi-stage feature or module development without losing context between Codex sessions. Designed first for the SkillCue coordination workspace with independent backend, web, windows, and landing repositories, with fallback support for another coordination workspace or a single repository. Prepare each stage in Codex Plan Mode, execute after explicit user approval, preserve durable initiative context in ROADMAP.md and HANDOFF.md, record factual per-stage outcomes in RESULT.md, and carry stable deferred requirements into later stages. Use for substantial work spanning stages, repositories, migrations, future obligations, or multiple Codex sessions. Do not use for routine isolated tasks unless explicitly requested.
license: MIT
metadata:
  author: tsoyvit
  version: "3.0.0"
---

# Feature Development

Coordinate large staged features so a new Codex session can continue from repository state without reconstructing the whole discussion.

The workflow is SkillCue-first. Generic project support must not weaken the SkillCue behavior.

## Lifecycle

```text
idea and product discussion
→ Codex Plan Mode discovery and refinement
→ explicit user approval
→ durable stage checkpoint
→ implementation
→ factual stage result
→ roadmap and handoff update
→ next stage
```

The Codex plan is the working implementation plan. Repository documents retain confirmed decisions, active implementation context, actual results, and future obligations.

## Core rules

1. **Detect the project automatically.** Inspect root instructions, Git boundaries, remotes, and child repositories before asking the user to classify the project.
2. **Use the coordination repository for initiative state.** For SkillCue this is `tsoyvit/skillcue-workspace`.
3. **Keep current technical documentation beside the owning code.** Initiative documents coordinate work; they do not replace backend/web/windows/landing current docs.
4. **Ask for material decisions.** Product behavior, public copy, data contracts, destructive changes, scope expansion, and rollout semantics belong to the user unless already confirmed.
5. **Execution approval is the stage gate.** Approval of the current Codex plan transitions directly into implementation.
6. **Checkpoint before application changes.** Create missing initiative/stage files, mark the stage `In progress`, and record concise active context before changing code.
7. **Record facts, not discussion history.** Keep documents compact and do not copy chats, full plans, diffs, or logs.
8. **Preserve future obligations.** Every deferred requirement receives a stable ID, target stage or initiative, and acceptance condition.
9. **Keep handoff current.** Rewrite `HANDOFF.md` after meaningful checkpoints and before ending an incomplete run.
10. **Stay proportional.** Use this lifecycle for substantial staged work, not ordinary isolated fixes unless explicitly requested.

## Project topology

Run `scripts/detect_project.py` when available and inspect:

- root `README.md` and `AGENTS.md`;
- root Git remote;
- immediate child Git repositories;
- existing `docs/initiatives/*/ROADMAP.md`.

### SkillCue

Treat the root as SkillCue when strong signals identify `skillcue-workspace` and its independent repositories:

| Component | Local path | Git repository | Responsibility |
|---|---|---|---|
| Workspace | `.` | `tsoyvit/skillcue-workspace` | Initiative state, cross-repository decisions, shared docs and orchestration |
| Backend | `backend/` | `tsoyvit/skillcue` | Backend, API, billing, auth, resources, providers |
| Web | `web/` | `tsoyvit/skillcue-web` | User cabinet and owner/admin web app |
| Windows | `windows/` | `tsoyvit/skillcue-windows` | Windows client |
| Landing | `landing/` | `tsoyvit/skillcue-landing` | Public marketing site |

Use root Git only for workspace files. Target child repositories explicitly with `git -C backend`, `git -C web`, `git -C windows`, and `git -C landing`.

Read [references/skillcue-workspace.md](references/skillcue-workspace.md) before initializing or implementing a SkillCue initiative.

### Other coordination workspaces

Use the root as coordinator when it owns shared docs/orchestration and contains independent application repositories.

### Single repository

Use the root as both coordination and implementation repository when there are no independent child application repositories.

Ask one targeted question only when multiple roots are plausible, current instructions conflict with detected topology, or automatic selection would overwrite incompatible initiative state.

## Initiative structure

Default location:

```text
docs/initiatives/<initiative-slug>/
```

Required structure:

```text
<initiative-root>/
├── ROADMAP.md
├── HANDOFF.md
└── stages/
    └── NN-stage-slug/
        └── RESULT.md
```

Installation never creates project files. Use `scripts/init_feature.py` in a writable run when the initiative is first needed. Use `scripts/init_stage.py` when an approved stage starts. Never overwrite existing initiative or stage state.

## Document roles

- `ROADMAP.md`: project topology, feature scope, stage registry, active stage, durable decisions, deferred requirements, blockers, and implementation references.
- `HANDOFF.md`: bounded current position, active stage intent, progress, repositories, constraints, blockers, deferred requirements due now, and exact next action.
- `RESULT.md`: active checkpoint and final factual record for one started stage, including approved boundaries, actual changes, checks, docs, deviations, limitations, deferred requirements, and next-stage handoff.

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

`Implemented` means implementation finished and the result records checks and limitations. It does not claim an independent audit or external certification.

## Discover and plan

Use Codex Plan Mode.

1. Read project instructions and existing initiative context when present.
2. Inspect canonical current docs and actual code for every potentially affected repository.
3. Separate confirmed behavior, assumptions, open questions, and proposed changes.
4. Ask the user for material decisions instead of choosing silently.
5. Make affected repositories, scope, non-scope, invariants, failure/recovery behavior, migrations, rollout, checks, documentation changes, deferred obligations, and completion criteria explicit.
6. Refine the Codex plan until the user approves execution.

## Implement

After explicit approval of the current Codex plan:

1. initialize the initiative if missing;
2. create the stage result if missing;
3. set the stage `In progress` in `ROADMAP.md`;
4. checkpoint the concise objective, approved boundaries, durable decisions, affected repositories, deferred requirements due now, progress, and next action in `ROADMAP.md`, `HANDOFF.md`, and `RESULT.md`;
5. continue into implementation in the same run;
6. target each affected repository explicitly;
7. stay within approved scope and ask before making a new material decision;
8. update canonical current docs when behavior changes;
9. run relevant checks for every changed repository;
10. complete `RESULT.md` from actual Git state and command output;
11. record branch, commit, and PR references when available;
12. mark the stage `Implemented`, update the roadmap, and rewrite the handoff.

During a long or interrupted stage, update the handoff and active result with factual progress before the run ends.

## Deferred requirements

Record each future obligation in `ROADMAP.md` with:

- stable ID;
- concise requirement;
- source stage;
- target stage or initiative;
- status;
- acceptance condition;
- source/result link.

Use a domain prefix such as `BILL-ADM-001`. Never renumber an existing ID.

At stage start, collect deferred requirements targeted to it. At completion, mark each implemented with a result link or move it explicitly with a reason.

## Resume

1. Read `ROADMAP.md` and `HANDOFF.md`.
2. Read the active stage `RESULT.md` when it exists.
3. Inspect referenced repositories, branches, diffs, current docs, and code only as needed.
4. Reconstruct active intent, completed work, remaining work, blockers, deferred requirements due now, and the exact next action.
5. Continue an `In progress` stage from the checkpoint and actual Git state.
6. Ask one targeted question when a material boundary cannot be reconstructed.
7. Do not reopen implemented stages or active decisions without new evidence.

## Close stage

Use only when implementation finished but bookkeeping remains incomplete:

- finish `RESULT.md`;
- mark the stage `Implemented`;
- update decisions, deferred requirements, blockers, and repository references;
- rewrite `HANDOFF.md`;
- run `scripts/validate_feature_docs.py`.

There is no mandatory review or verification phase.

## Change control

When a durable requirement or decision changes:

1. record the new decision and rationale in `ROADMAP.md`;
2. mark the prior decision `Superseded` when applicable;
3. update affected scope, blockers, and deferred requirements;
4. identify work already implemented under the prior decision;
5. record implementation impact in the active or completed `RESULT.md`.

Minor implementation details belong only in the result.

## Final response

For writable runs, report:

- mode performed;
- initiative files updated;
- repositories, code files, and migrations changed;
- current docs read/created/updated;
- checks and outcomes;
- resulting stage status;
- blockers and deferred IDs;
- exact next action.

In Plan Mode, return the current plan and unresolved decisions without claiming repository changes.

## Validation

```bash
python scripts/validate_feature_docs.py <initiative-root>
```

The validator checks structure, required headings, stage completeness, bounded handoff size, allowed statuses, project topology, and deferred-ID consistency. It does not inspect application code.

Further references:

- [references/workflow.md](references/workflow.md)
- [references/examples.md](references/examples.md)
