# SPDX-License-Identifier: AGPL-3.0-or-later
"""Unabhängige Referenz- und Fehlerfälle zur synthetischen Erbausschlagung."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from rdflib import Graph, Literal, RDF, URIRef, XSD

from abbildungen.formate.erbausschlagung import EA, aus_rdf, nach_rdf
from scripts.erbausschlagung import pruefstand, validiere
from scripts.modellvertrag import Modellfehler, normalisiere
from scripts.pruefe_erbausschlagung import pruefe_erwartungen

WURZEL = Path(__file__).resolve().parents[1]
U = lambda name: "urn:beispiel:erbausschlagung:" + name
STICHTAG = {"wert": "2026-10-04T12:00:00Z", "praezision": "sekunde"}
WISSEN = "2026-10-06T18:00:00Z"


class Erbausschlagungspruefung(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ziel = WURZEL / "beispiele/synthetisch/erbausschlagung"
        cls.vorlage = json.loads((ziel / "faelle.json").read_text(encoding="utf-8"))
        cls.erwartungen = json.loads((ziel / "erwartungen.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.paket = deepcopy(self.vorlage)

    def fall(self, buchstabe):
        return next(f for f in self.paket["faelle"] if f["id"] == U("EA-" + buchstabe))

    def nachweis(self, name):
        return next(n for n in self.paket["nachweise"] if n["id"] == U(name))

    def abfrage(self, buchstabe="A", wissen=WISSEN):
        return pruefstand(self.paket, U("EA-" + buchstabe), STICHTAG, wissen)

    def test_quellszenarien_a_b_c_d_mit_unabhaengigen_erwartungen(self):
        pruefe_erwartungen(self.paket, self.erwartungen)
        for formatname in ("turtle", "json-ld"):
            with self.subTest(format=formatname):
                graph = nach_rdf(self.paket)
                rueckweg = aus_rdf(Graph().parse(data=graph.serialize(format=formatname), format=formatname))
                self.assertEqual(rueckweg, normalisiere(self.paket))
                pruefe_erwartungen(rueckweg, self.erwartungen)

    def test_versand_ist_kein_eingang_spaetere_erfassung_bleibt_getrennt(self):
        vorher = self.abfrage(wissen="2026-10-04T18:00:00Z")
        nachher = self.abfrage()
        self.assertEqual(vorher["personen"][0]["gerichtseingang"]["status"], "unbekannt")
        self.assertEqual(nachher["personen"][0]["gerichtseingang"]["nachweis_ids"], [U("A-EINGANG")])
        self.assertEqual(nachher["rechtliche_wirksamkeit"], "nicht_berechnet")
        self.assertEqual(self.nachweis("A-EINGANG")["zeit"]["wert"], "2026-10-03T10:00:00Z")

    def test_eingang_erst_ab_fachlichem_ereignis(self):
        for zeit, erwartet in [("2026-10-03T09:59:59Z", "unbekannt"), ("2026-10-03T10:00:00Z", "belegt")]:
            with self.subTest(zeit=zeit):
                ergebnis = pruefstand(self.paket, U("EA-A"), {"wert": zeit, "praezision": "sekunde"}, WISSEN)
                self.assertEqual(ergebnis["personen"][0]["gerichtseingang"]["status"], erwartet)

    def test_unscharfer_eingang_bleibt_unbestimmt(self):
        n = self.nachweis("A-EINGANG")
        n["zeit"] = {"wert": "2026-10-04", "praezision": "tag"}
        r = self.abfrage()["personen"][0]["gerichtseingang"]
        self.assertEqual(r["status"], "zeitlich_unbestimmt")
        self.assertEqual(r["nachweis_ids"], [])
        self.assertEqual(r["unbestimmte_nachweis_ids"], [U("A-EINGANG")])

    def test_ungepruefter_eingangsbeleg_ist_keine_bestaetigung(self):
        self.nachweis("A-EINGANG")["pruefstatus"] = "zu_pruefen"
        self.assertEqual(self.abfrage()["personen"][0]["gerichtseingang"]["status"], "unbekannt")

    def test_aushaendigung_ohne_nachkontrolle_ist_kein_eingang(self):
        r = self.abfrage("B")
        self.assertEqual(r["nachkontrolle_durch_notariat"], "nein")
        self.assertEqual(r["personen"][0]["gerichtseingang"]["status"], "unbekannt")
        self.fall("B")["nachkontrolle"] = "vereinbart"
        self.assertEqual(self.abfrage("B")["nachkontrolle_durch_notariat"], "ja")
        self.assertEqual(self.abfrage("B")["personen"][0]["gerichtseingang"]["status"], "unbekannt")

    def test_unbekannter_auftrag_oder_nachkontrolle_bleibt_unbekannt(self):
        self.fall("B")["nachkontrolle"] = "unbekannt"
        self.assertEqual(self.abfrage("B")["nachkontrolle_durch_notariat"], "unbekannt")
        self.fall("A")["vollzugsweg"] = "unbekannt"
        self.assertEqual(self.abfrage()["nachkontrolle_durch_notariat"], "unbekannt")

    def test_kind_ist_separate_person_ohne_abgeleitete_rechte(self):
        r = self.abfrage("C")
        self.assertEqual([p["person_id"] for p in r["personen"]], [U("C-KIND"), U("C-PERSON")])
        self.assertIn({"person_id": U("C-KIND"), "typ": "vertretung"}, r["offene_pruefungen"])
        self.assertIn({"person_id": U("C-KIND"), "typ": "genehmigung"}, r["offene_pruefungen"])
        self.assertEqual(r["erbenstellung"], "nicht_berechnet")
        self.assertEqual([b["typ"] for b in self.paket["beziehungen"]], ["eltern_kind"])
        vor = deepcopy(self.paket)
        self.abfrage("C")
        self.assertEqual(self.paket, vor)

    def test_unbekannte_kenntnis_wird_nicht_aus_tod_abgeleitet(self):
        self.nachweis("A-N-A-PERSON-kenntnis_berufungsgrund")["zeit"] = {"status": "unbekannt"}
        r = self.abfrage()["personen"][0]
        self.assertEqual(r["kenntnis_erbfall"]["status"], "belegt")
        self.assertEqual(r["kenntnis_berufungsgrund"]["status"], "zeitlich_unbestimmt")
        self.paket["nachweise"] = [n for n in self.paket["nachweise"] if n["typ"] not in {"kenntnis_erbfall", "kenntnis_berufungsgrund"}]
        self.assertEqual(self.abfrage()["personen"][0]["kenntnis_erbfall"]["status"], "unbekannt")

    def test_risiko_erzeugt_keine_annahme_oder_wirksamkeit(self):
        r = self.abfrage("D")
        self.assertEqual(r["annahmerisiko"], "zu_pruefen")
        self.assertEqual(r["offene_pruefungen"], [{"person_id": U("D-PERSON"), "typ": "annahmerisiko"}])
        self.assertEqual(r["rechtliche_wirksamkeit"], "nicht_berechnet")

    def test_fehlende_und_spaetere_pruefstaende_bleiben_offen(self):
        fall = self.fall("A")
        fall["pruefungen"] = [p for p in fall["pruefungen"] if p["typ"] != "frist"]
        next(p for p in fall["pruefungen"] if p["typ"] == "form")["erfasst_am"] = "2026-10-07T09:00:00Z"
        r = self.abfrage()
        self.assertEqual(r["offene_pruefungen"], [{"person_id": U("A-PERSON"), "typ": "frist"}, {"person_id": U("A-PERSON"), "typ": "form"}])

    def test_falsche_referenzen_rollen_und_selbstbeziehung_abgewiesen(self):
        for variante in ("quelle", "person", "fall", "rolle", "beziehung", "nachweisrolle"):
            with self.subTest(variante=variante):
                self.paket = deepcopy(self.vorlage)
                if variante == "quelle": self.nachweis("A-EINGANG")["quelle_id"] = U("FEHLT")
                if variante == "person": self.fall("A")["betroffene_person_ids"].append(U("FEHLT"))
                if variante == "fall": self.nachweis("A-EINGANG")["fall_id"] = U("FEHLT")
                if variante == "rolle": self.fall("A")["erblasser_id"] = U("A-PERSON")
                if variante == "beziehung": self.paket["beziehungen"][0]["objekt_id"] = U("C-PERSON")
                if variante == "nachweisrolle": self.nachweis("A-EINGANG")["person_id"] = U("B-PERSON")
                with self.assertRaises(Modellfehler): validiere(self.paket)

    def test_doppelte_identitaet_und_widerspruechlicher_pruefstand_abgewiesen(self):
        self.paket["quellen"][0]["id"] = self.paket["personen"][0]["id"]
        with self.assertRaises(Modellfehler): validiere(self.paket)
        self.paket = deepcopy(self.vorlage)
        p = deepcopy(self.fall("A")["pruefungen"][0])
        p.update(id=U("DUPLIKAT"), status="unbekannt")
        self.fall("A")["pruefungen"].append(p)
        with self.assertRaises(Modellfehler): validiere(self.paket)

    def test_ungueltige_zeit_und_zukunftsbeleg_abgewiesen(self):
        for zeit in ({"wert": "2026-02-30", "praezision": "tag"}, {"wert": "2026-10-07T09:00:00Z", "praezision": "sekunde"}, {"status": "unbekannt"}):
            with self.subTest(zeit=zeit):
                self.paket = deepcopy(self.vorlage)
                self.nachweis("A-EINGANG")["zeit"] = zeit
                with self.assertRaises(Modellfehler): validiere(self.paket)

    def test_sprachkennzeichen_richtung_und_mehrfachwerte_im_rdf(self):
        texte = self.paket["personen"][0]["bezeichnungen"]
        texte.append({"wert": "Synthetischer Text für Sprachparameter", "sprache": "tr"})
        texte.append({"wert": "Synthetischer Text mit Richtungsparameter", "sprache": "ar", "richtung": "rtl"})
        graph = nach_rdf(self.paket)
        self.assertTrue(any(o.language == "tr" for o in graph.objects(None, RDF.value)))
        self.assertEqual(aus_rdf(graph), normalisiere(self.paket))
        del texte[0]["sprache"]
        with self.assertRaises(Modellfehler): validiere(self.paket)

    def test_unbekanntes_sprachkennzeichen_und_textduplikat_abgewiesen(self):
        self.paket["personen"][0]["bezeichnungen"][0]["sprache"] = "ungueltig"
        with self.assertRaises(Modellfehler): validiere(self.paket)
        self.paket = deepcopy(self.vorlage)
        self.paket["personen"][0]["bezeichnungen"].append(deepcopy(self.paket["personen"][0]["bezeichnungen"][0]))
        with self.assertRaises(Modellfehler): validiere(self.paket)

    def test_fremde_akten_und_entscheidungsfelder_abgewiesen(self):
        for feld, wert in [("aktenzeichen", "Synthetischer Fremdwert"), ("wirksam", True), ("fristende", "2026-10-10")]:
            with self.subTest(feld=feld):
                self.paket = deepcopy(self.vorlage)
                self.fall("A")[feld] = wert
                with self.assertRaises(Modellfehler): validiere(self.paket)

    def test_rdf_fremde_unverbundene_tripeln_und_literalreferenz_abgewiesen(self):
        for variante in ("fremd", "unverbunden", "referenz", "mehrfach"):
            with self.subTest(variante=variante):
                graph = nach_rdf(self.paket)
                if variante == "fremd": graph.add((URIRef(U("PAKET")), URIRef("urn:fremd:feld"), Literal("Wert")))
                if variante == "unverbunden": graph.add((URIRef("urn:fremd:objekt"), RDF.value, Literal("Wert")))
                if variante == "referenz":
                    graph.set((URIRef(U("A-EINGANG")), EA.person_id, Literal(U("A-PERSON"))))
                if variante == "mehrfach": graph.add((URIRef(U("EA-A")), EA.vollzugsweg, Literal("unbekannt", datatype=XSD.string)))
                with self.assertRaises(Modellfehler): aus_rdf(graph)


if __name__ == "__main__":
    unittest.main()
