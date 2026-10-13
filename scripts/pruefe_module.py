# SPDX-License-Identifier: AGPL-3.0-or-later
"""Fachmodule, Versionsbindungen, Profile und optional portable Ausgabe prüfen."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WURZEL))

from scripts.modellvertrag import Modellfehler
from scripts.modulvertrag import PAKETPFAD, exportiere, lesen, pruefe_paket, pruefe_uebernahme, uebernahme, vergleiche
from scripts.profilpruefung import pruefe_profil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wurzel", type=Path, default=WURZEL, help="Wurzel des zu prüfenden Schema-/Prüfpakets")
    parser.add_argument("--paket", help="Relativer Paketmanifestpfad; sonst aktive Übernahme oder initialer Stand")
    parser.add_argument("--vergleich", type=Path, help="Frühere Übernahmebindung; abweichende Version bleibt offen")
    parser.add_argument("--profil", action="append", help="Exakte Profil-ID; standardmäßig alle Profile")
    parser.add_argument("--export", type=Path, help="Neue lokale portable Ausgabe; keine Anbieterübertragung")
    parser.add_argument("--speicherziel", choices=("github", "sharepoint", "s3"), help="Zielarchitektur; sonst aktive Bindung oder GitHub")
    args = parser.parse_args()
    try:
        bindungspfad = args.wurzel / "uebernahme.json"
        bindung = lesen(bindungspfad) if bindungspfad.exists() else None
        paketpfad = args.paket or (bindung["paketpfad"] if bindung else PAKETPFAD)
        paket = pruefe_paket(args.wurzel, paketpfad)
        if bindungspfad.exists():
            pruefe_uebernahme(paket, bindung)
        speicherziel = args.speicherziel or (bindung["speicherziel"] if bindung else "github")
        profile = [pruefe_profil(paket, p) for p in args.profil or sorted(paket.profile)]
        ausgabe = None
        if args.export:
            ausgabe = str(exportiere(paket, args.export, speicherziel))
        vergleich = vergleiche(paket, lesen(args.vergleich)) if args.vergleich else None
        offen = vergleich and vergleich["status"] == "pruefung_erforderlich"
        print(json.dumps({"status": "PRUEFUNG_ERFORDERLICH" if offen else "PASSED", "paket_id": paket.manifest["id"], "paket_version": paket.manifest["version"], "module": len(paket.module), "begriffszustaendigkeiten": len(paket.begriffe), "profile": profile, "uebernahme": uebernahme(paket, speicherziel), "export": ausgabe, "vergleich": vergleich}, ensure_ascii=False, indent=2))
        return 2 if offen else 0
    except (Modellfehler, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAILED", "fehler": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
