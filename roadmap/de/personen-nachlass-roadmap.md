# Roadmap: Personen, Genogramme, Vermögen und zeitliche Nachlassszenarien

Stand: 2026-10-12 · Status: P0-Pilot implementiert, weitere Profilisierung in Bearbeitung; P1–P6 Backlog
Einordnung: [Globale Roadmap](../GANTT.md)
Lizenz: CC-BY-4.0

## Projektzuständigkeit

Dieses Repository führt eigenständig das gemeinsame Fachmodell, JSON Schema, RDF/Turtle, SHACL/SPARQL, Graph-Projektionen, Referenzdaten und den gesamten P0–P6-Plan.

Die in den Tabellen genannten Datenstrukturen, Schnittstellen, Algorithmen und Szenarien sind Planungsziele, keine bereits verfügbaren Implementierungen. Eine konkrete nutzende Anwendung oder Speicherplattform ist nicht festgelegt.

Die Ontologie ist ein versionierter Modell-/Projektionsvertrag. Dieses Repository führt keine produktiven Personen-, Familien-, Unternehmens- oder Mandatsdaten. Das [Projektboard](../../docs/de/projekt.md) führt die Arbeitspakete.

Diese Roadmap bleibt ein Fachpfad innerhalb des [erweiterbaren Weltmodells](../../docs/de/architektur/p0-weltmodell.md). Der gemeinsame Kern und die Zielstruktur werden zusätzlich an Auto, Aktien und Kleidung geprüft; die bisherigen Fachfälle und Phasen bleiben erhalten.

## Ziel

Das Fachmodell beschreibt strukturierte Personen- und Familienbeziehungen, ein daraus abgeleitetes Genogramm, Vermögen mit Eigentumsanteilen sowie nachvollziehbare Szenarien für Schenkungen, Testamente und zeitlich unterschiedliche Erbfälle.

Fachliche Knowledge Graphs und allgemeine Regeln bleiben von konkreten Personen- und Vermögensdaten getrennt.

## Speicher- und Modellrichtung

Das Projekt definiert Datenstrukturen, Referenzdaten und Austauschverträge. Eine spätere nutzende Anwendung entscheidet über produktive Datenhaltung, Zugriffe und Betrieb. Speicherformate und Mapping-Grenzen werden in der ersten Designphase geprüft.

| Ebene | Geplanter Inhalt und Verantwortung |
| --- | --- |
| GitHub | Code, versionierte JSON Schemas, Ontologie, Validierungsregeln, freigegebene Fachregeln und synthetische Beispiele. Keine echten Personen- oder Mandatsdaten. |
| Datenhaltung der nutzenden Anwendung | Personenstammdaten, Beziehungen, Vermögensobjekte, Eigentumsanteile, Verfügungsmetadaten und Ereignisse in getrennten Entitätstypen; stabile fachliche IDs. Zugriff und Betrieb liegen bei der jeweiligen Anwendung. |
| Geschützte Payloads und Dokumente | Große strukturierte Personen-Payloads und Dokumente mit getrennten Schutzklassen, Versionen und Pointern. Speicherort und Verschlüsselung werden vor produktiver Nutzung geprüft. |
| Python-Graph-Projektion | Ein fall- und zeitpunktbezogener Graph für Familien- und Eigentumsabfragen; NetworkX als Kandidat für den In-Memory-Prototyp. |
| RDF/Turtle | Kandidat für semantische Ontologie und Graph-Austausch mit RDFLib, SPARQL und SHACL. RDF ist das Datenmodell, Turtle eine Serialisierung. |
| Graphdatenbank | Optionaler späterer Query-/Projektionsspeicher nach Benchmark und Betriebsentscheidung; nicht allein durch die Zahl 10.000 begründet. |

Ein führendes Datenmodell und definierte Mapping-/Versionsregeln vermeiden auseinanderlaufende Wahrheiten zwischen Speicherformaten, JSON und RDF. Ein großer Personen-Payload wird in Stammdaten, Beziehungen, Rollen, Nachweise und fachliche Erweiterungen gegliedert. Fehlende Angaben bleiben unbekannt, statt als Nein oder als erfundene Beziehung zu erscheinen.

Für alle Fachmodule gilt die [P0-Designvorgabe für mehrsprachige Werte](../../docs/de/architektur/mehrsprachige-werte.md): Phase 1 pflegt deutsche Inhalte; der allgemeine Texttyp unterstützt von Beginn an mehrere Werte mit BCP-47-Sprachkennzeichen. Sprache, Land und Rechtsraum bleiben getrennt. Dokumentfassungen und Übersetzungen erhalten eigenständige Identitäten und Versionsbindungen; die JSON-/RDF-Abbildung muss die Sprachinformationen erhalten. AC-10 bis AC-13 ergänzen die bisherigen Prüfziele.

Der [P0-Zeitvertrag](../../docs/de/architektur/zeit-und-bewertungen.md) trennt fachliche Zeit von erhaltenen Erfassungsrevisionen. Kaufpreise, Beobachtungen und konkurrierende Bewertungen besitzen eigene Kontexte; Prognosen nennen Modellversion, Eingabestand und Zielzeit. AC-14 bis AC-19 und die [synthetische Prüfmatrix](../../docs/de/anwendungsfaelle/zeitliche-referenzfaelle.md) konkretisieren die Anforderungen. Zwei Datumsfelder allein sind kein Nachweis einer funktionierenden Historie.

Für 10.000 Personen werden Indizes, selektive Abfragen, Pagination und ein vollständiger Export geprüft. Die Benchmarks messen die Modell- und Austauschverträge ohne Vorgabe eines bestimmten Speicherdienstes.

## Fachliche Bausteine

- Person: stabile person_id, modularer schema_version, relevante Stammdaten, Nachweisreferenzen und getrennte Aktenrollen.
- Beziehung: eigene relationship_id, Typ, beteiligte person_ids, Gültigkeitszeit, Quelle, Prüfstatus und Unsicherheit. Elternschaft, Adoption, Ehe und Trennung werden fachlich unterschieden; Personen können mehreren Akten zugeordnet sein.
- Vermögen: asset_id, Typ (Haus, Auto, Aktien/Beteiligung, Bargeld/Konto), Bewertungsstichtag, Währung, Eigentumsanteile, Verbindlichkeiten und belastende Rechte. Eigentum, Besitz und Nutzungsrechte sind getrennt.
- Verfügung: Testament, Erbvertrag oder Schenkungsvereinbarung mit Version, zeitlicher Wirkung, begünstigten IDs, Dokumentreferenz und fachlicher Bestätigung.
- Ereignis: beispielsweise Schenkung, Anteilstransfer, Bewertung, Todesfall oder dokumentierte Korrektur. effective_at beschreibt die fachliche Wirkung; recorded_at den Zeitpunkt der Erfassung. Unbekannte oder nur ungefähr bekannte Zeiten bleiben sichtbar.
- Szenario: isolierte Annahmen, Ereignisreihenfolge, Regelversion und Ergebnisse. Hypothetische Todesfälle verändern keine bestätigten Stammdaten.

## Phasen und überprüfbare Ergebnisse

Die Reihenfolge beschreibt Abhängigkeiten, keine zugesagten Kalendertermine. Alle Phasen sind geplant.

| Phase | Umfang | Ergebnis und Abnahmekriterium |
| --- | --- | --- |
| P0: Design und Speichergrenze | Gemeinsamen Kern, Fachmodule, JSON-/RDF-Rollen, Austauschverträge, Zugriffe, Schutzklassen, Rechtsraum, mehrsprachige Werte und zeitliche Revisionen bestimmen. | Geprüfte Spec mit AC-IDs und Prüfpfaden; kleiner JSON-first-Pilot mit RDF-Rückweg und unabhängigen Erwartungen umgesetzt. Weitere Fach-/Detailprofile und externe Übernahmeverträge stehen aus. |
| P1: Personen und Familie | Modulare JSON Schemas, stabile IDs, Beziehungen und Import-/Änderungsvertrag. | Ein kleiner synthetischer Familienfall validiert; fehlende Referenzen, unzulässige Selbstbeziehungen, widersprüchliche Zeiten und Dubletten werden nachvollziehbar behandelt. |
| P2: Austauschvertrag und 10.000er-Prototyp | Synthetische JSON-Dateien als Referenzdataset; Import und Export anhand des versionierten Modells. | 10.000 synthetische Personen importierbar; paginierte Lesewege, ID-Erhalt, Schema-Migration, Konflikte und Neustart geprüft. Laufzeit, Speicherbedarf und Abfragezeiten dokumentiert. |
| P3: Genogramm | Deterministische Familienprojektion, Legende, Export und Codex-Anbindung. | Gleiche Daten ergeben dieselben Knoten und Beziehungen; mehrere Partnerschaften, Adoption, Verstorbene und unbekannte Angaben sichtbar. Keine automatisch erfundenen Verbindungen. |
| P4: Vermögensgraph | Objekte, Anteilshistorie, Bewertungen, Verpflichtungen und Schenkungen. | Eigentum je Stichtag rekonstruierbar; vollständige Anteilsbestände summieren sich korrekt, unvollständige Bestände werden markiert. Werte bleiben an Bewertungsdatum und Quelle gebunden. |
| P5: Zeitliche Nachlassszenarien | Testamentabhängige Simulation, Sterbereihenfolge und Ereignishistorie. | Beide Sterbereihenfolgen und verschiedene Todeszeitpunkte sind reproduzierbar; Ergebnis nennt Annahmen, Daten-/Regelversion, Berechnungsweg, offene Fragen und notarielle Prüfpunkte. |
| P6: Anwendungsschnittstellen und Betriebsentscheidung | Anwendungsoffene Schnittstellen, Ansichten, Review-Flow und Backend-Benchmark. | Schnittstellen und Referenzansichten unterstützen Lesen, Validieren, Visualisieren und Szenarien; Graphdatenbank nur bei belegtem Nutzen für Query, Parallelität oder Betrieb. |

P0 → P1 → P2 → P3 ist der Familienpfad. P4 baut auf P1/P2 auf; P5 braucht P3/P4 und fachlich freigegebene Regeln. P6 integriert die geprüften Bausteine.

## Durchgehender synthetischer Referenzfall

1. Ein Mann überträgt seiner Frau zu Zeitpunkt T1 ein Haus oder einen dokumentierten Anteil.
2. Der Vater schenkt der Tochter zu T2 ein Auto.
3. Der Vater überträgt dem Sohn in mehreren Jahren Aktien; jede tatsächlich erfolgte Übertragung ist ein eigenes Ereignis.
4. Ein dokumentiertes Testament beziehungsweise mehrere Versionen werden mit ihrer zeitlichen Wirkung berücksichtigt.
5. Szenario A: Vater stirbt zuerst, Mutter später. Szenario B: Mutter stirbt zuerst, Vater später.
6. Todeszeitpunkte werden vor und nach einzelnen Übertragungen variiert. Auch unklare Reihenfolge und fehlende Zeitangaben müssen als Unsicherheit behandelbar sein.

Die Ausgabe soll Genogramm, Vermögen unmittelbar vor dem jeweiligen Todesfall, bereits erfolgte Übertragungen und potenzielle Nachlass-/Anspruchsfolgen nebeneinander zeigen. Eigentumsbestand, erbrechtliche Zuordnung, Pflichtteilsfragen und steuerliche Betrachtung sind getrennte Berechnungsebenen. Konkrete Regeln, Fristen und Rechtsfolgen werden erst nach Quellenprüfung und notarieller Freigabe implementiert; insbesondere keine pauschale Zehnjahreslogik für alle Schenkungen.

## Codex und fachliche Wahrheit

Codex strukturiert Eingaben und schlägt nachvollziehbare Patches vor. Schema- und Referenzvalidierung, Diff und menschliche Bestätigung gehen einer Änderung voraus. Genogramme werden aus belegten Beziehungen erzeugt; Berechnungen laufen deterministisch in Python. Jede Ausgabe ist an Datenstand, Stichtag, Regelversion und Quellenreferenzen gebunden. Offene Tatsachen und fehlende Regeln führen zu markierten offenen Ergebnissen.

Geplante Schnittstellen unterstützen Personen-/Beziehungsvalidierung, Genogramm-Export, Vermögensansicht zu einem Stichtag und Nachlassszenario-Vergleich. Namen und Verträge werden in P0 festgelegt; diese Roadmap behauptet keine bereits verfügbaren Befehle.

## Erweiterung: Unternehmen, Beteiligung und Geschäftsführung

Die Planung erweitert Personen um Beziehungen zu Organisationen im notariellen Gesellschafts- und Nachlasskontext. Sie enthält keine tatsächlichen Unternehmens- oder Rollenangaben einer Person.

Eine Person bleibt ein einziger Stammdatensatz. Familienrolle, Gesellschaftsbeteiligung, Geschäftsführeramt, Anstellungsverhältnis und Vertretung sind getrennte, zeitabhängige Beziehungen. Aus dem Geschäftsführeramt wird keine Beteiligung abgeleitet; aus einem Anteil keine Geschäftsführungsbefugnis. Die konkrete Rechtsform und das anwendbare Recht bleiben Pflichtangaben.

| Modellbaustein | Geplante Felder und Bedeutung |
| --- | --- |
| Organisation | organization_id, Name, Rechtsform, Sitz, Register und Registernummer, Quellen-/Dokumentreferenzen und Prüfstatus. Rechtsformgerechte Modellierung; keine Gleichsetzung aller Unternehmen mit juristischen Personen. |
| Organfunktion | role_assignment_id, person_id, organization_id, Funktion, Bestellung, Annahme, Ende, Gültigkeitszeitraum und Nachweis. Mehrere Unternehmen und mehrere Geschäftsführer pro Unternehmen möglich. |
| Vertretung | Einzel-/Gesamtvertretung, erforderliche Kombinationen, dokumentierte Beschränkungen, gegebenenfalls §-181-BGB-Befreiung, Registerstand und Gültigkeit. Vollmacht und Prokura als eigene Rechtsgrundlagen. |
| Beteiligung | participation_id, Anteilsinhaber (Person oder Organisation), Unternehmen, identifizierter Geschäftsanteil, Nominalbetrag/Quote, Stimmrechte, Bewertungsstichtag und Übertragungsereignisse. Unbekannte Beteiligung ist kein Nullanteil. |
| Rechte und Pflichten | Getrennte Anstellungs-/Vergütungs-, Darlehens-, Bürgschafts- und sonstige Anspruchs-/Verpflichtungsbeziehungen, soweit für den notariellen Fall relevant; keine pauschale persönliche Haftung aus dem Amt ableiten. |
| Nachfolgeregeln und Nachweise | Gesellschaftsvertrag, Gesellschafterliste, Registerauszug, Bestellungsbeschluss, relevante Vollmachten und Verfügungen als geschützte referenzierte Dokumente mit Version und zeitlicher Bindung. |

Beispiel für die GmbH: Geschäftsanteile sind nach [§ 15 Abs. 1 GmbHG](https://www.gesetze-im-internet.de/gmbhg/__15.html) vererblich. Die GmbH hat selbständige Rechte und Pflichten ([§ 13 GmbHG](https://www.gesetze-im-internet.de/gmbhg/__13.html)); Geschäftsführer vertreten sie nach [§ 35 GmbHG](https://www.gesetze-im-internet.de/gmbhg/__35.html). Das Modell trennt deshalb Anteilserbfolge, Unternehmensvermögen und Organ-/Vertretungsnachfolge. Ein Erbe wird nicht allein durch die Erbschaft zum Geschäftsführer. Unternehmensvermögen wird nicht zusätzlich zum Anteilswert als Privatvermögen des Gesellschafters gezählt. Übertragungs-, Einziehungs-, Abfindungs- und Nachfolgeklauseln werden als rechtsform- und dokumentabhängige Prüfpunkte geführt, nicht als pauschale Ergebnisregel.

### Daten- und Graph-Projektion

Zusätzlich zu Personen sind getrennte Entitätstypen für Organisationen, Organfunktionen/Vertretung und Beteiligungen geplant; Dokumente werden als geschützte Referenzen modelliert. Alle Beziehungen verweisen auf stabile fachliche IDs und tragen fachliche Gültigkeit, Erfassungszeit, Quelle und Prüfstatus. Personen werden nicht pro Unternehmen dupliziert.

Die Graph-Projektion unterscheidet beispielsweise Person → ist Geschäftsführer von → Organisation, Person/Organisation → hält Anteil an → Organisation und Person/Organisation → ist Eigentümer von → Vermögensobjekt. Organstellung begründet keine automatischen Zugriffs- oder Freigaberechte; fachliche Vertretung und technische Autorisierung bleiben getrennt.

### Roadmap-Wirkung und zusätzliche Akzeptanzkriterien

- P0/P1: Organisationen und zeitabhängige Funktionen/Beteiligungen in das Modell aufnehmen. AC-06: eine Person kann ohne Dublette Familienmitglied, Geschäftsführer mehrerer Organisationen und gegebenenfalls Gesellschafter sein; unbestätigte Beteiligung bleibt unbekannt.
- P2/P4: Austauschverträge und Vermögensprojektion um diese Entitäten ergänzen. AC-07: Eigentum der Organisation, private Anteile, Darlehen und Bürgschaften bleiben unterscheidbar; Unternehmenswerte werden im Privatvermögen nicht doppelt gezählt.
- P5: Tod, Ausfall, Amtsende und Anteilsübertragung als unterschiedliche Ereignisse prüfen. AC-08: Anteilserbfolge erzeugt keine automatische Organbestellung, Vollmacht oder technische Berechtigung; Änderungen der Vertretung werden anhand belegter Kombinationen und Dokumente geprüft.
- P6: Familiengenogramm, Beteiligungsgraph und Vertretungsansicht aus demselben Datenstand anbieten. AC-09: Ansichten und Szenarien nennen Stichtag, Nachweise, offene Tatsachen und fehlende Regeln.

Zusätzliche synthetische Referenzfälle: ein Geschäftsführer ohne Anteile; ein Gesellschafter-Geschäftsführer; zwei Geschäftsführer mit Gesamtvertretung; eine Beteiligung über eine Holding. Variiert werden Tod beziehungsweise Ausfall der Person, Eintritt eines Erben in die Anteilsposition und spätere Bestellung einer anderen Geschäftsführung. Fehlende Rechtsform, Satzung, Beteiligungsnachweise oder Vertretungsbelege führen zu offenen Prüfpunkten. Handlungsfähigkeit der Organisation und wirtschaftliche Erbfolgen werden getrennt angezeigt.

## Nächster Umsetzungsschritt

P0 fortführen: Den [ausführbaren JSON-/RDF-Piloten](../../docs/de/architektur/p0-pilot-benutzung.md) in weitere eigenständige Fachdefinitionen und Detailprofile ausbauen sowie externe Import-/Versionsverträge konkretisieren. Die synthetischen Auto-/Aktien-/Bekleidungsfälle ergänzen den erhaltenen Familienfall. Vor weiterer Umsetzung gelten die Design-, Spec-, Review-, Datenschutz- und Qualitätsregeln dieses Projekts.

Die erste Umsetzungsspezifikation entsteht in ontologie8/schema und legt den eigenständigen Modell- und Versionierungsvertrag fest.
