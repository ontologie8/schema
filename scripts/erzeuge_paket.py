# SPDX-License-Identifier: AGPL-3.0-or-later
"""Neuen Paketstand aus explizitem Entwurf erzeugen; nie einen Stand überschreiben."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WURZEL))

from scripts.modellvertrag import Modellfehler, fordere
from scripts.modulvertrag import PAKETPFAD, kanonisch, lesen, pruefe_fortschreibung, pruefe_paket, pruefsumme, sicherer_pfad
from scripts.profilpruefung import pruefe_profil


def erzeuge(wurzel: Path, entwurfpfad: str, ausgabe: str, version: str) -> dict:
    entwurf = lesen(sicherer_pfad(wurzel, entwurfpfad))
    fordere(set(entwurf) == {"paket_id", "module", "profile", "artefakte"}, "Unbekannte Paketentwurfsfelder")
    ziel = sicherer_pfad(wurzel, ausgabe)
    fordere(not ziel.exists(), "Paketstand existiert bereits; neue Version und neuen Pfad verwenden")
    artefakte = []
    for a in entwurf["artefakte"]:
        fordere(set(a) == {"id", "pfad", "art"}, "Unbekannte Artefaktfelder im Entwurf")
        artefakte.append({**a, "sha256": pruefsumme(sicherer_pfad(wurzel, a["pfad"]), a["art"])})
    index = {a["id"]: a for a in artefakte}
    manifest = {"art": "paket", "id": entwurf["paket_id"], "version": version, "vertrag_version": "0.1.0", "status": "entwicklungsstand", "artefakte": artefakte}
    for feld in ("module", "profile"):
        manifeste = []
        for artefakt_id in entwurf[feld]:
            fordere(artefakt_id in index, "Manifest fehlt im Paketentwurf")
            objekt = lesen(sicherer_pfad(wurzel, index[artefakt_id]["pfad"]))
            manifeste.append({"id": objekt["id"], "version": objekt["version"], "artefakt_id": artefakt_id})
        manifest[feld] = manifeste
    # Vor Veröffentlichung in einer isolierten Kopie samt Fachfragen prüfen.
    with TemporaryDirectory(prefix="schema-paket-") as tmp:
        probe = Path(tmp)
        for a in artefakte:
            datei = sicherer_pfad(probe, a["pfad"])
            datei.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(sicherer_pfad(wurzel, a["pfad"]), datei)
        manifestpfad = sicherer_pfad(probe, ausgabe)
        manifestpfad.parent.mkdir(parents=True, exist_ok=True)
        manifestpfad.write_bytes(kanonisch(manifest))
        paket = pruefe_paket(probe, ausgabe)
        bisherige = {wurzel / PAKETPFAD}
        bindungspfad = wurzel / "uebernahme.json"
        if bindungspfad.exists():
            bisherige.add(sicherer_pfad(wurzel, lesen(bindungspfad)["paketpfad"]))
        registerpfad = wurzel / "register/pakete.json"
        if registerpfad.exists():
            register = lesen(registerpfad)
            for verweis in register["pakete"]:
                alt = (registerpfad.parent / verweis).resolve()
                fordere(alt.is_relative_to(wurzel.resolve()), "Paketregister verlässt Repository")
                bisherige.add(alt)
        for alt in bisherige:
            if alt.exists():
                alter_stand = lesen(alt)
                fordere(tuple(map(int, version.split("."))) > tuple(map(int, alter_stand["version"].split("."))), "Neuer Paketstand muss eine höhere Version erhalten")
                pruefe_fortschreibung(wurzel, alt.relative_to(wurzel).as_posix(), paket)
        for profil_id in paket.profile:
            pruefe_profil(paket, profil_id)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    with ziel.open("x", encoding="utf-8", newline="\n") as datei:
        json.dump(manifest, datei, ensure_ascii=False, indent=2)
        datei.write("\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entwurf", default="register/paketentwurf.json")
    parser.add_argument("--ausgabe", required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    try:
        manifest = erzeuge(WURZEL, args.entwurf, args.ausgabe, args.version)
        print(json.dumps({"status": "PASSED", "paket_id": manifest["id"], "version": manifest["version"], "ausgabe": args.ausgabe}, ensure_ascii=False))
        return 0
    except (Modellfehler, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAILED", "fehler": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
