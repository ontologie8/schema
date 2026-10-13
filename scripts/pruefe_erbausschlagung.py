# SPDX-License-Identifier: AGPL-3.0-or-later
"""Vier Quellszenarien und unabhängige Erwartungen offline prüfen."""
import json
from pathlib import Path
import sys

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WURZEL))

from rdflib import Graph
from abbildungen.formate.erbausschlagung import aus_rdf, nach_rdf
from scripts.erbausschlagung import VERTRAG, pruefstand, validiere
from scripts.modellvertrag import SCHEMA, Modellfehler, fordere, normalisiere


def pruefe_profil(paket):
    pfad = WURZEL / "profile/anwendungsfaelle/erbausschlagung/profil.json"
    profil = json.loads(pfad.read_text(encoding="utf-8"))
    fordere(profil["schema_id"] == VERTRAG["$id"] and profil["kern_schema_id"] == SCHEMA["$id"] and profil["version"] == paket["version"], "Profilversion stimmt nicht mit Prüfvertrag überein")
    for feld in ("schema", "beispiele", "erwartungen", "dokumentation"):
        ziel = (pfad.parent / profil[feld]).resolve()
        fordere(ziel.is_relative_to(WURZEL) and ziel.is_file(), "Profilpfad fehlt oder verlässt Repository")
    zuordnung = profil["herkunft"]["zuordnung"]
    fordere({"urn:beispiel:erbausschlagung:" + z["fall"] for z in zuordnung} == {f["id"] for f in paket["faelle"]}, "Quellszenarien sind nicht vollständig zugeordnet")


def pruefe_erwartungen(paket, erwartungen):
    for fall in erwartungen["abfragen"]:
        ergebnis = pruefstand(paket, fall["fall_id"], fall["stichtag"], fall["wissen"])
        projektion = {
            "nachkontrolle_durch_notariat": ergebnis["nachkontrolle_durch_notariat"],
            "annahmerisiko": ergebnis["annahmerisiko"],
            "offene_pruefungen": ergebnis["offene_pruefungen"],
            "personen": [{"person_id": p["person_id"], **{typ: p[typ]["status"] for typ in ("gerichtseingang", "kenntnis_erbfall", "kenntnis_berufungsgrund")}} for p in ergebnis["personen"]],
            "rechtliche_wirksamkeit": ergebnis["rechtliche_wirksamkeit"],
            "erbenstellung": ergebnis["erbenstellung"]
        }
        fordere(projektion == fall["erwartet"], "Erbausschlagungserwartung nicht erfüllt: " + fall["id"])


def main():
    try:
        paket = json.loads((WURZEL / "beispiele/synthetisch/erbausschlagung/faelle.json").read_text(encoding="utf-8"))
        erwartungen = json.loads((WURZEL / "beispiele/synthetisch/erbausschlagung/erwartungen.json").read_text(encoding="utf-8"))
        pruefe_profil(paket)
        validiere(paket)
        pruefe_erwartungen(paket, erwartungen)
        graph = nach_rdf(paket)
        for formatname in ("turtle", "json-ld"):
            rueckweg = aus_rdf(Graph().parse(data=graph.serialize(format=formatname), format=formatname))
            fordere(rueckweg == normalisiere(paket), "Erbausschlagungs-Rückweg verändert Modellbedeutung")
            pruefe_erwartungen(rueckweg, erwartungen)
        print(json.dumps({"status": "PASSED", "pruefvertrag": "erbausschlagung:0.1.0", "faelle": len(paket["faelle"]), "abfragen": len(erwartungen["abfragen"]), "rdf_tripel": len(graph), "rueckwege": ["turtle", "json-ld"]}, indent=2))
        return 0
    except (Modellfehler, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "FAILED", "fehler": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
