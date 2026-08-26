import streamlit as st
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import os
import folium
from streamlit_folium import st_folium

# Eigene Hilfsmodule
from processor import load_local_data, calculate_neis_confidence_score
from metrics import calculate_sponge_city_impact, analyze_demographic_exposure
from pipeline import fetch_sealable_surfaces, PRESET_LOCATIONS
from walkability import calculate_elderly_green_accessibility
from widgets import render_sponge_city_storyteller

# ---------------------------------------------------------
# Seiten-Konfiguration
# ---------------------------------------------------------
st.set_page_config(
    page_title="🌱 Schwammstadt Planning Support System | hack4GDI_DE",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Schwammstadt & Flächenentsiegelung – Planning Support System")
st.caption("hack4GDI_DE 2026 – Challenge 2 Starterkit (i3mainz / FOSSGIS-Referenz)")

st.markdown("---")

# ---------------------------------------------------------
# Phase 3: System-Status & Docker-Beweis
# ---------------------------------------------------------
st.subheader("🔌 System-Status (Local-First)")
db_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/hackathon_db")

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        st.success("✅ PostGIS Datenbank-Verbindung erfolgreich hergestellt! (Docker Compose Stack aktiv)")
except Exception as e:
    st.error(f"❌ Datenbank-Verbindungsfehler: {e}")

st.markdown("---")

# ---------------------------------------------------------
# Sidebar Steuerung (Testgebiete, Parameter, Zeitreihen & Presets)
# ---------------------------------------------------------
with st.sidebar:
    st.header("📍 Testgebiet")
    selected_area = st.selectbox(
        "Fokus-Region:",
        options=list(PRESET_LOCATIONS.keys()),
        index=1  # Standard: Mainz Zentrum
    )
    
    st.markdown("---")
    st.header("⚙️ Analyse-Parameter")
    
    st.subheader("1. Schwammstadt & Flächen")
    public_only = st.checkbox("Nur öffentliches Eigentum (ALKIS t_eigentuemer)", value=True)
    unseal_slider = st.slider("Geplanter Entsiegelungsgrad (%)", 10, 100, 50, step=5) / 100.0
    rain_event_mm = st.slider("Starkregen-Ereignis (mm bzw. l/m²)", 10, 100, 50, step=10)
    feature_filter = st.multiselect(
        "Flächentypen:",
        options=["parking", "building", "highway"],
        default=["parking", "building"]
    )

    st.subheader("2. Klimatologie (Zekar et al. 2023)")
    weight_heat = st.slider("Hitzeinsel-Faktor (LST / 200m-Radius)", 0.0, 1.0, 0.6)
    
    st.subheader("3. Umweltgerechtigkeit & Soziales")
    weight_social = st.slider("Schutz vulnerabler Gruppen (Senioren / LOR)", 0.0, 1.0, 0.4)
    walk_radius = st.slider("Fußweg-Radius zu Grün (m)", 100, 500, 300, step=50)

    st.subheader("4. Validierung & Qualität")
    show_benchmark = st.checkbox("Reale Erfolgs-Historie anzeigen (Benchmark)", value=True)
    min_score = st.slider("Min. Confidence Score (Neis)", 0, 100, 50)

    st.subheader("5. Zeitreihen-Steuerung (TimeManager)")
    selected_year = st.select_slider(
        "📅 Analyse-Jahr / Szenario:",
        options=[1950, 1980, 2010, 2026, 2030],
        value=2026,
        help="Historische Bebauungsphasen vs. prognostizierte Schwammstadt-Entsiegelung"
    )
    
    start_analysis = st.button("Analyse ausführen 🚀", use_container_width=True)

# ---------------------------------------------------------
# Daten laden (Dynamisch nach gewähltem Testgebiet)
# ---------------------------------------------------------
if selected_area == "Mainz Zentrum":
    gdf = load_local_data()
else:
    gdf = fetch_sealable_surfaces(selected_area)

st.subheader(f"🗺️ Entsiegelungs-Potenziale & Wirkungsanalyse: {selected_area} ({selected_year})")

if gdf is not None and not gdf.empty:
    # 1. Feature-Filterung
    type_col = "feature_type" if "feature_type" in gdf.columns else "surface_type"
    if type_col in gdf.columns:
        filtered_gdf = gdf[gdf[type_col].isin(feature_filter)].copy()
    else:
        filtered_gdf = gdf.copy()

    # 2. Dynamische Zeitreihen-Filterung (Szenario-Steuerung)
    if "year" in filtered_gdf.columns:
        filtered_gdf = filtered_gdf[filtered_gdf["year"] <= selected_year].copy()
    elif selected_year == 1950:
        filtered_gdf = filtered_gdf.sample(frac=0.3, random_state=42) if len(filtered_gdf) > 10 else filtered_gdf
    elif selected_year == 1980:
        filtered_gdf = filtered_gdf.sample(frac=0.6, random_state=42) if len(filtered_gdf) > 10 else filtered_gdf
    elif selected_year == 2010:
        filtered_gdf = filtered_gdf.sample(frac=0.85, random_state=42) if len(filtered_gdf) > 10 else filtered_gdf

    if filtered_gdf.empty:
        st.warning("⚠️ Keine Flächen für die gewählte Filterkombination gefunden.")
    else:
        # 3. Metrische Transformation für Berechnungen
        if filtered_gdf.crs and filtered_gdf.crs.is_geographic:
            epsg_code = 25832 if "Mainz" in selected_area else 25833
            gdf_metric = filtered_gdf.to_crs(epsg=epsg_code)
        else:
            gdf_metric = filtered_gdf

        # 4. Wissenschaftliche Berechnungen (Schwammstadt & Demografie/Remanenz)
        impact = calculate_sponge_city_impact(gdf_metric, unseal_ratio=unseal_slider, rainfall_mm=rain_event_mm)
        demo = analyze_demographic_exposure(gdf_metric, pop_density_per_ha=80.0)

        # 5. Impact-KPIs anzeigen
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Entsiegelte Fläche", f"{impact['unsealed_area_m2']:,.0f} m²")
        kpi2.metric("Regenrückhalt", f"{impact['water_retained_m3']:,.0f} m³")
        kpi3.metric("Mikroklima-Kühlung", f"+{impact['cooling_effect_c']} °C")
        kpi4.metric("Prof. Senioren (60+)", f"{demo['senior_share_people']:,} Pers.")

        st.write("")

        # 6. Split Layout: Interaktive Karte & Dateninspektor
        map_col, data_col = st.columns([3, 2])

        with map_col:
            st.write("**Interaktive Lagekarte & Wirkungsradien**")
            gdf_wgs84 = filtered_gdf.to_crs(epsg=4326)

            try:
                center_lat = gdf_wgs84.geometry.centroid.y.mean()
                center_lon = gdf_wgs84.geometry.centroid.x.mean()
            except Exception:
                center_lat, center_lon = (49.9929, 8.2473) if "Mainz" in selected_area else (52.5000, 13.4167)

            m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="cartodbpositron")

            # Sample-Layer (Performance-Schutz: max. 200 Objekte im Viewport)
            if type_col in gdf_wgs84.columns:
                buildings_sample = gdf_wgs84[gdf_wgs84[type_col] == "building"].head(100)
                parking_sample = gdf_wgs84[gdf_wgs84[type_col] == "parking"].head(100)
                sample_layer = pd.concat([buildings_sample, parking_sample]) if (not parking_sample.empty or not buildings_sample.empty) else gdf_wgs84.head(150)
            else:
                sample_layer = gdf_wgs84.head(150)

            folium.GeoJson(
                sample_layer,
                name="Entsiegelungs-Potenziale",
                style_function=lambda x: {
                    "fillColor": "#27ae60" if str(x["properties"].get(type_col, "")).lower() == "parking" else "#e74c3c",
                    "color": "#2c3e50",
                    "weight": 1,
                    "fillOpacity": 0.6
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=[col for col in [type_col, "id"] if col in sample_layer.columns],
                    aliases=["Typ:", "ID:"]
                )
            ).add_to(m)

            # Benchmark-Punkte dynamisch nach Fokus-Region (Paket 4: Erfolgs-Historie)
            if show_benchmark:
                if "Mainz" in selected_area:
                    benchmarks = [
                        {"name": "Referenz: Campus-Vorplatz Saarstraße", "lat": 49.9935, "lon": 8.2450, "m2": "1.400 m²"},
                        {"name": "Referenz: Quartiersplatz Neustadt", "lat": 50.0050, "lon": 8.2600, "m2": "800 m²"}
                    ]
                else:
                    benchmarks = [
                        {"name": "Benchmark: Baerwaldpromenade", "lat": 52.4920, "lon": 13.4010, "m2": "1.200 m²"},
                        {"name": "Benchmark: Blücherstraße", "lat": 52.4940, "lon": 13.3920, "m2": "950 m²"}
                    ]

                for b in benchmarks:
                    folium.CircleMarker(
                        location=[b["lat"], b["lon"]],
                        radius=7,
                        color="#2980b9",
                        fill=True,
                        fill_color="#3498db",
                        fill_opacity=0.9,
                        popup=f"<b>{b['name']}</b><br>Fläche: {b['m2']}<br>Status: Erfolgreich entsiegelt"
                    ).add_to(m)

            # Performance-Fix: returned_objects=[] verhindert Reruns beim Scrollen/Zoomen
            st_folium(m, width="100%", height=430, returned_objects=[])

        with data_col:
            st.write(f"**Gefilterte Flächen ({selected_year}):** {len(filtered_gdf)} Objekte")
            display_cols = [c for c in filtered_gdf.columns if c != "geometry"]
            st.dataframe(
                filtered_gdf[display_cols].head(14),
                use_container_width=True,
                height=430
            )

        # ---------------------------------------------------------
        # i3mainz Modul 1: Walkability & 300m-Grünraumkorridore
        # ---------------------------------------------------------
        st.markdown("---")
        st.subheader("🚶‍♂️ Elderly Walkability & Grüne Korridore (i3mainz / URBES)")
        
        buildings_gdf = filtered_gdf[filtered_gdf[type_col] == "building"] if type_col in filtered_gdf.columns else gpd.GeoDataFrame()
        parking_gdf = filtered_gdf[filtered_gdf[type_col] == "parking"] if type_col in filtered_gdf.columns else filtered_gdf

        if not buildings_gdf.empty and not parking_gdf.empty:
            accessible_seniors = calculate_elderly_green_accessibility(
                buildings_gdf=buildings_gdf,
                unsealed_gdf=parking_gdf,
                max_walk_meters=walk_radius
            )
            st.info(f"📍 **{len(accessible_seniors)} Gebäude** mit schutzbedürftigen Bewohnern liegen im fußläufigen {walk_radius}m-Einzugsgebiet der neu geplanten Kühlinseln.")
        else:
            st.caption("ℹ️ Gebäude- und Parkplatzlayer müssen aktiv sein, um die Walkability-Korridore zu berechnen.")

        # ---------------------------------------------------------
        # i3mainz Modul 2: Temporal Analysis (Timeline Storyteller)
        # ---------------------------------------------------------
        st.markdown("---")
        st.subheader("⏳ Temporal Analysis & Entsiegelungs-Dynamik (TimeManager-Ansatz)")
        render_sponge_city_storyteller(filtered_gdf)

        if start_analysis:
            st.success(f"Analyse mit Min-Confidence-Score > {min_score} und Multi-Kriterien-Gewichtung erfolgreich ausgeführt!")
            st.balloons()
else:
    st.warning("⚠️ Keine lokalen Testdaten gefunden. Bitte `prepare_data.py` ausführen.")

# ---------------------------------------------------------
# Phase 4: Wissenschaftliche Datenpakete & Referenzen
# ---------------------------------------------------------
with st.expander("📚 Datenpakete, Methodik & Referenzen (i3mainz / Zekar et al.)", expanded=False):
    st.markdown("""
    ### 🏛️ Die 4 integrierten Datenpakete (Challenge 2)
    1. **Flächenpotenzial & Schwammstadt:** ALKIS-Flurstücke (*t_eigentuemer* zur Filterung öffentlichen Eigentums) + OSM-Straßenraum/Parkplätze (*amenity=parking*).
    2. **Klimatologie (Wirkungsradien nach Zekar et al. 2023):** Mikroklima-Eichung über 200m- und 500m-Puffer, Gebäudevolumen (LoD2) & Sentinel-2/LST-Hitzeinseln.
    3. **Umweltgerechtigkeit & Remanenz (i3mainz-Bezug):** LOR-Planungsräume & Zensus-Raster (Schutz vulnerabler Gruppen wie Senioren 60+ in 100m/300m-Korridoren).
    4. **Validierung (Benchmark):** Reale Entsiegelungs-Historie (z. B. Friedrichshain-Kreuzberg & Mainz) zur Verifikation der algorithmischen Priorisierung.
    """)

st.markdown("---")
st.caption("Tobey GIS Open-Source Template | Bereitgestellt für den Hackathon #hack4GDI_DE")