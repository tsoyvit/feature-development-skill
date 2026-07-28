#!/usr/bin/env python3
"""Initialize a bounded feature-development documentation workspace."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Target repository root")
    parser.add_argument("--slug", required=True, help="Feature slug in kebab-case")
    parser.add_argument("--title", required=True, help="Human-readable feature title")
    parser.add_argument("--prefix", required=True, help="Stable uppercase ID prefix, e.g. BILL")
    parser.add_argument(
        "--docs-root",
        default="docs/feature-development",
        help="Repository-relative feature docs root",
    )
    args = parser.parse_args()

    if not SLUG_RE.fullmatch(args.slug):
        parser.error("--slug must be lowercase kebab-case")
    if not PREFIX_RE.fullmatch(args.prefix):
        parser.error("--prefix must be 2-16 uppercase letters/digits/hyphens")

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        parser.error(f"Repository directory does not exist: {repo}")

    feature_root = repo / args.docs_root / args.slug
    if feature_root.exists():
        print(f"Refusing to overwrite existing feature workspace: {feature_root}", file=sys.stderr)
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
    }

    (feature_root / "ROADMAP.md").write_text(
        render(template_root / "ROADMAP.md.tpl", values), encoding="utf-8"
    )
    (feature_root / "HANDOFF.md").write_text(
        render(template_root / "HANDOFF.md.tpl", values), encoding="utf-8"
    )

    print(feature_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
