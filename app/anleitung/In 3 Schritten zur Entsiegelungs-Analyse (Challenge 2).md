# 🌿 Recipe: In 3 Schritten zur Entsiegelungs-Analyse (Challenge 2)

Mit diesem Rezept baut ihr in unter 15 Minuten eine vollständige Schwammstadt-Analyse in euer Streamlit-Dashboard ein.

### Schritt 1: Daten laden
```python
from pipeline import fetch_sealable_surfaces
gdf = fetch_sealable_surfaces("Mainz, Germany")