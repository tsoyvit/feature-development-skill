#!/usr/bin/env python3
"""Validate initiative documentation structure without reviewing application code."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ALLOWED_STAGE_STATUSES = {
    "Backlog",
    "Discovery",
    "In progress",
    "Implemented",
    "Deferred",
    "Blocked",
    "Cancelled",
}
REQUIRED_ROOT = {"ROADMAP.md", "HANDOFF.md"}
REQUIRED_STAGE = {"RESULT.md"}
ROADMAP_HEADINGS = {
    "Project topology",
    "Feature summary",
    "Confirmed scope",
    "Non-scope",
    "Stage registry",
    "Active stage",
    "Confirmed decisions",
    "Deferred requirements",
    "Known blockers",
    "Implementation references",
    "Recent changes",
}
HANDOFF_HEADINGS = {
    "Current position",
    "Active stage intent",
    "Last implemented result",
    "Current progress",
    "Active repositories",
    "Active constraints and decisions",
    "Open blockers",
    "Deferred requirements due now",
    "Read next",
    "Next concrete action",
}
RESULT_HEADINGS = {
    "Stage objective and approved boundaries",
    "Repository references",
    "Actual changes",
    "Changed files and migrations",
    "Checks run",
    "Current documentation",
    "Deviations from approved scope",
    "Remaining work and limitations",
    "Deferred requirements",
    "Next stage handoff",
}
STAGE_DIR_RE = re.compile(r"^\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
STATUS_RE = re.compile(r"^Status:\s*(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
DEFERRED_ID_RE = re.compile(r"^[A-Z][A-Z0-9-]{1,15}-(?:REQ|ADM)-\d{3}$")


def headings(text: str) -> set[str]:
    return set(HEADING_RE.findall(text))


def section_lines(text: str, heading: str) -> list[str]:
    lines: list[str] = []
    in_section = False
    marker = f"## {heading}"
    for line in text.splitlines():
        if line.strip() == marker:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            lines.append(line)
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("initiative_root")
    args = parser.parse_args()

    root = Path(args.initiative_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"ERROR: initiative root does not exist: {root}")
        return 2

    for name in REQUIRED_ROOT:
        if not (root / name).is_file():
            errors.append(f"Missing root file: {name}")

    roadmap = root / "ROADMAP.md"
    if roadmap.is_file():
        text = roadmap.read_text(encoding="utf-8")
        for item in sorted(ROADMAP_HEADINGS - headings(text)):
            errors.append(f"ROADMAP.md missing heading: {item}")

        if "Coordination repository:" not in text:
            errors.append("ROADMAP.md missing coordination repository")
        if "| Component | Local path | Git repository | Role |" not in text:
            errors.append("ROADMAP.md missing project topology table")
        if "| Stage | Status | Objective or implemented result | Result |" not in text:
            errors.append("ROADMAP.md missing stage registry table")

        for line in section_lines(text, "Stage registry"):
            if not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] not in {"Stage", "---", ""}:
                status = cells[1]
                if status not in ALLOWED_STAGE_STATUSES:
                    errors.append(f"ROADMAP.md has unsupported stage status: {status}")

        deferred_ids: list[str] = []
        for line in section_lines(text, "Deferred requirements"):
            if line.startswith("|"):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
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
        for item in sorted(HANDOFF_HEADINGS - headings(text)):
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
            result = path / "RESULT.md"
            if result.is_file():
                text = result.read_text(encoding="utf-8")
                status_match = STATUS_RE.search(text)
                if not status_match:
                    errors.append(f"{path.name}/RESULT.md missing Status")
                elif status_match.group(1) not in {"In progress", "Implemented", "Blocked", "Cancelled"}:
                    errors.append(
                        f"{path.name}/RESULT.md has unsupported active/result status: {status_match.group(1)}"
                    )
                for item in sorted(RESULT_HEADINGS - headings(text)):
                    errors.append(f"{path.name}/RESULT.md missing heading: {item}")

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
