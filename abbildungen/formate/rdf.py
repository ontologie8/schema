# SPDX-License-Identifier: AGPL-3.0-or-later
"""Explizite RDF-Abbildung des geschlossenen Pilotvertrags, ohne JSON-Payload."""
from __future__ import annotations

from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef, XSD

from scripts.modellvertrag import DEZIMALFELDER, SCHEMA, Modellfehler, fordere, normalisiere, validiere

KERN = Namespace("urn:ontologie8:kern:")
SAMMLUNGEN = {"entitaeten", "revisionen", "szenarien", "bezeichnungen", "texte", "eingaben", "eingabe_ids"}
REFERENZEN = {"typ", "aussage_id", "subjekt_id", "objekt_id", "quelle_id", "ersetzt_id", "methode_id", "szenario_id", "markt_id", "modell_id", "einheit", "wertart", "zustand", "anlass", "eingaben", "eingabe_ids"}
FELDER = set(SCHEMA["properties"])
for definition in SCHEMA["$defs"].values():
    FELDER.update(definition.get("properties", {}))
    for variante in definition.get("oneOf", []):
        FELDER.update(variante.get("properties", {}))
FELDER.update({"faktor", "perioden", "kurs", "waehrung"})


def _klasse(objekt: dict):
    if "schema_version" in objekt:
        return KERN.Modellpaket
    if "aussage_id" in objekt:
        return KERN.Revision
    if "modell_id" in objekt:
        return KERN.Szenario
    if "bezeichnungen" in objekt:
        return KERN.Entitaet
    if "sprache" in objekt:
        return KERN.Textwert
    if objekt.get("art") == "zeitpunkt":
        return KERN.Zeitpunkt
    if objekt.get("art") == "intervall":
        return KERN.Intervall
    return KERN.Struktur


def nach_rdf(modell: dict) -> Graph:
    validiere(modell)
    graph = Graph()
    graph.bind("kern", KERN)

    def schreiben(objekt: dict):
        knoten = URIRef(objekt["id"]) if "id" in objekt else BNode()
        graph.add((knoten, RDF.type, _klasse(objekt)))
        if _klasse(objekt) == KERN.Entitaet:
            graph.add((knoten, RDF.type, URIRef(objekt["typ"])))
        for feld, wert in objekt.items():
            if feld == "id" or (feld == "sprache" and _klasse(objekt) == KERN.Textwert):
                continue
            if feld == "wert" and _klasse(objekt) == KERN.Textwert:
                graph.add((knoten, RDF.value, Literal(wert, lang=objekt["sprache"])))
                continue
            if wert == []:
                graph.add((knoten, KERN.leereSammlung, Literal(feld)))
                continue
            for eintrag in wert if isinstance(wert, list) else [wert]:
                if isinstance(eintrag, dict):
                    ziel = schreiben(eintrag)
                elif feld in REFERENZEN:
                    ziel = URIRef(eintrag)
                elif feld in DEZIMALFELDER:
                    ziel = Literal(eintrag, datatype=XSD.decimal, normalize=False)
                elif isinstance(eintrag, bool):
                    ziel = Literal(eintrag, datatype=XSD.boolean)
                elif isinstance(eintrag, int):
                    ziel = Literal(eintrag, datatype=XSD.integer)
                else:
                    ziel = Literal(eintrag, datatype=XSD.string)
                graph.add((knoten, KERN[feld], ziel))
        return knoten

    schreiben(normalisiere(modell))
    return graph


def aus_rdf(graph: Graph) -> dict:
    wurzeln = list(graph.subjects(RDF.type, KERN.Modellpaket))
    fordere(len(wurzeln) == 1 and isinstance(wurzeln[0], URIRef), "RDF braucht genau ein benanntes Modellpaket")
    verarbeitet = set()
    pfad = set()

    def lesen(knoten):
        fordere(knoten not in pfad, "Zyklische RDF-Teilstruktur")
        pfad.add(knoten)
        objekt = {"id": str(knoten)} if isinstance(knoten, URIRef) else {}
        felder: dict[str, list] = {}
        typen = set()
        for s, p, o in graph.triples((knoten, None, None)):
            verarbeitet.add((s, p, o))
            if p == RDF.type:
                typen.add(o)
                continue
            if p == RDF.value:
                fordere(isinstance(o, Literal) and o.language, "Textwert benötigt ein Sprachliteral")
                fordere("wert" not in objekt, "Mehrfacher RDF-Textwert")
                objekt.update(wert=str(o), sprache=o.language)
                continue
            if p == KERN.leereSammlung:
                fordere(isinstance(o, Literal) and (o.datatype is None or o.datatype == XSD.string) and not o.language, "Ungültige Metadaten für leere Sammlung")
                feld = str(o)
                fordere(feld in SAMMLUNGEN and feld not in objekt, "Unbekannte oder doppelte leere Sammlung")
                objekt[feld] = []
                continue
            fordere(str(p).startswith(str(KERN)), "Fremdes RDF-Prädikat")
            feld = str(p)[len(str(KERN)):]
            fordere(feld in FELDER and feld not in {"id", "sprache"}, "Unbekanntes RDF-Feld")
            if feld in REFERENZEN:
                fordere(isinstance(o, URIRef), "RDF-Referenz ist keine IRI")
                wert = str(o)
            elif isinstance(o, (BNode, URIRef)):
                wert = lesen(o)
            else:
                fordere(isinstance(o, Literal) and not o.language, "Unerwartetes Sprachliteral")
                if feld in DEZIMALFELDER:
                    fordere(o.datatype == XSD.decimal, "Dezimalwert hat ungeeigneten RDF-Datentyp")
                    wert = str(o)
                elif feld in {"folge", "perioden"}:
                    fordere(o.datatype == XSD.integer and isinstance(o.toPython(), int), "Ungültiger RDF-Ganzzahlwert")
                    wert = int(o)
                elif feld == "vollstaendig":
                    fordere(o.datatype == XSD.boolean and str(o) in {"true", "false", "1", "0"} and isinstance(o.toPython(), bool), "Ungültiger RDF-Wahrheitswert")
                    wert = o.toPython()
                else:
                    fordere(o.datatype in {None, XSD.string}, "Ungeeigneter RDF-Textdatentyp")
                    wert = str(o)
            felder.setdefault(feld, []).append(wert)
        for feld, werte in felder.items():
            fordere(feld not in objekt, "RDF-Feld besitzt leere und befüllte Werte")
            fordere(feld in SAMMLUNGEN or len(werte) == 1, "Mehrfachwert für ein RDF-Einzelfeld")
            objekt[feld] = werte if feld in SAMMLUNGEN else werte[0]
        erwartet = {_klasse(objekt)}
        if _klasse(objekt) == KERN.Entitaet and "typ" in objekt:
            erwartet.add(URIRef(objekt["typ"]))
        fordere(typen == erwartet, "Fehlende oder ungeeignete RDF-Strukturtypen")
        pfad.remove(knoten)
        return objekt

    modell = lesen(wurzeln[0])
    fordere(verarbeitet == set(graph), "RDF enthält unverbundene oder nicht abgebildete Aussagen")
    validiere(modell)
    return normalisiere(modell)
