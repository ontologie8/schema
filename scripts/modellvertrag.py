# SPDX-License-Identifier: AGPL-3.0-or-later
"""Kleiner Pilotvertrag: Form, Referenzen, Zeit, Revisionen und Szenarien."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from decimal import Decimal, localcontext
from functools import wraps
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator, FormatChecker
import langcodes

WURZEL = Path(__file__).resolve().parents[1]
BEGRIFF = "urn:ontologie8:begriff:"
REGISTER = json.loads((WURZEL / "modelle/kern/begriffe.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((WURZEL / "modelle/kern/modell.schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(SCHEMA)
FORM = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
DEZIMALFELDER = {"betrag", "menge", "faktor", "kurs"}


class Modellfehler(ValueError):
    """Der Datensatz verletzt den Pilotvertrag."""


def fordere(bedingung: bool, meldung: str) -> None:
    if not bedingung:
        raise Modellfehler(meldung)


def zeitstempel(wert: str) -> datetime:
    try:
        fordere(bool(re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)", wert)), "Zeitstempel braucht Datum, Uhrzeit und Offset")
        return datetime.fromisoformat(wert.replace("Z", "+00:00")).astimezone(timezone.utc)
    except (ValueError, TypeError) as exc:
        raise Modellfehler("Ungültiger Zeitstempel") from exc


def zeitfenster(punkt: dict) -> tuple[datetime, datetime]:
    """Mögliche zeitliche Position: exakter Zeitpunkt oder Präzisionsfenster."""
    wert, praezision = punkt["wert"], punkt["praezision"]
    try:
        if praezision == "sekunde":
            zeit = zeitstempel(wert)
            return zeit, zeit
        muster = {"tag": r"\d{4}-\d\d-\d\d", "monat": r"\d{4}-\d\d", "jahr": r"\d{4}"}
        fordere(bool(re.fullmatch(muster[praezision], wert)), "Zeitwert passt nicht zur Präzision")
        teile = [int(t) for t in wert.split("-")]
        jahr, monat, tag = (teile + [1, 1])[:3] if len(teile) == 1 else (teile + [1])[:3]
        unten = datetime(jahr, monat, tag, tzinfo=timezone.utc)
        if praezision == "tag":
            oben = unten + timedelta(days=1)
        elif praezision == "monat":
            oben = datetime(jahr + (monat == 12), 1 if monat == 12 else monat + 1, 1, tzinfo=timezone.utc)
        else:
            oben = datetime(jahr + 1, 1, 1, tzinfo=timezone.utc)
        return unten, oben
    except (ValueError, KeyError, OverflowError) as exc:
        raise Modellfehler("Ungültiger Zeitwert oder Präzision") from exc


def pruefe_zeit(zeit: dict) -> None:
    if zeit.get("art") == "zeitpunkt":
        zeitfenster(zeit)
        return
    beginn, ende = zeit["beginn"], zeit["ende"]
    fordere(beginn.get("status") != "offen", "Offener Beginn wird im Pilot nicht unterstützt")
    for grenze in (beginn, ende):
        if "wert" in grenze:
            zeitfenster(grenze)
    if "wert" in beginn and "wert" in ende:
        fordere(beginn != ende, "Intervall ist leer")
        b, e = zeitfenster(beginn), zeitfenster(ende)
        fordere(b[0] < e[1] or (e[0] == e[1] and b[0] < e[0]), "Intervall ist leer oder umgekehrt")
        if b[0] == b[1] and e[0] == e[1]:
            fordere(b[0] < e[0], "Zeitpunkt darf nicht als leeres Intervall geführt werden")


def gilt_am(zeit: dict, stichtag: dict) -> bool | None:
    q0, q1 = zeitfenster(stichtag)
    if zeit["art"] == "zeitpunkt":
        z0, z1 = zeitfenster(zeit)
        if (z0, z1) == (q0, q1):
            return True
        if z0 == z1 and q0 <= z0 < q1:
            return True
        if z0 == z1 and q0 == q1:
            return z0 == q0
        if (q0 >= z1 and z0 != z1) or (z0 >= q1 and q0 != q1) or z1 < q0 or q1 < z0:
            return False
        return None
    beginn, ende = zeit["beginn"], zeit["ende"]
    unsicher = False
    if "wert" in beginn:
        b0, b1 = zeitfenster(beginn)
        if q1 < b0 or (q1 == b0 and q0 != q1):
            return False
        if q0 < b1:
            unsicher = True
    else:
        unsicher = True
    if "wert" in ende:
        e0, e1 = zeitfenster(ende)
        if q0 >= e1:
            return False
        if q1 > e0 or (q0 == q1 and q0 == e0):
            unsicher = True
    elif ende["status"] == "unbekannt":
        unsicher = True
    return None if unsicher else True


def normalisiere(wert):
    """Sammlungen ungeordnet, Sprachkennzeichen klein, Dezimallexik einheitlich."""
    if isinstance(wert, list):
        return sorted((normalisiere(v) for v in wert), key=lambda v: json.dumps(v, sort_keys=True, ensure_ascii=False))
    if isinstance(wert, dict):
        ergebnis = {k: normalisiere(v) for k, v in wert.items()}
        if "sprache" in ergebnis:
            ergebnis["sprache"] = langcodes.standardize_tag(ergebnis["sprache"]).lower()
        for feld in DEZIMALFELDER & ergebnis.keys():
            zahl = Decimal(ergebnis[feld])
            lexik = format(zahl, "f")
            ergebnis[feld] = "0" if zahl == 0 else lexik.rstrip("0").rstrip(".") if "." in lexik else lexik
        return ergebnis
    return wert


def _texte_pruefen(wert) -> None:
    if isinstance(wert, list):
        kanonisch = [json.dumps(normalisiere(v), sort_keys=True, ensure_ascii=False) for v in wert]
        fordere(len(kanonisch) == len(set(kanonisch)), "Semantische Dublette in einer Sammlung")
        for v in wert:
            _texte_pruefen(v)
    elif isinstance(wert, dict):
        if "sprache" in wert:
            fordere(langcodes.tag_is_valid(wert["sprache"]), "Ungültiges BCP-47-Sprachkennzeichen")
        for v in wert.values():
            _texte_pruefen(v)


def _ordnungswert(revision: dict):
    return zeitstempel(revision["erfasst_am"]), revision.get("folge", 0)


def _mit_genauigkeit(funktion):
    """Genug Stellen für alle Eingabeziffern und bis zu 100 Faktorperioden."""
    @wraps(funktion)
    def aufruf(modell, *args, **kwargs):
        laengen = [1]

        def sammeln(wert):
            if isinstance(wert, dict):
                for k, v in wert.items():
                    if k in DEZIMALFELDER and isinstance(v, str):
                        laengen.append(len(v))
                    sammeln(v)
            elif isinstance(wert, list):
                for v in wert:
                    sammeln(v)
        sammeln(modell)
        with localcontext() as kontext:
            kontext.prec = max(28, max(laengen) * 102 + len(str(len(modell.get("revisionen", [])))) + 32)
            return funktion(modell, *args, **kwargs)
    return aufruf


def _aktive(modell: dict, wissen: str) -> list[dict]:
    grenze = zeitstempel(wissen)
    gruppen: dict[str, list[dict]] = {}
    for revision in modell["revisionen"]:
        if zeitstempel(revision["erfasst_am"]) <= grenze:
            gruppen.setdefault(revision["aussage_id"], []).append(revision)
    return [max(rs, key=_ordnungswert) for rs in gruppen.values() if max(rs, key=_ordnungswert)["art"] != "ruecknahme"]


def validiere(modell: dict) -> None:
    fehler = sorted(FORM.iter_errors(modell), key=lambda e: str(list(e.path)))
    fordere(not fehler, "Schemafehler: " + (str(list(fehler[0].path)) + ": " + fehler[0].message if fehler else ""))
    try:
        _texte_pruefen(modell)
    except langcodes.LanguageTagError as exc:
        raise Modellfehler("Ungültiges BCP-47-Sprachkennzeichen") from exc
    alle = [modell] + modell["entitaeten"] + modell["revisionen"] + modell["szenarien"]
    ids = [v["id"] for v in alle]
    fordere(len(ids) == len(set(ids)), "Doppelte Ressourcen-ID")
    fordere(not set(ids).intersection(r["aussage_id"] for r in modell["revisionen"]), "Aussage-ID ist zugleich eine andere Ressourcenidentität")
    entitaeten = {v["id"]: v for v in modell["entitaeten"]}
    revisionen = {v["id"]: v for v in modell["revisionen"]}
    szenarien = {v["id"]: v for v in modell["szenarien"]}

    def entitaet(iri, typen=None):
        fordere(iri in entitaeten, "Fehlende Entitätsreferenz: " + iri)
        e = entitaeten[iri]
        if typen:
            fordere(e["typ"] in [BEGRIFF + t for t in typen], "Ungeeigneter Entitätstyp: " + iri)
        return e

    def methode(iri, version):
        e = entitaet(iri, ["methode"])
        fordere(e.get("version") == version, "Methodenversion stimmt nicht überein")

    for e in entitaeten.values():
        fordere(e["typ"] in [BEGRIFF + t for t in REGISTER["entitaetstypen"]], "Nicht registrierter Entitätstyp")
        if e["typ"] == BEGRIFF + "methode":
            fordere("version" in e, "Methodenentität braucht eine Version")
    gruppen: dict[str, list[dict]] = {}
    nachfolger: dict[str, list[dict]] = {}
    for r in revisionen.values():
        pruefe_zeit(r["fachliche_zeit"])
        zeitstempel(r["erfasst_am"])
        if "quellzeit" in r:
            zeitstempel(r["quellzeit"])
        entitaet(r["quelle_id"], ["quelle"])
        typ = r["typ"].removeprefix(BEGRIFF)
        fordere(r["typ"].startswith(BEGRIFF) and typ in REGISTER["aussagetypen"], "Nicht registrierter Aussagetyp")
        regel = REGISTER["aussagetypen"][typ]
        entitaet(r["subjekt_id"], regel["subjekt"])
        if "objekt" in regel:
            fordere("objekt_id" in r, "Beziehung braucht eine Objektreferenz")
            entitaet(r["objekt_id"], regel["objekt"])
        else:
            fordere("objekt_id" not in r, "Objektreferenz ist für diesen Typ nicht definiert")
        if r["art"] != "ruecknahme":
            fordere(r["art"] == regel["art"], "Aussagetyp und Strukturart widersprechen sich")
            fordere(all(k in r["daten"] for k in regel["pflichtdaten"]), "Fachlich benötigte Nutzdaten fehlen")
        for feld, kategorie in (("einheit", "einheiten"), ("wertart", "wertarten"), ("zustand", "zustaende"), ("anlass", "anlaesse")):
            if feld in r["daten"]:
                fordere(r["daten"][feld] in [BEGRIFF + v for v in REGISTER[kategorie]], "Nicht registrierter Nutzdatenbegriff")
        if "markt_id" in r["daten"]:
            entitaet(r["daten"]["markt_id"], ["markt"])
        if "methode_id" in r:
            methode(r["methode_id"], r["methode_version"])
        for iri in r.get("eingabe_ids", []):
            fordere(iri in revisionen, "Fehlende Eingaberevision")
            fordere(zeitstempel(revisionen[iri]["erfasst_am"]) <= zeitstempel(r["erfasst_am"]), "Aussage verwendet noch unbekannte Eingabe")
        if r["art"] == "empfehlung":
            fordere(r["aussageart"] == "empfehlung" and "methode_id" in r and r.get("eingabe_ids"), "Empfehlung braucht Methode und Eingabestand")
        if "szenario_id" in r:
            fordere(r["szenario_id"] in szenarien, "Fehlendes Szenario")
            s = szenarien[r["szenario_id"]]
            fordere((r["methode_id"], r["methode_version"]) == (s["modell_id"], s["modell_version"]), "Prognose bindet ein anderes Modell als ihr Szenario")
            fordere(r["fachliche_zeit"]["art"] == "zeitpunkt" and zeitfenster(r["fachliche_zeit"]) == zeitfenster(s["zielzeit"]), "Prognose und Szenario haben verschiedene Zielzeiten")
            fordere(zeitstempel(r["erfasst_am"]) >= zeitstempel(s["berechnet_am"]), "Prognose wurde vor ihrer Berechnung erfasst")
        if typ in {"anfangsbestand", "bestandsbewegung", "kurs"}:
            fordere(r["fachliche_zeit"]["art"] == "zeitpunkt", "Finanzpilot braucht einen Zeitpunkt mit bekannter Präzision")
        if typ == "eigentum" and r["art"] != "ruecknahme":
            fordere(r["fachliche_zeit"]["art"] == "intervall", "Eigentum braucht ein Gültigkeitsintervall")
            fordere(r["daten"]["einheit"] == BEGRIFF + "anteil" and Decimal(r["daten"]["menge"]) == 1, "Pilot unterstützt nur ausdrücklich vollständiges Eigentum")
        gruppen.setdefault(r["aussage_id"], []).append(r)
        if "ersetzt_id" in r:
            fordere(r["ersetzt_id"] in revisionen, "Fehlende Vorgängerrevision")
            p = revisionen[r["ersetzt_id"]]
            fordere(p["aussage_id"] == r["aussage_id"], "Korrektur wechselt die Aussageidentität")
            for feld in ("typ", "subjekt_id", "objekt_id", "szenario_id"):
                fordere(p.get(feld) == r.get(feld), "Korrektur wechselt den fachlichen Kontext")
            fordere(_ordnungswert(p) < _ordnungswert(r), "Rückdatierte oder ungeordnete Revision")
            if zeitstempel(p["erfasst_am"]) == zeitstempel(r["erfasst_am"]):
                fordere("folge" in p and "folge" in r, "Gleichzeitige Revisionen brauchen explizite Reihenfolge")
            nachfolger.setdefault(p["id"], []).append(r)
    for rs in gruppen.values():
        fordere(len([r for r in rs if "ersetzt_id" not in r]) == 1, "Parallele Wurzeln oder zyklische Revisionskette")
        fordere(all(len(nachfolger.get(r["id"], [])) <= 1 for r in rs), "Verzweigte Revisionskette")
        for r in rs:
            gesehen = set()
            while "ersetzt_id" in r:
                fordere(r["id"] not in gesehen, "Zyklische Revisionskette")
                gesehen.add(r["id"])
                r = revisionen[r["ersetzt_id"]]
    for s in szenarien.values():
        methode(s["modell_id"], s["modell_version"])
        zeitfenster(s["zielzeit"])
        berechnet = zeitstempel(s["berechnet_am"])
        fordere(zeitfenster(s["zielzeit"])[0] > berechnet, "Prognoseziel muss sicher nach der Berechnung liegen")
        fordere(len({revisionen[iri]["aussage_id"] for iri in s["eingaben"] if iri in revisionen}) == len(s["eingaben"]), "Szenario verwendet mehrere Revisionen derselben Aussage")
        for iri in s["eingaben"]:
            fordere(iri in revisionen, "Fehlende Szenarioeingabe")
            fordere(zeitstempel(revisionen[iri]["erfasst_am"]) <= berechnet, "Szenario verwendet noch unbekannte Eingabe")
            fordere(revisionen[iri]["aussageart"] != "prognose", "Verschachtelte Prognose im Pilot nicht unterstützt")
            fordere(revisionen[iri]["art"] != "ruecknahme" and revisionen[iri]["aussageart"] != "geplant", "Szenario verwendet Rücknahme oder geplanten Bestand als Tatsache")
        if s["art"] == "wertfaktor":
            fordere(set(s["parameter"]) == {"faktor", "perioden"}, "Wertfaktor braucht Faktor und Perioden")
            fordere(Decimal(s["parameter"]["faktor"]) >= 0, "Negativer Wertfaktor")
        else:
            fordere(set(s["parameter"]) == {"kurs", "waehrung"}, "Kursannahme braucht Kurs und Währung")
    _eigentum_pruefen(modell)


def _eigentum_pruefen(modell: dict) -> None:
    """Prüft konkurrierendes exklusives Eigentum für jeden bekannten Revisionsstand."""
    for wissen in {r["erfasst_am"] for r in modell["revisionen"]}:
        rs = [r for r in _aktive(modell, wissen) if r["typ"] == BEGRIFF + "eigentum" and r["aussageart"] not in {"prognose", "geplant", "empfehlung"}]
        for i, a in enumerate(rs):
            for b in rs[i + 1:]:
                if a["objekt_id"] != b["objekt_id"]:
                    continue
                az, bz = a["fachliche_zeit"], b["fachliche_zeit"]
                if any(g.get("status") == "unbekannt" for g in (az["beginn"], az["ende"], bz["beginn"], bz["ende"])):
                    continue
                if any("wert" in g and g["praezision"] != "sekunde" for g in (az["beginn"], az["ende"], bz["beginn"], bz["ende"])):
                    continue
                start = max(zeitfenster(az["beginn"])[0], zeitfenster(bz["beginn"])[0])
                enden = [zeitfenster(z["ende"])[0] for z in (az, bz) if "wert" in z["ende"]]
                fordere(enden and min(enden) <= start, "Überlappende exklusive Eigentumszuordnungen")


def auswahl(modell: dict, stichtag: dict, wissen: str, *, typ: str | None = None, szenario_id: str | None = None) -> dict:
    validiere(modell)
    zeitfenster(stichtag)
    ergebnis = {"treffer": [], "unbestimmt": []}
    for r in _aktive(modell, wissen):
        if typ and r["typ"] != BEGRIFF + typ:
            continue
        if szenario_id is None and r["aussageart"] in {"prognose", "geplant", "empfehlung"}:
            continue
        if szenario_id is not None and r.get("szenario_id") != szenario_id:
            continue
        trifft = gilt_am(r["fachliche_zeit"], stichtag)
        if trifft is not False:
            ergebnis["treffer" if trifft is True else "unbestimmt"].append(deepcopy(r))
    for key in ergebnis:
        ergebnis[key].sort(key=lambda r: r["id"])
    return ergebnis


@_mit_genauigkeit
def bestand(modell: dict, position_id: str, stichtag: dict, wissen: str) -> dict:
    validiere(modell)
    rs = [r for r in _aktive(modell, wissen) if r["subjekt_id"] == position_id and r["aussageart"] in {"belegt", "beobachtet"}]
    return _bestandsdaten(rs, stichtag)


def _bestandsdaten(rs: list[dict], stichtag: dict) -> dict:
    q0, q1 = zeitfenster(stichtag)
    starts = [r for r in rs if r["typ"] == BEGRIFF + "anfangsbestand"]
    if len(starts) != 1 or not starts[0]["daten"]["vollstaendig"]:
        return {"status": "offen", "grund": "Vollständiger Anfangsbestand fehlt"}
    start = starts[0]
    t0, t1 = zeitfenster(start["fachliche_zeit"])
    if t1 > q0 and (t0, t1) != (q0, q1):
        return {"status": "offen", "grund": "Anfangszeit nicht sicher vor dem Stichtag"}
    menge = Decimal(start["daten"]["menge"])
    eingaben = [start["id"]]
    for r in rs:
        if r["typ"] != BEGRIFF + "bestandsbewegung":
            continue
        a, b = zeitfenster(r["fachliche_zeit"])
        if a >= q1 and q0 != q1 or a > q0 and q0 == q1:
            continue
        if b > q0 and (a, b) != (q0, q1):
            return {"status": "offen", "grund": "Bewegung zeitlich unbestimmt"}
        if b < t0 or (b == t0 and a != b):
            continue
        if a < t1 or (a == t0 and a == b):
            return {"status": "offen", "grund": "Bewegung nicht sicher nach dem Anfangsstand"}
        if r["objekt_id"] != start["objekt_id"] or r["daten"]["einheit"] != start["daten"]["einheit"]:
            return {"status": "offen", "grund": "Bestands-/Stückbasis widersprüchlich"}
        menge += Decimal(r["daten"]["menge"])
        eingaben.append(r["id"])
    return {"status": "berechnet", "menge": format(menge, "f"), "instrument_id": start["objekt_id"], "einheit": start["daten"]["einheit"], "eingaben": sorted(eingaben)}


@_mit_genauigkeit
def bestandswert(modell: dict, position_id: str, stichtag: dict, wissen: str, waehrung: str, markt_id: str) -> dict:
    b = bestand(modell, position_id, stichtag, wissen)
    if b["status"] == "offen":
        return b
    q = auswahl(modell, stichtag, wissen, typ="kurs")
    unsichere_kurse = [r for r in q["unbestimmt"] if r["subjekt_id"] == b["instrument_id"] and r["daten"]["waehrung"] == waehrung and r["daten"]["markt_id"] == markt_id and r["daten"]["einheit"] == b["einheit"]]
    if unsichere_kurse:
        return {"status": "offen", "grund": "Zeitlich unbestimmte konkurrierende Kursbasis"}
    kurse = [r for r in q["treffer"] if r["subjekt_id"] == b["instrument_id"] and r["daten"]["waehrung"] == waehrung and r["daten"]["markt_id"] == markt_id and r["daten"]["einheit"] == b["einheit"]]
    if len(kurse) != 1:
        return {"status": "offen", "grund": "Kein eindeutiger passender Kurs"}
    kurs = kurse[0]
    return {"status": "berechnet", "betrag": format(Decimal(b["menge"]) * Decimal(kurs["daten"]["betrag"]), "f"), "waehrung": waehrung, "eingaben": sorted(b["eingaben"] + [kurs["id"]])}


@_mit_genauigkeit
def berechne_szenario(modell: dict, szenario_id: str) -> dict:
    validiere(modell)
    s = next((s for s in modell["szenarien"] if s["id"] == szenario_id), None)
    fordere(s is not None, "Szenario fehlt")
    eingaben = [r for r in modell["revisionen"] if r["id"] in s["eingaben"]]
    p = s["parameter"]
    if s["art"] == "wertfaktor":
        fordere(len(eingaben) == 1 and eingaben[0]["art"] == "bewertung", "Wertfaktor erwartet genau eine Bewertung")
        betrag = Decimal(eingaben[0]["daten"]["betrag"])
        for _ in range(p["perioden"]):
            betrag *= Decimal(p["faktor"])
        waehrung = eingaben[0]["daten"]["waehrung"]
    else:
        fordere(all(r["typ"] in {BEGRIFF + "anfangsbestand", BEGRIFF + "bestandsbewegung", BEGRIFF + "kurs"} for r in eingaben), "Kursannahme erwartet Bestandsdaten und optional eine Kursbasis")
        bewegungen = [r for r in eingaben if r["typ"] != BEGRIFF + "kurs"]
        starts = [r for r in bewegungen if r["typ"] == BEGRIFF + "anfangsbestand"]
        fordere(len(starts) == 1 and starts[0]["daten"]["vollstaendig"], "Szenario braucht vollständigen Anfangsbestand")
        fordere(len({(r["subjekt_id"], r["objekt_id"], r["daten"]["einheit"]) for r in bewegungen}) == 1, "Szenario mischt Bestandsbasen")
        for r in eingaben:
            if r["typ"] == BEGRIFF + "kurs":
                fordere(r["subjekt_id"] == starts[0]["objekt_id"] and r["daten"]["einheit"] == starts[0]["daten"]["einheit"] and r["daten"]["waehrung"] == p["waehrung"], "Szenario besitzt ungeeignete Kursbasis")
        basis = _bestandsdaten(bewegungen, {"wert": s["berechnet_am"], "praezision": "sekunde"})
        fordere(basis["status"] == "berechnet", "Szenariobestand ist zeitlich unbestimmt")
        betrag = Decimal(basis["menge"]) * Decimal(p["kurs"])
        waehrung = p["waehrung"]
    return {"szenario_id": s["id"], "betrag": format(betrag, "f"), "waehrung": waehrung, "zielzeit": deepcopy(s["zielzeit"]), "berechnet_am": s["berechnet_am"], "modell_id": s["modell_id"], "modell_version": s["modell_version"], "eingaben": sorted(s["eingaben"])}
