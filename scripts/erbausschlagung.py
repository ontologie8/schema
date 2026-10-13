# SPDX-License-Identifier: AGPL-3.0-or-later
"""Synthetischer Prüfvertrag: Nachweiskontext, keine Rechtsentscheidung."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
import langcodes
from referencing import Registry, Resource

from scripts.modellvertrag import SCHEMA, fordere, normalisiere, pruefe_zeit, zeitfenster, zeitstempel

WURZEL = Path(__file__).resolve().parents[1]
VERTRAG = json.loads((WURZEL / "profile/anwendungsfaelle/erbausschlagung/prueffaelle.schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(VERTRAG)
FORM = Draft202012Validator(VERTRAG, registry=Registry().with_resource(SCHEMA["$id"], Resource.from_contents(SCHEMA)), format_checker=FormatChecker())


def validiere(paket: dict) -> None:
    fehler = list(FORM.iter_errors(paket))
    fordere(not fehler, "Prüfvertrag verletzt: " + (fehler[0].message if fehler else ""))
    personen = {p["id"] for p in paket["personen"]}
    quellen = {q["id"] for q in paket["quellen"]}
    faelle = {f["id"]: f for f in paket["faelle"]}
    ids = [paket["id"]]

    def objekt(wert):
        if isinstance(wert, list):
            for v in wert:
                objekt(v)
        elif isinstance(wert, dict):
            if "id" in wert:
                ids.append(wert["id"])
            if "bezeichnungen" in wert:
                texte = wert["bezeichnungen"]
                for text in texte:
                    fordere(langcodes.tag_is_valid(text["sprache"]), "Ungültiges Sprachkennzeichen")
                fordere(len({json.dumps(normalisiere(t), sort_keys=True) for t in texte}) == len(texte), "Doppelter Textwert")
            if "quelle_id" in wert:
                fordere(wert["quelle_id"] in quellen, "Unbekannte Nachweisquelle")
            if "erfasst_am" in wert:
                zeitstempel(wert["erfasst_am"])
            for v in wert.values():
                objekt(v)

    # Die Paket-ID wird nicht doppelt durchlaufen.
    for feld in ("personen", "quellen", "beziehungen", "faelle", "nachweise"):
        objekt(paket[feld])
    fordere(len(set(ids)) == len(ids), "Identitäten müssen paketweit eindeutig sein")
    for fall in faelle.values():
        betroffen = set(fall["betroffene_person_ids"])
        fordere(fall["erblasser_id"] in personen and betroffen <= personen, "Unbekannte Person im Fall")
        fordere(fall["ausschlagende_person_id"] in betroffen and fall["erblasser_id"] not in betroffen, "Unzulässige Rollenvermischung")
        keys = [(p["person_id"], p["typ"]) for p in fall["pruefungen"]]
        fordere(len(set(keys)) == len(keys), "Widersprüchlicher Prüfstand; separater Revisionsvertrag erforderlich")
        fordere(all(p["person_id"] in betroffen for p in fall["pruefungen"]), "Prüfung gehört nicht zu betroffener Person")
    for b in paket["beziehungen"]:
        fordere(b["subjekt_id"] in personen and b["objekt_id"] in personen and b["subjekt_id"] != b["objekt_id"], "Unzulässige Personenbeziehung")
        pruefe_zeit(b["fachliche_zeit"])
    for n in paket["nachweise"]:
        fordere(n["fall_id"] in faelle, "Nachweis verweist auf unbekannten Fall")
        fall = faelle[n["fall_id"]]
        erwartet = {fall["erblasser_id"]} if n["typ"] == "tod" else set(fall["betroffene_person_ids"])
        fordere(n["person_id"] in erwartet, "Nachweis gehört nicht zur passenden Fallrolle")
        if "wert" in n["zeit"]:
            unten, _ = zeitfenster(n["zeit"])
            fordere(unten <= zeitstempel(n["erfasst_am"]), "Nachweis vor seinem möglichen Ereignis erfasst")
        if n["typ"] == "gerichtseingang":
            fordere("wert" in n["zeit"], "Eingangsnachweis benötigt einen Zeitpunkt")


def pruefstand(paket: dict, fall_id: str, stichtag: dict, wissen: str) -> dict:
    """Explizite Prüfstände und Nachweise auswählen, ohne Erben zu bestimmen."""
    validiere(paket)
    fordere(stichtag["praezision"] == "sekunde", "Nachweisabfrage benötigt einen exakten Stichtag")
    fachzeit = zeitfenster(stichtag)[0]
    wissenszeit = zeitstempel(wissen)
    fordere(fall_id in {f["id"] for f in paket["faelle"]}, "Unbekannter Fall")
    fall = next(f for f in paket["faelle"] if f["id"] == fall_id)
    bekannte = [n for n in paket["nachweise"] if n["fall_id"] == fall_id and zeitstempel(n["erfasst_am"]) <= wissenszeit and n["pruefstatus"] == "bestaetigt"]

    def nachweisstatus(typ, person_id):
        sicher, unsicher = [], []
        for n in bekannte:
            if n["typ"] != typ or n["person_id"] != person_id:
                continue
            if "wert" not in n["zeit"]:
                unsicher.append(n["id"])
                continue
            unten, oben = zeitfenster(n["zeit"])
            if oben <= fachzeit:
                sicher.append(n["id"])
            elif unten <= fachzeit:
                unsicher.append(n["id"])
        return {"status": "belegt" if sicher else "zeitlich_unbestimmt" if unsicher else "unbekannt", "nachweis_ids": sorted(sicher), "unbestimmte_nachweis_ids": sorted(unsicher)}

    pruefungen = {(p["person_id"], p["typ"]): p for p in fall["pruefungen"] if zeitstempel(p["erfasst_am"]) <= wissenszeit}
    offen = []
    for person_id in sorted(fall["betroffene_person_ids"]):
        for typ in ("auftrag", "frist", "gericht", "form", "belehrung", "vertretung", "genehmigung", "annahmerisiko"):
            if pruefungen.get((person_id, typ), {}).get("status") != "bestaetigt":
                offen.append({"person_id": person_id, "typ": typ})
    if fall["vollzugsweg"] == "notariat":
        kontrolle = "ja"
    elif fall["vollzugsweg"] == "unbekannt" or fall["nachkontrolle"] == "unbekannt":
        kontrolle = "unbekannt"
    else:
        kontrolle = "ja" if fall["nachkontrolle"] == "vereinbart" else "nein"
    return {
        "fall_id": fall_id, "fachlicher_stichtag": stichtag, "wissensstichtag": wissen,
        "vollzugsweg": fall["vollzugsweg"], "nachkontrolle_durch_notariat": kontrolle,
        "annahmerisiko": fall["annahmerisiko"], "offene_pruefungen": offen,
        "personen": [{"person_id": p, "gerichtseingang": nachweisstatus("gerichtseingang", p), "kenntnis_erbfall": nachweisstatus("kenntnis_erbfall", p), "kenntnis_berufungsgrund": nachweisstatus("kenntnis_berufungsgrund", p)} for p in sorted(fall["betroffene_person_ids"])],
        "rechtliche_wirksamkeit": "nicht_berechnet", "erbenstellung": "nicht_berechnet"
    }
