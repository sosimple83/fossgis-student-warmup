# 🛠️ QGIS-Spickzettel: Werkzeuge & Ausdrücke

### 1. Daten robust öffnen
Zieht die GeoPackage-Datei eures Gebiets per Drag & Drop direkt ins leere QGIS-Kartenfenster:
* Mainz: `data/mainz/mainz_base.gpkg`
* Berlin: `data/berlin_fk/berlin_fk_base.gpkg`

---

### 2. Öffentlichen Grund filtern (ALKIS)
1. Attributtabelle von `alkis_flurstuecke` öffnen (`F6`).
2. Auf **Objekte über Ausdruck wählen** (`Strg + F3`) klicken:
   ```sql
   "t_eigentuemer" ILIKE '%Kommune%' 
   OR "t_eigentuemer" ILIKE '%Land%'
   OR "t_eigentuemer" ILIKE '%Stadt%'