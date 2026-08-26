# 🔬 Forschungs-Transfer: i3mainz Konzepte in Challenge 2

Unser Starterkit übersetzt aktuelle Forschungsergebnisse des **i3mainz (Prof. Markus Schaffert)** direkt in prämierungswürdige Hackathon-Codebausteine:

### 1. Remanenzgebäude & Vulnerable Gruppen
* **Wissenschaftlicher Hintergrund:** Ältere Einfamilienhausgebiete weisen oft eine hohe Dichte an 1-2-Personen-Seniorenhaushalten auf ("Remanenz")[cite: 2].
* **Transfer in den Code:** `app/metrics.py` & `app/walkability.py` priorisieren Entsiegelungen im direkten Umfeld dieser Quartiere zum Schutz vor Hitzeinseln (LST)[cite: 1, 2, 3, 4].

### 2. Historische Zeitreihen & Bebauungspläne
* **Wissenschaftlicher Hintergrund:** Visualisierung des kontinuierlichen Flächenverbrauchs seit 1945 mittels TimeManager / GIS-Animationen[cite: 1].
* **Transfer in den Code:** Invertierung im Streamlit-Widget (`widgets.py`): Visualisierung der *Entsiegelungs-Dynamik* bis 2030[cite: 1].

### 3. Elderly Walk Score (Senioren-Fußläufigkeit)
* **Wissenschaftlicher Hintergrund:** Bewertung der Erreichbarkeit von Infrastrukturen für ältere Menschen auf OSM-Basis[cite: 2].
* **Transfer in den Code:** `walkability.py` prüft, ob kühle, entsiegelte Freiräume innerhalb von 300m Fußweg für Senioren erreichbar sind[cite: 2].