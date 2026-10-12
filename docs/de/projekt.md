# Projekt: Ontologie und Schemas

Stand: 2026-10-12. Eigenständiges Projekt in [ontologie8/schema](https://github.com/ontologie8/schema).

## Auftrag und Projektstatus

Das Projekt entwirft einen gemeinsamen Modellkern mit Fachmodulen, Anwendungsfallprofilen und unabhängigen Speicherprofilen. Zeit, Herkunft, Bewertungen, Szenarien und mehrsprachige Textwerte sind gemeinsame Bausteine. Der [P0-Entwurf](architektur/p0-weltmodell.md) führt diese Struktur zusammen. Die [Personen-/Nachlassroadmap](../../roadmap/de/personen-nachlass-roadmap.md) bleibt ein Fachpfad einschließlich JSON Schema, RDF/Turtle, SHACL, SPARQL, NetworkX und optionaler Graphdatenbank.

Arbeitsmethode: Kanban, wöchentlicher Review, bedarfsbezogener Kurzsync; Maintainer funktion8 / ofunk. Dies plant keine Termine oder Erinnerungen. P0 ist in Bearbeitung; P1–P6 bleiben Backlog.

## Versionskontrolliertes Projektboard

| Arbeitspaket | Scope | Status | Abhängigkeit |
| --- | --- | --- | --- |
| P0 | Weltmodell, Modellgrenzen, Zeit und Versionierungsvertrag | In Bearbeitung | — |
| P1 | Personen, Familie, Organisationen und zeitabhängige Rollen | Backlog | P0 |
| P2 | JSON-Referenzdataset, Import-/Exportvertrag und 10.000er-Prüfung | Backlog | P1 |
| P3 | Genogramm-Projektion und Exportvertrag | Backlog | P2 |
| P4 | Vermögen, Beteiligungen, Verpflichtungen und Übertragungen | Backlog | P1/P2 |
| P5 | Zeitliche Szenarien und geprüfte Nachlassregeln | Backlog | P3/P4 |
| P6 | Anwendungsschnittstellen, Ansichten und Backend-Benchmark | Backlog | P1–P5 |

Die Arbeitspakete werden in diesem Board geführt. [Akzeptanzkriterien](akzeptanz.md) definieren die fachlichen Prüfziele.

## P0-Zwischenschritt: mehrsprachige Werte

Auftrag: Die Projektpflege bleibt in Phase 1 vollständig deutsch. Das Schema muss sprachabhängige Werte von Beginn an mehrsprachig modellieren können, ohne eine spätere Änderung ihrer Grundstruktur zu benötigen. Echtdaten bleiben ausgeschlossen.

Scope: Sprachkennzeichen am Textwert, Trennung von Sprache/Land/Rechtsraum, stabile Begriffsidentitäten, JSON-/RDF-Abbildung und eigenständige Dokumentfassungen. Keine Übersetzungen, fremdsprachigen Parallelfassungen, Domänenschemas oder Speicheranbindungen implementieren. AC-10 bis AC-13 ergänzen die bisherigen Prüfziele.

Risiko: Ein einzelner Text ohne Sprachkennzeichen, ein ausschließlich auf `de` begrenzter Kerntyp oder Sprachfelder wie `titel_de` würden die spätere Erweiterung erschweren. Eine Sprachmap allein verliert bei dokumentierten Fassungen Quellen, Status und Versionen.

Plan und Validierung: Standards zu BCP 47, RDF und JSON-LD prüfen; die [Designvorgabe](architektur/mehrsprachige-werte.md) mit Alternativen und Prüfpfaden festhalten; Agentenregeln, Einstieg und Roadmap daran ausrichten; Inhalt und vollständigen Git-Diff reviewen; Projektvalidator und Remote-CI prüfen. Dieser Zwischenschritt liefert die Designvorgabe, keine laufende Mehrsprachigkeitsfunktion. Die Vorgabe ist geliefert; P0 wird durch den aktuellen Architekturauftrag fortgeführt.

## Nächster Schritt

P0-Entwurf prüfen und konkretisieren: führende Modellrepräsentation anhand des synthetischen Piloten bestimmen; danach Schemas und ausführbare Erwartungsfälle umsetzen.

## Aktueller Auftrag: P0-Entwurf mit Zeitmodell

Auftrag: Den freigegebenen Architekturweg ausarbeiten und Zeit als gemeinsamen Bestandteil für Ereignisse, Beziehungen, Beobachtungen, Bewertungen und Szenarien aufnehmen.

Scope: Ordner- und Modulstruktur als Zielbild, Modellgrenzen, Schemaübernahme in externe Anwendungen, JSON-/RDF-Alternativen, zeitliche Gültigkeit und Erfassungsrevisionen, Kauf/Bestand/Bewertung, externe Bewertungsmodelle und Prognosen. Kleine vollständig synthetische Fälle für Auto, Aktien und Kleidung prüfen das Design. AC-14 bis AC-19 ergänzen die bestehenden Kriterien.

Risiko: Überschreiben eines Wertes würde Historie verlieren; eine Erfassungszeit könnte mit fachlicher Wirkung verwechselt werden; Kaufpreis, Marktwert und Prognose könnten unbemerkt zusammenfallen. Ein ungeprüftes zeitliches RDF-Mapping oder eine automatische Auswahl der neuesten Bewertung könnte falsche Ergebnisse erzeugen.

Plan: [Architekturentwurf](architektur/p0-weltmodell.md) und [Zeitvertrag](architektur/zeit-und-bewertungen.md) mit Alternativen erstellen, [synthetische Eingaben und unabhängig festgelegte Erwartungsergebnisse](anwendungsfaelle/zeitliche-referenzfaelle.md) gegenüberstellen, Entwurf gegen die Anforderungen reviewen und korrigieren. Anschließend Struktur-/Linkvalidator, vollständigen Git-Diff und CI prüfen, committen und über PR liefern. Umfang dieser Lieferung ist der geprüfte Entwurf; ausführbare Fachschemata, zeitliche Abfragen und Bewertungsprogramme folgen in der Umsetzung.
