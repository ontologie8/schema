# Schema-/Prüfpaket 0.1.1

Entwicklungsstand, ausschließlich synthetische Referenzdaten. Kein produktiver Speicher und keine Rechtsentscheidung. Die Pflege erfolgt deutsch; Textwerte besitzen erweiterbare Sprachsammlungen. Die Lizenzhinweise stehen im mitgelieferten `NOTICE` und unter `LICENSES/`.

Das Paket liefert fünf Module und fünf Fallprofile: Auto, Aktien, Bekleidung, kombinierter Pilot und Erbausschlagung. Die beiden ausdrücklich benannten Datensatzverträge bleiben getrennt und verwenden gemeinsame Text-/Zeittypen.

In der Wurzel einer portablen Kopie ausführen:

```powershell
python -m pip install -r requirements.txt
python scripts/pruefe_module.py
python scripts/pruefe_module.py --profil urn:ontologie8:profil:auto
```

Die aktive Python-Umgebung muss die festgehaltenen Abhängigkeiten bereitstellen. Die Übernahmedatei `uebernahme.json` bindet Paket-ID, Version und kanonische Prüfsumme. Sie wird bei vorhandener Datei ebenfalls geprüft. SHA-256 beweist Integrität relativ zu einer vertrauenswürdig erhaltenen Bindung, keine fachliche Freigabe oder automatische Echtdatenfreiheit.

Ein benanntes Speicherziel erzeugt eine neue lokale Schema-/Prüfkopie:

```powershell
python scripts/pruefe_module.py --export out/schema-sharepoint-0.1.1 --speicherziel sharepoint
```

Auch `github` und `s3` sind mögliche Zielkennzeichen. Es erfolgt kein Upload. Bestehende Exportziele werden nicht überschrieben. Echte Anwendungsdaten bleiben außerhalb dieses Repositories und dieses Pakets.

Neue Paketstände werden mit `scripts/erzeuge_paket.py` aus `register/paketentwurf-0.1.1.json` vorbereitet. Bestehende Paketdateien werden nicht überschrieben. Fachlich veränderte Module und Profile erhalten zuvor eigene neue Versionsstände; der bewegliche Entwurf ist keine produktive Versionsbindung. Frühere Stände werden über ihren festgehaltenen Git-Commit oder die unveränderte portable Kopie verwendet. Der aktuelle Arbeitsbaum ist kein Archiv verschiedener Dateiinhalte am selben Pfad.

Der aktuelle Paketstand ergänzt die zuvor fehlende Lizenzzuordnungsdatei. In der Repositorywurzel wird dieser Stand ausdrücklich gewählt: `python scripts/pruefe_module.py --paket pakete/0.1.1/paket.json`. Der initiale Stand 0.1.0 bleibt unverändert erhalten. Neue Ausgaben werden mit dem Generator und `--entwurf register/paketentwurf-0.1.1.json` vorbereitet.
