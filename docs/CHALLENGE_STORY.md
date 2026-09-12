# 🏙️ Challenge 2: Flächenentsiegelung & Schwammstadt (#hack4GDI_DE)

### Das Szenario
Ihr seid das städtische Transformationsteam. Die Stadtverordnetenversammlung hat ein Sofortprogramm für Klimaanpassung beschlossen: Bis 2030 müssen hitzebelastete, versiegelte Verkehrsräume in multifunktionale Schwammstadt-Elemente umgewandelt werden.

**Euer Auftrag:**
Identifiziert im Fokusraum (Mainz oder Berlin Friedrichshain-Kreuzberg) die Top-Potenzialflächen und definiert für jeden Standort eine konkrete bauliche Maßnahme.

---

### Die 3 planerischen Leitfragen (MCE-Logik)

1. **Rechtliche Machbarkeit (Wo darf die Stadt sofort bauen?):**
   * Wo kann die Kommune ohne langwierigen Grunderwerb oder private Verhandlungen eingreifen?
   * *Datenbasis:* `alkis_flurstuecke` (Attribut `t_eigentuemer`).

2. **Flächenpotenzial (Was bauen wir um?):**
   * Welche Flächen im Straßenraum sind monoton versiegelt und bieten ausreichend Raum für Versickerung?
   * *Datenbasis:* `osm_graues_band_parkplaetze`.

3. **Dringlichkeit & Grünraumdefizit (Wo brennt es am meisten?):**
   * In welchen Quartieren fehlt es an wohnungsnahen Grünflächen? Reicht der Abstand zu vorhandenen Parks?
   * *Datenbasis:* `osm_gruenflaechen_groesser_2ha` (z. B. 300 m Puffer).

---

### Das finale Übergabeformat
Für den Pitch-Viewer im Dashboard (`app/app.py`) exportiert ihr euren Ergebnis-Layer als `data/ergebnis.geojson` (KBS: EPSG:4326) mit folgenden drei Spalten:
* `flaeche_m2`: Flächengröße in m² (z. B. berechnet via `round($area, 0)`)
* `prioritaet`: "Hoch", "Mittel" oder "Niedrig"
* `massnahme`: Eure planerische Idee (z. B. "Pocket-Park", "Baumrigole", "Versickerungsmulde")