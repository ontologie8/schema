# SPDX-License-Identifier: AGPL-3.0-or-later
"""Unabhängige Erwartungen für Modellfragen, Historie und RDF-Rückweg."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import unittest

from rdflib import BNode, Graph, Literal, RDF, URIRef, XSD

from abbildungen.formate.rdf import KERN, aus_rdf, nach_rdf
from scripts.modellvertrag import BEGRIFF, Modellfehler, auswahl, berechne_szenario, bestand, bestandswert, gilt_am, normalisiere, validiere

WURZEL = Path(__file__).resolve().parents[1]
U = lambda name: "urn:beispiel:" + name


def punkt(wert, praezision="tag"):
    return {"art": "zeitpunkt", "wert": wert, "praezision": praezision}


class Pilotpruefung(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vorlage = json.loads((WURZEL / "beispiele/synthetisch/p0-pilot.json").read_text(encoding="utf-8"))
        cls.erwartungen = json.loads((WURZEL / "beispiele/synthetisch/p0-erwartungen.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.modell = deepcopy(self.vorlage)

    def revision(self, name):
        return next(r for r in self.modell["revisionen"] if r["id"] == U(name))

    def beide_formate(self):
        yield self.modell
        graph = nach_rdf(self.modell)
        yield aus_rdf(Graph().parse(data=graph.serialize(format="turtle"), format="turtle"))

    def test_zf_01_02_06_kaufpreisrevision(self):
        for modell in self.beide_formate():
            for erwartet in self.erwartungen["kaufpreis"]:
                with self.subTest(wissen=erwartet["wissen"]):
                    rs = auswahl(modell, punkt("2024-03-10T10:00:00Z", "sekunde"), erwartet["wissen"], typ="kauf")["treffer"]
                    self.assertEqual(len(rs), 1)
                    self.assertEqual(rs[0]["id"], erwartet["revision"])
                    self.assertEqual(Decimal(rs[0]["daten"]["betrag"]), Decimal(erwartet["betrag"]))

    def test_zf_03_04_05_eigentum_nach_wissensstand(self):
        for modell in self.beide_formate():
            for erwartet in self.erwartungen["eigentum"]:
                with self.subTest(stichtag=erwartet["stichtag"], wissen=erwartet["wissen"]):
                    rs = auswahl(modell, punkt(erwartet["stichtag"], "sekunde"), erwartet["wissen"], typ="eigentum")["treffer"]
                    self.assertEqual([r["subjekt_id"] for r in rs], [erwartet["person"]])

    def test_fehlende_kenntnis_bleibt_unbekannt(self):
        r = auswahl(self.modell, punkt("2024-03-10T10:00:00Z", "sekunde"), "2024-03-15T00:00:00Z", typ="kauf")
        self.assertEqual(r, {"treffer": [], "unbestimmt": []})

    def test_zf_07_08_konkurrierende_quellen(self):
        for modell in self.beide_formate():
            rs = auswahl(modell, punkt("2026-06-01"), "2026-06-06T00:00:00Z", typ="bewertung")["treffer"]
            auto = [r for r in rs if r["subjekt_id"] == U("AUTO-1")]
            self.assertEqual(sorted(r["daten"]["betrag"] for r in auto), self.erwartungen["bewertungen"])
            self.assertEqual({r["quelle_id"] for r in auto}, {U("Q-A"), U("Q-B")})

    def test_zf_09_10_13_szenarien_ohne_historienaenderung(self):
        for modell in self.beide_formate():
            vorher = deepcopy(modell)
            for s_id, betrag in self.erwartungen["szenarien"].items():
                ergebnis = berechne_szenario(modell, s_id)
                self.assertEqual(Decimal(ergebnis["betrag"]), Decimal(betrag))
                self.assertEqual(ergebnis["zielzeit"], {"wert": "2028-06-01", "praezision": "tag"})
            self.assertEqual(modell, vorher)
            self.assertEqual(auswahl(modell, punkt("2028-06-01"), "2026-09-01T00:00:00Z", typ="bewertung")["treffer"], [])
            rs = auswahl(modell, punkt("2028-06-01"), "2026-09-01T00:00:00Z", typ="bewertung", szenario_id=U("S-A"))["treffer"]
            self.assertEqual([Decimal(r["daten"]["betrag"]) for r in rs], [Decimal("17820")])

    def test_zf_11_keine_automatische_fortschreibung(self):
        rs = auswahl(self.modell, punkt("2026-06-02"), "2026-06-06T00:00:00Z", typ="bewertung")
        self.assertEqual(rs, {"treffer": [], "unbestimmt": []})

    def test_zf_12_bestand_und_wert(self):
        for modell in self.beide_formate():
            b = bestand(modell, U("POSITION-1"), punkt("2026-06-01"), "2026-06-06T00:00:00Z")
            self.assertEqual(Decimal(b["menge"]), Decimal(self.erwartungen["bestand"]))
            wert = bestandswert(modell, U("POSITION-1"), punkt("2026-06-01"), "2026-06-06T00:00:00Z", "EUR", U("MARKT-1"))
            self.assertEqual(Decimal(wert["betrag"]), Decimal(self.erwartungen["bestandswert"]))
            self.assertEqual(wert["waehrung"], "EUR")

    def test_zf_14_fehlender_kurs(self):
        self.modell["szenarien"] = []
        self.modell["revisionen"] = [r for r in self.modell["revisionen"] if r["id"] != U("C-4-R1") and r["aussageart"] != "prognose"]
        r = bestandswert(self.modell, U("POSITION-1"), punkt("2026-06-01"), "2026-06-06T00:00:00Z", "EUR", U("MARKT-1"))
        self.assertEqual(r["status"], "offen")
        self.assertNotIn("betrag", r)

    def test_zf_15_waehrung_und_marktbasis(self):
        for waehrung, markt in [("USD", U("MARKT-1")), ("EUR", U("MARKT-2"))]:
            r = bestandswert(self.modell, U("POSITION-1"), punkt("2026-06-01"), "2026-06-06T00:00:00Z", waehrung, markt)
            self.assertEqual(r["status"], "offen")

    def test_zf_16_separater_splitfall(self):
        self.modell["szenarien"] = []
        self.modell["revisionen"] = [r for r in self.modell["revisionen"] if r["id"] in {U("C-0-R1"), U("C-1-R1"), U("C-2-R1"), U("C-4-R1")}]
        self.revision("C-2-R1")["daten"]["menge"] = "10"
        self.revision("C-2-R1")["daten"].update(anlass=BEGRIFF + "split", betrag="0")
        self.revision("C-4-R1")["daten"]["betrag"] = "50"
        b = bestand(self.modell, U("POSITION-1"), punkt("2026-06-01"), "2026-06-06T00:00:00Z")
        r = bestandswert(self.modell, U("POSITION-1"), punkt("2026-06-01"), "2026-06-06T00:00:00Z", "EUR", U("MARKT-1"))
        self.assertEqual(Decimal(b["menge"]), Decimal(self.erwartungen["split"]["menge"]))
        self.assertEqual(Decimal(r["betrag"]), Decimal(self.erwartungen["split"]["betrag"]))

    def test_zf_17_18_19_kleidung_zustand_empfehlung(self):
        for modell in self.beide_formate():
            nach_id = {r["id"]: r for r in modell["revisionen"]}
            self.assertEqual(nach_id[U("D-1-R1")]["daten"]["betrag"], self.erwartungen["kleidung"]["kaufpreis"])
            self.assertEqual(nach_id[U("D-5-R1")]["daten"]["betrag"], self.erwartungen["kleidung"]["wiederverkaufswert"])
            self.assertEqual(nach_id[U("D-3-R1")]["daten"], {})
            self.assertEqual(nach_id[U("D-4-R1")]["daten"]["zustand"], BEGRIFF + "repariert")
            self.assertEqual(nach_id[U("D-6-R1")]["eingabe_ids"], [U("D-4-R1")])
            self.assertEqual(auswahl(modell, punkt("2026-06-01"), "2026-06-06T00:00:00Z", typ="stilempfehlung")["treffer"], [])

    def test_zf_20_sprachwerte_und_richtung(self):
        texte = self.modell["entitaeten"][0]["bezeichnungen"]
        texte.extend([
            {"wert": "Synthetischer Text für einen Sprachparameter", "sprache": "tr"},
            {"wert": "Weiterer synthetischer Text für einen Sprachparameter", "sprache": "en"},
            {"wert": "Synthetischer Text mit Richtungsparameter", "sprache": "ar", "richtung": "rtl"},
            {"wert": "Synthetischer regionaler Text", "sprache": "de-AT"}
        ])
        g = nach_rdf(self.modell)
        sprachen = {o.language for o in g.objects(None, RDF.value)}
        self.assertTrue({"de", "tr", "en", "ar", "de-at"}.issubset(sprachen))
        self.assertEqual(aus_rdf(g), normalisiere(self.modell))

    def test_zf_21_ungueltige_intervalle(self):
        for grenze in ["2024-03-10T10:00:00Z", "2024-03-09T10:00:00Z"]:
            m = deepcopy(self.modell)
            next(r for r in m["revisionen"] if r["id"] == U("E-A-R1"))["fachliche_zeit"]["ende"] = {"wert": grenze, "praezision": "sekunde"}
            with self.assertRaises(Modellfehler):
                validiere(m)

    def test_zf_22_monat_unbestimmt(self):
        zeit = punkt("2026-04", "monat")
        self.assertIsNone(gilt_am(zeit, punkt("2026-04-15")))
        self.assertFalse(gilt_am(zeit, punkt("2026-05-01")))

    def test_zf_23_unbekannte_grenze(self):
        self.revision("E-A-R1")["fachliche_zeit"]["beginn"] = {"status": "unbekannt"}
        r = auswahl(self.modell, punkt("2024-03-10T10:00:00Z", "sekunde"), "2024-03-25T00:00:00Z", typ="eigentum")
        self.assertEqual(r["treffer"], [])
        self.assertEqual([r["id"] for r in r["unbestimmt"]], [U("E-A-R1")])

    def test_zf_24_zyklus_und_verzweigung(self):
        m = deepcopy(self.modell)
        next(r for r in m["revisionen"] if r["id"] == U("K-1-R1"))["ersetzt_id"] = U("K-1-R2")
        with self.assertRaises(Modellfehler):
            validiere(m)
        kopie = deepcopy(self.revision("K-1-R2"))
        kopie.update(id=U("K-1-R3"), erfasst_am="2024-04-02T09:00:00Z")
        self.modell["revisionen"].append(kopie)
        with self.assertRaises(Modellfehler):
            validiere(self.modell)

    def test_zf_25_exklusives_eigentum(self):
        self.revision("E-B-R1")["fachliche_zeit"]["beginn"]["wert"] = "2026-07-01T12:00:00Z"
        with self.assertRaisesRegex(Modellfehler, "Eigentumszuordnungen"):
            validiere(self.modell)

    def test_zf_26_zukuenftiger_plan(self):
        r = self.revision("D-1-R1")
        r.update(aussageart="geplant", fachliche_zeit=punkt("2028-09-01"))
        validiere(self.modell)
        rs = auswahl(self.modell, punkt("2028-09-01"), "2026-09-01T00:00:00Z", typ="kauf")["treffer"]
        self.assertEqual(rs, [])
        self.assertEqual(r["aussageart"], "geplant")

    def test_zf_27_quellzeit_kein_systemwissen(self):
        self.revision("D-1-R1").update(quellzeit="2024-01-01T00:00:00Z", erfasst_am="2026-07-01T10:00:00Z")
        rs = auswahl(self.modell, punkt("2025-05-01"), "2026-06-01T00:00:00Z", typ="kauf")["treffer"]
        self.assertEqual(rs, [])

    def test_ruecknahme_bleibt_historisch(self):
        r = deepcopy(self.revision("D-3-R1"))
        r.update(id=U("D-3-R2"), art="ruecknahme", ersetzt_id=U("D-3-R1"), erfasst_am="2026-05-01T10:00:00Z")
        self.modell["revisionen"].append(r)
        vorher = auswahl(self.modell, punkt("2026-04-10"), "2026-04-20T00:00:00Z", typ="reparatur")
        danach = auswahl(self.modell, punkt("2026-04-10"), "2026-05-02T00:00:00Z", typ="reparatur")
        self.assertEqual(len(vorher["treffer"]), 1)
        self.assertEqual(danach["treffer"], [])

    def test_gleichzeitige_revision_braucht_folge(self):
        self.revision("K-1-R2")["erfasst_am"] = self.revision("K-1-R1")["erfasst_am"]
        with self.assertRaises(Modellfehler):
            validiere(self.modell)
        self.revision("K-1-R1")["folge"] = 0
        self.revision("K-1-R2")["folge"] = 1
        validiere(self.modell)

    def test_bestand_ohne_anfangsbeleg_offen(self):
        self.revision("C-0-R1")["daten"]["vollstaendig"] = False
        r = bestand(self.modell, U("POSITION-1"), punkt("2026-06-01"), "2026-06-06T00:00:00Z")
        self.assertEqual(r["status"], "offen")

    def test_anfangsstand_deckt_aeltere_bewegung_ab(self):
        self.revision("C-0-R1")["fachliche_zeit"] = punkt("2025-04-01")
        self.revision("C-0-R1")["daten"]["menge"] = "10"
        b = bestand(self.modell, U("POSITION-1"), punkt("2026-06-01"), "2026-06-06T00:00:00Z")
        self.assertEqual(Decimal(b["menge"]), Decimal("12"))

    def test_szenariobestand_deckt_aeltere_bewegung_ab(self):
        self.revision("C-0-R1")["fachliche_zeit"] = punkt("2025-04-01")
        self.revision("C-0-R1")["erfasst_am"] = "2025-04-01T10:00:00Z"
        self.revision("C-0-R1")["daten"]["menge"] = "10"
        r = berechne_szenario(self.modell, U("S-C"))
        self.assertEqual(Decimal(r["betrag"]), Decimal("1800"))

    def test_grosse_dezimalberechnung_ohne_stellenverlust(self):
        self.revision("B-A-R1")["daten"]["betrag"] = "123456789012345678901234567890"
        s = next(s for s in self.modell["szenarien"] if s["id"] == U("S-A"))
        s["parameter"] = {"faktor": "1", "perioden": 2}
        r = berechne_szenario(self.modell, U("S-A"))
        self.assertEqual(r["betrag"], "123456789012345678901234567890")

    def test_null_perioden_erhalten_ausgangswert(self):
        s = next(s for s in self.modell["szenarien"] if s["id"] == U("S-A"))
        s["parameter"] = {"faktor": "0", "perioden": 0}
        self.assertEqual(berechne_szenario(self.modell, U("S-A"))["betrag"], "22000")

    def test_deutsche_unicode_texte_erhalten(self):
        text = self.revision("D-6-R1")["daten"]["texte"][0]["wert"]
        self.assertIn("Geschäftstermin", text)
        self.assertIn("Kleidungsstück", text)
        rueckweg = aus_rdf(nach_rdf(self.modell))
        r = next(r for r in rueckweg["revisionen"] if r["id"] == U("D-6-R1"))
        self.assertEqual(r["daten"]["texte"][0]["wert"], text)

    def test_szenario_keine_doppelten_aussagerevisionen(self):
        s = next(s for s in self.modell["szenarien"] if s["id"] == U("S-A"))
        s["eingaben"] = [U("K-1-R1"), U("K-1-R2")]
        with self.assertRaisesRegex(Modellfehler, "Revisionen derselben"):
            validiere(self.modell)

    def test_prognoseziel_und_erfassungszeit(self):
        self.revision("S-A-R1")["fachliche_zeit"] = punkt("2027-06-01")
        with self.assertRaisesRegex(Modellfehler, "Zielzeiten"):
            validiere(self.modell)

    def test_zeitpraezision_nicht_auf_mitternacht_geraten(self):
        zeit = {"art": "intervall", "beginn": {"wert": "2026-06-01", "praezision": "tag"}, "ende": {"status": "offen"}}
        self.assertIsNone(gilt_am(zeit, punkt("2026-06-01T12:00:00Z", "sekunde")))
        self.assertTrue(gilt_am(zeit, punkt("2026-06-02T00:00:00Z", "sekunde")))

    def test_unbestimmter_konkurrierender_kurs_bleibt_offen(self):
        r = deepcopy(self.revision("C-4-R1"))
        r.update(id=U("C-4-B-R1"), aussage_id=U("C-4-B"), fachliche_zeit=punkt("2026-06", "monat"), quelle_id=U("Q-B"))
        self.modell["revisionen"].append(r)
        wert = bestandswert(self.modell, U("POSITION-1"), punkt("2026-06-01"), "2026-06-06T00:00:00Z", "EUR", U("MARKT-1"))
        self.assertEqual(wert["status"], "offen")

    def test_schema_referenzen_typen_und_sprachen(self):
        mutationen = [
            lambda m: m.update(unbekannt="Fremdes Feld"),
            lambda m: m["entitaeten"][0].update(typ=BEGRIFF + "nicht_registriert"),
            lambda m: m["entitaeten"][0]["bezeichnungen"][0].update(sprache="de_DE"),
            lambda m: m["entitaeten"][0]["bezeichnungen"][0].update(sprache="zz"),
            lambda m: m["revisionen"][0].update(quelle_id=U("fehlt")),
            lambda m: m["revisionen"][0].update(subjekt_id=U("AUTO-1")),
            lambda m: m["revisionen"][0].update(aussage_id=U("AUTO-1")),
            lambda m: m["szenarien"][0].update(modell_version="2.0.0"),
            lambda m: m["szenarien"][0].update(eingaben=[U("fehlt")]),
            lambda m: m["revisionen"][0]["fachliche_zeit"].update(wert="2024-02-30T00:00:00Z"),
        ]
        for mutation in mutationen:
            m = deepcopy(self.modell)
            mutation(m)
            with self.subTest(mutation=mutation), self.assertRaises(Modellfehler):
                validiere(m)

    def test_dezimallexik_grosser_zahl_erhalten(self):
        self.revision("K-1-R1")["daten"]["betrag"] = "123456789012345678901234567890.00"
        r = aus_rdf(nach_rdf(self.modell))
        rr = next(v for v in r["revisionen"] if v["id"] == U("K-1-R1"))
        self.assertEqual(rr["daten"]["betrag"], "123456789012345678901234567890")

    def test_rdf_unabhaengig_von_reihenfolge_und_leere_sammlungen(self):
        self.modell["entitaeten"][0]["bezeichnungen"] = []
        vorher = normalisiere(self.modell)
        for feld in ["entitaeten", "revisionen", "szenarien"]:
            self.modell[feld].reverse()
        g = nach_rdf(self.modell)
        self.assertEqual(aus_rdf(g), vorher)
        self.assertEqual(aus_rdf(Graph().parse(data=g.serialize(format="json-ld"), format="json-ld")), vorher)

    def test_rdf_fremde_und_mehrfache_felder(self):
        mutationen = [
            lambda g: g.add((URIRef(self.modell["id"]), URIRef("urn:fremd:feld"), Literal("Fremd"))),
            lambda g: g.add((URIRef(U("K-1-R1")), KERN.erfasst_am, Literal("2026-01-01T00:00:00Z", datatype=XSD.string))),
            lambda g: g.add((BNode(), KERN.art, Literal("unverbunden"))),
        ]
        for mutation in mutationen:
            g = nach_rdf(self.modell)
            mutation(g)
            with self.assertRaises(Modellfehler):
                aus_rdf(g)

    def test_rdf_dezimaltyp_und_sprachkennzeichen(self):
        g = nach_rdf(self.modell)
        s, p, o = next(g.triples((None, KERN.betrag, None)))
        g.remove((s, p, o))
        g.add((s, p, Literal(str(o), datatype=XSD.string)))
        with self.assertRaises(Modellfehler):
            aus_rdf(g)
        g = nach_rdf(self.modell)
        s, p, o = next(g.triples((None, RDF.value, None)))
        g.remove((s, p, o))
        g.add((s, p, Literal(str(o))))
        with self.assertRaises(Modellfehler):
            aus_rdf(g)


if __name__ == "__main__":
    unittest.main()
