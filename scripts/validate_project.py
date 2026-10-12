# SPDX-License-Identifier: AGPL-3.0-or-later
"""Projektstruktur, Dokumentationslinks und Roadmap-Umfang offline prüfen."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    required = [
        "README.md", "AGENTS.md", "NOTICE", "AUTHORS.md",
        "LICENSES/README.md", "LICENSES/CC-BY-4.0.txt",
        "LICENSES/AGPL-3.0-or-later.txt", "roadmap/GANTT.md",
        ".github/workflows/project-quality.yml",
    ]
    for path in required:
        if not (root / path).is_file():
            errors.append(f"Erforderliche Datei fehlt: {path}")
    for path in root.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]*\]\(([^\s)]+)\)", content):
            target = match.group(1)
            parts = urlsplit(target)
            if parts.scheme or not parts.path:
                continue
            resolved = (path.parent / unquote(parts.path)).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f"Lokaler Link ungültig: {path.relative_to(root)} -> {target}")
    roadmaps = list((root / "roadmap").rglob("personen-nachlass-roadmap.md"))
    if not roadmaps:
        errors.append("Fachroadmap fehlt")
    for roadmap in roadmaps:
        section = roadmap.parent.relative_to(root / "roadmap")
        acceptance = root / "docs" / section / "akzeptanz.md"
        if not acceptance.exists():
            errors.append(f"Akzeptanzkriterien fehlen: {acceptance.relative_to(root)}")
            continue
        content = roadmap.read_text(encoding="utf-8")
        for term in ("JSON", "RDF/Turtle", "RDFLib", "SHACL", "SPARQL",
                     "NetworkX", "effective_at", "recorded_at"):
            if term not in content:
                errors.append(f"Technischer Umfang fehlt ({term}): {roadmap.relative_to(root)}")
        for phase in (f"P{i}" for i in range(7)):
            if phase + ":" not in content:
                errors.append(f"Phase fehlt ({phase}): {roadmap.relative_to(root)}")
        ac = acceptance.read_text(encoding="utf-8")
        for identifier in (f"AC-{i:02}" for i in range(1, 10)):
            if identifier not in ac:
                errors.append(f"Akzeptanzkriterium fehlt ({identifier}): {acceptance.relative_to(root)}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        errors = validate(root)
    except (OSError, ValueError, KeyError) as exc:
        errors = [f"Prüffehler: {exc}"]
    print(json.dumps({"status": "FAILED" if errors else "PASSED",
                      "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
