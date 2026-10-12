# Pilot 0.1.0 verwenden und prüfen

Stand: 2026-10-12 · Entwicklungspilot, kein produktives Release
Lizenz: CC-BY-4.0

## Vertragsstand und Einstieg

JSON ist für diesen Pilot der führende Austauschvertrag. Das [Kernschema](../../../modelle/kern/modell.schema.json) definiert die Struktur. Das [Begriffsregister](../../../modelle/kern/begriffe.json), die [Modulzuordnung](../../../register/module.json) und das [Pilotprofil](../../../profile/anwendungsfaelle/p0-pilot.json) legen den geprüften Umfang fest. Die allgemeinen Schemas erzwingen keine deutsche Datensprache; die hier gepflegten Textinhalte sind deutsch und vollständig synthetisch.

Der Kern enthält Entitäten, Textwerte, Zeitpunkte/-intervalle, Aussagerevisionen und Szenarien. Finanz- und Bekleidungsmanifeste verweisen auf die im gemeinsamen Pilotregister definierten Typen; sie sind noch keine umfassenden Branchenschemas. Neue Typen benötigen eine explizite Definition im Register; neue Nutzdatenfelder benötigen einen neuen Vertragsstand. Es gibt keine ungeprüfte automatische Annahme fremder Felder oder beliebiger RDF-Graphen.

## Lokale Prüfung unter Windows

Voraussetzung ist ein verifiziertes Python 3.12. Eine Projektumgebung wird damit angelegt; Abhängigkeiten werden ausschließlich darin installiert. In Codex gilt der zentrale pc-setup-Weg zur Auswahl des Interpreters.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/validate_project.py
.\.venv\Scripts\python.exe scripts/pruefe_pilot.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Die CI führt denselben Vertrags- und Testumfang mit Python 3.12 aus. Abhängigkeiten einschließlich transitiver Versionen liegen in [requirements.txt](../../../requirements.txt). Der lokale Pilot wurde mit Python 3.12.14, RDFLib 7.6.0, jsonschema 4.26.0 und langcodes 3.5.1 geprüft.

## Schnittstellen und Zeit

[modellvertrag.py](../../../scripts/modellvertrag.py) bietet:

- `validiere(modell)`: JSON-Form und semantische Regeln prüfen. Fehler werden als `Modellfehler` zurückgegeben.
- `auswahl(modell, stichtag, wissen, typ=...)`: aktive Aussagen zu fachlichem und Wissensstichtag auswählen. Sichere Treffer und zeitlich unbestimmte Aussagen bleiben getrennt. Prognosen, Empfehlungen und geplante Aussagen erscheinen nicht automatisch als eingetretene Tatsachen.
- `bestand(...)` und `bestandswert(...)`: synthetischen Finanzpilot aus explizitem vollständigem Anfangsstand und Bewegungen berechnen. Eine Bewertung verlangt einen passenden, eindeutigen Kurs mit Währung, Markt und Stückbasis.
- `berechne_szenario(...)`: explizit gebundene Faktor- oder Kursannahme berechnen; Eingaben werden nicht verändert.
- `normalisiere(...)`: semantische Vergleichsform erzeugen.

Das Stichtagsobjekt trägt `wert` und `praezision`. Uhrzeiten sind offsetgebunden; Tages-, Monats- und Jahresangaben werden nicht zu erfundenen Uhrzeiten. Für Finanzbewegungen und Kurse unterstützt der Pilot Zeitpunkte mit bekannter Präzision; unklare Lage zum Stichtag liefert ein offenes Ergebnis. Anteilseigentum und weitere Finanzereignisse benötigen ein eigenes erweitertes Profil. Der aktuelle Eigentumspilot unterstützt vollständige Zuordnungen.

Die Semantik und Konventionen stehen im [Zeitvertrag](zeit-und-bewertungen.md). Die Bibliothek arbeitet mit einem übergebenen Modellpaket im Speicher. Sie ist keine produktive Datenbank, vergibt keine Zugriffsrechte und garantiert keine extern tatsächlich vollständige Bewegungs- oder Quellenlage.

## RDF-Hin- und Rückweg

[rdf.py](../../../abbildungen/formate/rdf.py) bildet den Vertrag über `nach_rdf(modell)` und `aus_rdf(graph)` ab. Das [RDF-Vokabular](../../../abbildungen/formate/vokabular.ttl) beschreibt Strukturklassen; die [Abbildungsmetadaten](../../../abbildungen/formate/p0-rdf.json) binden den Vertragsstand. OWL-Time-/PROV-O-Alignment und SHACL sind spätere zusätzliche Artefakte; sie werden nicht als bereits implementiert ausgegeben.

Die Abbildung enthält einzelne Ressourcen und Eigenschaften, keine eingebettete JSON-Gesamtzeichenfolge. Textwerte tragen echte RDF-Sprachliterale; Richtung bleibt am Textwert erhalten. Referenzen sind RDF-IRIs. Revisionen erhalten eigene Ressourcen, sodass die Beziehung nicht ohne Zeitkontext am Objekt behauptet wird.

Sammlungen sind ungeordnet. Sprachkennzeichen werden über die verifizierte Bibliothek vereinheitlicht und kleingeschrieben. Dezimalzeichenfolgen werden ohne Stellenverlust normalisiert; unbedeutende Nachkommastellen und negatives Null werden vereinheitlicht. Leere Sammlungen besitzen explizite Abbildungsmetadaten. Diese kanonische Form erhält die Bedeutung, nicht notwendigerweise die ursprüngliche Bytefolge.

Der Rückweg weist fremde Prädikate, unverbundene Aussagen, Einzelfelder mit mehreren Werten und ungeeignete Literaltypen zurück. Er validiert anschließend das gesamte zurückgewonnene Modell. Der RDF-Vokabulargraph ist eine getrennte Schemaressource; er wird nicht ungeprüft in einen Instanzgraphen gemischt.

## Nachgewiesener Umfang

Die gemeinsame [synthetische Eingabe](../../../beispiele/synthetisch/p0-pilot.json) enthält 17 Entitäten, 26 Revisionen und vier Szenarien. Die [Erwartungen](../../../beispiele/synthetisch/p0-erwartungen.json) sind getrennt festgelegt. Turtle und JSON-LD werden tatsächlich serialisiert, erneut geparst und zurückvalidiert. Die historischen und numerischen Erwartungen gelten vor und nach dem Austausch.

Die Tests überführen ZF-01 bis ZF-27 aus der [Prüfmatrix](../anwendungsfaelle/zeitliche-referenzfaelle.md) in konkrete Erwartungen; zusätzliche Randfälle prüfen Rücknahmen, gleichzeitige Revisionen, großen Dezimalumfang, Anfangsstand und fehlerhafte RDF-Eingaben. Anderssprachige Kennzeichen verwenden deutsche synthetische Testtexte als technische Parameter; es werden keine Übersetzungen gepflegt.

Nächste Erweiterung: die Moduldefinitionen weiter fachlich trennen, Detailprofile und notwendige Beziehungen ausbauen und die Import-/Versionsverträge für externe Anwendungen konkretisieren. Produktive Speicherprofile und die Familien-/Nachlassfälle der Fachroadmap bleiben eigene folgende Arbeitspakete.
