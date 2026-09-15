

```markdown
# 🛠️ QGIS-Spickzettel: Multi-Kriterien-Analyse (MCE)

Dieser Leitfaden führt Schritt für Schritt durch alle Werkzeuge, um aus den Rohdaten priorisierte Entsiegelungsflächen abzuleiten.

---


## Schritt 1: Rechtliche Machbarkeit filtern (ALKIS)

**Ziel:** Nur Flurstücke behalten, die sich im öffentlichen Eigentum befinden.

1. Wähle den Layer `alkis_flurstuecke` im Layer-Fenster an.
2. Drücke **`F6`** (Attributtabelle öffnen) oder klicke auf das Tabellen-Symbol.
3. Klicke oben auf **Nach Ausdruck wählen** (`Strg + F3` bzw. das $\varepsilon$-Symbol).
4. Gib folgenden Filterausdruck ein:

```sql
"t_eigentuemer" ILIKE '%öffentlich%' OR "t_eigentuemer" ILIKE '%Gemeinde%' OR "t_eigentuemer" ILIKE '%Land%'

```

> **Syntax-Hinweis:**
> * `"t_eigentuemer"`: Doppelte Anführungszeichen kennzeichnen immer Feld- bzw. Spaltennamen in QGIS.
> * `ILIKE`: Vergleicht Strings ohne Beachtung von Groß- und Kleinschreibung (`Gemeinde` vs. `gemeinde`).
> * `%`: Wildcard-Platzhalter für beliebige Zeichen vor oder nach dem Suchbegriff.
> * `OR`: Logisches Oder – trifft zu, wenn mindestens eine Bedingung wahr ist.
> 
> 

5. Klicke auf **Objekte wählen** und schließe das Dialogfenster.
6. Rechtsklick auf `alkis_flurstuecke` ➔ **Exportieren ➔ Gewählte Objekte speichern als...**:
* **Format:** GeoPackage
* **Dateiname:** Im Projektordner als `data/analyse_temp.gpkg` speichern
* **Layername:** `alkis_oeffentlich`
* **KBS:** Projekt-KBS beibehalten (`EPSG:25833` bzw. `EPSG:25832`)


7. Klicke auf **OK**.

---

## Schritt 2: Potenzialflächen zuschneiden (OSM & ALKIS)

**Ziel:** Straßenbegleitende Parkplätze (`osm_graues_band_parkplaetze`) auf öffentlich zugängliche Grundstücke begrenzen.

1. Menüleiste: **Vektor ➔ Geoverarbeitungswerkzeuge ➔ Verschneidung (Intersection)**
* **Eingabelayer:** `osm_graues_band_parkplaetze`
* **Überlagerungslayer:** `alkis_oeffentlich`
* **Verschneidung:** Als Layer `parkplaetze_oeffentlich` in `data/analyse_temp.gpkg` speichern


2. Klicke auf **Starten**.

---

## Schritt 3: Grünraumdefizit ermitteln (Pufferung)

**Ziel:** Prüfen, welche Flächen außerhalb des Einzugsbereichs großer Parks (> 2 ha) liegen.

1. Menüleiste: **Vektor ➔ Geoverarbeitungswerkzeuge ➔ Puffer (Buffer)**
* **Eingabelayer:** `osm_gruenflaechen_groesser_2ha`
* **Abstand:** `300` Meter *(oder die Vorgabe der Lehrkraft)*
* **Ergebnis zusammenführen (Dissolve):** Häkchen setzen!
* **Ausgabe:** Als Layer `parks_einzugsgebiet` anlegen


2. Klicke auf **Starten**.

> **Syntax-Hinweis:**
> * **Abstand / Distance:** Richtet sich nach den Einheiten des KBS (bei `EPSG:25832` / `EPSG:25833` immer in Metern). Niemals Grad-Werte (WGS84) bei Pufferungen nutzen!
> * **Dissolve (Zusammenführen):** Verschmilzt überlappende Pufferkreise zu einem einheitlichen Polygon und verhindert spätere Doppelberechnungen.
> 
> 

3. **Flächen außerhalb identifizieren:**
* Menüleiste: **Vektor ➔ Geoverarbeitungswerkzeuge ➔ Differenz (Difference)**
* **Eingabelayer:** `parkplaetze_oeffentlich` (aus Schritt 2)
* **Überlagerungslayer:** `parks_einzugsgebiet`
* **Ausgabe:** `potenzial_ohne_gruen`


4. Klicke auf **Starten**.

---

## Schritt 4: Thermische Belastung verschneiden (Hitzeinseln)

**Ziel:** Hitzedaten an die identifizierten Flächen koppeln.

1. Menüleiste: **Vektor ➔ Geoverarbeitungswerkzeuge ➔ Verschneidung (Intersection)**
* **Eingabelayer:** `potenzial_ohne_gruen`
* **Überlagerungslayer:** `klima_hitzeinseln`
* **Ausgabe:** `potenzial_mit_klima`


2. Klicke auf **Starten**.

---

## Schritt 5: Attributberechnung & Priorisierung (Feldrechner)

Öffne die Attributtabelle von `potenzial_mit_klima` und klicke auf das **Feldrechner-Symbol** (`Strg + I`).

### 1. Fläche in m² berechnen:

* Häkchen bei **Neues Feld anlegen**.
* **Feldname:** `flaeche_m2`
* **Feldtyp:** Ganze Zahl (Integer)
* **Ausdruck:**

```sql
round($area, 0)

```

> **Syntax-Hinweis:**
> * `$area`: Greift dynamisch auf die planare Geometrie des Layers zu (in Quadratmetern $m^2$).
> * `round(wert, 0)`: Rundet auf ganze Quadratmeter ohne Nachkommastellen.
> 
> 

### 2. Priorität vergeben:

* Feldrechner erneut öffnen (`Strg + I`).
* Häkchen bei **Neues Feld anlegen**.
* **Feldname:** `prioritaet`
* **Feldtyp:** Text (String)
* **Ausdruck:**

```sql
CASE 
  WHEN "temp_klasse" = 'Extrem' AND "flaeche_m2" >= 200 THEN 'Hoch'
  WHEN "temp_klasse" IN ('Extrem', 'Hoch') THEN 'Mittel'
  ELSE 'Niedrig'
END

```

> **Syntax-Hinweis:**
> * `CASE ... WHEN ... THEN ... ELSE ... END`: Bedingte Wenn-Dann-Logik, die von oben nach unten prüft.
> * `'Hoch'`: Einfache Anführungszeichen kennzeichnen Textwerte (Strings).
> * `IN ('Extrem', 'Hoch')`: Prüft, ob der Wert in der Liste enthalten ist.
> 
> 

### 3. Maßnahme eintragen:

* Feldrechner öffnen, Feldname: `massnahme` (Text).
* Trag deine planerische Entscheidung ein (z. B. `'Baumrigole'`, `'Pocket-Park'` oder `'Versickerungsmulde'`).

---

## Schritt 6: Übergabe-Export (`ergebnis.geojson`)

1. Rechtsklick auf den finalen Layer ➔ **Exportieren ➔ Objekte speichern als...**
2. **Format:** `GeoJSON`
3. **Dateiname:** `data/ergebnis.geojson`
4. **KBS:** Zwingend auf **`EPSG:4326 - WGS 84`** umstellen!
5. Klicke auf **OK**.

```

⚠️ Typische Fallstricke & Troubleshooting
Fehler: GEOS exception: TopologyException / Invalid Geometry

Ursache: OSM- oder ALKIS-Polygone enthalten minimale Selbstüberschneidungen.

Lösung: Verarbeitungsleiste ➔ Werkzeug Geometrien reparieren (Fix geometries) über den Eingabelayer laufen lassen und das Ergebnis weiterverwenden.

Problem: Fläche (flaeche_m2) ist plötzlich 0 oder hat winzige Kommazahlen

Ursache: Die Berechnung wurde ausgeführt, nachdem der Layer bereits in EPSG:4326 (WGS84) umgewandelt wurde (Berechnung in Quadratgrad statt Quadratmetern).

Lösung: Schritt 5 zwingend im metrischen Projekt-KBS (EPSG:25832 oder EPSG:25833) ausführen.

Problem: Einteilige Parkstreifen hängen zusammen (Multipolygon)

Ursache: Durch Verschneidungen entstehen Multipart-Geometrien, wodurch $area die Summe mehrerer Einzelstreifen liefert.

Lösung: Werkzeug Vektor ➔ Geometrie-Werkzeuge ➔ Mehrteilige in einteilige Objekte zerlegen (Multipart to singleparts) vorschalten.

Problem: NULL-Werte bei der Temperaturklasse

Ursache: Die Fläche liegt am Kachelrand des Hitzemodells oder außerhalb der Modellausdehnung.

Lösung: Im Feldrechner mit COALESCE("temp_klasse", 'Mittel') arbeiten oder Randflächen prüfen.


