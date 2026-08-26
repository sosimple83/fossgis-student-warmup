from metrics import calculate_sponge_city_impact
# Berechnet den Effekt bei 50% Entsiegelung und 50mm Starkregen
results = calculate_sponge_city_impact(gdf, unseal_ratio=0.5, rainfall_mm=50)
print(f"Eingesparte Versiegelung: {results['unsealed_area_m2']} m²")