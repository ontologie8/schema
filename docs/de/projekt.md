# Projekt: Ontologie und Schemas

Stand: 2026-10-13. Eigenständiges Projekt in [ontologie8/schema](https://github.com/ontologie8/schema).

## Auftrag und Projektstatus

Das Projekt entwickelt einen gemeinsamen Modellkern mit Fachmodulen, Anwendungsfallprofilen und unabhängigen Speicherprofilen. Zeit, Herkunft, Bewertungen, Szenarien und mehrsprachige Textwerte sind gemeinsame Bausteine. Der [P0-Entwurf](architektur/p0-weltmodell.md) führt diese Struktur zusammen; der [Pilot 0.1.0](architektur/p0-pilot-benutzung.md) prüft den ersten ausführbaren Vertrag. Die [Personen-/Nachlassroadmap](../../roadmap/de/personen-nachlass-roadmap.md) bleibt ein Fachpfad einschließlich JSON Schema, RDF/Turtle, SHACL, SPARQL, NetworkX und optionaler Graphdatenbank.

Arbeitsmethode: Kanban, wöchentlicher Review, bedarfsbezogener Kurzsync; Maintainer funktion8 / ofunk. Dies plant keine Termine oder Erinnerungen. P0 ist in Bearbeitung; P1–P6 bleiben Backlog.

## Versionskontrolliertes Projektboard

| Arbeitspaket | Scope | Status | Abhängigkeit |
| --- | --- | --- | --- |
| P0 | Weltmodell, Modellgrenzen, Zeit und Versionierungsvertrag | Pilot, Erbausschlagung und allgemeiner Fachmodul-/Versionsvertrag geliefert; weitere Fachdefinitionen und Migrationen offen | — |
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

Weitere Fachdefinitionen im allgemeinen Modulvertrag ergänzen; bei einem tatsächlichen Versionswechsel einen gerichteten Migrationsvertrag mit unabhängigen Erwartungen erstellen.

## Aktueller Auftrag: allgemeiner Fachmodul- und Versionsvertrag

Auftrag: Auto, Aktien, Kleidung und Erbausschlagung gemeinsam für den allgemeinen Fachmodul-/Versionsvertrag nutzen. AC-21 bis AC-23 ergänzen die bestehenden Prüfziele. Scope, Alternativen, Risiko, Plan und Designreview vor Code stehen in der [Spezifikation](architektur/fachmodule-und-versionen.md).

Scope: Geschlossene gemeinsame Modul-/Profil-/Paket-/Übernahmemetadaten, eindeutige Begriffsverantwortung, exakte Abhängigkeiten, fünf Fallprofile, SHA-256-Artefaktbindung und eine portable offline geprüfte Kopie mit benanntem Speicherziel. Die vorhandenen Datenverträge und Referenzfälle bleiben erhalten; die beiden Datensatzformen werden ausdrücklich unterschieden.

Plan und Review: Profilgrenzen zusätzlich zur bestehenden fachlichen Validierung prüfen; Abhängigkeiten und bereitgestellte Begriffe geschlossen auflösen; Einzelproben gegen unabhängige Fragen und tatsächliche RDF-Rückwege prüfen; Identitätsverletzungen und Export-/Versionsfehler zurückweisen. Eine unterschiedliche Versionsnummer allein beweist keine Kompatibilität. Ein Paketgenerator erstellt nur neue Stände und prüft sie vor Veröffentlichung in einer separaten Kopie.

Ergebnis: Fünf versionierte Module, fünf Profile, 29 Begriffszuständigkeiten und drei zusätzliche Einzelproben mit 17 unabhängigen Fragen. Der aktuelle Paketstand 0.1.1 bindet 50 Artefakte einschließlich der vollständigen Lizenzzuordnung; 0.1.0 bleibt unverändert erhalten. Die 78 Testmethoden einschließlich 24 zusätzlicher Versions-/Profil-/Übernahmeprüfungen bestehen. Portable CLI und lokale Dokumentabhängigkeiten werden außerhalb ihrer bisherigen Ablage geprüft. Anbieterbetrieb, produktive Rechtsdatenschemata und gerichtete Migrationen sind weiterhin eigene Aufgaben.

## Aktueller Auftrag: erster Schema- und RDF-Pilot

Ergänzung vom 2026-10-13: Auf ausdrücklichen Auftrag werden vier Erbausschlagungs-Modellproben aus einem festgehaltenen `ontology`-Quellstand aufgenommen. Scope, Alternativen, AC-20, Risiken und Plan vor Umsetzung stehen im [Prüfvertrag](anwendungsfaelle/erbausschlagung.md). Ein eigenes Prüfprofil verwendet gemeinsame Kerntext-/Zeittypen; ein allgemeines Rechtsfachmodul und Rechtsfolgenrechnung bleiben spätere Aufgaben. Quelle und synthetische Zeitwerte sind getrennt; der Quellentwurf ist noch nicht notariell freigegeben.

Ergebnis: Vier frei erfundene Fälle mit neun Personen und 17 Nachweisen, fünf unabhängige historische Erwartungsabfragen, eigene JSON-/Turtle-/JSON-LD-Abbildung und 18 ergänzende positive/negative Testmethoden. Die CI prüft beide Verträge. Die Pflege bleibt deutsch und die Ausführung vollständig offline; das Quellprojekt dient der Herkunftszuordnung. Der bestehende Pilotvertrag bleibt unverändert.

Auftrag: Den geprüften Entwurf in konkrete Schemaartefakte überführen und JSON/RDF einschließlich mehrsprachiger Werte und zeitlicher Revisionen ausführbar prüfen. AC-03/04/10/11/12 und AC-14 bis AC-19 bilden den Umfang.

Scope: Versionierter kleiner JSON-Schema-Vertrag, Modul-/Begriffsregister, synthetischer Auto-/Aktien-/Bekleidungspilot, semantische Validierung, RDF-Hin-/Rückweg und historische Abfragen mit unabhängigen Erwartungen. Deutsch bleibt Pflegesprache; andere Sprachkennzeichen werden nur als technische Testparameter mit deutschen synthetischen Texten verwendet.

Risiko: RDF könnte bei ungeprüfter Konvertierung Reihenfolge, Zahlenbedeutung, Sprachkennzeichen oder zeitlichen Kontext verlieren. JSON Schema allein prüft keine referenzierten Entitäten, Revisionsketten oder konkurrierenden Zuordnungen. Diese Prüfungen werden getrennt implementiert und getestet.

Plan und Review: JSON-first für diesen Pilot mit expliziten Aussagen-/Revisionsressourcen vergleichen und als überprüfbare Umsetzung festlegen; die [Implementierungsspezifikation](architektur/p0-schema-pilot.md) vor dem Code ausarbeiten und gegen den bisherigen Entwurf reviewen. Danach Schema, Daten und Abbildung umsetzen, unabhängige positive/negative Erwartungen und Hin-/Rückweg prüfen, Befunde korrigieren und CI erweitern. Ausführbare Banken-/Rechts-/Steuerlogik und produktive Speicheranbindungen gehören nicht zu dieser Lieferung.

Ergebnis: JSON-first-Vertrag 0.1.0 mit Schema, semantischer Validierung, drei Modulmanifesten, Pilotprofil, 17 synthetischen Entitäten, 26 Revisionen und vier Szenarien implementiert. Turtle-/JSON-LD-Rückweg erhält die kanonische Modellbedeutung; unabhängige historische und numerische Erwartungen sowie negative Fälle sind ausführbar. Die [Benutzung](architektur/p0-pilot-benutzung.md) nennt Befehle und Grenzen. P0 bleibt für weitere Fach-/Detailprofile und externe Übernahmeverträge in Bearbeitung.

## Aktueller Auftrag: P0-Entwurf mit Zeitmodell

Auftrag: Den freigegebenen Architekturweg ausarbeiten und Zeit als gemeinsamen Bestandteil für Ereignisse, Beziehungen, Beobachtungen, Bewertungen und Szenarien aufnehmen.

Scope: Ordner- und Modulstruktur als Zielbild, Modellgrenzen, Schemaübernahme in externe Anwendungen, JSON-/RDF-Alternativen, zeitliche Gültigkeit und Erfassungsrevisionen, Kauf/Bestand/Bewertung, externe Bewertungsmodelle und Prognosen. Kleine vollständig synthetische Fälle für Auto, Aktien und Kleidung prüfen das Design. AC-14 bis AC-19 ergänzen die bestehenden Kriterien.

Risiko: Überschreiben eines Wertes würde Historie verlieren; eine Erfassungszeit könnte mit fachlicher Wirkung verwechselt werden; Kaufpreis, Marktwert und Prognose könnten unbemerkt zusammenfallen. Ein ungeprüftes zeitliches RDF-Mapping oder eine automatische Auswahl der neuesten Bewertung könnte falsche Ergebnisse erzeugen.

Plan: [Architekturentwurf](architektur/p0-weltmodell.md) und [Zeitvertrag](architektur/zeit-und-bewertungen.md) mit Alternativen erstellen, [synthetische Eingaben und unabhängig festgelegte Erwartungsergebnisse](anwendungsfaelle/zeitliche-referenzfaelle.md) gegenüberstellen, Entwurf gegen die Anforderungen reviewen und korrigieren. Anschließend Struktur-/Linkvalidator, vollständigen Git-Diff und CI prüfen, committen und über PR liefern. Umfang dieser Lieferung ist der geprüfte Entwurf; ausführbare Fachschemata, zeitliche Abfragen und Bewertungsprogramme folgen in der Umsetzung.
