import geopandas as gpd
import osmnx as ox
import pandas as pd
import os

PRESET_LOCATIONS = {
    "Mainz Zentrum": "Mainz, Germany",
    "Berlin Friedrichshain-Kreuzberg": "Bezirk Friedrichshain-Kreuzberg, Berlin, Germany"
}

def fetch_sealable_surfaces(location_key: str = "Berlin Friedrichshain-Kreuzberg") -> gpd.GeoDataFrame:
    """
    Lädt entsiegelbare Flächen für das gewählte Preset (Mainz oder Berlin Friedrichshain-Kreuzberg).
    Nutzt prioritär lokale GeoPackage-Caches aus dem /data-Ordner als Offline-Fallback.
    """
    place_name = PRESET_LOCATIONS.get(location_key, location_key)
    
    # 1. Mögliche Dateinamen für den lokalen Cache prüfen
    clean_name = location_key.lower().replace(" ", "_")
    alt_name = location_key.lower().replace(" ", "-")
    
    possible_cache_paths = [
        f"data/{clean_name}.gpkg",
        f"data/{alt_name}.gpkg",
        f"/data/{clean_name}.gpkg",
        f"/data/{alt_name}.gpkg"
    ]
    
    # Spezial-Mapping für Mainz & Standard-Musterdateien
    if "mainz" in location_key.lower():
        possible_cache_paths.extend(["data/sample_data.gpkg", "/data/sample_data.gpkg", "data/mainz_zentrum.gpkg"])
    elif "berlin" in location_key.lower():
        possible_cache_paths.extend(["data/berlin_friedrichshain_kreuzberg.gpkg", "/data/berlin_friedrichshain_kreuzberg.gpkg"])

    for cache_file in possible_cache_paths:
        if os.path.exists(cache_file):
            print(f"Lade Offline-Cache aus {cache_file} für '{location_key}'...")
            gdf_cached = gpd.read_file(cache_file)
            
            # Einheitliche Spaltenbenennung sicherstellen
            if "feature_type" in gdf_cached.columns and "surface_type" not in gdf_cached.columns:
                gdf_cached["surface_type"] = gdf_cached["feature_type"]
            elif "surface_type" in gdf_cached.columns and "feature_type" not in gdf_cached.columns:
                gdf_cached["feature_type"] = gdf_cached["surface_type"]
                
            if "id" not in gdf_cached.columns:
                gdf_cached["id"] = gdf_cached.index.astype(str)
                
            return gdf_cached
        
    # 2. Live-Abruf über OSMnx (Overpass API), falls kein lokaler Cache vorliegt
    print(f"Kein lokaler Cache gefunden. Starte Live-Abruf via OSMnx für '{place_name}'...")
    
    # Erweitertes Tag-Dictionary für das „Graue Band“ (Parkplätze, Straßenland, Verkehrsinseln)
    tags = {
        'amenity': ['parking', 'parking_space'],
        'highway': ['service', 'pedestrian', 'living_street', 'footway', 'traffic_island'],
        'traffic_calming': True,
        'area:highway': True,
        'landuse': ['commercial', 'industrial', 'retail'],
        'building': True
    }
    
    try:
        # Kompatibilität für neuere und ältere OSMnx-Versionen
        if hasattr(ox, 'features_from_place'):
            gdf = ox.features_from_place(place_name, tags=tags)
        else:
            gdf = ox.geometries_from_place(place_name, tags=tags)
            
        # Nur Flächen-Geometrien behalten
        gdf = gdf[gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])].copy()
        
        # Auf metrisches Koordinatensystem projizieren (UTM 32N / 33N)
        gdf = ox.projection.project_gdf(gdf)
        
        # Typ-Klassifizierung für MCE und Visualisierung
        def classify_feature(row):
            amenity = str(row.get('amenity', '')).lower()
            highway = str(row.get('highway', '')).lower()
            building = row.get('building', None)
            area_hw = row.get('area:highway', None)
            
            if amenity in ['parking', 'parking_space']:
                return 'parking'
            if pd.notnull(building) and str(building).lower() not in ['none', 'nan', 'no']:
                return 'building'
            if highway in ['service', 'pedestrian', 'living_street', 'traffic_island'] or pd.notnull(area_hw):
                return 'highway'
            return 'other'

        gdf['surface_type'] = gdf.apply(classify_feature, axis=1)
        gdf['feature_type'] = gdf['surface_type']
        
        if 'id' not in gdf.columns:
            gdf['id'] = gdf.index.astype(str)
            
        # Spalten bereinigen
        return gdf[['surface_type', 'feature_type', 'id', 'geometry']].reset_index(drop=True)
        
    except Exception as e:
        print(f"Fehler beim Live-Abruf der OSM-Daten für {place_name}: {e}")
        
        # Letzter Notfall-Fallback auf Standard-Musterdaten
        fallback_files = ["data/sample_data.gpkg", "data/mainz_zentrum.gpkg"]
        for fb in fallback_files:
            if os.path.exists(fb):
                print(f"Verwende Notfall-Fallback: {fb}")
                fallback_gdf = gpd.read_file(fb)
                if "feature_type" not in fallback_gdf.columns and "surface_type" in fallback_gdf.columns:
                    fallback_gdf["feature_type"] = fallback_gdf["surface_type"]
                return fallback_gdf
            
        return gpd.GeoDataFrame()