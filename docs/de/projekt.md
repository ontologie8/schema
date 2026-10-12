# Projekt: Ontologie und Schemas

Stand: 2026-10-12. Eigenständiges Projekt in [ontologie8/schema](https://github.com/ontologie8/schema).

## Auftrag und Projektstatus

Das Projekt umfasst: Personen/Familie, Organisationen/Geschäftsführung, Beteiligungen/Vermögen, Ereignisse, Schenkungen/Testamente, Zeit und Szenarien sowie JSON Schema, RDF/Turtle, SHACL, SPARQL, NetworkX und optionale Graphdatenbank. [Vollständige Roadmap](../../roadmap/de/personen-nachlass-roadmap.md).

Arbeitsmethode: Kanban, wöchentlicher Review, bedarfsbezogener Kurzsync; Maintainer funktion8 / ofunk. Dies plant keine Termine oder Erinnerungen. P0–P6 bleiben Backlog.

## Versionskontrolliertes Projektboard

| Arbeitspaket | Scope | Status | Abhängigkeit |
| --- | --- | --- | --- |
| P0 | Design, Modellgrenzen und Versionierungsvertrag | Backlog | — |
| P1 | Personen, Familie, Organisationen und zeitabhängige Rollen | Backlog | P0 |
| P2 | JSON-Referenzdataset, Import-/Exportvertrag und 10.000er-Prüfung | Backlog | P1 |
| P3 | Genogramm-Projektion und Exportvertrag | Backlog | P2 |
| P4 | Vermögen, Beteiligungen, Verpflichtungen und Übertragungen | Backlog | P1/P2 |
| P5 | Zeitliche Szenarien und geprüfte Nachlassregeln | Backlog | P3/P4 |
| P6 | Anwendungsschnittstellen, Ansichten und Backend-Benchmark | Backlog | P1–P5 |

Die Arbeitspakete werden in diesem Board geführt. [Akzeptanzkriterien](akzeptanz.md) definieren die fachlichen Prüfziele.

## Nächster Schritt

Mit P0 beginnen: Design-Spec mit JSON-first/RDF-first-Vergleich, Modellgrenzen und kleinem synthetischem Pilot vorbereiten.
