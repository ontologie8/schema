# P0-Entwurf: erweiterbares Weltmodell

Stand: 2026-10-12 · Entwurf fachlich geprüft · P0 weiterhin in Bearbeitung
Lizenz: CC-BY-4.0

## Auftrag und Ergebnis dieser Lieferung

Das Projekt pflegt ein speicherunabhängiges, versioniertes Schema für erweiterbare Entitäten und Beziehungen. Hier liegen Spezifikationen, Schemas, allgemeine Fachmodule und ausschließlich synthetische Beispiele. Echtdaten verbleiben vollständig außerhalb dieses Projekts, einschließlich produktiver Exporte, Protokolle und Anhänge. Die Pflege ist deutsch; sprachabhängige Werte sind von Beginn an mehrsprachig angelegt.

Dieser Entwurf führt Modellkern, Zielstruktur, Anwendungsfallprofile, Zeit und Versionsübernahme zusammen. [Zeit, Bewertungen und Szenarien](zeit-und-bewertungen.md) konkretisieren den zeitlichen Vertrag. [Synthetische Referenzfälle](../anwendungsfaelle/zeitliche-referenzfaelle.md) enthalten Eingaben und erwartete Ergebnisse. Das sind Designartefakte, keine bereits implementierten Fachschemata oder Abfragen.

Der Umfang ist AC-02, AC-03, AC-04, AC-06, AC-07 und AC-09 bis AC-19 zugeordnet. Die bisherigen Nachlassfälle mit beiden Sterbereihenfolgen bleiben nach AC-01 erhalten. Die zeitlichen und fachlichen Prüfungen im Entwurf ersetzen keine spätere ausführbare Prüfung.

## Modellkern und Erweiterung

| Baustein | Bedeutung |
| --- | --- |
| Entität | Stabile Identität einer Person, Organisation, eines Gegenstands, Dokuments oder fachlichen Konzepts |
| Typ und Begriff | Stabile ID/IRI, deutsche Definition und sprachabhängige Bezeichnungen; fachliche Bedeutung unabhängig vom Ordner |
| Beziehung | Eigene referenzierbare Verbindung mit definierten Beteiligtenrollen, Eigenschaften und bei Bedarf Gültigkeit |
| Rollenbelegung | Kontextabhängige Zuordnung, etwa Käufer, Eigentümer, Berater oder Geschäftsführer |
| Ereignis | Kauf, Verkauf, Reparatur, Übertragung oder dokumentierte Korrektur; beteiligte Entitäten und fachliche Zeit |
| Aussage/Revision | Referenzierbare Beschreibung mit Herkunft und Wissenshistorie; Aussageidentität von ihrer jeweiligen Revision getrennt |
| Beobachtung | Feststellung einer Eigenschaft zu einem Zeitpunkt, etwa Zustand, Kilometerstand oder Kurs |
| Bewertung | Ergebnis zu einem Objekt, Wertart und Stichtag mit Betrag, Währung, Quelle und Methode |
| Szenario/Berechnung | Getrennte Annahmen, Eingabestand, Modellversion, Zielzeit und Ergebnisse |

Nicht jedes Objekt benötigt alle Bausteine. Der Kern liefert gemeinsame Strukturen; Fachmodule legen passende Einschränkungen fest. Ein einzelner Datensatz erhält keine erfundene Quelle oder Zeit, nur weil sein Profil diese für eine endgültige Bewertung benötigt. Unvollständige Eingaben bleiben als unvollständig erkennbar.

Eine Beziehung darf neue Kombinationen von Entitätstypen verbinden, wenn ihr Typ die Bedeutung, Beteiligtenrollen und zulässigen Typen definiert. Die Erweiterbarkeit erlaubt keine beliebigen unbenannten Verbindungen. Person → Eigentumsbeziehung → Auto und Organisation → Eigentumsbeziehung → Auto nutzen denselben Beziehungstyp. Person → Beratung → Person und Shop → Angebot → Produktmodell besitzen andere Verträge.

Ein Kleidungsstück mit eigener Identität ist von seinem Produktmodell und einem Verkaufsangebot getrennt. Ein Finanzinstrument ist von einem Depotbestand und einem Kurs unterschieden. Eigentum, Besitz, Vertretung und technischer Zugriff sind verschiedene Beziehungen. Empfehlungen und Prognosen sind keine beobachteten Tatsachen.

## Struktur als Zielbild

Die folgende Struktur ist das Ziel für die schrittweise Umsetzung. Aktuell neu angelegt sind die verlinkten Design- und Referenzfalldokumente; Modell-, Profil- und Laufzeitordner entstehen mit ihren ersten prüfbaren Artefakten. Leere Verzeichnisgerüste sind kein Implementierungsnachweis.

```text
docs/de/
  architektur/
  anwendungsfaelle/
  recherche/
roadmap/
  GANTT.md
  de/
modelle/
  kern/
    entitaeten/
    begriffe/
    beziehungen/
    ereignisse/
    aussagen-und-zeit/
  fachmodule/
    finanzen/
    bekleidung/
    handel/
    familie/
    recht/
    steuern/
    gesellschaften/
profile/
  anwendungsfaelle/
  speicherziele/
abbildungen/
  standards/
  formate/
anwendungsfaelle/
  katalog/
  indizes/
    berufsbilder/
    branchen/
beispiele/synthetisch/
tests/
  modellfragen/
  zeit-und-revisionen/
  abbildungen/
register/
```

Maschinelle Definitionen werden nicht pro Dokumentationssprache dupliziert. Weitere Dokumentationssprachen können später dieselben relativen Pfade unter eigenen Sprachordnern verwenden. Für die Datenwerte gilt [die vorhandene Mehrsprachigkeitsvorgabe](mehrsprachige-werte.md).

Jedes Modul bekommt bei Umsetzung ein Manifest mit ID, Version, Zweck, Abhängigkeiten, bereitgestellten Typen und Referenzen auf seine Dokumentation und Prüffälle. Ein zentrales Register verweist auf diese Manifeste. Fachliche IDs bleiben bei einer Ordneränderung erhalten; lokale Pfadverweise werden entsprechend aktualisiert und geprüft.

Die vorhandene [Personen-/Nachlassroadmap](../../../roadmap/de/personen-nachlass-roadmap.md) beschreibt einen Fachpfad. Finanzen und Bekleidung erproben die gemeinsame Struktur zusätzlich. Das Projekt erhält dadurch keine Bindung an eine bisherige nutzende Anwendung.

## Profile und Anwendungsfälle

Ein Anwendungsfall wählt Module, benötigte Detailtiefe, Pflichtangaben, Abfragekontext und Ergebnisform. Er redefiniert keine gemeinsam verwendete Person oder Beziehung. Speicherprofile beschreiben dagegen die Umsetzung in einem Speicherziel; sie sind eine eigene Dimension.

| Anwendungsfall | Gemeinsame Bausteine und Fachmodule |
| --- | --- |
| Konto und Vermögen | Person/Organisation, Eigentum, Konto, Bestand, Bewertung, Zeit und Herkunft |
| Kleiderschrank und Stilberatung | Person, konkrete Kleidungsstücke, Zustand, Anlass, Bestand und ausdrücklich gekennzeichnete Empfehlungen |
| Einkauf | Shop, Produktmodell, Angebot, Preis-/Verfügbarkeitsbeobachtung und vorhandener Bestand |
| Notariat | Beteiligte und Rollen, Dokumentfassungen, Vermögen, Verfügungen und Ereignisse |
| Rechtsberatung | Mandatsbeziehungen, Beteiligte, Dokumente, Aussagen und zeitliche Vorgänge |
| Steuererklärung | Zeitraum, Belege, Vermögens- und Einkommensvorgänge; eigene geprüfte Fachregeln |
| Gesellschaftsgründung | Personen/Organisationen, Anteile, Funktionen, Dokumente und Gründungsereignisse |

Der Katalog definiert einen Fall einmal. Berufsbilder und Branchen bilden getrennte Indizes mit Referenzen auf die Fall-ID; ein Fall darf in mehreren Indizes erscheinen. Klassifikationscodes sind spätere explizite Abbildungen, keine frei erfundenen Nummern.

Die Detailtiefe kann etwa vom einfachen Objektverzeichnis bis zur belegten Historie mit mehreren Bewertungen reichen. Ein Profil mit wenig Daten behauptet keine Vollständigkeit; fehlende Werte werden nicht mit null oder Nullbeträgen gleichgesetzt.

## Ein führendes Modell, überprüfbare Repräsentationen

| Alternative | Nutzen | Zu prüfende Grenze |
| --- | --- | --- |
| JSON als führende Repräsentation, RDF abgeleitet | Explizite Datensatz- und Austauschstruktur | Identität, Referenzen, Mehrfachwerte, Zeit und Herkunft müssen im Mapping erhalten bleiben |
| RDF als führende Repräsentation, JSON als Eingabevertrag | Beziehungen und gemeinsame Begriffe direkt als Graph | Benötigte Validierung, Revisionen und JSON-Export dürfen nicht allein aus offenen Graphannahmen abgeleitet werden |
| Separates deklaratives Modell, daraus erzeugte Repräsentationen | Gemeinsame Definition für mehrere Formate | Generatoren müssen den fachlichen Vertrag einschließlich Einschränkungen und Historie tatsächlich erhalten |

Empfehlung: Zuerst denselben kleinen Modellvertrag an den Referenzfällen abbilden und die Repräsentation wählen, die nachvollziehbare Pflege und verlustfreien Austausch ermöglicht. Ein bestimmtes Werkzeug wird hier noch nicht verbindlich gewählt. JSON und RDF dürfen keine unabhängig gepflegten Fachwahrheiten bilden.

Für die erste Abbildungsprüfung werden Eigenschaftstypen, IDs, Sprachkennzeichen, mehrwertige Eigenschaften, qualifizierte Beziehungen, Revisionen und Szenarien verwendet. Die erwartete Bedeutung nach Hin- und Rückweg wird unabhängig von der Dateireihenfolge geprüft.

## Zentrale Pflege und produktive Übernahme

Eine Anwendung übernimmt ein veröffentlichtes Paket, einen bestimmten Commit oder eine ausdrücklich versionierte Kopie. Clone und Fork sind zulässige Transportwege. Ein beweglicher `main`-Verweis reicht nicht als produktive Versionsbindung.

Die Anwendung hält die Versionen von Kern, Modulen, Profilen und Abbildungen samt überprüfbarer Paket-/Commitidentität fest. Eigene Erweiterungen bekommen eigene IDs und einen eigenen Namensraum. Allgemein geeignete Änderungen können in dieses zentrale Projekt zurückgeführt werden; lokale Übernahmen behalten ihre bisherige Version bis zu einem geprüften Wechsel.

Veröffentlichte Artefakte werden nicht unter derselben Versionsidentität geändert. Kompatibilität betrifft Eingabevalidierung, Ausgabestruktur und Bedeutung. Eine neue optionale Eigenschaft ist nicht automatisch kompatibel, wenn etwa ein geschlossenes Verbraucherprofil zusätzliche Eigenschaften zurückweist. Geänderte Bedeutungen, Einheiten, Pflichtfelder oder Kardinalitäten benötigen eine ausdrücklich bewertete Versionsänderung.

Frühere Versionen bleiben nachvollziehbar. Der aktuelle Kern trägt keine permanenten Sonderfälle für jede frühere Anwendung; Versionsabbildungen und Migrationen sind eigene Artefakte mit Prüfungen. Die Supportdauer alter Versionen ist vor dem ersten produktiven Release festzulegen.

GitHub, SharePoint und S3 sind mögliche Speicherziele außerhalb dieses Schema-Repositories. Ihre Profile müssen Referenzen, Versionen, Zeit, Herkunft und Sprachwerte erhalten und eine reproduzierbare Ansicht liefern können. Eine produktive Anwendung verantwortet Zugriff, Betrieb und Historienaufbewahrung; die Wahl eines Speicherdienstes garantiert diese Eigenschaften nicht von selbst.

## Review, Grenzen und Umsetzung

Designreview: Auto, Aktien und Kleidung wurden gegen denselben Kern betrachtet; die Fälle benötigen keine Domäne als Mittelpunkt. Bei der Prüfung wurden Erfassungsrevisionen, Bewertungsstichtag versus Gültigkeitsintervall, konkurrierende Quellen und getrennte Prognosen ausdrücklich ergänzt. [Prüfmatrix und Ergebnisse](../anwendungsfaelle/zeitliche-referenzfaelle.md) dokumentieren die fachliche Prüfung.

Es bestehen keine ausführbaren Domänenschemas, Query-Engines, Kursimporte, produktiven Speicheranbindungen oder Berechnungsdienste. Automatische Rechts-/Steuerergebnisse sind weiterhin an die fachlichen Prüfpfade der bisherigen Roadmap gebunden. P0 ist erst abgeschlossen, wenn Repräsentationswahl und Abbildungsprüfung konkret durchgeführt und die Modellverträge für die erste Umsetzung festgelegt sind.

Nächste Umsetzung in dieser Reihenfolge:

1. Gemeinsamen kleinen Modellvertrag und Modulmanifeste für die beiden fachübergreifenden Pilotfälle ausarbeiten.
2. JSON-/RDF-Abbildungsprobe einschließlich Sprache und zeitlicher Revisionen durchführen; führende Repräsentation anhand der Ergebnisse bestimmen.
3. Ausführbare Schemas und unabhängige positive/negative Erwartungsfälle erstellen, insbesondere für historische Stichtagsabfragen und Prognosetrennung.
4. Anwendungsfallprofile und Speicherprofile auf demselben Vertragsstand ergänzen; Anschluss an die erhaltene Fachroadmap prüfen.

[Projektboard](../projekt.md) und [Akzeptanzkriterien](../akzeptanz.md) führen Umfang und Status. Struktur-/Linkprüfung und GitHub-CI bestätigen die Dokumentlieferung, nicht die noch ausstehende Fachimplementierung.
