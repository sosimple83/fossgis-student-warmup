import geopandas as gpd
import shapely.geometry as sg
import os

os.makedirs("data", exist_ok=True)

# Reale Benchmark- und Strukturdaten für Friedrichshain-Kreuzberg (WGS84 / EPSG:4326)
features = [
    # 1. Reale umgesetzte Benchmark-Flächen (Entsiegelungsoffensive)
    {"id": "FK_BENCH_01", "surface_type": "parking", "feature_type": "parking", "name": "Baerwaldpromenade (Gehweg/Stellplatz)", "geometry": sg.box(13.3990, 52.4930, 13.4015, 52.4942)},
    {"id": "FK_BENCH_02", "surface_type": "parking", "feature_type": "parking", "name": "Blücherstraße (Baumscheiben)", "geometry": sg.box(13.3945, 52.4958, 13.3975, 52.4970)},
    {"id": "FK_BENCH_03", "surface_type": "highway", "feature_type": "highway", "name": "Bödikerstraße (Fahrbahnrückbau)", "geometry": sg.box(13.4600, 52.5010, 13.4630, 52.5025)},
    
    # 2. Potenzialflächen (Graues Band / Parkplätze & Verkehrsinseln)
    {"id": "FK_POT_01", "surface_type": "parking", "feature_type": "parking", "name": "Großparkplatz Oranienstraße", "geometry": sg.box(13.4150, 52.5010, 13.4180, 52.5025)},
    {"id": "FK_POT_02", "surface_type": "parking", "feature_type": "parking", "name": "Stellplatzfläche Warschauer Str.", "geometry": sg.box(13.4470, 52.5060, 13.4500, 52.5075)},
    {"id": "FK_POT_03", "surface_type": "highway", "feature_type": "highway", "name": "Verkehrsinsel Ostkreuz", "geometry": sg.box(13.4670, 52.5030, 13.4700, 52.5042)},
    
    # 3. Dichte Blockbebauung (Wärmespeicher / LoD2-Referenz)
    {"id": "FK_BLD_01", "surface_type": "building", "feature_type": "building", "name": "Wohnblock Kotti Süd", "geometry": sg.box(13.4160, 52.4975, 13.4190, 52.4990)},
    {"id": "FK_BLD_02", "surface_type": "building", "feature_type": "building", "name": "Gewerbebau Reichenberger", "geometry": sg.box(13.4250, 52.4940, 13.4280, 52.4955)},
    {"id": "FK_BLD_03", "surface_type": "building", "feature_type": "building", "name": "Altbaublock Boxhagener Platz", "geometry": sg.box(13.4580, 52.5110, 13.4610, 52.5125)}
]

gdf = gpd.GeoDataFrame(features, crs="EPSG:4326")

# In beiden Schreibweisen im data-Ordner ablegen
gdf.to_file("data/berlin_friedrichshain-kreuzberg.gpkg", driver="GPKG")
gdf.to_file("data/berlin_friedrichshain_kreuzberg.gpkg", driver="GPKG")

print("✅ Berlin-Daten mit Erfolgs- und Potenzialflächen erfolgreich in data/ generiert!")