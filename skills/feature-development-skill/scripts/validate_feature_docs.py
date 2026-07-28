#!/usr/bin/env python3
"""Validate structure and bounded state of feature-development documents."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ALLOWED_STAGE_STATUSES = {
    "Backlog",
    "Discovery",
    "Planned",
    "In progress",
    "Implemented — unverified",
    "Needs changes",
    "Verified",
    "Deferred",
    "Blocked",
    "Cancelled",
}
REQUIRED_ROOT = {"ROADMAP.md", "HANDOFF.md"}
REQUIRED_STAGE = {"PLAN.md", "IMPLEMENTATION.md", "REVIEW.md"}
ROADMAP_HEADINGS = {
    "Feature summary",
    "Confirmed scope",
    "Non-scope",
    "Stage registry",
    "Active stage",
    "Confirmed decisions",
    "Deferred requirements",
    "Known risks and blockers",
    "Evidence index",
    "Recent changes",
}
HANDOFF_HEADINGS = {
    "Current position",
    "Last verified result",
    "Active constraints and decisions",
    "Open blockers",
    "Deferred requirements due now",
    "Read next",
    "Next concrete action",
}
STAGE_DIR_RE = re.compile(r"^\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
DEFERRED_ID_RE = re.compile(r"^[A-Z][A-Z0-9-]{1,15}-(?:REQ|ADM)-\d{3}$")


def headings(text: str) -> set[str]:
    return set(HEADING_RE.findall(text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feature_root")
    args = parser.parse_args()

    root = Path(args.feature_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"ERROR: feature root does not exist: {root}")
        return 2

    for name in REQUIRED_ROOT:
        if not (root / name).is_file():
            errors.append(f"Missing root file: {name}")

    roadmap = root / "ROADMAP.md"
    if roadmap.is_file():
        text = roadmap.read_text(encoding="utf-8")
        missing = ROADMAP_HEADINGS - headings(text)
        for item in sorted(missing):
            errors.append(f"ROADMAP.md missing heading: {item}")

        statuses = []
        for line in text.splitlines():
            if line.startswith("|") and " — " in line:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) >= 2 and cells[0] not in {"Stage", "---"}:
                    statuses.append(cells[1])
        for status in statuses:
            if status and status not in ALLOWED_STAGE_STATUSES:
                errors.append(f"ROADMAP.md has unsupported stage status: {status}")

        deferred_ids: list[str] = []
        in_deferred = False
        for line in text.splitlines():
            if line.strip() == "## Deferred requirements":
                in_deferred = True
                continue
            if in_deferred and line.startswith("## "):
                in_deferred = False
            if in_deferred and line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells and cells[0] not in {"ID", "---", ""}:
                    deferred_ids.append(cells[0])
        seen: set[str] = set()
        for item in deferred_ids:
            if not DEFERRED_ID_RE.fullmatch(item):
                warnings.append(f"Deferred requirement ID is nonstandard: {item}")
            if item in seen:
                errors.append(f"Duplicate deferred requirement row: {item}")
            seen.add(item)

    handoff = root / "HANDOFF.md"
    if handoff.is_file():
        text = handoff.read_text(encoding="utf-8")
        missing = HANDOFF_HEADINGS - headings(text)
        for item in sorted(missing):
            errors.append(f"HANDOFF.md missing heading: {item}")
        line_count = len(text.splitlines())
        if line_count > 200:
            errors.append(f"HANDOFF.md exceeds hard limit: {line_count} lines")
        elif line_count > 150:
            warnings.append(f"HANDOFF.md exceeds recommended size: {line_count} lines")

    stages = root / "stages"
    if not stages.is_dir():
        errors.append("Missing stages directory")
    else:
        for path in sorted(stages.iterdir()):
            if not path.is_dir():
                continue
            if not STAGE_DIR_RE.fullmatch(path.name):
                warnings.append(f"Nonstandard stage directory name: {path.name}")
            for name in REQUIRED_STAGE:
                if not (path / name).is_file():
                    errors.append(f"{path.name} missing {name}")
            plan = path / "PLAN.md"
            if plan.is_file():
                status_match = STATUS_RE.search(plan.read_text(encoding="utf-8"))
                if not status_match:
                    errors.append(f"{path.name}/PLAN.md missing Status")

    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")

    if errors:
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"Validation passed: {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
