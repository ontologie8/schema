# SPDX-License-Identifier: AGPL-3.0-or-later
"""Schema, Module, synthetischen Pilot und RDF-Rückweg offline prüfen."""
from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import sys

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WURZEL))

from rdflib import Graph
from abbildungen.formate.rdf import aus_rdf, nach_rdf
from scripts.modellvertrag import SCHEMA, Modellfehler, auswahl, berechne_szenario, bestand, bestandswert, fordere, normalisiere, validiere


def _lesen(pfad: Path):
    return json.loads(pfad.read_text(encoding="utf-8"))


def pruefe_module() -> int:
    registerpfad = WURZEL / "register/module.json"
    register = _lesen(registerpfad)
    module = {}
    for verweis in register["manifeste"]:
        pfad = (registerpfad.parent / verweis).resolve()
        fordere(pfad.is_relative_to(WURZEL), "Modulpfad verlässt Repository")
        modul = _lesen(pfad)
        fordere(modul["id"] not in module, "Doppelte Modulidentität")
        module[modul["id"]] = modul
        if "dokumentation" in modul:
            dokument = (pfad.parent / modul["dokumentation"]).resolve()
            fordere(dokument.is_relative_to(WURZEL) and dokument.is_file(), "Moduldokumentation fehlt")
        for artefakt in modul.get("artefakte", []):
            ziel = (pfad.parent / artefakt).resolve()
            fordere(ziel.is_relative_to(WURZEL) and ziel.is_file(), "Modulartefakt fehlt")
    for modul in module.values():
        for abhaengigkeit in modul["abhaengigkeiten"]:
            fordere(abhaengigkeit["id"] in module and module[abhaengigkeit["id"]]["version"] == abhaengigkeit["version"], "Modulabhängigkeit stimmt nicht überein")
    for verweis in register["profile"]:
        pfad = (registerpfad.parent / verweis).resolve()
        fordere(pfad.is_relative_to(WURZEL), "Profilpfad verlässt Repository")
        profil = _lesen(pfad)
        fordere(profil["schema_id"] == SCHEMA["$id"], "Profil verweist auf anderen Schema-Vertrag")
        for referenz in profil["module"]:
            fordere(referenz["id"] in module and module[referenz["id"]]["version"] == referenz["version"], "Profil verwendet unbekannten Modulstand")
    return len(module)


def pruefe_erwartungen(modell: dict, erwartet: dict) -> None:
    for fall in erwartet["kaufpreis"]:
        rs = auswahl(modell, {"wert": "2024-03-10T10:00:00Z", "praezision": "sekunde"}, fall["wissen"], typ="kauf")["treffer"]
        fordere(len(rs) == 1 and rs[0]["id"] == fall["revision"] and Decimal(rs[0]["daten"]["betrag"]) == Decimal(fall["betrag"]), "Kaufpreiserwartung nicht erfüllt")
    for fall in erwartet["eigentum"]:
        rs = auswahl(modell, {"wert": fall["stichtag"], "praezision": "sekunde"}, fall["wissen"], typ="eigentum")["treffer"]
        fordere([r["subjekt_id"] for r in rs] == [fall["person"]], "Eigentumserwartung nicht erfüllt")
    stichtag = {"wert": "2026-06-01", "praezision": "tag"}
    b = bestand(modell, "urn:beispiel:POSITION-1", stichtag, "2026-06-06T00:00:00Z")
    fordere(Decimal(b["menge"]) == Decimal(erwartet["bestand"]), "Bestandserwartung nicht erfüllt")
    wert = bestandswert(modell, "urn:beispiel:POSITION-1", stichtag, "2026-06-06T00:00:00Z", "EUR", "urn:beispiel:MARKT-1")
    fordere(Decimal(wert["betrag"]) == Decimal(erwartet["bestandswert"]), "Bewertungserwartung nicht erfüllt")
    for s_id, betrag in erwartet["szenarien"].items():
        ergebnis = berechne_szenario(modell, s_id)
        fordere(Decimal(ergebnis["betrag"]) == Decimal(betrag), "Szenarioerwartung nicht erfüllt")
        rs = [r for r in modell["revisionen"] if r.get("szenario_id") == s_id]
        fordere(len(rs) == 1 and Decimal(rs[0]["daten"]["betrag"]) == Decimal(betrag), "Gespeicherte Prognose weicht von Erwartung ab")


def main() -> int:
    try:
        module = pruefe_module()
        modell = _lesen(WURZEL / "beispiele/synthetisch/p0-pilot.json")
        erwartet = _lesen(WURZEL / "beispiele/synthetisch/p0-erwartungen.json")
        validiere(modell)
        pruefe_erwartungen(modell, erwartet)
        graph = nach_rdf(modell)
        rueckwege = []
        for formatname in ("turtle", "json-ld"):
            rueckweg = aus_rdf(Graph().parse(data=graph.serialize(format=formatname), format=formatname))
            fordere(rueckweg == normalisiere(modell), "RDF-Rückweg verändert Modellbedeutung")
            pruefe_erwartungen(rueckweg, erwartet)
            rueckwege.append(formatname)
        Graph().parse(WURZEL / "abbildungen/formate/vokabular.ttl", format="turtle")
        print(json.dumps({"status": "PASSED", "schema_version": modell["schema_version"], "module": module, "entitaeten": len(modell["entitaeten"]), "revisionen": len(modell["revisionen"]), "szenarien": len(modell["szenarien"]), "rdf_tripel": len(graph), "rueckwege": rueckwege}, ensure_ascii=False, indent=2))
        return 0
    except (Modellfehler, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "FAILED", "fehler": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
