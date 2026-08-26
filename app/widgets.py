import streamlit as st
import geopandas as gpd

def render_sponge_city_storyteller(gdf: gpd.GeoDataFrame):
    """
    Rendert das TimeManager- & Szenarien-Widget zur Visualisierung
    der zeitlichen Dynamik von Flächenfraß und Entsiegelungs-Zielen.
    """
    st.write("### ⏳ Zeitliche Entwicklung & Entsiegelungs-Dynamik")
    
    # TimeManager-Slider (nach i3mainz Temporal Analysis Methodik)
    selected_year = st.select_slider(
        "📅 Analyse-Jahr / Szenario:",
        options=[1950, 1980, 2010, 2026, 2030],
        value=2026,
        help="Historische Bebauungsphasen vs. prognostizierte Schwammstadt-Entsiegelung"
    )
    
    # Dynamisches Storytelling passend zum gewählten Zeitschritt
    if selected_year == 2030:
        st.success(
            "🎯 **Ziel 2030 (Schwammstadt-Transformation):** Vollständige Entsiegelung "
            "überdimensionierter Parkbuchten und Umbau in retentive Grünstreifen."
        )
    elif selected_year == 2026:
        st.info(
            "📍 **IST-Zustand 2026:** Aktuelle Erfassung der Flächenpotenziale "
            "(Verkehrsflächen, Parkplätze und versiegelte Liegenschaften)."
        )
    elif selected_year == 2010:
        st.caption(
            "🏢 **Zustand 2010:** Verdichtung der urbanen Blockstrukturen vor Start "
            "der kommunalen Entsiegelungsoffensiven."
        )
    else:
        st.caption(
            f"🏛️ **Historischer Referenzstand ({selected_year}):** Siedlungsgefüge vor der "
            "massiven Zunahme von versiegelten Verkehrsflächen."
        )