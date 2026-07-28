#!/usr/bin/env python3
"""Initialize an initiative after automatically detecting project topology."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

from detect_project import detect_project

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PREFIX_RE = re.compile(r"^[A-Z][A-Z0-9-]{1,15}$")


def render(template: Path, values: dict[str, str]) -> str:
    text = template.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = re.findall(r"\{\{[A-Z0-9_]+\}\}", text)
    if unresolved:
        raise ValueError(f"Unresolved template placeholders: {sorted(set(unresolved))}")
    return text


def topology_rows(project: dict) -> str:
    rows = []
    for repo in project["repositories"]:
        role = {
            "coordination": "Coordination repository and initiative source of truth",
            "application": "Independent application repository",
            "coordination-and-application": "Single repository: coordination and implementation",
        }.get(repo["role"], repo["role"])
        rows.append(
            f'| {repo["name"]} | `{repo["path"]}` | `{repo["remote"]}` | {role} |'
        )
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".", help="Project or workspace root")
    parser.add_argument("--slug", required=True, help="Initiative slug in kebab-case")
    parser.add_argument("--title", required=True, help="Human-readable initiative title")
    parser.add_argument("--prefix", required=True, help="Stable uppercase ID prefix, e.g. BILL")
    parser.add_argument(
        "--docs-root",
        default="docs/initiatives",
        help="Coordination-repository-relative initiative root",
    )
    args = parser.parse_args()

    if not SLUG_RE.fullmatch(args.slug):
        parser.error("--slug must be lowercase kebab-case")
    if not PREFIX_RE.fullmatch(args.prefix):
        parser.error("--prefix must be 2-16 uppercase letters/digits/hyphens")

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        parser.error(f"Project directory does not exist: {repo}")

    project = detect_project(repo)
    if project["confidence"] == "low":
        print("Topology detection is ambiguous; inspect project instructions before initialization.", file=sys.stderr)
        return 3

    feature_root = repo / args.docs_root / args.slug
    if feature_root.exists():
        print(f"Refusing to overwrite existing initiative: {feature_root}", file=sys.stderr)
        return 2

    template_root = Path(__file__).resolve().parents[1] / "assets" / "templates"
    feature_root.mkdir(parents=True)
    (feature_root / "stages").mkdir()
    (feature_root / "stages" / ".gitkeep").write_text("", encoding="utf-8")

    today = dt.date.today().isoformat()
    relative_root = feature_root.relative_to(repo).as_posix()
    values = {
        "FEATURE_TITLE": args.title.strip(),
        "FEATURE_PREFIX": args.prefix,
        "FEATURE_ROOT": relative_root,
        "DATE": today,
        "PROJECT_KIND": project["kind"],
        "COORDINATOR_REPO": project["coordinator"],
        "PROJECT_TOPOLOGY_ROWS": topology_rows(project),
    }

    (feature_root / "ROADMAP.md").write_text(
        render(template_root / "ROADMAP.md.tpl", values), encoding="utf-8"
    )
    (feature_root / "HANDOFF.md").write_text(
        render(template_root / "HANDOFF.md.tpl", values), encoding="utf-8"
    )

    print(feature_root)
    print(f'Detected project kind: {project["kind"]} ({project["confidence"]})')
    for note in project["notes"]:
        print(f"NOTE: {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
