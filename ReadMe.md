Markdown# 🌱 hack4GDI_DE 2026 – Challenge 2: Schwammstadt & Flächenentsiegelung Starterkit

Dieses Repository bietet ein schlüsselfertiges, digital souveränes **FOSSGIS-Starterkit / Planning Support System (PSS)** für die Bearbeitung von **Challenge 2 (Flächenentsiegelung & Schwammstadt)** beim **hack4GDI_DE 2026** in Mainz.

Das Template nimmt euch das zeitraubende Aufsetzen der Docker-Infrastruktur, PostGIS-Treiber und Datenextraktion ab, sodass ihr sofort mit der räumlichen Analyse, multikriteriellen Bewertung (MCE) und interaktiven Dashboards loslegen könnt.

---

## 🛠️ Die Architektur auf einen Blick

Das System basiert auf einer modularen, entkoppelten Drei-Schichten-Architektur:

```text
[Offene Daten: GDI-DE / ALKIS / OSM / LOR] 
           │
           ▼
[PostGIS-Datenbank (PostgreSQL 16 / Docker)] 
           │
           ▼
[Python ETL & Analyse-Engine (GeoPandas / Shapely / Overpass)] 
           │
           ▼
[Streamlit & Folium Web-Frontend (Interaktives PSS & Storyteller)]

🎛️ Docker & Docker Compose: Kapselung der gesamten Infrastruktur (keine manuellen GDAL/GEOS-Treiber-Installationen nötig).🐘 PostGIS (PostgreSQL 16): Spatial Database für performante räumliche Verschneidungen und Geometrie-Operationen.🐍 Python Engine: Modular aufgebaute Pipelines für Schwammstadt-KPIs, Erreichbarkeitsmodelle und Hitzeinsel-Puffer.📊 Streamlit & Folium: Interaktives Planungs-Dashboard mit Live-Karten, Filtern und Szenario-Storyteller.🔬 Wissenschaftliche Datenpakete & MethodikDas Starterkit verknüpft vier methodische Säulen direkt im Code:Flächenpotenziale & ALKIS-Eigentümerfilterung (pipeline.py / processor.py):Filterung öffentlicher Grundstücke (t_eigentuemer) und Versiegelungstypen (Parkplätze, Straßenraum, Gebäudeüberhang).Klimatologie & Wirkungsradien (metrics.py):Quantifizierung von Retentionsvolumen ($m^3$) und Mikroklima-Kühlung ($^\circ\text{C}$) basierend auf Wirkungsradien nach Zekar et al. 2023.Umweltgerechtigkeit & Walkability (walkability.py):Berechnung fußläufiger 300m-Grünraumkorridore zu neuen Kühlinseln zum Schutz vulnerabler Bevölkerungsgruppen (Senioren 60+ / Zensus- & LOR-Räume nach URBES-Ansatz).Spatio-Temporal Analysis (widgets.py):Interaktives Zeitreihen- und Szenarien-Storyteller-Widget zur Darstellung historischer Versiegelungsstufen (1950–2026) und Ziel-Szenarien für 2030.OSM-Qualitätsvalidierung (Neis-Methodik):Integrierter Confidence-Score zur Bewertung der Datenreife anhand von Bearbeitungsdichte und Edit-Historie (ohsome API).🚀 Schnellstart (Local-First)1. Repository klonenBashgit clone [https://github.com/sosimple83/fossgis-student-warmup.git](https://github.com/sosimple83/fossgis-student-warmup.git)

cd fossgis-student-warmup
2. Testdaten generieren (Einmalig vorab)Generiert die lokalen Offline-GeoPackages für Mainz und Berlin Friedrichshain-Kreuzberg, um beim Hackathon unabhängig vom WLAN zu bleiben:Bashpython prepare_data.py
python prepare_berlin.py
3. Container startenBashdocker-compose up --build
Öffne anschließend http://localhost:8501 im Browser. Wenn das grüne Banner ✅ PostGIS Datenbank-Verbindung erfolgreich hergestellt! leuchtet, seid ihr startklar!📁 ProjektstrukturPlaintext.
├── docker-compose.yaml             # Container-Orchestrierung (PostGIS + Streamlit)
├── Dockerfile                      # Python + GDAL/GEOS Build-Rezept
├── prepare_data.py                 # Offline-Vorbereitung: Mainz Zentrum
├── prepare_berlin.py               # Offline-Vorbereitung: Berlin Friedrichshain-Kreuzberg
├── README.md                       # Projektdokumentation & Setup
├── data/                           # Lokale Geodaten (sample_data.gpkg, berlin_*.gpkg)
├── db/                             # PostGIS Init-Skripte
└── app/                            # Python & Streamlit Source Code
    ├── app.py                      # Streamlit UI & Folium-Integration
    ├── metrics.py                  # Schwammstadt-KPIs, Retention & LST-Kühlung
    ├── pipeline.py                 # Overpass/OSM-Extraktion & Testgebiet-Presets
    ├── processor.py                # PostGIS-Verbindung & Neis Confidence Score
    ├── walkability.py              # 300m-Senioren-Erreichbarkeitsanalyse
    ├── widgets.py                  # Spatio-Temporal Storyteller Widget
    ├── requirements.txt            # Python-Dependencies (GeoPandas, Folium, etc.)
    └── anleitung/                  # Schritt-für-Schritt-Guides & Forschungskonzepte

📖 Weiterführende Dokumentation & WikiAusführliche Hintergrundinformationen, didaktische Einstiegs-Tutorials und Forschungsnotizen findet ihr direkt im Projekt:📚 GitHub Wiki: fossgis-student-warmup Wiki📑 Anleitungen im Repo (app/anleitung/):06-i3mainz-Research-Konzepte.md – Wissenschaftliche Bezüge & PSS-MethodikIn 3 Schritten zur Entsiegelungs-Analyse (Challenge 2).md – Schnellstart-Leitfaden für TeamsSchritt 2 Impact berechnen.py & Schritt 3 Pitch-Widget einbinden.py – Copy-Paste-Vorlagen für eigene Widgets🔍 Troubleshooting (Häufige Hürden unter Windows & Docker)🚨 Fehler: unable to get image ... open //./pipe/dockerDesktopLinuxEngineUrsache: Docker Desktop läuft nicht.Lösung: Docker Desktop über das Startmenü starten und warten, bis die Engine grün leuchtet.🚨 Fehler: Port 5432 is already allocatedUrsache: Es läuft bereits ein lokales PostgreSQL/PostGIS auf dem Rechner.Lösung: Lokalen Dienst stoppen oder in docker-compose.yaml den Host-Port auf "5433:5432" umstellen.🚨 Fehler: FATAL: password authentication failed for user "user"Ursache: Die Datenbank-Volumes enthalten alte Zugangsdaten.Lösung: Volumes zurücksetzen:Bashdocker-compose down -v
docker-compose up --build
Tobey GIS Open-Source Template | Bereitgestellt für den Hackathon #hack4GDI_DE 2026 (Mainz)
