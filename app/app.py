import os
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Schwammstadt Pitch-Viewer", layout="wide")[cite: 1]

st.title("🏙️ Challenge 2: Schwammstadt-Potenzialflächen (Jury-Pitch)")[cite: 1]
st.caption("Präsentations-Dashboard zur Visualisierung der in QGIS berechneten MCE-Ergebnisse")[cite: 1]

# Standard-Dateipfade oder Upload
DEFAULT_PATHS = ["data/ergebnis.geojson", "data/ergebnis.gpkg"][cite: 1]
selected_file = None[cite: 1]

for path in DEFAULT_PATHS:[cite: 1]
    if os.path.exists(path):[cite: 1]
        selected_file = path[cite: 1]
        break[cite: 1]

uploaded_file = st.sidebar.file_uploader("Ergebnisdatei hochladen (.geojson, .gpkg)", type=["geojson", "gpkg"])[cite: 1]
file_to_load = uploaded_file if uploaded_file is not None else selected_file[cite: 1]

if not file_to_load:[cite: 1]
    st.info("ℹ️ Bitte exportiert euren finalen Analyse-Layer aus QGIS nach `data/ergebnis.geojson` oder ladet ihn links in der Leiste hoch.")[cite: 1]
    st.stop()[cite: 1]

# Vektordaten laden
@st.cache_data[cite: 1]
def load_data(file_source):[cite: 1]
    gdf = gpd.read_file(file_source)[cite: 1]
    if gdf.crs != "EPSG:4326":[cite: 1]
        gdf = gdf.to_crs(epsg=4326)[cite: 1]
    return gdf[cite: 1]

gdf = load_data(file_to_load)[cite: 1]

# Sidebar: Dynamische Filter
st.sidebar.header("🎯 Filter & Steuerung")[cite: 1]

filtered_gdf = gdf.copy()[cite: 1]

# Filter nach Priorität (falls vorhanden)
if "prioritaet" in gdf.columns:[cite: 1]
    priorities = list(gdf["prioritaet"].dropna().unique())[cite: 1]
    selected_prio = st.sidebar.multiselect("Priorität filtern", priorities, default=priorities)[cite: 1]
    if selected_prio:[cite: 1]
        filtered_gdf = filtered_gdf[filtered_gdf["prioritaet"].isin(selected_prio)][cite: 1]

# Filter nach Maßnahme (falls vorhanden)
if "massnahme" in gdf.columns:[cite: 1]
    measures = list(gdf["massnahme"].dropna().unique())[cite: 1]
    selected_measures = st.sidebar.multiselect("Maßnahme wählen", measures, default=measures)[cite: 1]
    if selected_measures:[cite: 1]
        filtered_gdf = filtered_gdf[filtered_gdf["massnahme"].isin(selected_measures)][cite: 1]

# Filter nach Mindestfläche
if "flaeche_m2" in gdf.columns:[cite: 1]
    min_val = float(gdf["flaeche_m2"].min())[cite: 1]
    max_val = float(gdf["flaeche_m2"].max())[cite: 1]
    min_size = st.sidebar.slider("Mindestgröße (m²)", min_val, max_val, min_val)[cite: 1]
    filtered_gdf = filtered_gdf[filtered_gdf["flaeche_m2"] >= min_size][cite: 1]

# Spalte für Karteneinfärbung
colorable_cols = [col for col in ["prioritaet", "massnahme", "gesamt_score"] if col in gdf.columns][cite: 1]
color_col = st.sidebar.selectbox("Karte einfärben nach:", colorable_cols) if colorable_cols else None[cite: 1]

# KPI-Kacheln (Dynamische Summen)
col1, col2, col3 = st.columns(3)[cite: 1]
with col1:[cite: 1]
    st.metric("Ausgewählte Maßnahmen", f"{len(filtered_gdf):,} Flächen")[cite: 1]
with col2:[cite: 1]
    if "flaeche_m2" in filtered_gdf.columns:[cite: 1]
        st.metric("Entsiegelbare Gesamtfläche", f"{filtered_gdf['flaeche_m2'].sum():,.0f} m²")[cite: 1]
    else:
        st.metric("Entsiegelbare Gesamtfläche", "N/A (Spalte fehlt)")[cite: 1]
with col3:[cite: 1]
    if "gesamt_score" in filtered_gdf.columns:[cite: 1]
        st.metric("Durchschnittlicher Score", f"{filtered_gdf['gesamt_score'].mean():.2f}")[cite: 1]
    else:
        st.metric("Analysierte Region", f"{gdf.get('stadt', ['Mainz / Berlin'])[0] if 'stadt' in gdf.columns else 'Fokusraum'}")[cite: 1]

# Interaktive Folium-Karte
st.subheader("🗺️ Interaktive Potenzialflächenkarte")[cite: 1]

if not filtered_gdf.empty:[cite: 1]
    bounds = filtered_gdf.total_bounds[cite: 1]
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2][cite: 1]
    
    # Standard OpenStreetMap-Tiles ohne API-Key-Wasserzeichen
    m = folium.Map(location=center, zoom_start=14, tiles="OpenStreetMap")

    tooltip_fields = [col for col in ["standort", "flaeche_m2", "prioritaet", "massnahme", "gesamt_score"] if col in filtered_gdf.columns][cite: 1]

    folium.GeoJson(
        filtered_gdf,[cite: 1]
        style_function=lambda x: {[cite: 1]
            "fillColor": "#2ecc71" if x["properties"].get("prioritaet") == "Hoch" else "#f39c12",[cite: 1]
            "color": "#27ae60",[cite: 1]
            "weight": 1.5,[cite: 1]
            "fillOpacity": 0.6,[cite: 1]
        },
        tooltip=folium.GeoJsonTooltip(fields=tooltip_fields, aliases=[f"{f.capitalize()}:" for f in tooltip_fields])[cite: 1]
    ).add_to(m)[cite: 1]

    st_folium(m, width="100%", height=520)[cite: 1]
else:
    st.warning("Keine Flächen für die ausgewählten Filterkriterien gefunden.")[cite: 1]