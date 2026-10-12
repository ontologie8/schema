# Agentenregeln

## Geltungsbereich und Wahrheit

- Dieses Repository führt eigenständig das Fachmodell und die Schema-/Ontologie-Roadmap. Produktiver Speicher, Zugriffe und fachliche Entscheidungen gehören zur jeweiligen nutzenden Anwendung.
- Fakten, Entität, Rolle, Eigentum und technische Berechtigung bleiben getrennt. Fehlende Angaben bleiben unbekannt. Kein automatischer Personenmerge und keine erfundenen Beziehungen.
- JSON/RDF sind geplante Repräsentationen eines führenden Modells. Turtle ist eine RDF-Serialisierung.

## Sprache

- Unabhängig von der Sprache des Prompts wird dieses Projekt ausschließlich auf Deutsch gepflegt.
- Antworten zum Projekt, Dokumentation, Agentenregeln, Issue- und PR-Texte sowie Commitnachrichten werden auf Deutsch verfasst. Aktuell werden keine anderssprachigen Parallelfassungen angelegt.
- Sprachabhängige Fachdokumentation liegt in Ordnern mit ISO-639-Sprachkürzeln: derzeit `docs/de/` und `roadmap/de/`. Gemeinsame Einstiegs-, Regel- und Metadatendateien bleiben an ihren bestehenden Orten.
- Die Struktur bleibt um weitere Sprachordner mit gleicher relativer Dateistruktur erweiterbar. Weitere Sprachen werden erst nach einem ausdrücklichen Auftrag zur Mehrsprachigkeit angelegt und gepflegt.
- Die deutsche Projektpflege begrenzt nicht die Sprachen nutzender Anwendungen. Sprachabhängige Werte werden von Beginn an als explizite Textwerte mit BCP-47-Sprachkennzeichen und erweiterbarer Kardinalität entworfen; Phase 1 pflegt nur deutsche Inhalte. Sprache, Land, Rechtsraum und stabile Begriffsidentität bleiben getrennt. [Designvorgabe](docs/de/architektur/mehrsprachige-werte.md).

## Arbeitsfluss

- Auftrag, Scope, AC-IDs, Risiko, Plan und Validierung vor Änderungen dokumentieren. [Projektboard](docs/de/projekt.md) und [Roadmap](roadmap/de/personen-nachlass-roadmap.md) pflegen, wenn Scope oder Status betroffen ist.
- Klar beauftragte Dokumentmigrationen dürfen direkt vorbereitet werden. Nichttriviale Implementierung braucht zuerst eine prüfbare Design-Spec mit Alternativen, AC-IDs und Review; dann Plan → Review → Korrektur und Umsetzung → Review → Korrektur.
- Bootstrap eines leeren Repos ist direkt zulässig. Danach Branch + PR; vollständige base...head-Diff, Dateien und Commits vor Merge prüfen. Keine Fertigmeldung ohne belegte Lieferung und bestandene CI.
- Keine ungefragten Logins, Tokenimporte, Credential-Umwandlungen oder Accountwechsel. Bestehende autorisierte Zugänge verwenden.

## Lizenzen und Sicherheit

- Keine echten Personen-, Familien-, Gesundheits-, Nachlass-, Unternehmens-, Register- oder Mandatsdaten und keine Secrets. Nur klar synthetische Referenzdaten.
- Code, Schemas und Validatoren: AGPL-3.0-or-later. Dokumentation und Roadmap: CC-BY-4.0. [NOTICE](NOTICE) und [AUTHORS.md](AUTHORS.md) erhalten.

## Prüfung und Abschluss

- `python scripts/validate_project.py` muss Struktur, lokale Links und Roadmap-Umfang prüfen. Inhalt gegen den Auftrag reviewen; neue fachliche Berechnungen brauchen unabhängige Erwartungsfälle.
- Jede Abschlussmeldung nennt unter Nächster Schritt die konkrete Fortsetzung oder den externen Blocker.
