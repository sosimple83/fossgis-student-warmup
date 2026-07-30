import requests
import geopandas as gpd
import os

def load_local_data(filepath="/data/sample_data.gpkg"):
    """
    Lädt das lokal vorbereitete GeoPackage (Mainz-Testdaten).
    """
    if os.path.exists(filepath):
        return gpd.read_file(filepath)
    return None

def calculate_neis_confidence_score(osm_id):
    """
    Stumpf-Beispiel für den Neis-Ansatz (OSM-Historien-Analyse):
    Fragt die ohsome API ab, um anhand von Bearbeitungen/Usern
    einen Confidence Score (0-100) zu berechnen.
    """
    url = f"https://api.ohsome.org/v1/elements/geometry?bounces={osm_id}"
    try:
        # Platzhalter-Logik für den Hackathon:
        # Hier kann das Team echte ohsome-API-Requests einbauen
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return 85  # Hohe Datenqualität/Aktivität
        return 50
    except Exception:
        # Fallback bei Offline-Betrieb oder API-Timeouts
        return 60