# SPDX-License-Identifier: AGPL-3.0-or-later
"""RDF-Abbildung des eigenständigen synthetischen Erbausschlagungsvertrags."""
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef, XSD

from scripts.erbausschlagung import VERTRAG, validiere
from scripts.modellvertrag import SCHEMA, fordere, normalisiere

EA = Namespace("urn:ontologie8:pruefvertrag:erbausschlagung:rdf:0.1.0:")
SAMMLUNGEN = {"personen", "quellen", "beziehungen", "faelle", "nachweise", "bezeichnungen", "betroffene_person_ids", "pruefungen"}
REFERENZEN = {"erblasser_id", "ausschlagende_person_id", "betroffene_person_ids", "fall_id", "person_id", "subjekt_id", "objekt_id", "quelle_id"}
FELDER = set(VERTRAG["properties"])
for definition in list(VERTRAG["$defs"].values()) + list(SCHEMA["$defs"].values()):
    FELDER.update(definition.get("properties", {}))
    for variante in definition.get("oneOf", []):
        FELDER.update(variante.get("properties", {}))


def _klasse(objekt):
    return EA.Pruefpaket if "datenart" in objekt else EA.Textwert if "sprache" in objekt else EA.Struktur


def nach_rdf(paket: dict) -> Graph:
    validiere(paket)
    graph = Graph()
    graph.bind("ea", EA)

    def schreiben(objekt):
        knoten = URIRef(objekt["id"]) if "id" in objekt else BNode()
        graph.add((knoten, RDF.type, _klasse(objekt)))
        for feld, wert in objekt.items():
            if feld == "id" or (feld == "sprache" and _klasse(objekt) == EA.Textwert):
                continue
            if feld == "wert" and _klasse(objekt) == EA.Textwert:
                graph.add((knoten, RDF.value, Literal(wert, lang=objekt["sprache"])))
                continue
            if wert == []:
                graph.add((knoten, EA.leereSammlung, Literal(feld)))
                continue
            for v in wert if isinstance(wert, list) else [wert]:
                ziel = schreiben(v) if isinstance(v, dict) else URIRef(v) if feld in REFERENZEN else Literal(v, datatype=XSD.string)
                graph.add((knoten, EA[feld], ziel))
        return knoten

    schreiben(normalisiere(paket))
    return graph


def aus_rdf(graph: Graph) -> dict:
    wurzeln = list(graph.subjects(RDF.type, EA.Pruefpaket))
    fordere(len(wurzeln) == 1 and isinstance(wurzeln[0], URIRef), "Genau ein benanntes Erbausschlagungspaket erforderlich")
    verarbeitet, pfad = set(), set()

    def lesen(knoten):
        fordere(knoten not in pfad, "Zyklische RDF-Teilstruktur")
        pfad.add(knoten)
        objekt = {"id": str(knoten)} if isinstance(knoten, URIRef) else {}
        typen, felder = set(), {}
        for s, p, o in graph.triples((knoten, None, None)):
            verarbeitet.add((s, p, o))
            if p == RDF.type:
                typen.add(o)
                continue
            if p == RDF.value:
                fordere(isinstance(o, Literal) and o.language and "wert" not in objekt, "Genau ein Sprachliteral je Textwert erforderlich")
                objekt.update(wert=str(o), sprache=o.language)
                continue
            if p == EA.leereSammlung:
                fordere(isinstance(o, Literal) and not o.language and o.datatype in {None, XSD.string}, "Ungültige leere Sammlung")
                feld = str(o)
                fordere(feld in SAMMLUNGEN and feld not in objekt, "Unbekannte oder doppelte leere Sammlung")
                objekt[feld] = []
                continue
            fordere(str(p).startswith(str(EA)), "Fremdes RDF-Prädikat")
            feld = str(p)[len(str(EA)):]
            fordere(feld in FELDER and feld not in {"id", "sprache"}, "Unbekanntes RDF-Feld")
            if feld in REFERENZEN:
                fordere(isinstance(o, URIRef), "Referenz muss eine IRI sein")
                wert = str(o)
            elif isinstance(o, (BNode, URIRef)):
                wert = lesen(o)
            else:
                fordere(isinstance(o, Literal) and not o.language and o.datatype in {None, XSD.string}, "Ungeeigneter Literaldatentyp")
                wert = str(o)
            felder.setdefault(feld, []).append(wert)
        for feld, werte in felder.items():
            fordere(feld not in objekt and (feld in SAMMLUNGEN or len(werte) == 1), "Widersprüchliche RDF-Kardinalität")
            objekt[feld] = werte if feld in SAMMLUNGEN else werte[0]
        fordere(typen == {_klasse(objekt)}, "Ungeeigneter RDF-Strukturtyp")
        pfad.remove(knoten)
        return objekt

    paket = lesen(wurzeln[0])
    fordere(verarbeitet == set(graph), "Nicht angebundene RDF-Aussagen")
    validiere(paket)
    return normalisiere(paket)
