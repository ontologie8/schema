# Synthetische Referenzfälle für den P0-Zeitvertrag

Stand: 2026-10-12 · Fachliche Designprüfung und ausführbarer Pilot vorhanden
Lizenz: CC-BY-4.0

Alle Personen, Objekte, Instrumente, Quellen, Vorgänge und Zahlen sind vollständig erfunden. Die Kurz-IDs in den Tabellen stehen für getrennte synthetische Entitäten. Es liegen keine echten Gegenstände, Kurse, Belege oder Produktdaten zugrunde.

Diese Fälle prüfen den [Zeitvertrag](../architektur/zeit-und-bewertungen.md) im [Weltmodell](../architektur/p0-weltmodell.md). Eingaben und erwartete Ausgaben wurden vor der Query-Implementierung unabhängig festgelegt. Die Tabellen beschreiben die Prüfziele; der [Pilot](../architektur/p0-pilot-benutzung.md) führt sie inzwischen mit konkreten synthetischen Daten und Tests aus.

## Fall A: Auto, Preisrevision und Eigentumswechsel

Entitäten: Personen `P-A` und `P-B`, Auto `AUTO-1`, getrennte synthetische Quellen. Eigentum wird im Fall als vollständig belegte Gesamtzuordnung behandelt; die Kaufereignisse und die Eigentumsbeziehungen sind getrennt.

| Aussage/Vorgang | Fachliche Zeit | Im System erfasst | Inhalt |
| --- | --- | --- | --- |
| Kauf `K-1`, Revision `K-1-R1` | 2024-03-10T10:00:00Z | 2024-03-20T09:00:00Z | P-A kauft AUTO-1; Gesamtpreis zunächst mit 30.000 EUR erfasst |
| Korrektur `K-1-R2` | Derselbe Kaufzeitpunkt | 2024-04-01T09:00:00Z | Eingabefehler korrigiert: Gesamtpreis 28.000 EUR; löst K-1-R1 ab |
| Eigentum `E-A-R1` | Ab 2024-03-10T10:00:00Z, Ende nach damaligem Wissen offen | 2024-03-20T09:00:00Z | P-A besitzt 100 Prozent von AUTO-1 |
| Eigentumsübertragung `U-1` | 2026-08-01T12:00:00Z | 2026-08-02T09:00:00Z | Übergang der gesamten Eigentumsposition von P-A auf P-B |
| Eigentum `E-A-R2` | [2024-03-10T10:00:00Z, 2026-08-01T12:00:00Z) | 2026-08-02T09:00:00Z | Erfasst das belegte Ende von E-A; löst E-A-R1 ab |
| Eigentum `E-B-R1` | Ab 2026-08-01T12:00:00Z, Ende nach Wissen offen | 2026-08-02T09:00:00Z | P-B besitzt 100 Prozent von AUTO-1 |

Eine Anfrage zum Kaufzeitpunkt mit Wissensstichtag 2024-03-15 findet noch keine erfasste Kauf- oder Eigentumsaussage. Das Ergebnis ist unbekannt, nicht „kein Kauf“ oder „kein Eigentümer“.

| Prüffall | Fachlicher Bezug / Wissensstichtag | Unabhängig festgelegtes Ergebnis |
| --- | --- | --- |
| ZF-01 | Kauf / Wissen 2024-03-25T00:00:00Z | Kaufpreis 30.000 EUR laut damaliger Revision |
| ZF-02 | Derselbe Kauf / Wissen 2024-04-02T00:00:00Z | Kaufpreis 28.000 EUR; ursprüngliche Revision weiter nachvollziehbar |
| ZF-03 | Eigentum 2026-08-01T12:00:00Z / Wissen 2026-08-01T18:00:00Z | P-A laut damals erfasstem Stand; spätere Übertragung noch unbekannt |
| ZF-04 | Derselbe Eigentumsstichtag / Wissen 2026-08-03T00:00:00Z | P-B; P-A wegen ausgeschlossenem Intervallende nicht mehr zugeordnet |
| ZF-05 | Eigentum 2026-08-01T11:59:59Z / Wissen 2026-08-03T00:00:00Z | P-A; Beginn der neuen Zuordnung liegt später |
| ZF-06 | Kauf / Wissen genau 2024-04-01T09:00:00Z | K-1-R2 aktiv; K-1-R1 in der Historie, nicht zugleich aktuelle Revision |

Die Abfrage bezeichnet ZF-03 als damaligen Kenntnisstand. Sie behauptet keine trotz Übertragung fortbestehende tatsächliche Eigentumsposition.

## Fall B: konkurrierende Bewertung und Prognosen des Autos

| Datensatz | Bezug | Inhalt und Herkunft |
| --- | --- | --- |
| `B-A` | AUTO-1, Marktwert zum 2026-06-01, Tagespräzision | Schätzung 22.000 EUR, Quelle Q-A, erfasst 2026-06-03T09:00:00Z |
| `B-B` | Dasselbe Auto, dieselbe Wertart und derselbe Tag | Unabhängige Schätzung 21.000 EUR, Quelle Q-B, erfasst 2026-06-04T09:00:00Z |
| `S-A` | Ziel 2028-06-01; Ausgangswert B-A | Hypothetischer Faktor 0,90 pro Jahr über genau zwei Modelljahre |
| `S-B` | Dasselbe Ziel und derselbe Ausgangswert | Hypothetischer Faktor 0,95 pro Jahr über genau zwei Modelljahre |

Beide Szenarien werden am 2026-06-05 berechnet. S-A bindet das synthetische Modell M-A in Version 1.0.0, S-B das synthetische Modell M-B in Version 1.0.0. Beide verwenden die erste Revision B-A-R1 der Bewertung B-A. Zwei Modelljahre sind hier ein festgelegter Parameter; es wird keine allgemeine Tages-/Jahresumrechnung eingeführt.

Erwartungswerte: S-A = 22.000 × 0,90 × 0,90 = 17.820 EUR. S-B = 22.000 × 0,95 × 0,95 = 19.855 EUR. Die Faktoren sind reine synthetische Annahmen und keine Regel über Autos.

| Prüffall | Frage | Erwartetes Ergebnis |
| --- | --- | --- |
| ZF-07 | Welche Schätzungen sind nach Erfassung beider Quellen vorhanden? | B-A und B-B bleiben erhalten; späterer Import macht Q-B nicht zur Korrektur von Q-A |
| ZF-08 | Wie hoch ist der eine Marktwert ohne Auswahlprofil? | Keine unbegründete eindeutige Auswahl; beide Schätzungen mit Quelle und Stichtag zurückgeben |
| ZF-09 | Welche Werte werden zum Zieltag prognostiziert? | S-A 17.820 EUR und S-B 19.855 EUR in getrennten Szenarien |
| ZF-10 | Ändert die Prognose den Kaufpreis oder B-A? | Nein; K-1-R2 bleibt 28.000 EUR, B-A bleibt eine damalige Schätzung von 22.000 EUR |
| ZF-11 | Ist B-A ein nachgewiesener Wert an einem beliebigen späteren Tag? | Nein; spätere Übernahme benötigt eine explizite Fortschreibungs-/Auswahlregel |

## Fall C: Aktienbestand, Kursbasis und Zukunft

Entitäten: Person P-A, fiktives Instrument `INSTRUMENT-1`, Depotposition `POSITION-1`. Der Anfangsbestand vor C-1 ist ausdrücklich mit null Stück belegt; er wird nicht aus fehlenden Angaben abgeleitet. Alle Bewegungen sind in diesem Fall vollständig belegt, rechtzeitig erfasst, in derselben Währung EUR und ohne weitere Bestandsereignisse. Es gibt keinen echten Emittenten oder Ticker.

| Ereignis | Fachlicher Tag | Mengenwirkung |
| --- | --- | --- |
| Erwerb C-1 | 2025-03-10 | +10 Stück, Kaufpreis 100 EUR je Stück |
| Erwerb C-2 | 2025-06-01 | +5 Stück, Kaufpreis 110 EUR je Stück |
| Verkauf C-3 | 2025-09-01 | −3 Stück, Verkaufspreis 120 EUR je Stück |
| Kursbeobachtung C-4 | 2026-06-01 | 125 EUR je Stück auf einer ausdrücklich bezeichneten synthetischen Markt-/Kursbasis |

Zum 2026-06-01 beträgt der Bestand 10 + 5 − 3 = 12 Stück. Seine Bewertung anhand C-4 ergibt 12 × 125 = 1.500 EUR. Die Kaufpreise sind weiterhin Teil ihrer Transaktionen. Diese Prüfung berechnet weder steuerliche Anschaffungskosten noch Rendite.

Zwei isolierte Szenarien halten den Bestand von 12 Stück konstant und setzen einen hypothetischen Kurs von 150 beziehungsweise 80 EUR zum 2028-06-01. Sie binden die ersten Revisionen C-1 bis C-4 und das synthetische Bestandsmodell M-C in Version 1.0.0; ihre Berechnung erfolgt am 2026-06-02. Ihre erwarteten Bestandswerte sind 1.800 beziehungsweise 960 EUR. Sie sind keine beobachteten Kurse.

| Prüffall | Frage | Erwartetes Ergebnis |
| --- | --- | --- |
| ZF-12 | Bestand und Bewertung am 2026-06-01? | 12 Stück, 1.500 EUR nach genau dieser Kursbasis |
| ZF-13 | Prognostizierte Bestandswerte? | 1.800 und 960 EUR; Ausgangsbestand und Kursbeobachtung unverändert |
| ZF-14 | Für die Position fehlt eine passende Kursbeobachtung? | Bewertung offen; kein geratenes Nullergebnis und keine automatische Fortschreibung eines Kaufpreises |
| ZF-15 | Nur USD-Kurs zu einem EUR-Bewertungsauftrag vorhanden? | Keine stille Gleichsetzung; passende versionierte Währungsumrechnung mit Stichtag nötig |
| ZF-16 | Separater Fall: Split 2:1 aus 10 Stück bei 100 EUR, vergleichbare neue Kursbasis 50 EUR | 20 Stück und 1.000 EUR Gesamtwert; keine scheinbare Halbierung des Bestandswerts durch isolierten Kursvergleich |

Der Splitfall ist unabhängig von POSITION-1 und verändert ihre Ereignisfolge nicht. Unbekannte weitere Ereignisse würden die Vollständigkeit der Bestandsrekonstruktion einschränken; das Rechenbeispiel setzt diese Vollständigkeit ausdrücklich voraus.

## Fall D: Kleidungsstück, Zustand und Empfehlung

Entitäten: Person P-A, konkretes Kleidungsstück `KLEIDUNG-1`, Produktmodell `MODELL-1`, Shop `SHOP-1` und Angebot `ANGEBOT-1`. Das Kleidungsstück ist eine einzelne Instanz; Produktmodell und Angebot erhalten eigene IDs.

| Aussage/Vorgang | Fachlicher Bezug | Inhalt |
| --- | --- | --- |
| Kauf D-1 | 2025-05-01 | P-A kauft KLEIDUNG-1 für 100 EUR |
| Zustandsbeobachtung D-2 | 2026-04-01 | Beschädigung dokumentiert |
| Reparatur D-3 | 2026-04-10 | Reparaturereignis mit synthetischem Nachweis |
| Zustandsbeobachtung D-4 | 2026-04-11 | Reparierter Zustand festgestellt; früherer Zustand bleibt historisch |
| Bewertung D-5 | 2026-06-01 | Geschätzter Wiederverkaufswert 30 EUR, eigene Methode und Quelle |
| Empfehlung D-6 | Eingabestand einschließlich D-4 | Stilberatung schlägt eine Kombination vor; Anlass und Kriterien ausdrücklich genannt |

Die Empfehlung D-6 bindet die erste Revision der Zustandsbeobachtung D-4 und die synthetische Beratungsmethode M-D in Version 1.0.0. Als Anlass ist ein fiktiver Geschäftstermin, als Kriterium die Verwendung eines vorhandenen reparierten Kleidungsstücks vorgegeben. Eine bestimmte Kombination ist ein späteres methodenabhängiges Ergebnis; dieser Fall prüft die Trennung der Aussagearten.

| Prüffall | Frage | Erwartetes Ergebnis |
| --- | --- | --- |
| ZF-17 | Gehören Kaufpreis, Wiederverkaufswert und Zustand zu einem einzigen Wert? | Nein: 100 EUR Transaktionspreis, 30 EUR Schätzung und getrennte Zustandsbeobachtungen |
| ZF-18 | Muss Reparatur automatisch einen bestimmten neuen Wert oder Zustand setzen? | Nein; Reparaturereignis, Zustandsbeobachtung und Bewertung sind eigene Aussagen |
| ZF-19 | Ist eine Stilberatung eine bestätigte Objekteigenschaft? | Nein; Empfehlung nennt Kriterien und Eingaberevisionen und bleibt von Bestand/Zustand getrennt |
| ZF-20 | Dupliziert eine neue Produktbezeichnung in einer anderen Sprache das Kleidungsstück? | Nein; stabile IDs bleiben erhalten. Phase 1 pflegt nur deutsche Textinhalte. |

## Negative und unbestimmte Fälle

| Prüffall | Eingabe | Erwartetes Verhalten der späteren Umsetzung |
| --- | --- | --- |
| ZF-21 | Vollständiges Intervall mit Ende vor Beginn oder Null-Länge für eine als Zeitraum definierte Zuordnung | Zurückweisen; Zeitpunkt besitzt einen eigenen Typ |
| ZF-22 | Nur Monat eines Kaufs bekannt; zweites Ereignis liegt innerhalb desselben Monats | Keine erfundene genaue Reihenfolge; Ergebnis unbestimmt |
| ZF-23 | Eigentumsbeginn ausdrücklich unbekannt | Keine sichere Stichtagszuordnung daraus ableiten |
| ZF-24 | Revisionsverweis bildet einen Kreis oder widersprüchliche parallele Ablösung | Zurückweisen beziehungsweise Konflikt melden; keine beliebige aktive Revision wählen |
| ZF-25 | Zwei exklusive Gesamtzuordnungen überlappen | Konflikt melden. Bei anteiligem Eigentum andere profilabhängige Prüfung verwenden. |
| ZF-26 | Zukünftige Lieferung dokumentiert geplant, Zielzeit bereits gesetzt | Geplant erhalten; weder automatisch als eingetreten noch als reine Wertprognose behandeln |
| ZF-27 | Ein 2024 erstellter Beleg wird erst 2026 importiert | Quellzeit 2024 getrennt erhalten; Erfassungszeit 2026, kein rückwirkender Kenntnisstand im System |

## Review-Ergebnis und nächste Prüfungen

Fachlicher Review des Entwurfs:

- Auto, Aktien und Kleidung verwenden dieselben Identitäts-, Zeit-, Herkunfts- und Bewertungsbausteine. Unterschiede liegen in Fachtypen, Mengeneinheiten, Methoden und benötigter Detailtiefe.
- Die Preisrevision in ZF-01/02/06 ist von konkurrierenden Quellen in ZF-07/08 unterschieden. Dadurch wird ein späterer Import nicht pauschal zur Wahrheit.
- ZF-03 bis ZF-05 erklären Wissenszeit und exklusive Intervallgrenzen. Eine neue Revisionshistorie wird nicht durch Überschreiben eines Datums ersetzt.
- ZF-09/13/19 trennen Szenario beziehungsweise Empfehlung von beobachteten oder geschätzten Aussagen. Die Prognosen erhalten keine feste Richtung einer Wertentwicklung.
- ZF-11/14/15/16/22/23 verhindern unbegründete Fortschreibung, falsche Währungs-/Stückbasis und erfundene Zeitpräzision.
- ZF-27 verhindert eine Rückdatierung des Systemwissens durch importierte Quellzeitstempel.

Die einfachen Dezimalrechnungen und historischen Abfragen werden gegen die unabhängig angegebenen Ergebnisse geprüft. Struktur und lokale Verweise prüft der Projektvalidator. Die [Pilotprüfroutine](../../../scripts/pruefe_pilot.py) prüft Schema, Modulstände und erwartete Ergebnisse vor und nach Turtle-/JSON-LD-Rückkonvertierung.

ZF-01 bis ZF-27 sind in [ausführbare Tests](../../../tests/test_pilot.py) überführt; verwandte Fälle werden teilweise gemeinsam geprüft. Zusätzliche Tests prüfen Rücknahme, gleichzeitige Revisionen, großen Dezimalumfang, Anfangsstände und fehlerhafte RDF-Eingaben. Identische kanonische Bedeutung bei geänderter Sammlungsreihenfolge und RDF-Hin-/Rückweg ist geprüft. Ein künftiges produktives Speicherprofil muss die entsprechenden Revisionen und Kontexte ebenfalls erhalten.
