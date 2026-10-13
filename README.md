# ontologie8/schema

Eigenständiges Projekt für ein erweiterbares Weltmodell mit versionierten Fachmodulen, Schemas und Ontologie-Projektionen. Personen, Organisationen, Gegenstände, Rollen, Vermögen und zeitliche Aussagen nutzen einen gemeinsamen Kern. Dieses Repository führt das Fachmodell und seine Roadmap unabhängig von einer konkreten Anwendung oder Speicherplattform.

Status: Erster ausführbarer Schema-/RDF-Pilot 0.1.0; P0 weiterhin in Bearbeitung. Synthetische Auto-, Aktien- und Bekleidungsfälle prüfen denselben Modellvertrag. Es bestehen keine produktiven Speicheranbindungen.

Der allgemeine [Fachmodul-/Versionsvertrag](docs/de/architektur/fachmodule-und-versionen.md) bindet fünf Module und fünf Fallprofile einschließlich Erbausschlagung in ein geprüftes [Schema-/Prüfpaket](pakete/0.1.0/README.md). Exakte Versionen, Begriffsverantwortung und kanonische Prüfsummen werden offline geprüft. GitHub, SharePoint und S3 sind als Zielkennzeichen für eine portable lokale Schemaübernahme möglich.

| Einstieg | Dokument |
| --- | --- |
| Projekt und Board | [Projekt](docs/de/projekt.md) |
| Ausführbarer Pilot und lokale Prüfung | [Benutzung](docs/de/architektur/p0-pilot-benutzung.md) |
| Führender JSON-Vertrag | [Kernschema](modelle/kern/modell.schema.json) |
| Implementierung, Alternativen und Prüfplan | [Pilotspezifikation](docs/de/architektur/p0-schema-pilot.md) |
| Weltmodell und geplante Ordnerstruktur | [P0-Architekturentwurf](docs/de/architektur/p0-weltmodell.md) |
| Zeit, Historie, Bewertungen und Prognosen | [P0-Zeitvertrag](docs/de/architektur/zeit-und-bewertungen.md) |
| Auto, Aktien und Kleidung | [Synthetische Referenzfälle und Prüfmatrix](docs/de/anwendungsfaelle/zeitliche-referenzfaelle.md) |
| Erbausschlagung aus `ontology` | [Vier synthetische Fälle mit eigenem Prüfvertrag](docs/de/anwendungsfaelle/erbausschlagung.md) |
| Fachmodule, Profile, Versionen und Übernahme | [Allgemeiner Vertrag](docs/de/architektur/fachmodule-und-versionen.md) |
| Vollständige Roadmap | [Roadmap](roadmap/de/personen-nachlass-roadmap.md) |
| Mehrsprachige Werte bei deutscher Pflege | [P0-Designvorgabe](docs/de/architektur/mehrsprachige-werte.md) |

[Agentenregeln](AGENTS.md), [Gantt-Index](roadmap/GANTT.md) und [Lizenzzuordnung](LICENSES/README.md).

Start: [P0 — Weltmodell und Modellgrenzen](docs/de/architektur/p0-weltmodell.md). Die bisherige Personen-/Nachlassplanung bleibt ein erhaltener Fachpfad.

## Dokumentationsstruktur

Die Fachdokumentation liegt unter `docs/de/`, die Fachroadmap unter `roadmap/de/`. Sprachkürzel nach ISO 639 trennen die Inhalte; gemeinsame Einstiegs- und Metadatendateien bleiben an ihren bestehenden Orten.

Bei später beauftragter Mehrsprachigkeit können zusätzliche Sprachordner mit derselben relativen Dateistruktur ergänzt werden. Aktuell wird ausschließlich Deutsch gepflegt; weitere Sprachfassungen werden nicht angelegt.

Die Sprache der Projektpflege begrenzt nicht die Datenwerte späterer Anwendungen. Sprachabhängige Werte werden von Beginn an mit BCP-47-Sprachkennzeichen und einer erweiterbaren Sammlung entworfen. Sprachunabhängige IDs, Zahlen und Codes bleiben davon getrennt; `de` bezeichnet die Sprache Deutsch, `DE` als Ländercode Deutschland. [Modellierung, Alternativen und Prüfpfade](docs/de/architektur/mehrsprachige-werte.md).

Prüfung mit dem verifizierten Projekt-Python: `scripts/validate_project.py`, `scripts/pruefe_pilot.py`, `scripts/pruefe_erbausschlagung.py`, `scripts/pruefe_module.py` und `python -m unittest discover -s tests -v`. [Umgebung und vollständige Befehle](docs/de/architektur/p0-pilot-benutzung.md).

Keine produktiven Personen-, Mandats- oder Unternehmensdaten und keine Secrets.
