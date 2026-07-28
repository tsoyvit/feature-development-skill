#!/usr/bin/env python3
"""Create one stage folder without modifying approved existing documents."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def render(template: Path, values: dict[str, str]) -> str:
    text = template.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = re.findall(r"\{\{[A-Z0-9_]+\}\}", text)
    if unresolved:
        raise ValueError(f"Unresolved template placeholders: {sorted(set(unresolved))}")
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_root", help="Feature documentation root")
    parser.add_argument("--number", required=True, type=int, help="Positive stage number")
    parser.add_argument("--slug", required=True, help="Stage slug in kebab-case")
    parser.add_argument("--title", required=True, help="Human-readable stage title")
    args = parser.parse_args()

    if args.number < 1 or args.number > 99:
        parser.error("--number must be between 1 and 99")
    if not SLUG_RE.fullmatch(args.slug):
        parser.error("--slug must be lowercase kebab-case")

    feature_root = Path(args.feature_root).resolve()
    if not (feature_root / "ROADMAP.md").is_file():
        parser.error("feature_root must contain ROADMAP.md")

    stage_number = f"{args.number:02d}"
    stage_root = feature_root / "stages" / f"{stage_number}-{args.slug}"
    if stage_root.exists():
        print(f"Refusing to overwrite existing stage: {stage_root}", file=sys.stderr)
        return 2
    stage_root.mkdir(parents=True)

    template_root = Path(__file__).resolve().parents[1] / "assets" / "templates"
    values = {"STAGE_NUMBER": stage_number, "STAGE_TITLE": args.title.strip()}
    for name in ("PLAN.md", "IMPLEMENTATION.md", "REVIEW.md"):
        (stage_root / name).write_text(
            render(template_root / f"{name}.tpl", values), encoding="utf-8"
        )

    print(stage_root)
    print("Add the stage row and active-stage link to ROADMAP.md manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
