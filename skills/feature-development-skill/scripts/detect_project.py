#!/usr/bin/env python3
"""Detect SkillCue, another coordination workspace, or a single repository."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


SKILLCUE_CHILDREN = {
    "backend": "tsoyvit/skillcue",
    "web": "tsoyvit/skillcue-web",
    "windows": "tsoyvit/skillcue-windows",
    "landing": "tsoyvit/skillcue-landing",
}


def git_value(path: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    value = result.stdout.strip()
    return value or None


def normalize_remote(remote: str | None) -> str:
    if not remote:
        return "unknown"
    value = remote.removesuffix(".git")
    for prefix in ("git@github.com:", "https://github.com/", "http://github.com/"):
        if value.startswith(prefix):
            return value[len(prefix):]
    return value


def is_git_repo(path: Path) -> bool:
    top = git_value(path, "rev-parse", "--show-toplevel")
    return top is not None and Path(top).resolve() == path.resolve()


def detect_project(root: Path) -> dict[str, Any]:
    root = root.resolve()
    readme = (root / "README.md").read_text(encoding="utf-8", errors="ignore") if (root / "README.md").is_file() else ""
    agents = (root / "AGENTS.md").read_text(encoding="utf-8", errors="ignore") if (root / "AGENTS.md").is_file() else ""
    root_remote = normalize_remote(git_value(root, "config", "--get", "remote.origin.url"))

    child_repos: list[dict[str, str]] = []
    for child in sorted(root.iterdir()) if root.is_dir() else []:
        if not child.is_dir() or child.name.startswith("."):
            continue
        if is_git_repo(child):
            child_repos.append(
                {
                    "name": child.name,
                    "path": child.name,
                    "remote": normalize_remote(
                        git_value(child, "config", "--get", "remote.origin.url")
                    ),
                }
            )

    skillcue_signal = (
        root_remote == "tsoyvit/skillcue-workspace"
        or "# SkillCue Workspace" in readme
        or (
            all(name in {repo["name"] for repo in child_repos} for name in SKILLCUE_CHILDREN)
            and ("SkillCue" in readme or "SkillCue" in agents)
        )
    )

    if skillcue_signal:
        repos = [
            {
                "name": "workspace",
                "path": ".",
                "remote": root_remote if root_remote != "unknown" else "tsoyvit/skillcue-workspace",
                "role": "coordination",
            }
        ]
        child_map = {repo["name"]: repo for repo in child_repos}
        for name, expected_remote in SKILLCUE_CHILDREN.items():
            detected = child_map.get(name)
            repos.append(
                {
                    "name": name,
                    "path": name,
                    "remote": detected["remote"] if detected and detected["remote"] != "unknown" else expected_remote,
                    "role": "application",
                }
            )
        return {
            "kind": "skillcue-workspace",
            "confidence": "high",
            "root": str(root),
            "coordinator": "tsoyvit/skillcue-workspace",
            "repositories": repos,
            "notes": [],
        }

    if len(child_repos) >= 2:
        return {
            "kind": "coordination-workspace",
            "confidence": "high" if root_remote != "unknown" else "medium",
            "root": str(root),
            "coordinator": root_remote,
            "repositories": [
                {
                    "name": "workspace",
                    "path": ".",
                    "remote": root_remote,
                    "role": "coordination",
                },
                *[
                    {**repo, "role": "application"}
                    for repo in child_repos
                ],
            ],
            "notes": [],
        }

    notes = []
    if len(child_repos) == 1:
        notes.append(
            "One independent child repository was detected; inspect README/AGENTS if the coordination boundary is unclear."
        )

    return {
        "kind": "single-repository",
        "confidence": "high" if not child_repos else "medium",
        "root": str(root),
        "coordinator": root_remote,
        "repositories": [
            {
                "name": root.name,
                "path": ".",
                "remote": root_remote,
                "role": "coordination-and-application",
            }
        ],
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    result = detect_project(Path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
