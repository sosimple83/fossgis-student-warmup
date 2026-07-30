import os
import osmnx as ox
import geopandas as gpd

def download_sample_data():
    print("🌍 Lade OpenStreetMap-Testdaten für Mainz herunter...")
    
    # Untersuchungsgebiet definieren (Zentrum Mainz)
    place_name = "Mainz, Germany"
    
    # 1. Gebäude (potenzielle Dach-Entsiegelung)
    print("🏢 Lade Gebäude...")
    buildings = ox.features_from_place(place_name, tags={"building": True})
    buildings = buildings[buildings.geometry.type == "Polygon"]
    buildings = buildings[["geometry"]]
    buildings["feature_type"] = "building"

    # 2. Parkplätze / Versiegelte Flächen
    print("🚗 Lade Parkplätze...")
    parking = ox.features_from_place(place_name, tags={"amenity": "parking"})
    parking = parking[parking.geometry.type == "Polygon"]
    parking = parking[["geometry"]]
    parking["feature_type"] = "parking"

    # Zusammenführen & Speichern
    print("📦 Kombiniere Daten zu GeoPackage...")
    gdf = gpd.pd.concat([buildings, parking])
    
    os.makedirs("data", exist_ok=True)
    output_path = "data/sample_data.gpkg"
    gdf.to_file(output_path, layer="osm_features", driver="GPKG")
    print(f"✨ Fertig! Datei gespeichert unter: {output_path}")

if __name__ == "__main__":
    download_sample_data()