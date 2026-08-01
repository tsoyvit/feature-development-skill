# Feature Development Skill

A SkillCue-first Codex skill for implementing large, multi-stage features without losing decisions, future obligations, implementation state, or handoff context between sessions.

The skill is designed first for the SkillCue layout:

```text
skillcue-workspace/
├── backend/   # independent Git repository: tsoyvit/skillcue
├── web/       # independent Git repository: tsoyvit/skillcue-web
├── windows/   # independent Git repository: tsoyvit/skillcue-windows
├── landing/   # independent Git repository: tsoyvit/skillcue-landing
├── docs/
├── scripts/
└── Makefile
```

It also supports ordinary single-repository projects and other coordination workspaces.

## Workflow

```text
idea and product discussion
→ Codex Plan Mode investigation
→ plan refinement and user decisions
→ user approves execution
→ initiative/stage context is checkpointed
→ implementation starts immediately
→ RESULT.md records factual outcome
→ ROADMAP.md and HANDOFF.md move the initiative forward
```

The plan is refined in Codex Plan Mode. Repository documents retain durable context rather than a copy of the working plan.

There is no mandatory post-implementation review phase.

## Durable documents

For SkillCue, initiatives live in:

```text
docs/initiatives/<initiative-slug>/
├── ROADMAP.md
├── HANDOFF.md
└── stages/
    └── 01-<stage-slug>/
        └── RESULT.md
```

- `ROADMAP.md` keeps stage boundaries, statuses, confirmed decisions, blockers, deferred requirements, and repository references.
- `HANDOFF.md` keeps the active stage intent, current progress, constraints, and exact next action for a new Codex session.
- `RESULT.md` is created when a stage starts and becomes the factual implementation record when the stage completes.

## Install in Codex

```text
$skill-installer install https://github.com/tsoyvit/feature-development-skill/tree/main/skills/feature-development-skill
```

Restart Codex after installation.

Manual installation:

```bash
git clone https://github.com/tsoyvit/feature-development-skill.git
mkdir -p ~/.agents/skills
cp -R feature-development-skill/skills/feature-development-skill ~/.agents/skills/feature-development-skill
```

Installation only installs the skill. It does not modify the current project.

## Normal use

Open Codex from the SkillCue workspace root and start in Plan Mode:

```text
Use $feature-development-skill.
Prepare the next stage of the Billing initiative.
Inspect the actual repositories and current documentation, ask me for product decisions, and do not implement until I approve the Codex plan.
```

The agent should:

1. detect the workspace and independent repositories;
2. read existing initiative context when present;
3. inspect actual code and canonical current documentation;
4. ask the user for material product/scope decisions rather than guessing;
5. refine the Codex plan until the user approves execution.

After approval, the same run should:

1. create any missing initiative/stage structure;
2. checkpoint the active context in `ROADMAP.md`, `HANDOFF.md`, and `RESULT.md`;
3. continue directly into implementation;
4. run relevant checks and update current technical docs;
5. complete `RESULT.md` and move the initiative to the next stage.

## Resume in a new chat

```text
Use $feature-development-skill.
Resume the current Billing initiative from repository documents and actual Git state. Continue from the next concrete action.
```

The agent should read the bounded roadmap, handoff, active result, and only the code/current docs needed for the next action.

## Documentation placement

- Cross-repository roadmap, handoff, stage results, decisions, and deferred requirements live in the coordination repository.
- Current technical documentation for backend, web, Windows, or landing behavior stays next to the corresponding application code when that behavior changes.
- Do not duplicate the same contract in the workspace and an application repository. Initiative documents coordinate work and link to canonical current documents.

## Optional AGENTS.md rule

```md
For large, multi-stage SkillCue initiatives, use the installed
`feature-development-skill`. Store cross-repository initiative state in
`docs/initiatives/`. Do not apply the skill to routine isolated tasks unless
explicitly requested.
```

## License

MIT. See [LICENSE](LICENSE).
