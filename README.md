# Feature Development Skill

A SkillCue-first Codex skill for running large, multi-stage feature or module development without losing decisions, deferred requirements, implementation state, or handoff context.

The skill is designed first for the real SkillCue layout:

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

It remains reusable for ordinary single-repository projects and other coordination workspaces.

The lifecycle is deliberately small:

```text
initialize or resume
→ discover
→ PLAN.md
→ explicit plan approval
→ implementation
→ RESULT.md
→ ROADMAP.md and HANDOFF.md update
→ next stage
```

There is no mandatory post-implementation review phase and no `REVIEW.md`.

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

## Initialize in a project

Open Codex from the project root and invoke:

```text
Use $feature-development-skill.
Initialize a multi-stage initiative for Billing.
Detect the project topology automatically and create the required documents.
```

The agent should:

1. read root `README.md` and `AGENTS.md`;
2. inspect Git boundaries and child repositories;
3. identify SkillCue, another coordination workspace, or a single repository;
4. create the initiative in the coordination repository;
5. ask a question only when the topology is genuinely ambiguous.

For SkillCue, the default location is:

```text
docs/initiatives/<initiative-slug>/
├── ROADMAP.md
├── HANDOFF.md
└── stages/
    └── 01-<stage-slug>/
        ├── PLAN.md
        └── RESULT.md
```

## Common invocations

Prepare a stage plan:

```text
Use $feature-development-skill.
Prepare the plan for the next Billing stage. Do not implement it.
```

Implement an approved stage:

```text
Use $feature-development-skill.
Implement the approved active stage, write RESULT.md, and update ROADMAP.md and HANDOFF.md.
```

Resume in a new chat:

```text
Use $feature-development-skill.
Resume the current Billing initiative from repository documents and continue from the next action.
```

## Documentation placement

- Cross-repository initiative plans, stage results, decisions, and handoffs live in the coordination repository.
- Current technical documentation for backend, web, Windows, or landing behavior stays next to the corresponding application code when that behavior changes.
- Do not duplicate the same contract in the workspace and an application repository. The initiative documents coordinate work and link to the canonical current documents.

## Optional AGENTS.md rule

```md
For large, multi-stage SkillCue initiatives, use the installed
`feature-development-skill`. Store cross-repository initiative state in
`docs/initiatives/`. Do not apply the skill to routine isolated tasks unless
explicitly requested.
```

## License

MIT. See [LICENSE](LICENSE).
