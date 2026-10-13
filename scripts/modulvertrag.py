# SPDX-License-Identifier: AGPL-3.0-or-later
"""Exakte Modul-, Profil-, Paket- und Übernahmebindung ohne Anbieterzugriff."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil

from jsonschema import Draft202012Validator, FormatChecker
import langcodes
from referencing import Registry, Resource

from scripts.modellvertrag import Modellfehler, SCHEMA, fordere

WURZEL = Path(__file__).resolve().parents[1]
PAKETPFAD = "pakete/0.1.0/paket.json"
METAPFAD = "vertraege/module/0.1.0/vertrag.schema.json"


def _paare(paare):
    objekt = {}
    for key, wert in paare:
        fordere(key not in objekt, "Doppelter JSON-Schlüssel")
        objekt[key] = wert
    return objekt


def lesen(pfad: Path):
    try:
        return json.loads(pfad.read_text(encoding="utf-8"), object_pairs_hook=_paare, parse_constant=lambda _: (_ for _ in ()).throw(Modellfehler("Nichtendliche JSON-Zahl")))
    except (OSError, ValueError) as exc:
        raise Modellfehler("Artefakt nicht lesbar: " + str(pfad)) from exc


def kanonisch(objekt) -> bytes:
    return json.dumps(objekt, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def pruefsumme(pfad: Path, art: str) -> str:
    fordere(art in {"json", "text"}, "Unbekannte Artefaktart")
    try:
        daten = kanonisch(lesen(pfad)) if art == "json" else pfad.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise Modellfehler("Artefakt nicht lesbar") from exc
    return hashlib.sha256(daten).hexdigest()


def sicherer_pfad(wurzel: Path, relativ: str) -> Path:
    fordere(isinstance(relativ, str) and relativ and "\\" not in relativ and ":" not in relativ, "Kein portabler relativer Pfad")
    teile = relativ.split("/")
    fordere(all(t not in {"", ".", "..", ".git", ".venv", ".aws", ".codex", ".agents", "out"} for t in teile), "Unzulässiger Artefaktpfad")
    fordere(not PurePosixPath(relativ).is_absolute(), "Absoluter Artefaktpfad")
    pfad = (wurzel / relativ).resolve()
    fordere(pfad.is_relative_to(wurzel.resolve()), "Artefakt verlässt Paketwurzel")
    return pfad


def _texte(objekt):
    if isinstance(objekt, dict):
        if "sprache" in objekt:
            fordere(langcodes.tag_is_valid(objekt["sprache"]), "Ungültiges Sprachkennzeichen im Manifest")
        for wert in objekt.values():
            _texte(wert)
    elif isinstance(objekt, list):
        for wert in objekt:
            _texte(wert)


@dataclass
class Paket:
    wurzel: Path
    pfad: Path
    manifest: dict
    module: dict
    profile: dict
    artefakte: dict
    begriffe: dict
    abhaengigkeiten: dict

    def artefakt(self, identitaet: str) -> Path:
        fordere(identitaet in self.artefakte, "Unbekanntes Artefakt")
        a = self.artefakte[identitaet]
        pfad = sicherer_pfad(self.wurzel, a["pfad"])
        fordere(pruefsumme(pfad, a["art"]) == a["sha256"], "Artefaktinhalt verändert: " + a["pfad"])
        return pfad


def pruefe_paket(wurzel: Path = WURZEL, paketpfad: str = PAKETPFAD) -> Paket:
    wurzel = wurzel.resolve()
    meta = lesen(wurzel / METAPFAD)
    Draft202012Validator.check_schema(meta)
    registry = Registry().with_resources([(SCHEMA["$id"], Resource.from_contents(SCHEMA)), (meta["$id"], Resource.from_contents(meta))])

    def form(objekt, art):
        validator = Draft202012Validator({"$ref": meta["$id"] + "#/$defs/" + art}, registry=registry, format_checker=FormatChecker())
        fehler = list(validator.iter_errors(objekt))
        fordere(not fehler, "Manifestvertrag verletzt: " + (fehler[0].message if fehler else ""))
        _texte(objekt)

    pfad = sicherer_pfad(wurzel, paketpfad)
    manifest = lesen(pfad)
    form(manifest, "paket")
    artefakte = {}
    pfade = set()
    for a in manifest["artefakte"]:
        fordere(a["id"] not in artefakte and a["pfad"].casefold() not in pfade, "Doppeltes Artefakt oder gleicher Dateipfad")
        ziel = sicherer_pfad(wurzel, a["pfad"])
        fordere(ziel != pfad and a["pfad"] != "uebernahme.json", "Prüfsummenschleife im Paket")
        fordere((ziel.suffix == ".json") == (a["art"] == "json"), "Artefaktart passt nicht zum Dateiformat")
        fordere(pruefsumme(ziel, a["art"]) == a["sha256"], "Artefaktinhalt verändert: " + a["pfad"])
        artefakte[a["id"]] = a
        pfade.add(a["pfad"].casefold())
    fordere(METAPFAD.casefold() in pfade and "modelle/kern/modell.schema.json" in pfade, "Metadaten- oder Kernvertrag nicht im Paket gebunden")

    def manifeste(feld, art):
        ergebnis = {}
        for verweis in manifest[feld]:
            fordere(verweis["artefakt_id"] in artefakte, "Manifestartefakt fehlt")
            a = artefakte[verweis["artefakt_id"]]
            fordere(a["art"] == "json", "Manifest muss JSON sein")
            objekt = lesen(sicherer_pfad(wurzel, a["pfad"]))
            form(objekt, art)
            fordere(objekt["id"] == verweis["id"] and objekt["version"] == verweis["version"], "Manifest-Version stimmt nicht mit Paketbindung überein")
            fordere(objekt["id"] not in ergebnis, "Mehrere Stände derselben Manifest-ID im Paket")
            ergebnis[objekt["id"]] = objekt
        return ergebnis

    module, profile = manifeste("module", "modul"), manifeste("profile", "profil")
    abhaengigkeiten, pfadmenge = {}, set()

    def abhaengig(modul_id):
        fordere(modul_id not in pfadmenge, "Zyklische Modulabhängigkeit")
        if modul_id in abhaengigkeiten:
            return abhaengigkeiten[modul_id]
        pfadmenge.add(modul_id)
        modul = module[modul_id]
        direkt = set()
        gesamt = {modul_id}
        for referenz in modul["abhaengigkeiten"]:
            identitaet = referenz["id"]
            fordere(identitaet not in direkt, "Doppelte Modulabhängigkeit")
            fordere(identitaet in module and module[identitaet]["version"] == referenz["version"], "Modulstand fehlt")
            direkt.add(identitaet)
            gesamt.update(abhaengig(identitaet))
        pfadmenge.remove(modul_id)
        abhaengigkeiten[modul_id] = gesamt
        return gesamt

    for modul_id in module:
        abhaengig(modul_id)
    begriffe = {}
    for modul_id, modul in module.items():
        fordere(set(modul["artefakt_ids"]) <= set(artefakte), "Modulartefakt fehlt")
        for begriff in modul["bereitstellungen"]:
            fordere(begriff["id"] not in begriffe, "Begriffsidentität wird überschrieben")
            begriffe[begriff["id"]] = (modul_id, begriff["art"])
    for modul_id, modul in module.items():
        for nutzung in modul["nutzungen"]:
            fordere(nutzung in begriffe and begriffe[nutzung][0] in abhaengigkeiten[modul_id], "Begriffsnutzung außerhalb der Modulabhängigkeiten")
    for profil in profile.values():
        ausgewaehlt = set()
        for referenz in profil["module"]:
            identitaet = referenz["id"]
            fordere(identitaet not in ausgewaehlt, "Mehrfache Modul-ID im Profil")
            fordere(identitaet in module and module[identitaet]["version"] == referenz["version"], "Profil-Modulstand fehlt")
            ausgewaehlt.add(identitaet)
        fordere(all(abhaengigkeiten[m] <= ausgewaehlt for m in ausgewaehlt), "Profil lässt transitive Abhängigkeit aus")
        for feld, art in (("schema_id", "schema"), ("abbildung_id", "abbildung")):
            identitaet = profil[feld]
            fordere(identitaet in begriffe and begriffe[identitaet][0] in ausgewaehlt and begriffe[identitaet][1] == art, "Profilvertrag nicht im gewählten Modulstand bereitgestellt")
        for feld, art in (("entitaetstypen", "entitaet"), ("aussagetypen", "aussage")):
            fordere(all(b in begriffe and begriffe[b][0] in ausgewaehlt and begriffe[b][1] == art for b in profil[feld]), "Profiltyp außerhalb der gewählten Module")
        fordere(profil["beispiel_id"] in artefakte and profil["erwartungen_id"] in artefakte, "Profilbeispiele fehlen")
    return Paket(wurzel, pfad, manifest, module, profile, artefakte, begriffe, abhaengigkeiten)


def uebernahme(paket: Paket, speicherziel: str) -> dict:
    fordere(speicherziel in {"github", "sharepoint", "s3"}, "Unbekanntes Speicherziel")
    return {"art": "uebernahme", "vertrag_version": "0.1.0", "paket_id": paket.manifest["id"], "paket_version": paket.manifest["version"], "paketpfad": paket.pfad.relative_to(paket.wurzel).as_posix(), "paket_sha256": pruefsumme(paket.pfad, "json"), "speicherziel": speicherziel}


def pruefe_uebernahme(paket: Paket, bindung: dict):
    fordere(bindung == uebernahme(paket, bindung.get("speicherziel")), "Übernahmebindung stimmt nicht mit Paket überein")


def vergleiche(paket: Paket, andere_bindung: dict) -> dict:
    fordere(andere_bindung.get("paket_id") == paket.manifest["id"], "Vergleich verschiedener Paketidentitäten")
    gleich = andere_bindung.get("paket_version") == paket.manifest["version"] and andere_bindung.get("paket_sha256") == pruefsumme(paket.pfad, "json")
    fordere(andere_bindung.get("paket_version") != paket.manifest["version"] or gleich, "Gleiche Versionsidentität mit abweichendem Paketinhalt")
    return {"status": "identisch" if gleich else "pruefung_erforderlich", "semantische_kompatibilitaet": "nicht_abgeleitet"}


def pruefe_fortschreibung(alte_wurzel: Path, alter_pfad: str, neu: Paket):
    """Veröffentlichte Manifeststände und ihre direkten Artefaktbindungen erhalten."""
    alt = lesen(sicherer_pfad(alte_wurzel, alter_pfad))
    fordere(alt["id"] == neu.manifest["id"], "Fortschreibung verschiedener Paketidentitäten")
    if alt["version"] == neu.manifest["version"]:
        fordere(kanonisch(alt) == kanonisch(neu.manifest), "Paketversion wird mit anderem Inhalt wiederverwendet")
    alte_artefakte = {a["id"]: a for a in alt["artefakte"]}
    for feld, neue_objekte in (("module", neu.module), ("profile", neu.profile)):
        for verweis in alt[feld]:
            a = alte_artefakte[verweis["artefakt_id"]]
            alter_manifestpfad = sicherer_pfad(alte_wurzel, a["pfad"])
            fordere(pruefsumme(alter_manifestpfad, a["art"]) == a["sha256"], "Veröffentlichter Manifeststand wurde verändert")
            if verweis["id"] not in neue_objekte or verweis["version"] != neue_objekte[verweis["id"]]["version"]:
                continue
            neues_verweis = next(v for v in neu.manifest[feld] if v["id"] == verweis["id"])
            neuer_hash = neu.artefakte[neues_verweis["artefakt_id"]]["sha256"]
            fordere(neuer_hash == a["sha256"], "Manifest-ID und Version werden für anderen Inhalt wiederverwendet")
            objekt = lesen(alter_manifestpfad)
            gebundene_ids = objekt["artefakt_ids"] if feld == "module" else [objekt["beispiel_id"], objekt["erwartungen_id"]]
            for identitaet in gebundene_ids:
                fordere(identitaet in neu.artefakte and identitaet in alte_artefakte and neu.artefakte[identitaet]["sha256"] == alte_artefakte[identitaet]["sha256"], "Artefaktänderung braucht einen neuen Manifeststand")


def exportiere(paket: Paket, ziel: Path, speicherziel: str) -> Path:
    ziel = ziel.resolve()
    fordere(not ziel.exists(), "Exportziel muss neu sein; bestehende Dateien werden nicht überschrieben")
    bindung = uebernahme(paket, speicherziel)
    # Erst alle Quellen und Pfade prüfen, dann die neue Ausgabe anlegen.
    quellen = [(paket.artefakt(a["id"]), a["pfad"]) for a in paket.manifest["artefakte"]]
    paketrelativ = paket.pfad.relative_to(paket.wurzel).as_posix()
    quellen.append((paket.pfad, paketrelativ))
    ziel.mkdir(parents=True)
    for quelle, relativ in quellen:
        datei = sicherer_pfad(ziel, relativ)
        datei.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(quelle, datei)
    (ziel / "uebernahme.json").write_bytes(kanonisch(bindung) + b"\n")
    kopie = pruefe_paket(ziel, paketrelativ)
    pruefe_uebernahme(kopie, lesen(ziel / "uebernahme.json"))
    return ziel
