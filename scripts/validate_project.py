# SPDX-License-Identifier: AGPL-3.0-or-later
"""Validate project structure, documentation links and roadmap scope offline."""
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
            errors.append(f"Missing required file: {path}")
    for category in ("docs", "roadmap"):
        de = {p.relative_to(root / category / "de")
              for p in (root / category / "de").rglob("*.md")}
        en = {p.relative_to(root / category / "en")
              for p in (root / category / "en").rglob("*.md")}
        if not de or de != en:
            errors.append(f"Unpaired language files in {category}: {de ^ en}")
    for path in root.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]*\]\(([^\s)]+)\)", content):
            target = match.group(1)
            parts = urlsplit(target)
            if parts.scheme or not parts.path:
                continue
            resolved = (path.parent / unquote(parts.path)).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f"Broken local link: {path.relative_to(root)} -> {target}")
            for lang, opposite in (("de", "en"), ("en", "de")):
                if f"/{lang}/" in "/" + path.relative_to(root).as_posix():
                    if f"/{opposite}/" in "/" + resolved.relative_to(root).as_posix():
                        errors.append(f"Cross-language local link: {path.name} -> {target}")
    for lang in ("de", "en"):
        roadmap = root / f"roadmap/{lang}/personen-nachlass-roadmap.md"
        acceptance = root / f"docs/{lang}/akzeptanz.md"
        if not roadmap.exists() or not acceptance.exists():
            errors.append(f"Missing roadmap or acceptance file: {lang}")
            continue
        content = roadmap.read_text(encoding="utf-8")
        for term in ("JSON", "RDF/Turtle", "RDFLib", "SHACL", "SPARQL",
                     "NetworkX", "SharePoint", "effective_at", "recorded_at"):
            if term not in content:
                errors.append(f"Missing technical scope {term}: {lang}")
        for phase in (f"P{i}" for i in range(7)):
            if phase + ":" not in content:
                errors.append(f"Missing phase {phase}: {lang}")
        ac = acceptance.read_text(encoding="utf-8")
        for identifier in (f"AC-{i:02}" for i in range(1, 10)):
            if identifier not in ac:
                errors.append(f"Missing acceptance {identifier}: {lang}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        errors = validate(root)
    except (OSError, ValueError, KeyError) as exc:
        errors = [f"Validation error: {exc}"]
    print(json.dumps({"status": "FAILED" if errors else "PASSED",
                      "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
