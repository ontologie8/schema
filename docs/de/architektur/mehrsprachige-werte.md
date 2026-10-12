# Designvorgabe: mehrsprachige Werte bei deutscher Projektpflege

Stand: 2026-10-12 · P0-Vorgabe · noch keine implementierten Datentypen oder Laufzeitfunktionen

## Auftrag und Grenze

Die Projektpflege bleibt in Phase 1 deutsch: Dokumentation, selbst gepflegte Begriffsbezeichnungen, Kommentare, Beispiele, Issues, PRs und Commitnachrichten. Die Modellarchitektur unterstützt von Beginn an mehrere Sprachen je sprachabhängiger Eigenschaft. Weitere gepflegte Sprachfassungen entstehen erst nach ausdrücklichem Auftrag. Das ist keine Einschränkung des allgemeinen Datentyps auf Deutsch.

Das Repository enthält niemals Echtdaten; Beispiele sind vollständig synthetisch. Produktive Inhalte und Dokumente verbleiben in den nutzenden Anwendungen. Eine Anwendung kann dasselbe Schema später mit türkischen, englischen oder anderen Werten verwenden, unabhängig von der deutschen Pflege dieses Projekts.

Diese Vorgabe bestimmt die fachliche Struktur. Ob JSON oder RDF das führende Modell repräsentiert, wird in der übergeordneten P0-Spec entschieden. Ebenso offen bleiben konkrete Bibliotheken und Speicheranbindungen.

## Sprache, Land und Rechtsraum

| Dimension | Kennzeichnung | Bedeutung |
| --- | --- | --- |
| Textsprache | BCP-47-Sprachkennzeichen, etwa `de`, `tr`, `en` | Sprache eines konkreten Textes |
| Sprachvariante | etwa `de-DE`, `de-AT`, `en-GB` | Sprachkennzeichen mit begründeter regionaler Unterscheidung |
| Schrift | bei Bedarf als Bestandteil des Sprachkennzeichens | Schreibsystem, unabhängig von Staatsangehörigkeit |
| Land | ISO-3166-1-Ländercode, etwa `DE`, `TR`, `GB` | Land mit ausdrücklich benannter fachlicher Rolle, etwa Sitz oder Staatsangehörigkeit |
| Rechtsraum | eigene fachliche Referenz | Anwendbares Recht; wird nicht aus Textsprache oder Land abgeleitet |

`de` in `docs/de/` bezeichnet Deutsch. `DE` als Ländercode bezeichnet Deutschland. Groß-/Kleinschreibung allein trennt die Bedeutung nicht zuverlässig: Sprachkennzeichen werden ohne Beachtung der Groß-/Kleinschreibung verglichen. Die Felder und ihre Typen müssen die Dimension unterscheiden. Für Sprachkennzeichen verwenden wir die üblichen Schreibkonventionen; eine RDF-Abbildung darf sie nach dem Standard kleinschreiben.

BCP 47 berücksichtigt auch Schrift- und Regionsbestandteile. Zwei Buchstaben reichen nicht für alle zulässigen Sprachen. Wir begrenzen den Kerntyp deshalb weder auf zwei Zeichen noch auf eine Liste der drei Beispielsprachen. Unbekannte Sprache wird nicht automatisch zu `de`; bei sprachlichem Text mit unbestimmter Sprache ist `und` vorgesehen. Fehlender Text bleibt fehlend.

## Werteklassen und Begriffsidentität

Jede modellierte Eigenschaft erklärt ihren Werttyp und ihre Kardinalität. Dadurch ist ersichtlich, ob Sprachvarianten zulässig sind oder der Wert sprachunabhängig ist.

| Werteklasse | Modellierung |
| --- | --- |
| Bezeichnung, Beschreibung, fachlicher Freitext | Ein oder mehrere Textwerte mit eigenem Sprachkennzeichen |
| Fachlicher Begriff, Entitätstyp oder Beziehungstyp | Stabile ID/IRI; angezeigte Bezeichnungen können mehrere Sprachfassungen haben |
| Zahl, Datum, Anteil, Betrag | Typisierter Wert; Währung, Einheit und weitere Bedeutung separat. Sprachabhängige Anzeige wird daraus erzeugt. |
| Referenz, ID, normierter Code | Sprachunabhängige Identität oder Code mit benanntem Codesystem |
| Eigenname oder Originalbezeichnung | Original erhalten; Schreibvarianten oder Transliteration ausdrücklich getrennt. Keine automatische Übersetzung. |
| Dokumentinhalt oder belegte Aussage | Eigenständige Fassung mit Sprache, Identität, Version, Quelle und Status |

Ein zusätzlicher übersetzter Anzeigetext erzeugt keinen neuen Beziehungstyp. Unterschiedliche Rechtsbegriffe werden umgekehrt nicht allein aufgrund ähnlicher Übersetzungen gleichgesetzt. Dieselbe Entität wird nicht pro Sprache dupliziert. Technische Schlüssel und IRIs behalten ihre Identität, auch wenn ihre Bezeichnungen später übersetzt werden.

## Textwerte: explizite Sammlung von Beginn an

Das fachliche Grundmuster ist eine Sammlung expliziter Textwerte. Jeder Textwert besitzt `wert` und `sprache`. Ein einzelner deutscher Text nutzt bereits dieselbe Struktur, die später mehrere Sprachfassungen trägt. Die Reihenfolge bestimmt weder Sprache noch Vorrang; exakte Dubletten können normalisiert werden. Mehrere unterschiedliche Werte derselben Sprache werden eigenschaftsspezifisch erlaubt oder begrenzt.

Illustratives JSON, vollständig synthetisch und ausschließlich deutsch:

```json
{
  "id": "urn:beispiel:dokument:001",
  "titel": [
    { "wert": "Synthetischer Ehevertrag", "sprache": "de" }
  ]
}
```

Der gemeinsame Texttyp nimmt später weitere BCP-47-Sprachkennzeichen auf. Es entstehen keine neuen Felder `titel_tr`, `titel_en` und keine Umstellung von String auf Array bei Einführung einer zweiten Sprache. Ob für eine konkrete Eigenschaft ein bevorzugter Text je Sprache verlangt wird, legt ihr Profil fest.

Alternativen:

| Variante | Bewertung |
| --- | --- |
| Einzelner String, Sprache nur aus Ordner oder globalem Standard | Für sprachabhängige Austauschwerte verworfen: Die Sprache des konkreten Wertes ist nicht zuverlässig erkennbar. |
| Eigenes Feld je Sprache | Verworfen: Jede zusätzliche Sprache verändert die Feldstruktur. |
| Sprachmap, zum Beispiel `{"de": "Synthetischer Ehevertrag"}` | Geeignet als einfache Darstellung oder JSON-LD-Sprachmap; bei Mehrfachwerten sind Sammlungen je Sprache nötig. Keine alleinige Struktur für belegte Fassungen. |
| Sammlung expliziter Textwerte | Fachliches Grundmuster: Sprachkennzeichnung am Wert, Mehrfachwerte ohne neue Sprachfelder und klarer Anschluss an RDF-Literale. |

## RDF-/JSON-LD-Abbildung

Ein einfacher Textwert wird in RDF auf ein Literal mit Sprachkennzeichen abgebildet. Beispielsweise:

```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<urn:beispiel:dokument:001>
    rdfs:label "Synthetischer Ehevertrag"@de .
```

In JSON-LD entspricht der Textwert einem Wertobjekt:

```json
{ "@value": "Synthetischer Ehevertrag", "@language": "de" }
```

Die deutsche JSON-Form mit `wert` und `sprache` ist für sich noch kein JSON-LD. Ein späterer Konverter oder eindeutig definierter Kontext muss die Abbildung herstellen. Sprachmaps benötigen ebenfalls einen passenden Kontext. JSON-Sammlungen werden dabei nicht versehentlich als geordnete RDF-Listen interpretiert.

Schriftrichtung und Unicode gehören zur Architekturprüfung. Für einfache Textwerte wird eine optionale Richtung `ltr`/`rtl` vorgesehen, wenn sie ausdrücklich benötigt wird. JSON-LD 1.1 kann Richtung kennzeichnen; ein gewöhnliches RDF-1.1-Sprachliteral allein bewahrt diese Zusatzinformation nicht. Die P0-Spec muss für solche Werte eine verlustfreie Abbildung festlegen, statt sie beim Export stillschweigend zu verlieren. Text wird in Unicode erhalten; Originalschreibweise, Diakritika und Schrift werden nicht für einen Vergleich zerstört.

## Dokumentfassungen und Übersetzungsbeziehungen

Ein Ehevertrag mit mehreren Sprachfassungen braucht mehr als mehrere Titel. Das Modell trennt das gemeinsame Dokument von seinen einzelnen Fassungen. Jede Fassung erhält eine eigene Identität und Version, die tatsächlich enthaltenen Sprachen, die externe Inhaltsreferenz sowie Quellen- und Statusangaben. Enthält eine Fassung mehrere Sprachen, ist dies eine Sammlung von Sprachkennzeichen; sprachlich abgegrenzte Abschnitte tragen bei Bedarf eigene Kennzeichnungen.

Originalfassung, Übersetzung und parallel erstellte Fassung bleiben unterscheidbar. Eine Übersetzungsbeziehung verweist auf die konkrete Ausgangsfassung und deren Version. Prüfstatus und eine ausdrücklich festgelegte maßgebliche Fassung sind eigene Angaben. Ein Sprachkennzeichen behauptet weder inhaltliche Gleichwertigkeit noch rechtliche Verbindlichkeit. Die verwendeten Sprachen werden nicht aus Staatsangehörigkeit, Namen oder Sitz der Beteiligten abgeleitet.

Einfache Labels bleiben Textwerte. Wo Herkunft, Übersetzungsstatus oder Version am einzelnen Inhalt wichtig sind, wird der Inhalt als eigener referenzierbarer Datensatz modelliert; diese Informationen werden nicht auf ein bloßes RDF-Literal reduziert.

## Phase 1 und spätere Nutzung

Der allgemeine Modellvertrag erlaubt Mehrsprachigkeit von Anfang an. Die Pflegevorgabe für Phase 1 legt nur deutsche Inhalte in diesem Repository fest. Eine spätere Anwendung darf andere Sprachen nutzen, ohne den Texttyp umzubauen. Deutsch ist keine Pflichtsprache für ihre produktiven Datensätze.

Ein Anzeige-Fallback ist eine explizite Anwendungsregel. Er darf einen vorhandenen deutschen Text anzeigen, aber ihn nicht als türkischen oder englischen Wert ausgeben. Fehlende Übersetzungen bleiben erkennbar; es entstehen weder leere Platzhalter noch automatisch erfundene Übersetzungen. Unterschiedliche Sprachen sind keine festen Arraypositionen.

## Akzeptanz und Prüfpfade

Die folgenden Prüfungen sind Ziele der späteren Modellimplementierung, noch keine vorhandenen Laufzeittests:

- AC-10: Deutsche Projektpflege und allgemeine Mehrsprachigkeit sind getrennt. In Phase 1 werden ausschließlich deutsche Texte gepflegt; eine spätere zweite Sprache benötigt keine neue Feldstruktur.
- AC-11: Ein Textwert trägt ein BCP-47-Sprachkennzeichen. Sprache, Land und Rechtsraum bleiben getrennt. Fehlende Sprache wird nicht aus anderen Angaben geraten; zusätzliche gültige Kennzeichen sind ohne Codeänderung am Kerntyp möglich.
- AC-12: Der JSON-/RDF-Austausch erhält Wert, Sprache, Begriffsidentität und Mehrfachwerte. Abweichende Reihenfolge verändert die Bedeutung nicht. Benötigte Schriftrichtung wird erhalten oder eine unzureichende Abbildung ausdrücklich zurückgewiesen.
- AC-13: Dokumentfassungen und Übersetzungen besitzen eigene Identität, Versionsbindung, Herkunft und Status. Eine spätere Sprachfassung ersetzt weder Original noch maßgebliche Fassung automatisch.

Vor der ersten Implementierung werden positive und negative Erwartungsfälle festgelegt: unbekannte Sprache, ungültiges Kennzeichen, gleicher Begriff mit zusätzlichem Sprachlabel, Mehrfachwerte derselben Sprache, fehlende Übersetzung, Sprachvariante mit Region sowie unterscheidbare Dokumentfassungen. Die Prüfung verwendet ausschließlich synthetische Inhalte; während Phase 1 bleiben Textinhalte deutsch. Sprachkennzeichen anderer Sprachen sind technische Testparameter, keine gepflegten Übersetzungen.

## Quellen

- [IETF RFC 5646: Sprachkennzeichen nach BCP 47](https://www.rfc-editor.org/rfc/rfc5646.html) für Sprach-, Schrift- und Regionsbestandteile sowie unbestimmte Sprache.
- [ISO 3166: Ländercodes](https://www.iso.org/iso-3166-country-codes.html) für die eigenständige Landesdimension.
- [W3C RDF 1.1: Literale](https://www.w3.org/TR/rdf11-concepts/#section-Graph-Literal) für Textwerte mit Sprachkennzeichen.
- [W3C JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) für Wertobjekte, Sprachmaps, Sammlungen und Schriftrichtung.

Die Wahl des fachlichen Grundmusters und der Dokumentfassungen ist eine Projektentscheidung, keine von diesen Standards vorgeschriebene Ordnerstruktur oder vollständige Vertragsmodellierung.
