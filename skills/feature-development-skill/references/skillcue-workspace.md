# SkillCue workspace profile

## Purpose

This profile is the primary project behavior of `feature-development-skill`.

## Canonical layout

```text
/home/vit/rep/skillcue/
├── README.md
├── AGENTS.md
├── Makefile
├── backend/   # tsoyvit/skillcue
├── web/       # tsoyvit/skillcue-web
├── windows/   # tsoyvit/skillcue-windows
├── landing/   # tsoyvit/skillcue-landing
├── docs/
└── scripts/
```

The root is `tsoyvit/skillcue-workspace`. Application directories are independent Git repositories, intentionally not submodules and not pinned by the workspace repository.

## Coordination rule

Store large-feature initiative state only in:

```text
docs/initiatives/<initiative-slug>/
```

This includes:

- roadmap;
- bounded handoff;
- per-stage factual results and active checkpoints;
- cross-repository decisions;
- deferred requirements;
- per-repository branch/commit/PR references.

Do not copy these files into backend, web, windows, or landing.

The working implementation plan lives in Codex Plan Mode. After approval, the agent checkpoints only the durable stage intent and approved boundaries needed to continue safely.

## Current documentation rule

Initiative documents do not replace current technical documentation.

When implementation changes behavior, update the canonical current document next to the owning code:

- backend behavior: `backend/docs/current/`;
- backend runbooks: `backend/docs/runbooks/`;
- web/admin behavior: `web/docs/current/`;
- Windows behavior: `windows/docs/current/`;
- landing behavior: `landing/docs/current/`;
- cross-repository architecture and project decisions: root `docs/`.

Link from the initiative result to the canonical current docs. Do not duplicate full contracts.

## Git rule

From the workspace root:

```bash
git status
git -C backend status
git -C web status
git -C windows status
git -C landing status
```

Never assume a root Git command includes child-repository changes.

Every stage result must record each touched repository separately:

| Repository | Local path | Branch | Commit/PR | Status |
|---|---|---|---|---|

## Checks

Use project instructions and the affected repository's own commands. Common workspace commands include:

```bash
make test-backend
make test-windows
make web-build
make test
```

Do not run every project check automatically when only one repository changed. Record exactly what ran.

## Graphify

Follow root `AGENTS.md`. Graphify is selective navigation support, not source-of-truth documentation. Do not invoke it by default when current docs and direct source inspection are sufficient.

## Planning and approval behavior

For a SkillCue stage:

1. work in Codex Plan Mode;
2. read root `AGENTS.md`, initiative context, relevant canonical current docs, and actual code;
3. identify every affected repository;
4. ask the user for material product, public-copy, data-contract, rollout, destructive, or scope decisions;
5. refine the Codex plan until the user approves execution;
6. after approval, create missing initiative/stage files, checkpoint durable context, and continue implementation without another approval stop.

## Initialization behavior

When this profile is detected in a writable run:

1. choose the root workspace as coordination repository;
2. create the initiative under root `docs/initiatives/` when it does not exist;
3. populate all five repository rows in `ROADMAP.md`;
4. mark affected repositories per stage rather than creating separate roadmaps;
5. create a stage `RESULT.md` when implementation begins;
6. ask the user only if the detected layout conflicts with current repository instructions.
