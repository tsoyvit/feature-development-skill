# Feature Development Skill

A Codex skill for running large, multi-stage feature or module development without losing decisions, deferred requirements, verification state, or handoff context.

The skill keeps durable project state in the target repository and separates:

- approved plans;
- implementation reports;
- independent reviews;
- verified completion;
- deferred obligations for future stages;
- bounded handoff context for new Codex sessions.

It is intentionally not a general replacement for ordinary task planning. Use it for substantial features, modules, migrations, cross-system changes, and long-running work that will span multiple plans, reviews, or sessions.

## Install in Codex

Ask Codex to install the skill from this GitHub directory:

```text
$skill-installer install https://github.com/tsoyvit/feature-development-skill/tree/main/skills/feature-development-skill
```

Restart Codex after installation.

Current Codex documentation recommends user-level skills under `~/.agents/skills`. Manual installation is also possible:

```bash
git clone https://github.com/tsoyvit/feature-development-skill.git
mkdir -p ~/.agents/skills
cp -R feature-development-skill/skills/feature-development-skill ~/.agents/skills/feature-development-skill
```

Copy the full directory rather than symlinking only `SKILL.md`, because a skill also contains scripts, references, and templates.

## Invoke

Explicit invocation is preferred for large work:

```text
Use $feature-development-skill. Initialize a multi-stage development workspace for the Billing module and prepare the first stage plan.
```

```text
Use $feature-development-skill. Implement the approved active stage, then write the implementation report. Do not mark it verified.
```

```text
Use $feature-development-skill. Review the implementation of the active stage against its approved plan and update the review record.
```

```text
Use $feature-development-skill. Resume this feature from its repository documents and tell me the next concrete action.
```

## Optional AGENTS.md rule

Keep the repository-level instruction short:

```md
For large, multi-stage feature or module work, use the installed `feature-development-skill`. Do not apply it to routine isolated tasks unless explicitly requested.
```

## Target-repository structure

By default, the skill creates and maintains:

```text
docs/feature-development/<feature-slug>/
├── ROADMAP.md
├── HANDOFF.md
└── stages/
    └── 01-<stage-slug>/
        ├── PLAN.md
        ├── IMPLEMENTATION.md
        └── REVIEW.md
```

The target repository, not the chat history, becomes the source of truth.

## License

MIT. See [LICENSE](LICENSE).
