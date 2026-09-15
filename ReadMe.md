

#### 3. `README.md` (im Hauptverzeichnis)

```markdown
# 🏙️ FOSSGIS Challenge 2: Schwammstadt-Potenzialflächen (#hack4GDI_DE)

Willkommen zur Challenge 2! In diesem Repository findet ihr alle Grundlagen, um versiegelte Verkehrsflächen in multifunktionale Schwammstadt-Elemente umzuplanen.

---

### 🚀 Schnellstart in 3 Schritten

1. **Aufgabe & Story verstehen:**
   Lest euch das Planungsmandat und die Leitfragen in [`docs/CHALLENGE_STORY.md`](docs/CHALLENGE_STORY.md) durch.

2. **Daten in QGIS laden & analysieren:**
   Zieht die GeoPackage-Datei eurer Wunschregion per Drag & Drop direkt in QGIS:
   - **Mainz:** `data/mainz/mainz_base.gpkg`
   - **Berlin:** `data/berlin_fk/berlin_fk_base.gpkg`
   *(Klickpfade und SQL-Filter findet ihr in [`docs/SPICKZETTEL_QGIS.md`](docs/SPICKZETTEL_QGIS.md))*

3. **Dashboard starten:**
   ```bash
   pip install -r requirements.txt
   streamlit run app/app.py
