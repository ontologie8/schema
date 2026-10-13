# Erbausschlagung: synthetische Modellprüfungen

Stand: 2026-10-13 · Lizenz: CC-BY-4.0

## Auftrag, Scope und Entscheidung vor Umsetzung

Auftrag: Die Erbausschlagung aus `notariat8/ontology` als weitere Testfälle aufnehmen. AC-04, AC-10/11/12, AC-14/18/19 und AC-20 bilden den Umfang. Vier synthetische Ausgangsfälle erhalten unabhängig festgelegte Erwartungen, negative Varianten und historische Nachweisabfragen.

Der Prüfvertrag erhält eine eigene ID und Version 0.1.0 unter `profile/anwendungsfaelle/erbausschlagung/`. Er ist ein ergänzender Vertrag für Modellproben, noch kein produktives Fachmodul und keine Erweiterung des bestehenden Kernschemas. Gemeinsame Text-, Identitäts- und Zeittypen werden aus dem Kernschema referenziert und offline aufgelöst. Die Kernversion 0.1.0 und ihre bisherigen Beispiele bleiben verwendbar.

Alternative: Die Rechtstypen sofort in das bisherige Pilotregister einbauen. Das würde dessen Vertragsumfang ändern und benötigt zuerst einen allgemeinen Modul- und Versionsvertrag. Alternative: Nur Markdown-Beispiele übernehmen. Das würde die zeitlichen und semantischen Fehler nicht ausführbar prüfen. Der eigene Prüfvertrag begrenzt den Auftrag und macht die offenen Fachfragen sichtbar.

Risiken: Versand, Aushändigung und Gerichtseingang könnten zusammenfallen; Eingangsbestätigung könnte als Wirksamkeit gelten; Eltern-Kind-Beziehung könnte automatisch Erbenstellung oder Vertretungsmacht erzeugen. Ein Todestag könnte als Fristbeginn geraten werden. Ein unbekannter Auftrag oder unbekannte Genehmigung darf nicht zu einer positiven Entscheidung werden.

Plan: Quelle und Primärnormen prüfen; A–D in synthetische Eingaben mit getrennten Personen, Beziehungen, Prüfständen und Nachweisen übertragen; JSON Schema und Referenzen validieren; Nachweisabfragen nach fachlichem und Wissensstichtag prüfen; Ergebnisse sowie Text-, Zeit- und Personenbeziehungen nach Turtle-/JSON-LD-Austausch vergleichen; negative Varianten und bestehenden Pilot ausführen; vollständigen Diff und CI vor Merge prüfen.

Review vor Umsetzung: Die Quelle ist ein ungeprüfter Entwurf auf einem eigenen Zweig. Deshalb werden ihre Szenarien als Modellproben übernommen. Kein Genehmigungserfordernis, Fristende, Erbe, Vertretungsrecht oder Wirksamkeitsurteil wird berechnet. Fehlende Daten bleiben unbekannt. Die neue RDF-Abbildung gilt nur für diesen Prüfvertrag; sie erweitert nicht still den bisherigen RDF-Kernvertrag. Personenbezogene Angaben aus Importnotizen und der vollständige Ablaufplan werden nicht kopiert.

## Herkunft und Lizenz

Quellprojekt: [notariat8/ontology](https://github.com/notariat8/ontology), veröffentlichter Zweig `codex/erbausschlagung-sop-depth`, überprüfter Stand **42631313ab5679a029db59d3bb714bdeb3f0eab6**. Dieser Stand ist kein Merge in `main`; dort liegt **d0b69e48d90b2ae42f81406833c094f74d9fdf77**.

- [Vier synthetische Szenarien A–D](https://github.com/notariat8/ontology/blob/42631313ab5679a029db59d3bb714bdeb3f0eab6/docs/erbausschlagung/synthetische-szenarien.md).
- [Fachbausteine und Beziehungen](https://github.com/notariat8/ontology/blob/42631313ab5679a029db59d3bb714bdeb3f0eab6/cases/erbausschlagung/ontology.ttl).
- [Lizenz- und Urheberhinweise](https://github.com/notariat8/ontology/blob/42631313ab5679a029db59d3bb714bdeb3f0eab6/NOTICE): funktion8 / ofunk; bereitgestellte Ablaufvorlage von Hannah-Silvia Heise. Fachtexte stehen unter CC-BY-4.0. Die Szenarien werden hier paraphrasiert, mit eigenen synthetischen Zeitwerten ergänzt und als technische Prüfungen umgesetzt. Code und Schemas stehen unter AGPL-3.0-or-later; die abgeleitete Szenariobeschreibung bleibt CC-BY-4.0.

Quellkennzeichen wie `local.decision.execution` dienen ausschließlich der Herkunftszuordnung. Es gibt keine Imports, Netzabfragen, fremden Namensräume als führende Identität oder Abhängigkeit von NaC beziehungsweise `ontology` zur Laufzeit. Der Quellentwurf ist nicht als fachlich freigegeben zu behandeln.

Primärquellen, geprüft am 2026-10-13: [§ 1944 BGB](https://www.gesetze-im-internet.de/bgb/__1944.html) zum kenntnisbezogenen Fristbeginn, [§ 1945 BGB](https://www.gesetze-im-internet.de/bgb/__1945.html) zu Erklärung, Form und Vollmacht sowie [§ 1953 BGB](https://www.gesetze-im-internet.de/bgb/__1953.html) zur Wirkung. Diese Normen begründen die getrennten Prüfgegenstände; der Testcode implementiert keine Rechtsfolgenberechnung. Die [Justiz-Services](https://www.service.justiz.de/erbausschlagung) beschreiben Kenntnis, Kinder und mögliche Annahmehandlungen allgemein.

## Unabhängige Erwartungen

| Fall | Eingabe | Erwartung der Modellprüfung |
| --- | --- | --- |
| EA-A | Volljährige ausschlagende Person, Vollzugsauftrag an Notariat; Versand bekannt, Gerichtseingang erst später erfasst | Vor Erfassung bleibt Gerichtseingang unbekannt; danach wird nur Eingang nachgewiesen. Keine Wirksamkeitsentscheidung. |
| EA-B | Selbsteinreichung, quittierte Aushändigung; keine gesonderte Nachkontrolle | Aushändigung ist kein Gerichtseingang; keine automatische Überwachung durch das Notariat. |
| EA-C | Ausschlagende Person mit minderjährigem Kind; mögliche Berufung und Vertretungs-/Genehmigungsfragen offen | Kind bleibt eigene Person. Eltern-Kind-Beziehung erzeugt keine Erbenstellung und keine Vertretungsmacht. Je Person bleiben getrennte Prüfstände und Kenntnisnachweise möglich. |
| EA-D | Mögliche Annahmehandlung, Risikoprüfung offen | Offene Risikoprüfung bleibt sichtbar; keine automatische Annahme und keine Wirksamkeitszusage. |

Zusatzvarianten prüfen unbekannten Vollzugsauftrag, gesonderte Nachkontrolle, fehlende Kenntnisbelege, unscharfen Eingangszeitpunkt, fehlende Quellenreferenz, unzulässige Rollenvermischung, widersprüchliche Nachweise und fehlende Sprachkennzeichen. Alle IDs, Personen und Zeitwerte sind frei erfunden. Es gibt keine Dokumentinhalte, Registerdaten, Aktenzeichen oder realen Mandanten.

Ein Nachweis trägt eigene Identität, Bezug zur Person, Typ, fachlichen Zeitpunkt, Erfassungszeit und synthetische Quelle. Nachweisabfragen geben `belegt`, `unbekannt` oder `zeitlich_unbestimmt` zurück. Unbekannte Kenntniszeit ist eine ausdrückliche Variante und wird nicht durch den Todestag ersetzt. Prüfstände sind synthetische Angaben im jeweiligen Fall; `bestaetigt` behauptet keine externe fachliche Freigabe.

Der Fallkontext (Vollzugsweg, vereinbarte Nachkontrolle und Risikohinweis) ist eine statische Annahme des jeweiligen Referenzfalls. Historische Auswahl gilt hier für datierte Nachweise und Prüfstände. Änderungen oder Rücknahmen des Fallkontexts benötigen künftig einen eigenen Revisionsvertrag. Bestätigte Genehmigungsprüfungen bedeuten nur einen erfassten Prüfstand; der Vertrag führt keine gerichtlichen Genehmigungen oder Ausnahmetatbestände.

## Validierung und Benutzung

`python scripts/pruefe_erbausschlagung.py` prüft die vier Fälle, ihre unabhängigen Erwartungen und tatsächlich serialisierte RDF-Rückwege. `python -m unittest discover -s tests -v` führt außerdem die negativen Varianten und die bisherigen Pilottests aus. Die Projekt-CI führt beide Prüfverträge aus.

Die RDF-Abbildung erhält eigene Fall-/Personen-/Beziehungs-/Nachweis-IRIs, strukturierte Zeiten und Sprachliterale. Sie akzeptiert nur den geschlossenen Prüfvertrag, lehnt fremde Prädikate und nicht angebundene Tripel ab und validiert das rückgewonnene JSON. Die Rückkonvertierung ist keine Unterstützung beliebiger RDF-Ontologien.

Umsetzungsreview: Referenzen müssen paketweit auf eindeutige Identitäten zeigen und Nachweise zur betroffenen Fallrolle gehören. Doppelte Prüfstände werden zurückgewiesen; mehrere Fassungen brauchen einen ausdrücklich erweiterten Vertrag. Unscharfer Eingang und unbekannte Kenntniszeit bleiben unbestimmt. Die historische Grenze des festen Fallkontexts ist oben ausdrücklich dokumentiert. Der Inhalt der Fixtures wurde auf frei erfundene Personen-/Quellen-IDs und fehlende Dokumentpayloads geprüft.

Lokale Evidenz: Struktur-/Linkprüfung, bisheriger Pilot und Erbausschlagungs-Prüfroutine bestanden. Insgesamt 54 Testmethoden bestanden, davon 18 neue. Die vier Fälle enthalten neun synthetische Personen und 17 Nachweise; fünf unabhängige Abfragen behalten nach Turtle und JSON-LD ihre Erwartungsergebnisse. Der Erbausschlagungsgraph enthält 598 Tripel.

## Nächster Schritt

Die Erbausschlagungsfälle beim allgemeinen Modul-/Versionsvertrag als Referenz für ein Rechtsfachmodul verwenden; fachlich freigegebene Rechtsregeln erst in einem gesonderten Auftrag ergänzen.
