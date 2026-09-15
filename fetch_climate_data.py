import os
import requests
import geopandas as gpd
from shapely.geometry import box

def fetch_berlin_climate(gpkg_path: str):
    """
    Lädt die Planungshinweiskarte Stadtklima (FIS-Broker Berlin)
    und schneidet sie auf die Bounding-Box der bestehenden Berlin-Daten zu.
    """
    print("--> Lade Klimadaten für Berlin (FIS-Broker WFS)...")
    
    # 1. Bounding-Box aus den vorhandenen Flurstücken ermitteln
    existing = gpd.read_file(gpkg_path, layer="alkis_flurstuecke")
    minx, miny, maxx, maxy = existing.total_bounds
    
    # 2. WFS-Anfrage für Berlin (Klimaanalyse 2020)
    wfs_url = "https://fbinter.stadt-berlin.de/fb/wfs/data/senstadt/s_04_11_klimaanalyse2020"
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeNames": "s_04_11_klimaanalyse2020",
        "outputFormat": "application/json",
        "srsName": "EPSG:25833",
        "bbox": f"{minx},{miny},{maxx},{maxy},urn:ogc:def:crs:EPSG::25833"
    }
    
    try:
        response = requests.get(wfs_url, params=params, timeout=30)
        response.raise_for_status()
        gdf = gpd.read_file(response.text)
        
        # Sicherstellen, dass das KBS passt
        gdf = gdf.to_crs(epsg=25833)
        
        # Auf Bounding-Box der Flurstücke clippen
        gdf_clipped = gpd.clip(gdf, existing.total_bounds)
        
        # In GeoPackage als neuen Layer schreiben
        gdf_clipped.to_file(gpkg_path, layer="klima_hitzeinseln", driver="GPKG")
        print(f" [OK] Berlin: {len(gdf_clipped)} Hitze-Polygone in {gpkg_path} gespeichert.")
        
    except Exception as e:
        print(f" [WARNUNG] WFS-Abruf Berlin fehlgeschlagen ({e}). Erzeuge Dummy-Zonen für Offline-Betrieb...")
        create_fallback_zones(existing, gpkg_path, 25833)

def fetch_mainz_climate(gpkg_path: str):
    """
    Lädt thermische Belastungszonen für Mainz (Geoportal RLP WFS)
    oder generiert ein standardisiertes Fallback-Grid bei Timeout.
    """
    print("--> Lade Klimadaten für Mainz (Geoportal RLP WFS)...")
    
    existing = gpd.read_file(gpkg_path, layer="alkis_flurstuecke")
    minx, miny, maxx, maxy = existing.total_bounds
    
    wfs_url = "https://geodaten.naturschutz.rlp.de/kartendienste_naturschutz/service.php"
    params = {
        "SERVICE": "WFS",
        "VERSION": "1.1.0",
        "REQUEST": "GetFeature",
        "TYPENAME": "klimaanalyse_belastung",
        "OUTPUTFORMAT": "application/json",
        "SRSNAME": "EPSG:25832",
        "BBOX": f"{minx},{miny},{maxx},{maxy},EPSG:25832"
    }
    
    try:
        response = requests.get(wfs_url, params=params, timeout=20)
        response.raise_for_status()
        gdf = gpd.read_file(response.text)
        gdf = gdf.to_crs(epsg=25832)
        gdf_clipped = gpd.clip(gdf, existing.total_bounds)
        
        gdf_clipped.to_file(gpkg_path, layer="klima_hitzeinseln", driver="GPKG")
        print(f" [OK] Mainz: {len(gdf_clipped)} Hitze-Polygone in {gpkg_path} gespeichert.")
        
    except Exception as e:
        print(f" [WARNUNG] WFS-Abruf Mainz fehlgeschlagen ({e}). Erzeuge Dummy-Zonen für Offline-Betrieb...")
        create_fallback_zones(existing, gpkg_path, 25832)

def create_fallback_zones(reference_gdf, gpkg_path: str, epsg: int):
    """
    Erzeugt ein leichtes 500m-Analyse-Raster als Mock-Layer 'klima_hitzeinseln',
    falls die WFS-Server der Ämter gerade nicht antworten.
    """
    import numpy as np
    from shapely.geometry import Polygon
    
    minx, miny, maxx, maxy = reference_gdf.total_bounds
    step = 500  # 500 Meter Raster
    
    polys = []
    labels = []
    classes = ["Mittel", "Hoch", "Extrem"]
    
    for x in range(int(minx), int(maxx), step):
        for y in range(int(miny), int(maxy), step):
            poly = box(x, y, x + step, y + step)
            polys.append(poly)
            # Pseudo-Klassifikation für Übungszwecke
            labels.append(np.random.choice(classes, p=[0.4, 0.4, 0.2]))
            
    grid_gdf = gpd.GeoDataFrame({"temp_klasse": labels, "geometry": polys}, crs=f"EPSG:{epsg}")
    grid_gdf = gpd.clip(grid_gdf, reference_gdf.total_bounds)
    grid_gdf.to_file(gpkg_path, layer="klima_hitzeinseln", driver="GPKG")
    print(f" [MOCK] {len(grid_gdf)} Fallback-Hitzezonen in {gpkg_path} abgelegt.")

if __name__ == "__main__":
    berlin_gpkg = os.path.join("data", "berlin_fk", "berlin_fk_base.gpkg")
    mainz_gpkg = os.path.join("data", "mainz", "mainz_base.gpkg")
    
    if os.path.exists(berlin_gpkg):
        fetch_berlin_climate(berlin_gpkg)
    else:
        print(f"Pfad nicht gefunden: {berlin_gpkg}")
        
    if os.path.exists(mainz_gpkg):
        fetch_mainz_climate(mainz_gpkg)
    else:
        print(f"Pfad nicht gefunden: {mainz_gpkg}")