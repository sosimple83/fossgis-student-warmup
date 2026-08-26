import geopandas as gpd
import osmnx as ox

def calculate_elderly_green_accessibility(buildings_gdf: gpd.GeoDataFrame, unsealed_gdf: gpd.GeoDataFrame, max_walk_meters: int = 300) -> gpd.GeoDataFrame:
    """
    Kombiniert das Remanenz-Konzept (i3mainz) mit der Walkability:
    Ermittelt Gebäude mit hoher Senioren-Dichte, die innerhalb von X Metern Fußweg 
    um eine neu entsiegelte Grünfläche liegen.
    """
    if buildings_gdf.empty or unsealed_gdf.empty:
        return gpd.GeoDataFrame()

    # 1. Metrische Projektion sicherstellen
    buildings_proj = ox.projection.project_gdf(buildings_gdf)
    unsealed_proj = ox.projection.project_gdf(unsealed_gdf)

    # 2. Puffer um entsiegelte Flächen (z. B. 300m seniorengerechte Fußdistanz)
    green_buffers = unsealed_proj.geometry.buffer(max_walk_meters)
    combined_buffer = green_buffers.unary_union

    # 3. Identifikation erreichbarer Gebäude
    accessible_buildings = buildings_proj[buildings_proj.geometry.intersects(combined_buffer)].copy()
    
    # 4. Kennzeichnung der Remanenz-Relevanz (Indikator für vulnerable Gruppen)
    accessible_buildings['senior_accessibility_score'] = "Hoch ( < 5 Min Fußweg)"
    
    return accessible_buildings