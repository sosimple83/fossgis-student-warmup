### 🚀 Schnellstart in 4 Schritten

1. **Aufgabe & Story verstehen:**  
   Lest euch das Planungsmandat und die Leitfragen in [`docs/CHALLENGE_STORY.md`](docs/CHALLENGE_STORY.md) durch.

2. **Daten in QGIS laden & analysieren:**  
   Zieht die GeoPackage-Datei eurer Wunschregion per Drag & Drop direkt in QGIS:
   - **Mainz:** `data/mainz/mainz_base.gpkg` (EPSG:25832)
   - **Berlin:** `data/berlin_fk/berlin_fk_base.gpkg` (EPSG:25833)  
   *(Klickpfade und SQL-Filter findet ihr in [`docs/SPICKZETTEL_QGIS.md`](docs/SPICKZETTEL_QGIS.md))*

3. **Ergebnisse validieren:**  
   Prüft euer Zwischen- und Endergebnis vorab mit dem integrierten Testskript auf Schemakonformität, Topologie und KBS:
   ```bash
   python validate_data.py
   ```

4. **Dashboard starten:**  
   Richtet eine virtuelle Umgebung ein und startet das Streamlit-Dashboard:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / macOS:
   source .venv/bin/activate

   pip install -r requirements.txt
   streamlit run app/app.py
   ```

---

### 📂 Repository-Struktur

```text
fossgis-student-warmup/
├── app/
│   └── app.py                          # Interaktives Streamlit-Dashboard
├── data/
│   ├── mainz/
│   │   ├── mainz_base.gpkg             # Basisdaten Mainz (EPSG:25832)
│   │   └── parkplaetze_klima.geojson   # [Ziel] Dein Zwischenergebnis (Mainz)
│   ├── berlin_fk/
│   │   └── berlin_fk_base.gpkg         # Basisdaten Berlin FK (EPSG:25833)
│   ├── templates/                      # Schema-Vorlagen zur Orientierung
│   │   ├── parkplaetze_klima.template.geojson
│   │   └── ergebnis.template.geojson
│   ├── benchmark_entsiegelung.geojson  # Referenz-Benchmark (EPSG:4326)
│   └── ergebnis.geojson                # [Ziel] Dein finaler Export (EPSG:4326)
├── docs/
│   ├── CHALLENGE_STORY.md              # Fachlicher Kontext & Planungsmandat
│   └── SPICKZETTEL_QGIS.md             # QGIS-Workflows, Filter & Tipps
├── validate_data.py                    # Automatisches Prüfskript
├── requirements.txt                    # Python-Dependencies
└── README.md
