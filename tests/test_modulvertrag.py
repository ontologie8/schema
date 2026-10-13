# SPDX-License-Identifier: AGPL-3.0-or-later
"""Unabhängige Paket-, Versions-, Profil- und Übernahmefehler prüfen."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from scripts.erzeuge_paket import erzeuge
from scripts.modellvertrag import Modellfehler
from scripts.modulvertrag import PAKETPFAD, WURZEL, exportiere, lesen, pruefe_fortschreibung, pruefe_paket, pruefe_uebernahme, pruefsumme, uebernahme, vergleiche
from scripts.profilpruefung import pruefe_modellfragen, pruefe_profil, validiere_daten

M = "urn:ontologie8:modul:"
P = "urn:ontologie8:profil:"


class Modulvertragspruefung(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = pruefe_paket()
        cls.vorbereitung = TemporaryDirectory(prefix="modulvertrag-vorlage-")
        cls.addClassCleanup(cls.vorbereitung.cleanup)
        cls.probe = Path(cls.vorbereitung.name) / "vorlage"
        exportiere(cls.original, cls.probe, "github")

    def setUp(self):
        self.tmp = TemporaryDirectory(prefix="modulvertrag-")
        self.addCleanup(self.tmp.cleanup)
        self.wurzel = Path(self.tmp.name) / "kopie"
        shutil.copytree(self.probe, self.wurzel)

    def schreiben(self, relativ, objekt):
        (self.wurzel / relativ).write_text(json.dumps(objekt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def aendern(self, relativ, funktion):
        objekt = lesen(self.wurzel / relativ)
        funktion(objekt)
        self.schreiben(relativ, objekt)

    def neu_binden(self):
        manifest = lesen(self.wurzel / PAKETPFAD)
        for a in manifest["artefakte"]:
            a["sha256"] = pruefsumme(self.wurzel / a["pfad"], a["art"])
        self.schreiben(PAKETPFAD, manifest)

    def test_fuenf_module_und_fuenf_profile_erhalten_erwartungen(self):
        paket = pruefe_paket(self.wurzel)
        self.assertEqual(set(paket.module), {M + n for n in ("kern", "fahrzeuge", "finanzen", "bekleidung", "recht")})
        self.assertEqual(len(paket.begriffe), 29)
        self.assertEqual(set(paket.profile), {P + n for n in ("auto", "aktien", "bekleidung", "p0-gesamt", "erbausschlagung")})
        for profil in paket.profile:
            self.assertEqual(pruefe_profil(paket, profil)["rueckwege"], ["turtle", "json-ld"])

    def test_exportierte_cli_laeuft_ohne_ursprungsrepository(self):
        ergebnis = subprocess.run([sys.executable, "-X", "utf8", str(self.wurzel / "scripts/pruefe_module.py")], cwd=self.wurzel, capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr + ergebnis.stdout)
        self.assertEqual(json.loads(ergebnis.stdout)["module"], 5)

    def test_drei_speicherziele_binden_denselben_paketstand(self):
        summen = set()
        for ziel in ("github", "sharepoint", "s3"):
            bindung = uebernahme(self.original, ziel)
            pruefe_uebernahme(self.original, bindung)
            summen.add(bindung["paket_sha256"])
        self.assertEqual(len(summen), 1)

    def test_falsche_uebernahme_und_unbekanntes_ziel_abgewiesen(self):
        for feld, wert in (("paket_version", "0.2.0"), ("paket_sha256", "0" * 64), ("paket_id", "urn:fremd:paket"), ("speicherziel", "unbekannt")):
            with self.subTest(feld=feld):
                bindung = uebernahme(self.original, "github")
                bindung[feld] = wert
                with self.assertRaises(Modellfehler): pruefe_uebernahme(self.original, bindung)

    def test_integritaetsfehler_abgewiesen(self):
        pfad = self.wurzel / "scripts/modellvertrag.py"
        pfad.write_text(pfad.read_text(encoding="utf-8") + "\n# Synthetische Manipulation\n", encoding="utf-8")
        with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)

    def test_json_format_und_zeilenenden_aendern_keine_identitaet(self):
        jsonpfad = self.wurzel / "beispiele/synthetisch/module/auto.json"
        vorher = pruefsumme(jsonpfad, "json")
        jsonpfad.write_text(json.dumps(lesen(jsonpfad), sort_keys=True), encoding="utf-8")
        self.assertEqual(pruefsumme(jsonpfad, "json"), vorher)
        textpfad = self.wurzel / "requirements.txt"
        vorher = pruefsumme(textpfad, "text")
        textpfad.write_bytes(textpfad.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        self.assertEqual(pruefsumme(textpfad, "text"), vorher)
        pruefe_paket(self.wurzel)

    def test_arrayreihenfolge_und_doppelte_jsonschluessel(self):
        pfad = self.wurzel / "beispiele/synthetisch/module/auto.json"
        vorher = pruefsumme(pfad, "json")
        self.aendern("beispiele/synthetisch/module/auto.json", lambda d: d["revisionen"].reverse())
        self.assertNotEqual(pruefsumme(pfad, "json"), vorher)
        pfad.write_text('{"id":"urn:beispiel:a","id":"urn:beispiel:b"}', encoding="utf-8")
        with self.assertRaises(Modellfehler): lesen(pfad)

    def test_exakte_versionsbindung_statt_bereich(self):
        for version in ("0.3.0", "latest", "^0.2.0", "0.2.0-beta", "00.2.0"):
            with self.subTest(version=version):
                self.schreiben("modelle/fachmodule/fahrzeuge/0.1.0/modul.json", deepcopy(self.original.module[M + "fahrzeuge"]))
                self.aendern("modelle/fachmodule/fahrzeuge/0.1.0/modul.json", lambda m: m["abhaengigkeiten"][0].update(version=version))
                self.neu_binden()
                with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)

    def test_zyklus_und_fehlende_abhaengigkeit_abgewiesen(self):
        self.aendern("modelle/kern/0.2.0/modul.json", lambda m: m["abhaengigkeiten"].append({"id": M + "finanzen", "version": "0.2.0"}))
        self.neu_binden()
        with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)
        self.schreiben("modelle/kern/0.2.0/modul.json", deepcopy(self.original.module[M + "kern"]))
        self.aendern("modelle/fachmodule/fahrzeuge/0.1.0/modul.json", lambda m: m["abhaengigkeiten"][0].update(id=M + "fehlt"))
        self.neu_binden()
        with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)

    def test_profil_muss_abhaengigkeiten_vollstaendig_waehlen(self):
        self.aendern("profile/anwendungsfaelle/versioniert/0.1.0/auto.json", lambda p: p.update(module=[p["module"][1]]))
        self.neu_binden()
        with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)

    def test_begriffsueberschreibung_und_fremde_nutzung_abgewiesen(self):
        self.aendern("modelle/fachmodule/fahrzeuge/0.1.0/modul.json", lambda m: m["bereitstellungen"].append(deepcopy(self.original.module[M + "kern"]["bereitstellungen"][0])))
        self.neu_binden()
        with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)
        self.schreiben("modelle/fachmodule/fahrzeuge/0.1.0/modul.json", deepcopy(self.original.module[M + "fahrzeuge"]))
        self.aendern("modelle/fachmodule/fahrzeuge/0.1.0/modul.json", lambda m: m["nutzungen"].append("urn:ontologie8:begriff:position"))
        self.neu_binden()
        with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)

    def test_aktienposition_nicht_im_autoprofil_zugelassen(self):
        paket = pruefe_paket(self.wurzel)
        aktien = lesen(paket.artefakt(paket.profile[P + "aktien"]["beispiel_id"]))
        with self.assertRaises(Modellfehler): validiere_daten(paket, P + "auto", aktien)

    def test_fachfragen_erhalten_die_dezimalbedeutung(self):
        profil = self.original.profile[P + "auto"]
        daten = lesen(self.original.artefakt(profil["beispiel_id"]))
        next(r for r in daten["revisionen"] if r["id"] == "urn:beispiel:K-1-R1")["daten"]["betrag"] = "30000.000"
        erwartungen = lesen(self.original.artefakt(profil["erwartungen_id"]))
        pruefe_modellfragen(daten, erwartungen)

    def test_unbekanntes_profil_und_erwartungsvertrag_abgewiesen(self):
        paket = pruefe_paket(self.wurzel)
        with self.assertRaises(Modellfehler): pruefe_profil(paket, P + "fehlt")
        paket.profile[P + "auto"]["erwartungsvertrag_id"] = "urn:fremd:erwartung"
        with self.assertRaises(Modellfehler): pruefe_profil(paket, P + "auto")

    def test_pfadueberschreitung_und_pruefsummenschleife_abgewiesen(self):
        manifest = lesen(self.wurzel / PAKETPFAD)
        for pfad in ("../fremd.json", "C:/fremd.json", "/fremd.json", ".git/config", ".GiT/config", "NUL.json", "ordner./datei.json", "datei?.json", "datei.json ", "modelle\\kern\\modell.schema.json", PAKETPFAD):
            with self.subTest(pfad=pfad):
                variante = deepcopy(manifest)
                variante["artefakte"][0]["pfad"] = pfad
                self.schreiben(PAKETPFAD, variante)
                with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)

    def test_mehrfache_module_und_artfremde_profiltypen_abgewiesen(self):
        self.aendern(PAKETPFAD, lambda p: p["module"].append(deepcopy(p["module"][0])))
        with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)
        self.schreiben(PAKETPFAD, deepcopy(self.original.manifest))
        self.aendern("profile/anwendungsfaelle/versioniert/0.1.0/auto.json", lambda p: p["entitaetstypen"].append("urn:ontologie8:begriff:kauf"))
        self.neu_binden()
        with self.assertRaises(Modellfehler): pruefe_paket(self.wurzel)

    def test_neue_optionale_eigenschaft_nicht_automatisch_kompatibel(self):
        paket = pruefe_paket(self.wurzel)
        daten = lesen(paket.artefakt(paket.profile[P + "auto"]["beispiel_id"]))
        daten["neue_optionale_eigenschaft"] = "Synthetischer Wert"
        with self.assertRaises(Modellfehler): validiere_daten(paket, P + "auto", daten)
        bindung = uebernahme(paket, "github")
        bindung["paket_version"] = "0.2.0"
        self.assertEqual(vergleiche(paket, bindung), {"status": "pruefung_erforderlich", "semantische_kompatibilitaet": "nicht_abgeleitet"})

    def test_gleiche_version_mit_anderem_inhalt_ist_identitaetsverletzung(self):
        bindung = uebernahme(self.original, "github")
        self.assertEqual(vergleiche(self.original, bindung)["status"], "identisch")
        bindung["paket_sha256"] = "0" * 64
        with self.assertRaises(Modellfehler): vergleiche(self.original, bindung)

    def test_paketgenerator_ueberschreibt_nichts_und_arbeitet_isoliert(self):
        with self.assertRaises(Modellfehler): erzeuge(self.wurzel, "register/paketentwurf.json", PAKETPFAD, "0.1.0")
        self.assertFalse((self.wurzel / "pakete/0.0.9/paket.json").exists())
        with self.assertRaises(Modellfehler): erzeuge(self.wurzel, "register/paketentwurf.json", "pakete/0.0.9/paket.json", "0.0.9")
        self.assertFalse((self.wurzel / "pakete/0.0.9/paket.json").exists())
        manifest = erzeuge(self.wurzel, "register/paketentwurf.json", "pakete/0.2.0/paket.json", "0.2.0")
        self.assertEqual(manifest["version"], "0.2.0")
        pruefe_paket(self.wurzel, "pakete/0.2.0/paket.json")

    def test_artefaktaenderung_erfordert_neuen_modulstand(self):
        pfad = self.wurzel / "scripts/modellvertrag.py"
        pfad.write_text(pfad.read_text(encoding="utf-8") + "\n# Synthetische Änderung\n", encoding="utf-8")
        self.neu_binden()
        self.aendern(PAKETPFAD, lambda p: p.update(version="0.2.0"))
        neu = pruefe_paket(self.wurzel)
        with self.assertRaises(Modellfehler): pruefe_fortschreibung(WURZEL, PAKETPFAD, neu)

    def test_neuer_paketstand_wird_in_portabler_kopie_aktiv_gewaehlt(self):
        erzeuge(self.wurzel, "register/paketentwurf.json", "pakete/0.2.0/paket.json", "0.2.0")
        neu = pruefe_paket(self.wurzel, "pakete/0.2.0/paket.json")
        ziel = Path(self.tmp.name) / "neuer-export"
        exportiere(neu, ziel, "sharepoint")
        ergebnis = subprocess.run([sys.executable, "-X", "utf8", str(ziel / "scripts/pruefe_module.py")], cwd=ziel, capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(ergebnis.returncode, 0, ergebnis.stderr + ergebnis.stdout)
        self.assertEqual(json.loads(ergebnis.stdout)["paket_version"], "0.2.0")
        self.assertEqual(json.loads(ergebnis.stdout)["uebernahme"]["speicherziel"], "sharepoint")

    def test_cli_meldet_abweichenden_stand_als_offen(self):
        bindung = uebernahme(self.original, "github")
        bindung["paket_version"] = "0.2.0"
        self.schreiben("vergleich.json", bindung)
        ergebnis = subprocess.run([sys.executable, "-X", "utf8", str(self.wurzel / "scripts/pruefe_module.py"), "--profil", P + "auto", "--vergleich", "vergleich.json"], cwd=self.wurzel, capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(ergebnis.returncode, 2, ergebnis.stderr + ergebnis.stdout)
        self.assertEqual(json.loads(ergebnis.stdout)["status"], "PRUEFUNG_ERFORDERLICH")

    def test_bestehendes_exportziel_wird_nicht_ueberschrieben(self):
        with self.assertRaises(Modellfehler): exportiere(self.original, self.wurzel, "s3")
        self.assertEqual(lesen(self.wurzel / "uebernahme.json")["speicherziel"], "github")


if __name__ == "__main__":
    unittest.main()
