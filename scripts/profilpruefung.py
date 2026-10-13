# SPDX-License-Identifier: AGPL-3.0-or-later
"""Ausgewählte Fachtypen und unabhängige Fragen je exaktem Profil prüfen."""
from __future__ import annotations

from rdflib import Graph

from abbildungen.formate import rdf as pilot_rdf
from abbildungen.formate import erbausschlagung as recht_rdf
from scripts import modellvertrag, erbausschlagung
from scripts.modulvertrag import Paket, lesen
from scripts.pruefe_pilot import pruefe_erwartungen as pruefe_pilot_erwartungen
from scripts.pruefe_erbausschlagung import pruefe_erwartungen as pruefe_recht_erwartungen

ERWARTUNG = "urn:ontologie8:erwartungsvertrag:"
PILOTSCHEMA = modellvertrag.SCHEMA["$id"]
RECHTSCHEMA = erbausschlagung.VERTRAG["$id"]


def validiere_daten(paket: Paket, profil_id: str, daten: dict):
    modellvertrag.fordere(profil_id in paket.profile, "Unbekanntes Fallprofil")
    profil = paket.profile[profil_id]
    if profil["schema_id"] == PILOTSCHEMA:
        modellvertrag.fordere(profil["abbildung_id"] == "urn:ontologie8:abbildung:p0-rdf", "Unbekannte Pilotabbildung")
        modellvertrag.validiere(daten)
        modellvertrag.fordere(all(e["typ"] in profil["entitaetstypen"] for e in daten["entitaeten"]), "Entitätstyp außerhalb des Fallprofils")
        modellvertrag.fordere(all(r["typ"] in profil["aussagetypen"] for r in daten["revisionen"]), "Aussagetyp außerhalb des Fallprofils")
        return pilot_rdf
    if profil["schema_id"] == RECHTSCHEMA:
        modellvertrag.fordere(profil["abbildung_id"] == "urn:ontologie8:abbildung:erbausschlagung:0.1.0", "Unbekannte Rechtsabbildung")
        modellvertrag.fordere(not profil["entitaetstypen"] and not profil["aussagetypen"], "Rechtsprüfvertrag unterstützt keinen impliziten Pilottypimport")
        erbausschlagung.validiere(daten)
        return recht_rdf
    raise modellvertrag.Modellfehler("Datenvertrag benötigt eine ausdrücklich unterstützte Validierungsfähigkeit")


def _projektion(ergebnis: dict, felder: list) -> dict:
    modellvertrag.fordere(felder and len(set(felder)) == len(felder), "Leere oder doppelte Projektionsfelder")
    ergebnis = modellvertrag.normalisiere(ergebnis)
    ausgabe = {}
    for feld in felder:
        wert = ergebnis
        for teil in feld.split("."):
            modellvertrag.fordere(isinstance(wert, dict) and teil in wert, "Erwartungsfeld fehlt: " + feld)
            wert = wert[teil]
        ausgabe[feld] = wert
    return ausgabe


def pruefe_modellfragen(daten: dict, erwartungen: dict):
    modellvertrag.fordere(set(erwartungen) == {"id", "abfragen"} and erwartungen["id"] == ERWARTUNG + "modellfragen:0.1.0", "Unbekannter Erwartungsvertrag")
    modellvertrag.fordere(erwartungen["abfragen"], "Unabhängige Fragen fehlen")
    ids = set()
    for frage in erwartungen["abfragen"]:
        modellvertrag.fordere(set(frage) == {"id", "operation", "argumente", "felder", "erwartet"}, "Unbekannte Fragefelder")
        modellvertrag.fordere(frage["id"] not in ids, "Doppelte Erwartungs-ID")
        ids.add(frage["id"])
        args, operation = frage["argumente"], frage["operation"]
        if operation == "auswahl":
            roh = modellvertrag.auswahl(daten, **args)
            ergebnis = {"treffer": [_projektion(r, frage["felder"]) for r in roh["treffer"]], "unbestimmt": [_projektion(r, frage["felder"]) for r in roh["unbestimmt"]]}
        elif operation in {"bestand", "bestandswert", "szenario"}:
            funktion = {"bestand": modellvertrag.bestand, "bestandswert": modellvertrag.bestandswert, "szenario": modellvertrag.berechne_szenario}[operation]
            ergebnis = _projektion(funktion(daten, **args), frage["felder"])
        elif operation == "revision":
            modellvertrag.fordere(set(args) == {"id"}, "Unbekannte Revisionsfrage")
            revisionen = [r for r in daten["revisionen"] if r["id"] == args["id"]]
            modellvertrag.fordere(len(revisionen) == 1, "Revisionsfrage benötigt genau eine Revision")
            ergebnis = _projektion(revisionen[0], frage["felder"])
        else:
            raise modellvertrag.Modellfehler("Unbekannte Frageoperation")
        modellvertrag.fordere(modellvertrag.normalisiere(ergebnis) == modellvertrag.normalisiere(frage["erwartet"]), "Unabhängige Erwartung nicht erfüllt: " + frage["id"])


def pruefe_profil(paket: Paket, profil_id: str) -> dict:
    modellvertrag.fordere(profil_id in paket.profile, "Unbekanntes Fallprofil")
    profil = paket.profile[profil_id]
    daten = lesen(paket.artefakt(profil["beispiel_id"]))
    erwartungen = lesen(paket.artefakt(profil["erwartungen_id"]))
    abbildung = validiere_daten(paket, profil_id, daten)
    erwartungsvertrag = profil["erwartungsvertrag_id"]
    if erwartungsvertrag == ERWARTUNG + "modellfragen:0.1.0" and profil["schema_id"] == PILOTSCHEMA:
        pruefer = pruefe_modellfragen
    elif erwartungsvertrag == ERWARTUNG + "p0-pilot:0.1.0" and profil["schema_id"] == PILOTSCHEMA:
        pruefer = pruefe_pilot_erwartungen
    elif erwartungsvertrag == ERWARTUNG + "erbausschlagung:0.1.0" and profil["schema_id"] == RECHTSCHEMA:
        pruefer = pruefe_recht_erwartungen
    else:
        raise modellvertrag.Modellfehler("Unbekannter oder ungeeigneter Erwartungsvertrag")
    pruefer(daten, erwartungen)
    graph = abbildung.nach_rdf(daten)
    for formatname in ("turtle", "json-ld"):
        rueckweg = abbildung.aus_rdf(Graph().parse(data=graph.serialize(format=formatname), format=formatname))
        modellvertrag.fordere(rueckweg == modellvertrag.normalisiere(daten), "Profil-Rückweg verliert Modellbedeutung")
        validiere_daten(paket, profil_id, rueckweg)
        pruefer(rueckweg, erwartungen)
    return {"profil_id": profil_id, "version": profil["version"], "rdf_tripel": len(graph), "rueckwege": ["turtle", "json-ld"]}
