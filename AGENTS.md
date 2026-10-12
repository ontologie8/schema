# Agentenregeln / Agent rules

## Geltungsbereich und Wahrheit / Scope and authority

- Dieses Repository führt das Fachmodell und die Schema-/Ontologie-Roadmap. NaC bleibt Consumer; fachliche Vorgangsarten, produktiver Speicher, Zugriffe und notarielle Entscheidungen gehören zur jeweiligen Anwendung.
- This repository owns the domain model and schema/ontology roadmap. NaC remains a consumer; workflows, production storage, authorization and professional decisions belong to the consuming application.
- Fakten, Entität, Rolle, Eigentum und technische Berechtigung bleiben getrennt. Fehlende Angaben bleiben unbekannt. Kein automatischer Personenmerge und keine erfundenen Beziehungen.
- Separate facts, entities, roles, ownership and technical permissions. Preserve unknown values. Never merge identities or invent relationships automatically.
- JSON/RDF sind geplante Repräsentationen eines führenden Modells. Turtle ist eine RDF-Serialisierung. Kein globaler Reasoner im NaC-Request-Pfad.
- JSON/RDF are planned representations of one authoritative model. Turtle serializes RDF. No global reasoner on NaC's request path.

## Arbeitsfluss / Delivery workflow

- Auftrag, Scope, AC-IDs, Risiko, Plan und Validierung vor Änderungen dokumentieren. [Projektboard](docs/de/projekt.md) und [Roadmap](roadmap/de/personen-nachlass-roadmap.md) pflegen, wenn Scope oder Status betroffen ist.
- Record request, scope, AC IDs, risk, plan and validation before edits. Maintain the [project board](docs/en/projekt.md) and [roadmap](roadmap/en/personen-nachlass-roadmap.md) when scope/status changes.
- Klar beauftragte Dokumentmigrationen dürfen direkt vorbereitet werden. Nichttriviale Implementierung braucht zuerst eine prüfbare Design-Spec mit Alternativen, AC-IDs und Review; dann Plan → Review → Korrektur und Umsetzung → Review → Korrektur.
- Explicit documentation migrations may be prepared directly. Nontrivial implementation first requires a reviewable design spec with alternatives, AC IDs and review; then plan/review/fix and implement/review/fix.
- Bootstrap eines leeren Repos ist direkt zulässig. Danach Branch + PR; vollständige base...head-Diff, Dateien und Commits vor Merge prüfen. Keine Fertigmeldung ohne belegte Lieferung und bestandene CI.
- Direct bootstrap of an empty repository is allowed. Afterwards use branch/PR, reviewing the complete base...head diff, files and commits before merge. Claim delivery only with evidence and passing CI.
- Keine ungefragten Logins, Tokenimporte, Credential-Umwandlungen oder Accountwechsel. Bestehende autorisierte Zugänge verwenden.
- No unsolicited logins, token imports, credential conversions or account changes. Use existing authorized access.

## Sprache, Lizenzen und Sicherheit / Language, licensing and privacy

- Deutsch ist fachlich führend; menschlich lesbare Fachdokumentation wird in de/en gepflegt. Lokale Links bleiben sprachgleich. Echte Umlaute verwenden.
- German leads professionally; maintain domain documents in de/en. Keep local links within their language. Use real German umlauts.
- Keine echten Personen-, Familien-, Gesundheits-, Nachlass-, Unternehmens-, Register- oder Mandatsdaten und keine Secrets. Nur klar synthetische Referenzdaten.
- No real personal, family, health, estate, corporate, register or mandate data or secrets. Only clearly synthetic reference data.
- Code, Schemas und Validatoren: AGPL-3.0-or-later. Dokumentation und Roadmap: CC-BY-4.0. [NOTICE](NOTICE) und [AUTHORS.md](AUTHORS.md) erhalten.
- Code, schemas and validators: AGPL-3.0-or-later. Documentation and roadmap: CC-BY-4.0. Preserve [NOTICE](NOTICE) and [AUTHORS.md](AUTHORS.md).

## Prüfung und Abschluss / Verification and completion

- `python scripts/validate_project.py` muss Struktur, Sprachpaare, lokale Links und Roadmap-Umfang prüfen. Inhalt gegen den Auftrag reviewen; neue fachliche Berechnungen brauchen unabhängige Erwartungsfälle.
- `python scripts/validate_project.py` validates structure, language pairs, local links and roadmap scope. Review content against the request; new domain calculations require independent expected cases.
- Jede Abschlussmeldung nennt unter Nächster Schritt / Next step die konkrete Fortsetzung oder den externen Blocker.
- Every completion message identifies the next action or external blocker.
