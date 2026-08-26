# 🌱 hack4GDI_DE 2026 – Challenge 2: Flächenentsiegelung Starterkit

Dieses Repository bietet ein schlüsselfertiges, digital souveränes **FOSSGIS-Starterkit** für die Bearbeitung der Challenge 2 (Flächenentsiegelung) beim **hack4GDI_DE 2026**.

Das Template nimmt euch das zeitraubende Aufsetzen der Infrastruktur und Datenbanktreiber ab, sodass ihr sofort mit der Datenverarbeitung und euren kreativen Konzepten durchstarten könnt.

<<<<<<< HEAD
---
=======
# Dieses Repository bietet ein schlüsselfertiges, digital souveränes \*\*FOSSGIS-Starterkit\*\* für die Bearbeitung der Challenge 2 (Flächenentsiegelung) beim \*\*hack4GDI\_DE 2026\*\*.
>>>>>>> e092431 (feat: sync live server state - add time-series scenario, fixed app layout & metrics)

## 🛠️ Die Architektur auf einen Blick

<<<<<<< HEAD
Das System basiert auf einer klassischen, modular getrennten Drei-Schichten-Architektur:
=======
# Das Template nimmt euch das zeitraubende Aufsetzen der Infrastruktur und Datenbanktreiber ab, sodass ihr sofort mit der Datenverarbeitung und euren kreativen Konzepten durchstarten könnt.
>>>>>>> e092431 (feat: sync live server state - add time-series scenario, fixed app layout & metrics)

```text
[Datenquellen: GDI-DE / OSM] ➔ [PostGIS-Datenbank (Docker)] ➔ [Streamlit Web-Frontend (Python)]
🎛️ Docker & Docker Compose: Kapselung der gesamten Infrastruktur (keine manuellen GDAL/GEOS-Installationen nötig).

🐘 PostGIS (PostgreSQL 16): Spatial Database für komplexe Geometrie-Operationen.

🐍 Python (GeoPandas / OSMnx / SQLAlchemy): ETL-Pipelines und Datenverarbeitung.

📊 Streamlit: Interaktives Dashboard für Visualisierung und Pitch.

🔬 Wissenschaftlicher Ansatz: OSM-Qualitätsvalidierung (Neis-Methodik)
Um die Akzeptanz von OpenStreetMap-Daten bei Kommunen zu erhöhen, integriert der Prototyp Ansätze der OSM-Historien-Analyse (ohsome API / Pascal Neis):

<<<<<<< HEAD
Confidence Score: Bewertung von Flächen anhand von Bearbeitungsdichte und Edit-Historie.
=======
# Das System basiert auf einer klassischen, modular getrennten Drei-Schichten-Architektur:
>>>>>>> e092431 (feat: sync live server state - add time-series scenario, fixed app layout & metrics)

Topologische Integrität: Automatisierte Bereinigung von Geometriefehlern direkt in PostGIS.

🚀 Schnellstart (Local-First)
1. Repository klonen
Bash
git clone [https://github.com/sosimple83/fossgis-student-warmup.git](https://github.com/sosimple83/fossgis-student-warmup.git)
cd fossgis-student-warmup
2. Testdaten generieren (Einmalig vorab)
Generiert die lokalen Testdaten (Mainz) ohne Live-API-Stress beim Event:

Bash
python prepare_data.py
3. Container starten
Bash
docker-compose up --build
Öffne anschließend http://localhost:8501 im Browser. Wenn das grüne Häkchen ✅ Datenbank-Verbindung steht! leuchtet, seid ihr startklar!

🔍 Troubleshooting (Häufige Hürden unter Windows & Docker)
🚨 1. Fehler: unable to get image ... open //./pipe/dockerDesktopLinuxEngine
Ursache: Der Docker Daemon läuft nicht auf deinem Rechner.

Lösung: Starte Docker Desktop über das Windows-Startmenü und warte, bis unten links "Engine running" (grünes Symbol) angezeigt wird. Starte den Befehl danach erneut.

🚨 2. Fehler: failed to read dockerfile: open Dockerfile: no such file or directory
Ursache: Die Datei Dockerfile fehlt im Root-Verzeichnis oder wurde von Windows fälschlicherweise als Dockerfile.txt gespeichert.

Lösung: Benenne die Datei in der PowerShell/Kommandozeile explizit um:

<<<<<<< HEAD
PowerShell
Rename-Item -Path "Dockerfile.txt" -NewName "Dockerfile"
(Achte darauf, dass die Datei im Explorer vom Typ "Datei" und nicht "Textdokument" ist).

🚨 3. Fehler: COPY app/requirements.txt .: not found
Ursache: Die Datei requirements.txt liegt im Hauptordner anstatt im Unterordner /app.

Lösung: Verschiebe die Datei requirements.txt direkt in den Ordner app/ (fossgis-student-warmup/app/requirements.txt).

🚨 4. Fehler: Port 5432 is already allocated
Ursache: Es läuft bereits ein lokales PostgreSQL/PostGIS auf deinem Rechner.

Lösung: Beende deinen lokalen PostgreSQL-Dienst oder passe in der docker-compose.yaml die Zeile -"5432:5432" zu -"5433:5432" an.

🚨 5. Fehler: Error: Invalid value: File does not exist: app.py (Container bricht ab)
Ursache: Streamlit findet die Datei app.py im Container nicht, weil der Ordner app/ nicht richtig gemountet ist oder der Befehl aus dem falschen Verzeichnis aufgerufen wird.

Lösung: Stelle sicher, dass app.py im Unterordner app/ liegt und in der docker-compose.yaml das Volume ./app:/app korrekt eingebunden ist.

🚨 6. Fehler: FATAL: password authentication failed for user "user" (Rotes Banner im Frontend)
Ursache: Die Datenbank-Zugangsdaten in der Streamlit-App (app.py) stimmen nicht mit den Umgebungsvariablen der PostGIS-Datenbank in der docker-compose.yaml überein.

Lösung: Synchronisiere die Zugangsdaten in der docker-compose.yaml (POSTGRES_USER=user, POSTGRES_PASSWORD=password) und führe einen Reset der Datenbank-Volumes durch:
=======
# \* 🐘 \*\*PostGIS (PostgreSQL 16):\*\* Spatial Database für komplexe Geometrie-Operationen.

# \* 🐍 \*\*Python (GeoPandas / OSMnx / SQLAlchemy):\*\* ETL-Pipelines und Datenverarbeitung.

# \* 📊 \*\*Streamlit:\*\* Interaktives Dashboard für Visualisierung und Pitch.
>>>>>>> e092431 (feat: sync live server state - add time-series scenario, fixed app layout & metrics)

Bash
docker-compose down -v
docker-compose up --build
🚨 7. Fehler: 502 Bad Gateway beim Ausführen von docker-compose up
Ursache: Docker Hub hat ein temporäres Erreichbarkeitsproblem beim Abrufen der Basis-Image-Metadaten (python:3.11-slim).

<<<<<<< HEAD
Lösung: Keine Sorge, das liegt nicht an eurem Code. Warte 1–2 Minuten und führe den Befehl erneut aus.

📁 Projektstruktur
Plaintext
.
├── docker-compose.yaml       # Container-Orchestrierung
├── Dockerfile                 # Python + GDAL/GEOS Build-Rezept
├── prepare_data.py            # Skript zum Download der Testdaten (Mainz)
├── README.md                  # Dokumentation & Quickstart
├── data/                      # Lokale Geodaten (sample_data.gpkg)
├── db/                        # PostGIS Init-Skripte
└── app/                       # Python & Streamlit Code
    ├── app.py                 # Streamlit UI
    ├── processor.py           # Validierungs- & Analyse-Logik
    └── requirements.txt       # Python-Abhängigkeiten

=======
# \---

# 

# \## 🔬 Wissenschaftlicher Ansatz: OSM-Qualitätsvalidierung (Neis-Methodik)

# 

# Um die Akzeptanz von OpenStreetMap-Daten bei Kommunen zu erhöhen, integriert der Prototyp Ansätze der \*\*OSM-Historien-Analyse (ohsome API / Pascal Neis)\*\*:

# 

# 1\. \*\*Confidence Score:\*\* Bewertung von Flächen anhand von Bearbeitungsdichte und Edit-Historie.

# 2\. \*\*Topologische Integrität:\*\* Automatisierte Bereinigung von Geometriefehlern direkt in PostGIS.

# 

# \---

# 

# \## 🚀 Schnellstart (Local-First)

# 

# \### 1. Repository klonen

# 

# ```bash

# git clone \[https://github.com/sosimple83/fossgis-student-warmup.git](https://github.com/sosimple83/fossgis-student-warmup.git)

# cd fossgis-student-warmup

# 

# ```

# 

# \### 2. Testdaten generieren (Einmalig vorab)

# 

# Generiert die lokalen Testdaten (Mainz) ohne Live-API-Stress beim Event:

# 

# ```bash

# python prepare\_data.py

# 

# ```

# 

# \### 3. Container starten

# 

# ```bash

# docker-compose up --build

# 

# ```

# 

# Öffne anschließend \*\*`http://localhost:8501`\*\* im Browser. Wenn das grüne Häkchen `✅ Datenbank-Verbindung steht!` leuchtet, seid ihr startklar!

# 

# \---

# 

# \## 🔍 Troubleshooting (Häufige Hürden unter Windows \& Docker)

# 

# \### 🚨 1. Fehler: `unable to get image ... open //./pipe/dockerDesktopLinuxEngine`

# 

# \* \*\*Ursache:\*\* Der Docker Daemon läuft nicht auf deinem Rechner.

# \* \*\*Lösung:\*\* Starte \*\*Docker Desktop\*\* über das Windows-Startmenü und warte, bis unten links "Engine running" (grünes Symbol) angezeigt wird. Starte den Befehl danach erneut.

# 

# \### 🚨 2. Fehler: `failed to read dockerfile: open Dockerfile: no such file or directory`

# 

# \* \*\*Ursache:\*\* Die Datei `Dockerfile` fehlt im Root-Verzeichnis oder wurde von Windows fälschlicherweise als `Dockerfile.txt` gespeichert.

# \* \*\*Lösung:\*\* Benenne die Datei in der PowerShell/Kommandozeile explizit um:

# ```powershell

# Rename-Item -Path "Dockerfile.txt" -NewName "Dockerfile"

# 

# ```

# 

# 

# \*(Achte darauf, dass die Datei im Explorer vom Typ "Datei" und nicht "Textdokument" ist)\*.

# 

# \### 🚨 3. Fehler: `COPY app/requirements.txt .: not found`

# 

# \* \*\*Ursache:\*\* Die Datei `requirements.txt` liegt im Hauptordner anstatt im Unterordner `/app`.

# \* \*\*Lösung:\*\* Verschiebe die Datei `requirements.txt` direkt in den Ordner `app/` (`fossgis-student-warmup/app/requirements.txt`).

# 

# \### 🚨 4. Fehler: `Port 5432 is already allocated`

# 

# \* \*\*Ursache:\*\* Es läuft bereits ein lokales PostgreSQL/PostGIS auf deinem Rechner.

# \* \*\*Lösung:\*\* Beende deinen lokalen PostgreSQL-Dienst oder passe in der `docker-compose.yaml` die Zeile `-"5432:5432"` zu `-"5433:5432"` an.

# 

# \### 🚨 5. Fehler: `Error: Invalid value: File does not exist: app.py` (Container bricht ab)

# 

# \* \*\*Ursache:\*\* Streamlit findet die Datei `app.py` im Container nicht, weil der Ordner `app/` nicht richtig gemountet ist oder der Befehl aus dem falschen Verzeichnis aufgerufen wird.

# \* \*\*Lösung:\*\* Stelle sicher, dass `app.py` im Unterordner `app/` liegt und in der `docker-compose.yaml` das Volume `./app:/app` korrekt eingebunden ist.

# 

# \### 🚨 6. Fehler: `FATAL: password authentication failed for user "user"` (Rotes Banner im Frontend)

# 

# \* \*\*Ursache:\*\* Die Datenbank-Zugangsdaten in der Streamlit-App (`app.py`) stimmen nicht mit den Umgebungsvariablen der PostGIS-Datenbank in der `docker-compose.yaml` überein.

# \* \*\*Lösung:\*\* Synchronisiere die Zugangsdaten in der `docker-compose.yaml` (`POSTGRES\_USER=user`, `POSTGRES\_PASSWORD=password`) und führe einen Reset der Datenbank-Volumes durch:

# ```bash

# docker-compose down -v

# docker-compose up --build

# 

# ```

# 

# 

# 

# \### 🚨 7. Fehler: `502 Bad Gateway` beim Ausführen von `docker-compose up`

# 

# \* \*\*Ursache:\*\* Docker Hub hat ein temporäres Erreichbarkeitsproblem beim Abrufen der Basis-Image-Metadaten (`python:3.11-slim`).

# \* \*\*Lösung:\*\* Keine Sorge, das liegt nicht an eurem Code. Warte 1–2 Minuten und führe den Befehl erneut aus.

# 

# \---

# 

# \## 📁 Projektstruktur

# 

# ```text

# .

# ├── docker-compose.yaml       # Container-Orchestrierung

# ├── Dockerfile                 # Python + GDAL/GEOS Build-Rezept

# ├── prepare\_data.py            # Skript zum Download der Testdaten (Mainz)

# ├── README.md                  # Dokumentation \& Quickstart

# ├── data/                      # Lokale Geodaten (sample\_data.gpkg)

# ├── db/                        # PostGIS Init-Skripte

# └── app/                       # Python \& Streamlit Code

# &#x20;   ├── app.py                 # Streamlit UI

# &#x20;   ├── processor.py           # Validierungs- \& Analyse-Logik

# &#x20;   └── requirements.txt       # Python-Abhängigkeiten

# 

# ```

# 

# ```

# 

# ```
>>>>>>> e092431 (feat: sync live server state - add time-series scenario, fixed app layout & metrics)

Wir haben auch noch ein Wiki:
https://github.com/sosimple83/fossgis-student-warmup/wiki
