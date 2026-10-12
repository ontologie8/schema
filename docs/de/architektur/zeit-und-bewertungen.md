# P0-Zeitvertrag: Historie, Bewertungen und Szenarien

Stand: 2026-10-12 · Geprüfter Designentwurf · Umsetzung steht aus
Lizenz: CC-BY-4.0

## Zweck und Geltungsbereich

Zeit ist ein Bestandteil des [gemeinsamen Modellkerns](p0-weltmodell.md). Entitäten behalten ihre Identität; Aussagen über Eigenschaften und Beziehungen können sich ändern. Fachmodule verwenden gemeinsame Zeit- und Herkunftsstrukturen mit der benötigten Detailtiefe. Konkrete Inhalte liegen in nutzenden Anwendungen; alle hiesigen Beispiele sind vollständig synthetisch.

Dieser Vertrag konkretisiert AC-14 bis AC-18 und wirkt auf AC-03/07/09/12. Er beschreibt keine automatisch laufende Historisierung. Die spätere Anwendung und ihr Speicherprofil müssen den Vertrag tatsächlich umsetzen.

## Eigenschaft, Beziehung und Ereignis

| Aussage | Modellform | Fachlicher Zeitbezug |
| --- | --- | --- |
| Objekt besitzt eine Identität | Stabile ID | Identität bleibt über Zustandswechsel erhalten |
| Person kauft einen Gegenstand | Kaufereignis mit Käufer, Verkäufer, Objekt und vereinbartem Preis | Zeitpunkt oder belegter Zeitraum des Kaufs |
| Person/Organisation besitzt einen Anteil | Qualifizierte Eigentumsbeziehung | Gültigkeit der konkreten Zuordnung |
| Auto hat einen dokumentierten Kilometerstand | Beobachtung zum Objekt | Beobachtungszeitpunkt |
| Kleidungsstück wird repariert | Ereignis; gegebenenfalls anschließende Zustandsbeobachtung | Reparaturzeit und Zeitpunkt der Feststellung |
| Kurs eines Finanzinstruments wird festgestellt | Kursbeobachtung mit Markt, Währung und Einheit | Kurszeitpunkt |
| Vermögensobjekt wird bewertet | Eigener Bewertungsdatensatz | Bewertungsstichtag oder ausdrücklich begrenzter Bewertungszeitraum |
| Künftiger Wert wird berechnet | Berechnung im Szenario | Prognoseziel getrennt vom Berechnungszeitpunkt |

Eine aktuelle Eigenschaftsansicht darf aus diesen Aussagen abgeleitet werden. Sie muss ihre Auswahl erklären können. Eine Bewertung zu einem Stichtag gilt nicht automatisch bis zur nächsten Bewertung; jede Fortschreibung oder Auswahl älterer Daten benötigt eine benannte Regel und einen sichtbaren Datenstand.

## Zwei Zeitachsen und eine erhaltene Historie

| Zeitachse | Frage | Inhalt |
| --- | --- | --- |
| Fachliche Zeit | Wann gilt oder geschieht etwas in der beschriebenen Welt? | Ereigniszeit, Beobachtungszeit, Bewertungsstichtag oder Gültigkeitsintervall |
| Wissenszeit | Wann war welche Aussage im Anwendungssystem bekannt? | Erfassungszeit einer Revision und Zeitpunkt ihrer Ablösung oder Rücknahme |

Die bisherige Roadmap nennt `effective_at` und `recorded_at`. Der Kern konkretisiert diese Bedeutungen über fachlichen Zeitbezug und Erfassungsrevisionen; diese Begriffe sind keine Vorgabe für englische selbst gepflegte Feldnamen.

Ein Kauf am 10. März kann am 20. März erfasst werden. Am 1. April kann eine Korrektur des eingegebenen Kaufpreises hinzukommen, ohne das Kaufdatum zu verändern. Historische Abfragen unterscheiden dann den Kaufstand nach heutigem Wissen vom damaligen Kenntnisstand.

Eine logische Aussage hat eine stabile Aussage-ID. Jede Revision hat eine eigene Revisions-ID, Erfassungszeit, Inhalt und Herkunft. Eine Korrektur verweist auf die abgelöste Revision. Eine Rücknahme wird als eigener Vorgang erhalten. Die ursprüngliche Revision bleibt unverändert verfügbar. Ein Ablösungsindex darf daraus berechnet werden; er ist nicht die einzige vorhandene Historie.

Die Anwendung vergibt die tatsächliche Erfassungszeit und eine eindeutige Erfassungsreihenfolge. Innerhalb derselben Revisionskette brauchen gleiche Zeitstempel eine ergänzende Reihenfolge oder werden als unaufgelöster Konflikt zurückgegeben. Eine neue Revision darf im Wissensverlauf nicht vor ihrer Vorgängerrevision liegen. Quellzeitstempel sind eigene Angaben und werden beim Import nicht zur rückdatierten Erfassungszeit. Revisionsketten sind azyklisch. Parallele Aussagen unabhängiger Quellen werden nicht durch eine beliebige spätere Importzeit zu Korrekturen erklärt.

Für vollständig bestimmte Intervalle gilt im Pilot die Konvention `[Beginn, Ende)`: Beginn enthalten, Ende ausgeschlossen. Wissensrevisionen verwenden entsprechend `[erfasst, abgelöst)`. Genau am Ablösungszeitpunkt gilt die neue Revision. Der historische Abfragekontext enthält fachlichen Stichtag und Wissensstichtag; zusätzlich werden benötigte Profil-/Regelversion und Szenariobezug ausdrücklich gewählt.

Fehlende Kenntnis über eine Aussage ist keine Aussage über ihre Unwahrheit. Eine nachträglich erfasste Übertragung verändert den damaligen Kenntnisstand nicht rückwirkend.

## Präzision, Grenzen und Unsicherheit

- Ein Zeitpunkt mit Uhrzeit trägt einen eindeutigen Offset, im Austausch bevorzugt UTC mit `Z`. Ein Kalenderdatum, Monat oder Jahr bleibt in seiner bekannten Präzision erhalten. Es wird keine scheinbar bekannte Uhrzeit ergänzt.
- Der zeitliche Typ unterscheidet Zeitpunkt, Zeitraum und ungefähre Angabe. Eine fehlende Intervallgrenze wird ausdrücklich als unbekannt oder nach aktuellem Wissen offen gekennzeichnet; sie wird nicht auf null Uhr, Null oder ein Fantasiedatum gesetzt.
- Offen bedeutet hier: kein Ende bekannt beziehungsweise festgelegt im gewählten Kenntnisstand. Es behauptet keine unveränderliche zukünftige Fortdauer. Bei einer unbekannten Grenze können Zugehörigkeit und Reihenfolge unbestimmt sein.
- Ungültige oder umgekehrte vollständige Intervalle werden zurückgewiesen. Überschneidungen werden je Beziehungstyp geprüft: mehrere zeitgleiche Eigentümer sind etwa bei Anteilen möglich, mehrere exklusive Gesamtzuordnungen benötigen Klärung.
- Vergleiche unterschiedlicher Präzision brauchen eine ausdrücklich festgelegte Auswertung. Wenn die vorhandenen Angaben die Reihenfolge nicht entscheiden, ist das Ergebnis unbestimmt.
- Ein Zukunftsdatum kennzeichnet nicht allein eine Prognose: geplante Ereignisse, bereits dokumentierte künftige Verpflichtungen und hypothetische Szenarien erhalten unterschiedliche Aussagearten und Statusangaben.

## Kaufpreis, Bestand und Bewertung

Ein Kaufpreis gehört zur konkreten Transaktion und nennt ihren Umfang sowie die Preisbasis, etwa Gesamtpreis oder Stückpreis. Er wird nicht automatisch zum aktuellen Marktwert. Die Transaktion und die daraus belegte Eigentums- oder Bestandsänderung bleiben unterscheidbar; ein Kaufbeleg allein ersetzt nicht in jedem Fachkontext den Nachweis der Übertragung.

Eine Bewertung benötigt folgenden Vertrag; unvollständige Bewertungsentwürfe werden erkennbar gehalten:

| Feldgruppe | Fachlicher Inhalt |
| --- | --- |
| Identität und Bezug | Bewertungs-ID, Revision und ID des bewerteten Objekts oder Bestands |
| Art und Umfang | Wertart, etwa Marktwert, Versicherungswert oder Wiederverkaufswert; Gesamt-/Stückwert und Menge soweit erforderlich |
| Ergebnis | Betrag, Währung und gegebenenfalls Spanne oder anderes benanntes Unsicherheitsmaß |
| Fachliche Zeit | Bewertungsstichtag und bekannte Präzision |
| Herkunft | Quelle, Bewertender und tatsächlicher Erfassungsstand; benötigte Quellenreferenzen |
| Methode | Methode beziehungsweise versioniertes Modell und verwendete Eingaben oder Berechnungsreferenz |
| Aussageart | Beobachtung, Schätzung, berechneter Wert oder Prognose |
| Prüfung | Eigenständiger Prüfstatus; keine automatische Bestätigung durch Import |

Marktwert, Versicherungswert, Angebotspreis, Buchwert und ein Verkaufserlös werden als unterschiedliche Größen behandelt. Zwei Quellen können verschiedene Marktwertschätzungen für denselben Stichtag liefern. Beide bleiben erhalten. Eine Anwendung darf eine Bewertung auswählen, wenn ihr Profil Wertart, Quelle, Stichtag und gegebenenfalls Aktualitätsgrenze erklärt. Fehlen passende Daten, bleibt das Ergebnis offen.

Beträge und Mengen werden dezimal und mit definierter Genauigkeit modelliert. In einer JSON-Darstellung können dafür Dezimalzeichenfolgen verwendet werden; die Schemaumsetzung muss Zahlenbedeutung, Währung, Einheit und Rundung erhalten. Unbekannter Wert ist kein Nullwert.

Bei Aktien werden Finanzinstrument, Eigentums-/Depotposition, zeitabhängige Stückzahl und Kurs getrennt. Die Bestandsbewertung verbindet die passende Menge und den passenden Kurs im selben fachlichen und Wissenskontext. Markt, Währung und Stückbasis müssen passen. Splits verändern beispielsweise Stückzahl und Kursbasis; reine Kursvergleiche ohne diese Basis können irreführen. Weitere Ereignisse und Ausschüttungen brauchen eigene fachliche Verträge.

## Externe Modelle und zukünftige Werte

Ein Bewertungsmodell ist ein referenzierbares, versioniertes Fachartefakt. Seine Zuordnung zu einem Objekt beziehungsweise Objekttyp ist kontextabhängig. Der Kern schreibt keine feste Wertentwicklung eines Autos, Kleidungsstücks oder Finanzinstruments vor.

Eine Berechnung verbindet Modellversion, explizite Parameter, Eingaberevisionen und Berechnungszeitpunkt. Ihr Ergebnis verweist auf die Berechnung. Für eine Prognose kommen Zielzeit beziehungsweise Horizont und Szenario-ID hinzu. Eine Unsicherheitsspanne oder Wahrscheinlichkeit wird nur geführt, wenn sie tatsächlich durch die Methode begründet ist.

Beispielsweise kann eine Anwendung ein hypothetisches Wertminderungsmodell für ein Auto wählen. Eine andere Methode kann aus Vergleichsangeboten schätzen. Das Schema benennt beide Methoden und ihre Ergebnisse, ohne eine allgemeine Behauptung über Wertverlust oder Wertsteigerung einzubauen. Ausführbare Modelle, echte Vergleichsdaten und Berechnungsbetrieb gehören zur jeweiligen Anwendung oder zu einem ausdrücklich implementierten Fachmodul.

Szenarien bilden isolierte Kontexte. Sie ändern weder bestätigte Historie noch Bestände einer anderen Ansicht. Später beobachtete Ergebnisse sind neue Beobachtungen; eine frühere Prognose bleibt als damalige Prognose erhalten und kann mit ihnen verglichen werden. Modellversion, Datenrevision und Zeitpunkt bleiben sichtbar.

## Illustrative JSON-Darstellung

Dieses Beispiel erläutert einen möglichen Austauschdatensatz. Es ist noch kein implementiertes JSON Schema und kein vollständiger Datensatz für den Import. Die verwendeten IDs, Quellen und Zahlen sind synthetisch.

```json
{
  "aussage_id": "urn:beispiel:bewertung:auto-001",
  "revision_id": "urn:beispiel:revision:bewertung-auto-001-1",
  "objekt_id": "urn:beispiel:auto:001",
  "wertart": "marktwert",
  "aussageart": "schaetzung",
  "betrag": "22000.00",
  "waehrung": "EUR",
  "fachliche_zeit": {
    "art": "zeitpunkt",
    "datum": "2026-06-01",
    "praezision": "tag"
  },
  "erfasst_am": "2026-06-03T09:00:00Z",
  "quelle_id": "urn:beispiel:quelle:gutachten-001",
  "methode_id": "urn:beispiel:methode:vergleichswert-1"
}
```

Wertart, Aussageart und Methode werden im späteren Schema über definierte Begriffe referenziert; ihre hier gezeigten kurzen Codes sind illustrative deutsche Bezeichner. Sprachabhängige Bezeichnungen zu diesen Begriffen folgen dem [Textvertrag](mehrsprachige-werte.md). Betrag, Währungscode und Zeitangaben werden nicht pro Sprache dupliziert.

## Abbildung und Alternativen

| Ansatz | Entscheidung im Entwurf |
| --- | --- |
| Aktuelles Feld überschreiben | Als führende Historie verworfen; nur als reproduzierbare abgeleitete Ansicht geeignet |
| Kauf-/Verkaufsereignisse allein | Für Bestandsänderungen nützlich, aber keine vollständige Erklärung unabhängiger Beobachtungen, Korrekturen oder Bewertungen |
| Zeit und Quelle nur an einem unqualifizierten RDF-Triple | Für den Pilot unzureichend: Historie und konkurrierende Aussagen müssen separat identifizierbar sein |
| Eigene Beziehungs-/Aussagedatensätze und Revisionen | Gewähltes fachliches Muster; gemeinsame Identität von Objekt, Aussage und Revision trennen |
| Einzelne benannte RDF-Graphen | Mögliche Zusatzstruktur; ihre Namen allein definieren noch keine Gültigkeits- oder Szenariosemantik |

Der Pilot bildet qualifizierte Beziehungen und Bewertungen auf eigene RDF-Ressourcen ab. Zeitpunkte und Intervalle können auf OWL-Time, Herkunft und Ableitungen auf PROV-O abgebildet werden. Der genaue Revisions-, Gültigkeits- und Szenariovertrag bleibt ein eigener Modellvertrag und wird durch keine dieser Abbildungen automatisch implementiert.

JSON-/RDF-Hin- und Rückweg müssen IDs, Zeitpräzision, Intervallgrenzen, Revisionsverweise, konkurrierende Aussagen, Quellen, Sprachwerte und Szenariokontext erhalten. Die standardisierte RDF-Repräsentation darf nicht durch bloße Dateizeitstempel oder Importreihenfolge ersetzt werden.

## Quellen und Review

- [W3C OWL-Time, Recommendation 2017](https://www.w3.org/TR/2017/REC-owl-time-20171019/) als Grundlage für Zeitpunkte, Intervalle und zeitliche Beziehungen.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) als Grundlage für Herkunft, beteiligte Akteure und Ableitungen.
- [W3C: Modellmuster für Beziehungen mit zusätzlichen Angaben](https://www.w3.org/TR/swbp-n-aryRelations/) für referenzierbare Beziehungen mit eigenem Kontext; dies ist eine Working Group Note.
- [IETF RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) für Zeitstempel mit Offset; Präzision und unbestimmte Grenzen sind zusätzliche Modellentscheidungen.

Die Zwei-Zeiten-Abfrage, Revisionsregeln und Halbintervallkonvention sind Entscheidungen dieses Entwurfs. Die [Referenzfälle und Review-Ergebnisse](../anwendungsfaelle/zeitliche-referenzfaelle.md) konkretisieren ihre Bedeutung. Ausführbare Prüfung und verlustfreies Mapping folgen vor einer produktiven Schemafreigabe.
