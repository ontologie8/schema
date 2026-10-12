# Implementierungsspezifikation: Schema- und RDF-Pilot 0.1.0

Stand: 2026-10-12 · Scope und Plan vor Implementierung geprüft; Pilot umgesetzt
Lizenz: CC-BY-4.0

## Entscheidung und Grenzen

Für den kleinen Pilot ist JSON mit JSON Schema 2020-12 der führende Austauschvertrag. RDF ist eine daraus erzeugte und zurückprüfbare Repräsentation. Die Entscheidung gilt für diesen Vertragsstand; sie legt keinen produktiven Speicher fest. Der [Weltmodellentwurf](p0-weltmodell.md), [Zeitvertrag](zeit-und-bewertungen.md) und [Textvertrag](mehrsprachige-werte.md) bleiben die fachliche Grundlage.

Alternative RDF-first: benötigt ebenso einen geschlossenen Eingabe-/Exportvertrag und explizite Revisionsvalidierung. Alternative separate Modellsprache: würde einen zusätzlichen Generatorvertrag erfordern. JSON-first hält im Pilot die konkrete Datenstruktur unmittelbar prüfbar; die erwarteten Ergebnisse müssen auch nach RDF-Rückkonvertierung gelten. Ein späteres anderes Autorenformat darf diesen Vertrag nicht stillschweigend verändern.

Version 0.1.0 ist ein Entwicklungsvertrag. Es entsteht kein produktives Release, keine Rechts-/Steuerberechnung, kein Kursimport und keine GitHub-/SharePoint-/S3-Anbindung. Die im Repo enthaltenen Instanzen und Quellen sind vollständig synthetisch. Die allgemeine Schemaform ist auch außerhalb dieses Repositories anwendbar.

## Artefakte und Aufgaben

| Bereich | Artefakt und Verantwortung |
| --- | --- |
| Modellkern | JSON Schema für Entitäten, Textwerte, Zeit, Revisionen und Szenarien |
| Begriffsregister | Stabile Typ-/Beziehungs-IDs, zulässige Beteiligte und deutsche Bezeichnungen |
| Fachmodule | Versionierte Manifeste für den Finanz- und Bekleidungspilot |
| Profil | Verknüpfung des geprüften Vertragsstands und seiner Module |
| Abbildung | RDF-Vokabular sowie Python-Hin-/Rückweg mit expliziten Referenzen und Sprachliteralen |
| Referenzdaten | Synthetische Auto-/Aktien-/Bekleidungsdaten und unabhängig festgelegte Erwartungen |
| Prüfung | Strukturvalidierung, Referenz-/Revisionsvalidierung, Stichtagsabfragen, Szenarien und negativer Datenumfang |

Alle Mengen und Geldbeträge werden im Austausch als Dezimalzeichenfolgen geführt; Berechnungen verwenden Dezimalarithmetik. Einheiten, Währung und Wertart sind eigene Angaben. Sprachwerte haben `wert`, `sprache` und optional `richtung`. Die synthetischen Textinhalte bleiben deutsch; andere gültige Sprachkennzeichen werden in Tests als technische Parameter verwendet.

## Datensatzvertrag

Ein Modellpaket besitzt eine ID, den Vertragsstand und Sammlungen für Entitäten, Revisionen und Szenarien. Entitäten besitzen ID, registrierten Typ und Textbezeichnungen. Modell-/Methodenentitäten können eine eigene Version tragen. Eine Quellenreferenz verweist im Pilot auf eine explizite Quellenentität.

Eine Revision besitzt ID, Aussage-ID, Aussageart, registrierten Typ, Subjekt und optional Objekt, fachliche Zeit, Erfassungszeit, Quelle, Prüfstatus und typisierte Nutzdaten. Eine Nachfolgerevision verweist auf die Vorgängerrevision. Methodenzuordnung und Szenarioverweis sind eigene Angaben. Freie unbekannte Felder werden zurückgewiesen; Erweiterungen erfolgen über registrierte Typen und eine ausdrücklich versionierte Vertragserweiterung.

Ein Szenario bindet Methode und Version, Eingaberevisionen, Zielzeit, Berechnungszeit und explizite Parameter. Im Pilot werden zwei klar benannte synthetische Rechenarten unterstützt: wiederholter Wertfaktor und Bestandswert bei hypothetischem Kurs. Das sind Referenzalgorithmen, keine allgemeine Wertentwicklungsannahme.

## Validierung und Abfragen

JSON Schema prüft Form, Pflichtangaben und geschlossene Objekte. Eine zusätzliche semantische Prüfung prüft Sprachkennzeichen, Zeitpräzision, registrierte Typen, IDs, Referenzen, Methodenversionen und Revisionsketten. Unbekannte Typen werden nicht als bereits unterstützte Erweiterung ausgegeben.

Aktive Revisionen werden je Aussage für einen Wissensstichtag ermittelt. Parallele Wurzeln, Verzweigungen, rückdatierte Ablösungen und Zyklen werden zurückgewiesen. Gleiche Erfassungszeit innerhalb einer Kette erfordert eine explizite steigende Reihenfolge. Rücknahmen bleiben in der Historie und entfernen die Aussage aus späteren aktiven Ansichten.

Historische Auswahl erhält fachlichen Stichtag und Wissensstichtag. Sie liefert sichere Treffer und unbestimmte zeitliche Zuordnungen getrennt. Die Pilotintervalle sind `[Beginn, Ende)`. Bei Tages-/Monats-/Jahrespräzision werden Grenzen nicht auf erfundene Uhrzeiten reduziert; überlappende unsichere Grenzen liefern ein unbestimmtes Ergebnis. Offene Enden und unbekannte Grenzen bleiben verschieden.

Bewertungsabfragen liefern konkurrierende Quellen. Kaufpreise werden nicht als Marktwert fortgeschrieben. Bestandsrechnung verlangt einen expliziten Anfangsbestand und vollständige Bewegungen im gewählten Kontext. Fehlen Menge, Kurs oder passende Währung/Stückbasis, wird ein offenes Ergebnis zurückgegeben. Szenarien verändern keine Eingabehistorie und werden in normalen Bestands-/Bewertungsansichten ausgeschlossen.

## RDF-Vertrag

Das Vokabular verwendet den projektspezifischen URN-Namensraum `urn:ontologie8:kern:`. Entitäten, Revisionen, Szenarien und das Modellpaket behalten ihre IDs. Referenzfelder werden zu RDF-IRIs; strukturierte Teilwerte werden eigene Ressourcen. Aussagen stehen an der jeweiligen Revision und werden nicht als unbedingte zeitlose Tatsachen am Objekt behauptet.

Textressourcen tragen `rdf:value` mit Sprachkennzeichen; optionale Richtung bleibt als ausdrückliche Angabe erhalten. Die Sammlung der Bezeichnungen ist ungeordnet. Wiederholungen werden im kanonischen Vertrag zurückgewiesen oder als eigenständige eindeutig identifizierte Aussagen modelliert. Leere Sammlungen bleiben durch explizite Abbildungsmetadaten von fehlenden optionalen Feldern unterscheidbar.

RDF-Rückkonvertierung akzeptiert nur diesen Mappingvertrag. Unbekannte Prädikate, mehrfache Werte für ein Einzelfeld, ungeeignete Literaltypen, fehlende Identitäten und zyklische Teilstrukturen werden zurückgewiesen. Das zurückgewonnene JSON wird erneut strukturell und semantisch geprüft. Ein fremder RDF-Graph ist damit noch kein unterstütztes Eingabeformat.

Semantische Gleichheit wird auf kanonischen Daten geprüft: Sammlungsreihenfolge, Sprachkennzeichen-Schreibkonvention und die Lexik dezimaler Zahlen beeinflussen die Bedeutung nicht. Zeitpräzision, IDs, Quellen, Revisions-/Szenariobezug und Richtung müssen dagegen erhalten bleiben. Die kanonische Form ist im Pilot dokumentiert und getestet.

## Prüfplan und Review vor Code

AC-03/10/11/12: Schemas prüfen, Textwerte mit zusätzlichen Kennzeichen und Richtung ohne Feldänderung austauschen, RDF-Sprachliterale tatsächlich im Graph prüfen, Rückkonvertierung und geänderte Sammlungsreihenfolge vergleichen.

AC-14/15/18: Kaufpreisrevision, verspätete Eigentumsübertragung, Grenze genau am Übergang, Rücknahme, gleichzeitige Revisionen und unbekannte Zeitpräzision mit unabhängigen Ergebnissen prüfen. Ungültige Intervalle und konkurrierende exklusive Eigentumszuordnungen zurückweisen.

AC-16/17: Anfangsbestand, Kurs-/Währungsbasis, zwei unabhängige Quellen, getrennte Prognosen und unveränderte Eingaben mit festgelegten Dezimalergebnissen prüfen. Fehlende Daten dürfen nicht zu Null oder einer geratenen Bewertung werden.

AC-04/19: Alle Referenzdaten synthetisch, Modul-/Profilversionen konsistent und Finanz-/Bekleidungsfälle im selben Kern. Die CI prüft Struktur, Semantik, Abbildung und Tests. Eine Synthetik-Kennzeichnung allein beweist keine Abwesenheit von Echtdaten; die konkreten Fixtures werden inhaltlich reviewt.

Review-Ergebnis vor Implementierung: JSON Schema genügt nicht für Revisions-/Referenzprüfung; diese wird separat eingeplant. Die RDF-Abbildung benötigt explizite Metadaten für leere Sammlungen und kontrollierte Rückkonvertierung. Historische Auswahl muss unbestimmte Fälle ausgeben können. Der Plan berücksichtigt diese Korrekturen.

## Durchführung

1. Kernschema, Register und Modul-/Profilmanifeste anlegen.
2. Synthetische Daten und unabhängige Erwartungen als gemeinsame Eingaben erstellen.
3. Semantische Validierung, zeitliche Auswahl und Referenzrechnungen umsetzen.
4. RDF-Abbildung und Rückkonvertierung umsetzen; Ergebnisse vor und nach dem Austausch vergleichen.
5. Tests, Review und Korrekturen durchführen; ausführbare CI ergänzen und über PR liefern.

RDFLib und jsonschema werden ausschließlich im verifizierten lokalen Projekt-Python verwendet; die CI installiert die festgehaltenen Abhängigkeiten. Die Standardbibliothek führt die Tests aus. [RDFLib](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.graph/) und [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/validate/) beschreiben die verwendeten Bibliotheksschnittstellen.

## Umsetzungsreview und Evidenz

Der [ausführbare Pilot](p0-pilot-benutzung.md) implementiert den Scope. Der Review ergänzte eine Prüfung der getrennten Aussage-/Ressourcenidentität, Prognosezielbindung, Eingaberevisionen und Anfangsbestandsgrenzen. Große Dezimalwerte werden beim RDF-Austausch nicht durch den Standard-Dezimalkontext gerundet; Referenzrechnungen wählen ausreichende Genauigkeit anhand des Eingabeumfangs.

Positive und negative Tests überführen ZF-01 bis ZF-27 in ausführbare Erwartungen. Die Prüfroutine kontrolliert dieselben historischen und numerischen Ergebnisse vor und nach tatsächlich serialisiertem Turtle und JSON-LD. Weitere Fachprofile, OWL-Time-/PROV-O-Alignment, SHACL und produktive Speicheranbindungen sind nicht Bestandteil dieser Implementierung.
