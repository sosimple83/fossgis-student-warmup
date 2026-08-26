import geopandas as gpd

def calculate_sponge_city_impact(gdf: gpd.GeoDataFrame, unseal_ratio: float, rainfall_mm: float = 50.0):
    """
    Berechnet die Kern-Metriken für den Schwammstadt- & Entsiegelungs-Pitch.
    
    :param gdf: GeoDataFrame der ausgewählten Flächen (in metrischer Projektion)
    :param unseal_ratio: Prozentualer Anteil der Entsiegelung (0.0 bis 1.0)
    :param rainfall_mm: Starkregen-Ereignis in mm (Liter pro m²)
    :return: Dictionary mit prägnanten Pitch-KPIs
    """
    if gdf.empty:
        return {"area_m2": 0, "water_m3": 0, "temp_cooling_c": 0.0}
    
    # 1. Entsiegelte Fläche in m²
    total_area_m2 = gdf.geometry.area.sum()
    unsealed_area_m2 = total_area_m2 * unseal_ratio
    
    # 2. Zurückgehaltenes Regenwasser (Schwammstadt-Effekt) in m³
    # Formel: Fläche (m²) * Niederschlag (m) * Abflussbeiwert-Reduktion (ca. 0.7)
    water_retained_m3 = (unsealed_area_m2 * (rainfall_mm / 1000.0)) * 0.7
    
    # 3. Empirischer Temperatur-Kühleffekt (Land Surface Temperature - LST)
    # Richtwert: Ca. 0.5°C bis 1.5°C Abkühlung pro 1.000 m² Grünelementen im Nahbereich
    cooling_effect_c = round((unsealed_area_m2 / 1000.0) * 0.12, 2)
    cooling_effect_c = min(cooling_effect_c, 3.5) # Deckelung auf realistisches Max
    
    return {
        "total_area_m2": round(total_area_m2, 1),
        "unsealed_area_m2": round(unsealed_area_m2, 1),
        "water_retained_m3": round(water_retained_m3, 1),
        "cooling_effect_c": cooling_effect_c
    }

def analyze_demographic_exposure(unsealed_gdf: gpd.GeoDataFrame, pop_density_per_ha: float = 80.0):
    """
    Schätzt ab, wie viele Anwohner (insb. ältere Menschen) vom Kühleffekt profitieren.
    """
    # 100m Puffer um die entsiegelten Flächen
    buffered = unsealed_gdf.buffer(100)
    buffer_area_ha = buffered.geometry.area.sum() / 10000.0
    
    affected_people = int(buffer_area_ha * pop_density_per_ha)
    senior_share_people = int(affected_people * 0.28) # Ø 28% Seniorenanteil in gealterten Quartieren
    
    return {
        "affected_people": affected_people,
        "senior_share_people": senior_share_people
    }