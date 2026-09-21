#!/usr/bin/env python3
"""
Prüfskript für die Schwammstadt-Challenge (#hack4GDI_DE).
Validiert Vorhandensein, KBS, Schemata und Topologie der Basisdaten (Mainz & Berlin)
sowie die Konformität der studentischen Ergebnisdateien.
"""

from pathlib import Path
import sys
import geopandas as gpd
import pyogrio

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# 1. Mainz GeoPackage Konfiguration
MAINZ_GPKG_PATH = DATA_DIR / "mainz" / "mainz_base.gpkg"
MAINZ_GPKG_ALT_PATH = DATA_DIR / "mainz_base.gpkg"

REQUIRED_MAINZ_LAYERS = {
    "alkis_flurstuecke": {
        "required_columns": ["geometry"],
        "optional_keys": ["flstkennz", "eigentuemer"],
        "allowed_crs": ["EPSG:25832"],
    },
    "osm_graues_band_parkplaetze": {
        "required_columns": ["geometry"],
        "optional_keys": ["amenity"],
        "allowed_crs": ["EPSG:25832"],
    },
    "osm_gruenflaechen_groesser_2ha": {
        "required_columns": ["geometry"],
        "optional_keys": ["flaeche_qm", "nutzung"],
        "allowed_crs": ["EPSG:25832"],
    },
    "klima_hitzeinseln": {
        "required_columns": ["geometry"],
        "optional_keys": ["temp_klasse", "klima_stufe"],
        "allowed_crs": ["EPSG:25832"],
    },
}

# 2. Berlin GeoPackage Konfiguration (data/berlin_fk/berlin_fk_base.gpkg)
BERLIN_GPKG_PATH = DATA_DIR / "berlin_fk" / "berlin_fk_base.gpkg"
BERLIN_GPKG_ALT_PATH = DATA_DIR / "berlin" / "berlin_base.gpkg"

REQUIRED_BERLIN_LAYERS = {
    "alkis_flurstuecke": {
        "required_columns": ["geometry"],
        "optional_keys": ["flstkennz", "eigentuemer"],
        "allowed_crs": ["EPSG:25833", "EPSG:25832"],
    },
    "osm_graues_band_parkplaetze": {
        "required_columns": ["geometry"],
        "optional_keys": ["amenity"],
        "allowed_crs": ["EPSG:25833", "EPSG:25832"],
    },
    "osm_gruenflaechen_groesser_2ha": {
        "required_columns": ["geometry"],
        "optional_keys": ["flaeche_qm", "nutzung"],
        "allowed_crs": ["EPSG:25833", "EPSG:25832"],
    },
    "klima_hitzeinseln": {
        "required_columns": ["geometry"],
        "optional_keys": ["temp_klasse", "klima_stufe"],
        "allowed_crs": ["EPSG:25833", "EPSG:25832"],
    },
}

BENCHMARK_PATH = DATA_DIR / "benchmark_entsiegelung.geojson"
BENCHMARK_ALT_PATH = DATA_DIR / "berlin" / "benchmark_entsiegelung.geojson"

STUDENT_OUTPUTS = {
    "Mainz Parkplaetze & Klima (Zwischenergebnis)": {
        "path": DATA_DIR / "mainz" / "parkplaetze_klima.geojson",
        "alt_path": DATA_DIR / "parkplaetze_klima.geojson",
        "template": DATA_DIR / "templates" / "parkplaetze_klima.template.geojson",
        "allowed_crs": ["EPSG:4326"],
        "required_columns": ["amenity", "temp_klasse", "score"],
    },
    "Mainz Schwammstadt-Potenziale (Endergebnis)": {
        "path": DATA_DIR / "mainz" / "ergebnis.geojson",
        "alt_path": DATA_DIR / "ergebnis.geojson",
        "template": DATA_DIR / "templates" / "ergebnis.template.geojson",
        "allowed_crs": ["EPSG:4326"],
        "required_columns": ["geometry"],
    },
}

def validate_gdf_layer(name, gdf, allowed_crs, required_columns, optional_keys=None):
    # 1. KBS-Prüfung
    actual_crs = gdf.crs.to_string() if gdf.crs else None
    if actual_crs not in allowed_crs:
        print(f"    [FEHLER] KBS '{actual_crs}' unzulaessig! Erlaubt: {allowed_crs}")
        return False
    print(f"    [OK] KBS gueltig: {actual_crs}")

    # 2. Pflicht-Attribute
    missing_cols = [c for c in required_columns if c not in gdf.columns]
    if missing_cols:
        print(f"    [FEHLER] Fehlende Pflichtattribute: {missing_cols}")
        return False
    print(f"    [OK] Pflichtspalten vorhanden: {required_columns}")

    if optional_keys:
        found_keys = [k for k in optional_keys if k in gdf.columns]
        if found_keys:
            print(f"    [INFO] Erkannte Attributfelder: {found_keys}")

    # 3. Topologische Gültigkeit
    invalid_cnt = (~gdf.geometry.is_valid).sum()
    empty_cnt = gdf.geometry.is_empty.sum()
    print(f"    [INFO] Features / Polygone: {len(gdf)}")

    if empty_cnt > 0:
        print(f"    [WARNUNG] Enthält {empty_cnt} leere Geometrien.")
    if invalid_cnt > 0:
        print(f"    [FEHLER] {invalid_cnt} Geometrien sind topologisch ungueltig!")
        return False

    print("    [OK] Geometrien sind topologisch gueltig.")
    return True

def validate_gpkg_dataset(title, primary_path, alt_path, required_layers):
    target = primary_path if primary_path.exists() else alt_path
    if not target or not target.exists():
        print(f"\n[FEHLER - BASISDATEN FEHLEN] {title} nicht gefunden unter: {primary_path.relative_to(BASE_DIR)}")
        return False

    print(f"\n[>] Validiere: {title} (./{target.relative_to(BASE_DIR)})")
    
    try:
        existing_layers = pyogrio.list_layers(target)[:, 0].tolist()
        print(f"    [INFO] Enthaltene Layer im GeoPackage: {existing_layers}")
    except Exception as e:
        print(f"    [FEHLER] GeoPackage kann nicht gelesen werden: {e}")
        return False

    all_layers_ok = True
    for layer_name, cfg in required_layers.items():
        print(f"\n  * Pruefe Layer: '{layer_name}'")
        if layer_name not in existing_layers:
            print(f"    [FEHLER] Pflicht-Layer '{layer_name}' fehlt im GeoPackage!")
            all_layers_ok = False
            continue

        try:
            gdf = gpd.read_file(target, layer=layer_name)
            if not validate_gdf_layer(
                layer_name,
                gdf,
                cfg["allowed_crs"],
                cfg["required_columns"],
                cfg.get("optional_keys")
            ):
                all_layers_ok = False
        except Exception as e:
            print(f"    [FEHLER] Layer '{layer_name}' unlesbar: {e}")
            all_layers_ok = False

    return all_layers_ok

def validate_student_output(name, config):
    target = config["path"] if config["path"].exists() else config.get("alt_path")

    if not target or not target.exists():
        print(f"\n[INFO - CHALLENGE STATUS] {name}")
        print(f"  -> Datei noch nicht vorhanden: ./{config['path'].relative_to(BASE_DIR)}")
        template_path = config.get("template")
        if template_path and template_path.exists():
            print(f"  -> Vorlage zur Orientierung: ./{template_path.relative_to(BASE_DIR)}")
        print("  -> Dieser Layer wird von den Studierenden im Workflow selbststaendig generiert.")
        return True

    rel_path = target.relative_to(BASE_DIR)
    print(f"\n[>] Validiere studentische Ergebnisdatei: {name} (./{rel_path})")

    try:
        gdf = gpd.read_file(target)
        print("    [OK] Geodaten erfolgreich geladen.")
    except Exception as e:
        print(f"    [FEHLER] Datei unlesbar: {e}")
        return False

    actual_crs = gdf.crs.to_string() if gdf.crs else None
    if actual_crs not in config["allowed_crs"]:
        print(f"    [AUTO-FIX] KBS war '{actual_crs}'. Reprojiziere automatisch nach EPSG:4326...")
        try:
            gdf = gdf.to_crs("EPSG:4326")
            gdf.to_file(target, driver="GeoJSON")
            actual_crs = "EPSG:4326"
            print("    [OK] Erfolgreich ueberschrieben mit EPSG:4326.")
        except Exception as e:
            print(f"    [FEHLER] Konvertierung nach EPSG:4326 fehlgeschlagen: {e}")
            return False

    return validate_gdf_layer(name, gdf, config["allowed_crs"], config["required_columns"])

def main():
    print("=" * 68)
    print("  Schwammstadt-Challenge: Daten- und Schema-Validierung")
    print(f"  Root: {BASE_DIR}")
    print("=" * 68)

    success = True

    print("\n--- Teil 1: Pruefung der bereitgestellten Basisdaten ---")
    
    # 1. Mainz GeoPackage
    if not validate_gpkg_dataset("Mainz Basisdaten", MAINZ_GPKG_PATH, MAINZ_GPKG_ALT_PATH, REQUIRED_MAINZ_LAYERS):
        success = False

    # 2. Berlin GeoPackage (data/berlin_fk/berlin_fk_base.gpkg)
    target_berlin = BERLIN_GPKG_PATH if BERLIN_GPKG_PATH.exists() else BERLIN_GPKG_ALT_PATH
    if target_berlin.exists():
        if not validate_gpkg_dataset("Berlin Basisdaten", BERLIN_GPKG_PATH, BERLIN_GPKG_ALT_PATH, REQUIRED_BERLIN_LAYERS):
            success = False
    else:
        print(f"\n[INFO] Keine berlin_fk_base.gpkg unter ./{BERLIN_GPKG_PATH.relative_to(BASE_DIR)} gefunden (optional).")

    # 3. Benchmark GeoJSON
    bench_target = BENCHMARK_PATH if BENCHMARK_PATH.exists() else BENCHMARK_ALT_PATH
    if bench_target and bench_target.exists():
        print(f"\n[>] Validiere: Berlin Benchmark (./{bench_target.relative_to(BASE_DIR)})")
        try:
            bench_gdf = gpd.read_file(bench_target)
            if not validate_gdf_layer("Benchmark", bench_gdf, ["EPSG:4326", "EPSG:25833", "EPSG:25832"], ["geometry"]):
                success = False
        except Exception as e:
            print(f"    [FEHLER] Benchmark nicht lesbar: {e}")
            success = False

    print("\n--- Teil 2: Status der studentischen Ergebnisdaten ---")
    for name, cfg in STUDENT_OUTPUTS.items():
        if not validate_student_output(name, cfg):
            success = False

    print("\n" + "=" * 68)
    if success:
        print("  ERGEBNIS: System- und Datencheck erfolgreich abgeschlossen.")
        print("=" * 68)
        sys.exit(0)
    else:
        print("  ERGEBNIS: Kritische Fehler in den Basisdaten oder Attributen!")
        print("=" * 68)
        sys.exit(1)

if __name__ == "__main__":
    main()