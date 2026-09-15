# 🛠️ QGIS-Spickzettel: Multi-Kriterien-Analyse (MCE)

Dieser Leitfaden führt Schritt für Schritt durch alle Werkzeuge, um aus den Rohdaten priorisierte Entsiegelungsflächen abzuleiten.

---

## Schritt 1: Rechtliche Machbarkeit filtern (ALKIS)

**Ziel:** Nur Flurstücke behalten, die sich im öffentlichen Eigentum befinden.

1. Wähle den Layer `alkis_flurstuecke` im Layer-Fenster an.
2. Drücke **`F6`** (Attributtabelle öffnen) oder klicke auf das Tabellen-Symbol.
3. Klicke oben auf **Nach Ausdruck wählen** (`Strg + F3` bzw. das $\varepsilon$-Symbol):
   ```sql
   "t_eigentuemer" ILIKE '%öffentlich%' OR "t_eigentuemer" ILIKE '%Gemeinde%' OR "t_eigentuemer" ILIKE '%Land%'
Klicke auf Objekte wählen.

Schließe die Tabelle.

Mache einen Rechtsklick auf alkis_flurstuecke ➔ Exportieren ➔ Gewählte Objekte speichern als...:

Format: GeoPackage

Dateiname: Im selben Projektordner als z. B. analyse_temp.gpkg

Layername: alkis_oeffentlich

KBS: Projekt-KBS beibehalten (EPSG:25833 bzw. EPSG:25832)

Klicke auf OK.

Schritt 2: Potenzialflächen zuschneiden (OSM & ALKIS)
Ziel: Straßenbegleitende Parkplätze (osm_graues_band_parkplaetze) auf öffentlich zugängliche Grundstücke begrenzen.

Menüleiste: Vektor ➔ Geoverarbeitungswerkzeuge ➔ Verschneidung (Intersection)

Eingabelayer: osm_graues_band_parkplaetze

Überlagerungslayer: alkis_oeffentlich

Verschneidung: Als temporären Layer oder in analyse_temp.gpkg als parkplaetze_oeffentlich speichern

Klicke auf Starten.

Schritt 3: Grünraumdefizit ermitteln (Pufferung)
Ziel: Prüfen, welche Flächen außerhalb des Einzugsbereichs großer Parks (> 2 ha) liegen.

Menüleiste: Vektor ➔ Geoverarbeitungswerkzeuge ➔ Puffer (Buffer)

Eingabelayer: osm_gruenflaechen_groesser_2ha

Abstand: z. B. 300 Meter (oder der von der Lehrkraft vorgegebene Schwellenwert)

Ergebnis zusammenführen (Dissolve): Häkchen setzen!

Ausgabe: Als Layer parks_einzugsgebiet anlegen

Klicke auf Starten.

Flächen außerhalb identifizieren:

Menüleiste: Vektor ➔ Geoverarbeitungswerkzeuge ➔ Differenz (Difference)

Eingabelayer: parkplaetze_oeffentlich (aus Schritt 2)

Überlagerungslayer: parks_einzugsgebiet

Ausgabe: potenzial_ohne_gruen

Klicke auf Starten.

Schritt 4: Thermische Belastung verschneiden (Hitzeinseln)
Ziel: Hitzedaten an die identifizierten Flächen koppeln.

Menüleiste: Vektor ➔ Geoverarbeitungswerkzeuge ➔ Verschneidung (Intersection)

Eingabelayer: potenzial_ohne_gruen (oder direkt parkplaetze_oeffentlich, falls Kriterien gewichtet werden)

Überlagerungslayer: klima_hitzeinseln

Ausgabe: potenzial_mit_klima

Klicke auf Starten.

Schritt 5: Attributberechnung & Priorisierung (Feldrechner)
Öffne die Attributtabelle von potenzial_mit_klima und klicke auf das Feldrechner-Symbol (Strg + I).

Fläche in m² berechnen:

Häkchen bei Neues Feld anlegen.

Feldname: flaeche_m2

Feldtyp: Ganze Zahl (Integer)

Ausdruck:

SQL
round($area, 0)
Klicke auf OK.

Priorität vergeben (Strg + I erneut öffnen):

Häkchen bei Neues Feld anlegen.

Feldname: prioritaet

Feldtyp: Text (String)

Ausdruck:

SQL
CASE 
  WHEN "temp_klasse" = 'Extrem' AND "flaeche_m2" >= 200 THEN 'Hoch'
  WHEN "temp_klasse" IN ('Extrem', 'Hoch') THEN 'Mittel'
  ELSE 'Niedrig'
END
Klicke auf OK.

Maßnahme definieren:

Feldrechner erneut öffnen (Strg + I).

Häkchen bei Neues Feld anlegen.

Feldname: massnahme

Feldtyp: Text (String)

Vergabe nach planerischer Logik (z. B. 'Baumrigole', 'Pocket-Park' oder 'Versickerungsmulde').

Klicke auf OK.

Schritt 6: Übergabe-Export (ergebnis.geojson)
Rechtsklick auf den finalen Layer ➔ Exportieren ➔ Objekte speichern als...

Format: GeoJSON

Dateiname: data/ergebnis.geojson (im Hauptordner des Repos)

KBS: Zwingend auf EPSG:4326 - WGS 84 umstellen!

Klicke auf OK.
