# NaC als Consumer

Dieses Repository führt Schema-/Ontologie-Artefakte und Roadmap. NaC führt weiter seine vorhandenen notariellen Usecases, BPMN-/Prozessverträge, Zugriffsgates und Integrationsadapter.

## Geplante Nutzung

- NaC bindet eine freigegebene Release-Version und einen unveränderlichen Commit-/Artefakt-Hash.
- Das Integrationsmanifest nennt Repository, Version, Hash und kompatible NaC-Adapterversion.
- Kein Verweis auf einen beweglichen main-Stand für produktive Ausführung.
- Keine manuell gepflegte Kopie der Domänenschemas oder dieser Roadmap in NaC.
- Falls Artefakte geladen werden, ist ein regenerierbarer Cache ausdrücklich als abgeleitet markiert; Schemaquelle bleibt ontologie8/schema.
- Updates laufen als überprüfbares Dependency-Update mit Kompatibilitäts- und Migrationstest.
- Keine Netzwerk-Abfrage der Ontologie pro Nutzer-Request; freigegebene Artefakte sind vorher gebunden.
- SharePoint bleibt NaC-Speicher, nicht Ontologieinhalt. Personen-/Familien-/Vermögensdaten werden nur unter dem privaten NaC-Betriebsrahmen verarbeitet.

## Zuständigkeit

| ontologie8/schema | NaC |
| --- | --- |
| Begriffe, stabile IDs, Feld-/Relationsdefinitionen | Vorgangszuordnung und Aktenrollen |
| JSON/RDF-Mapping, SHACL und Validierungsverträge | Adapter, CLI-/Bürooberfläche und Workflow-Gates |
| Synthetische Referenzfälle und Benchmarkdefinition | Freigegebene Tenant-Tests und produktive Datenhaltung |
| Versionierung und Breaking-Change-Hinweise | Dependency-Bindung und Update-Freigabe |

Noch kein Release, Paket oder Schema implementiert. P0 bestimmt Paketformat, Namespaces, führende Repräsentation und konkreten Versionsvertrag.
