# ontologie8/schema

Eigenständiges Projekt für versionierte Fachmodelle, Schemas und Ontologie-Projektionen zu Personen, Familien, Organisationen, Rollen, Vermögen und zeitlichen Ereignissen. Dieses Repository führt das gemeinsame Fachmodell und seine Roadmap unabhängig von einer konkreten Anwendung oder Speicherplattform.

Status: Projektinitialisierung und Roadmap; noch keine implementierten Domänenschemas oder Laufzeitfunktionen.

| Einstieg | Dokument |
| --- | --- |
| Projekt und Board | [Projekt](docs/de/projekt.md) |
| Vollständige Roadmap | [Roadmap](roadmap/de/personen-nachlass-roadmap.md) |
| Mehrsprachige Werte bei deutscher Pflege | [P0-Designvorgabe](docs/de/architektur/mehrsprachige-werte.md) |

[Agentenregeln](AGENTS.md), [Gantt-Index](roadmap/GANTT.md) und [Lizenzzuordnung](LICENSES/README.md).

Start: [P0 — Design und Modellgrenzen](roadmap/de/personen-nachlass-roadmap.md).

## Dokumentationsstruktur

Die Fachdokumentation liegt unter `docs/de/`, die Fachroadmap unter `roadmap/de/`. Sprachkürzel nach ISO 639 trennen die Inhalte; gemeinsame Einstiegs- und Metadatendateien bleiben an ihren bestehenden Orten.

Bei später beauftragter Mehrsprachigkeit können zusätzliche Sprachordner mit derselben relativen Dateistruktur ergänzt werden. Aktuell wird ausschließlich Deutsch gepflegt; weitere Sprachfassungen werden nicht angelegt.

Die Sprache der Projektpflege begrenzt nicht die Datenwerte späterer Anwendungen. Sprachabhängige Werte werden von Beginn an mit BCP-47-Sprachkennzeichen und einer erweiterbaren Sammlung entworfen. Sprachunabhängige IDs, Zahlen und Codes bleiben davon getrennt; `de` bezeichnet die Sprache Deutsch, `DE` als Ländercode Deutschland. [Modellierung, Alternativen und Prüfpfade](docs/de/architektur/mehrsprachige-werte.md).

Prüfung: `python scripts/validate_project.py`.

Keine produktiven Personen-, Mandats- oder Unternehmensdaten und keine Secrets.
