# Challenge 2: Flächenentsiegelung & Schwammstadt (#hack4GDI_DE)

**Mentoring & fachliche Konzeption:**  
Emmanuel Tobey | **Tobey GIS Consulting** (Berlin)  
*Open-Source-GIS • FOSSGIS • Geodaten-Automatisierung*  

**Lizenz:** MIT License – Copyright (c) 2026 Emmanuel Tobey  

---

# 🚀 Schnellstart in 3 Schritten

### 1. Aufgabe & Story verstehen:
Lest euch das Planungsmandat und die Leitfragen in `docs/CHALLENGE_STORY.md` durch.

### 2. Daten in QGIS laden & analysieren:
Zieht die GeoPackage-Datei eurer Region per Drag & Drop direkt in QGIS:
* **Mainz:** `data/mainz/mainz_base.gpkg` (`EPSG:25832`)
* **Berlin:** `data/berlin_fk/berlin_fk_base.gpkg` (`EPSG:25833`)

*(Klickpfade, Verschneidungslogik und SQL-Filter findet ihr in `docs/SPICKZETTEL_QGIS.md`)*


### 3. Ergebnisse validieren:
Prüft euer Zwischen- und Endergebnis vorab mit dem integrierten Testskript auf Schemakonformität, Topologie und KBS:

python validate_data.py

```
fossgis-student-warmup/
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
├── requirements.txt                    # Python-Dependencies (Core GIS Stack)
└── README.md
```
