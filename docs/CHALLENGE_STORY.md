# 🏙️ Challenge 2: Flächenentsiegelung & Schwammstadt (#hack4GDI_DE)

## Die 4 methodischen Kriterien (MCE-Grundlagen)

Die konkreten Schwellenwerte, Gewichtungen und Ausschlussradien werden durch die Challenge-Leitung (Prof. Dr. Markus Schaffert / Mentoren) im Kick-off bekannt gegeben oder im Team eigenständig begründet.

1. **Rechtliche Machbarkeit (Verfügbarkeit):**
   * Welche Liegenschaften liegen in kommunaler Hand, um Genehmigungsverfahren schlank zu halten?
   * *Datenbasis:* `alkis_flurstuecke` (Attribut: `t_eigentuemer`)
2. **Flächenpotenzial (Substanz):**
   * Wo befinden sich zusammenhängende Parkplatz- und Randstreifenflächen mit ausreichend Raum für Versickerung?
   * *Datenbasis:* `osm_graues_band_parkplaetze`
3. **Grünraumdefizit (Umfeldversorgung):**
   * Wo fehlen wohnungsnahe Erholungs- und Vegetationsflächen im Quartier?
   * *Datenbasis:* `osm_gruenflaechen_groesser_2ha` (Pufferdistanz nach Vorgabe)
4. **Thermische Dringlichkeit (Stadtklima):**
   * Welche Bereiche leiden besonders unter Überwärmung und Tropennächten?
   * *Datenbasis:* `klima_hitzeinseln` (Spalte: `temp_klasse`)

---

## Das finale Übergabeformat

Für die Auswertung und den Pitch-Viewer exportiert jedes Team seinen finalen Layer als `data/ergebnis.geojson` im KBS **EPSG:4326 (WGS 84)** mit folgenden Kernattributen:

* `flaeche_m2`: Flächengröße in m² (z. B. `round($area, 0)`)
* `prioritaet`: Dringlichkeitsstufe (`Hoch`, `Mittel` oder `Niedrig`)
* `massnahme`: Geplanter Schwammstadt-Typ (z. B. *„Pocket-Park“*, *„Baumrigole“*, *„Versickerungsmulde“*)
