import os
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Schwammstadt Pitch-Viewer", layout="wide")

st.title("🏙️ Challenge 2: Schwammstadt-Potenzialflächen (Jury-Pitch)")
st.caption("Präsentations-Dashboard zur Visualisierung der in QGIS berechneten MCE-Ergebnisse")

# Standard-Dateipfade oder Upload
DEFAULT_PATHS = ["data/ergebnis.geojson", "data/ergebnis.gpkg"]
selected_file = None

for path in DEFAULT_PATHS:
    if os.path.exists(path):
        selected_file = path
        break

uploaded_file = st.sidebar.file_uploader("Ergebnisdatei hochladen (.geojson, .gpkg)", type=["geojson", "gpkg"])
file_to_load = uploaded_file if uploaded_file is not None else selected_file

if not file_to_load:
    st.info("ℹ️ Bitte exportiert euren finalen Analyse-Layer aus QGIS nach `data/ergebnis.geojson` oder ladet ihn links in der Leiste hoch.")
    st.stop()

# Vektordaten laden
@st.cache_data
def load_data(file_source):
    gdf = gpd.read_file(file_source)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs(epsg=4326)
    return gdf

gdf = load_data(file_to_load)

# Sidebar: Dynamische Filter
st.sidebar.header("🎯 Filter & Steuerung")

filtered_gdf = gdf.copy()

# Filter nach Priorität (falls vorhanden)
if "prioritaet" in gdf.columns:
    priorities = list(gdf["prioritaet"].dropna().unique())
    selected_prio = st.sidebar.multiselect("Priorität filtern", priorities, default=priorities)
    if selected_prio:
        filtered_gdf = filtered_gdf[filtered_gdf["prioritaet"].isin(selected_prio)]

# Filter nach Maßnahme (falls vorhanden)
if "massnahme" in gdf.columns:
    measures = list(gdf["massnahme"].dropna().unique())
    selected_measures = st.sidebar.multiselect("Maßnahme wählen", measures, default=measures)
    if selected_measures:
        filtered_gdf = filtered_gdf[filtered_gdf["massnahme"].isin(selected_measures)]

# Filter nach Mindestfläche
if "flaeche_m2" in gdf.columns:
    min_val = float(gdf["flaeche_m2"].min())
    max_val = float(gdf["flaeche_m2"].max())
    min_size = st.sidebar.slider("Mindestgröße (m²)", min_val, max_val, min_val)
    filtered_gdf = filtered_gdf[filtered_gdf["flaeche_m2"] >= min_size]

# Spalte für Karteneinfärbung
colorable_cols = [col for col in ["prioritaet", "massnahme", "gesamt_score"] if col in gdf.columns]
color_col = st.sidebar.selectbox("Karte einfärben nach:", colorable_cols) if colorable_cols else None

# KPI-Kacheln (Dynamische Summen)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ausgewählte Maßnahmen", f"{len(filtered_gdf):,} Flächen")
with col2:
    if "flaeche_m2" in filtered_gdf.columns:
        st.metric("Entsiegelbare Gesamtfläche", f"{filtered_gdf['flaeche_m2'].sum():,.0f} m²")
    else:
        st.metric("Entsiegelbare Gesamtfläche", "N/A (Spalte fehlt)")
with col3:
    if "gesamt_score" in filtered_gdf.columns:
        st.metric("Durchschnittlicher Score", f"{filtered_gdf['gesamt_score'].mean():.2f}")
    else:
        st.metric("Analysierte Region", f"{gdf.get('stadt', ['Mainz / Berlin'])[0] if 'stadt' in gdf.columns else 'Fokusraum'}")

# Interaktive Folium-Karte
st.subheader("🗺️ Interaktive Potenzialflächenkarte")

if not filtered_gdf.empty:
    bounds = filtered_gdf.total_bounds
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
    m = folium.Map(location=center, zoom_start=14, tiles="CartoDB positron")

    tooltip_fields = [col for col in ["standort", "flaeche_m2", "prioritaet", "massnahme", "gesamt_score"] if col in filtered_gdf.columns]

    folium.GeoJson(
        filtered_gdf,
        style_function=lambda x: {
            "fillColor": "#2ecc71" if x["properties"].get("prioritaet") == "Hoch" else "#f39c12",
            "color": "#27ae60",
            "weight": 1.5,
            "fillOpacity": 0.6,
        },
        tooltip=folium.GeoJsonTooltip(fields=tooltip_fields, aliases=[f"{f.capitalize()}:" for f in tooltip_fields])
    ).add_to(m)

    st_folium(m, width="100%", height=520)
else:
    st.warning("Keine Flächen für die ausgewählten Filterkriterien gefunden.")