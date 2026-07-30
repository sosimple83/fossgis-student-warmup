import streamlit as st
import geopandas as gpd
from sqlalchemy import create_engine
import os
from processor import load_local_data, calculate_neis_confidence_score

# Page Configuration
st.set_page_config(
    page_title="🌱 Flächenentsiegelung Starterkit",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Schwammstadt & Flächenentsiegelung")
st.caption("hack4GDI_DE 2026 – Challenge 2 Starterkit")

st.markdown("---")

# 1. Datenbank-Verbindung prüfen
st.subheader("🔌 System-Status")
db_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/hackathon_db")

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        st.success("✅ PostGIS Datenbank-Verbindung erfolgreich hergestellt!")
except Exception as e:
    st.error(f"❌ Datenbank-Verbindungsfehler: {e}")

# 2. Daten laden & Analyse-Steuerung
st.markdown("---")
st.subheader("🗺️ Entsiegelungs-Potenziale (Mainz)")

col1, col2 = st.columns([1, 2])

with col1:
    st.write("**Qualitäts- & Filter-Einstellungen**")
    min_score = st.slider("Min. Confidence Score (Neis-Validierung)", 0, 100, 50)
    
    feature_filter = st.multiselect(
        "Flächentyp auswählen:",
        options=["building", "parking"],
        default=["building", "parking"]
    )
    
    start_analysis = st.button("Analyse ausführen 🚀", use_container_width=True)

with col2:
    gdf = load_local_data()
    
    if gdf is not None:
        st.write(f"**Geladene Geodaten:** {len(gdf)} Objekte aus `sample_data.gpkg` gefunden.")
        
        # Geodaten-Tabelle anzeigen (ohne Geometrie-Spalte für saubere Darstellung)
        st.dataframe(
            gdf.drop(columns=["geometry"]).head(10), 
            use_container_width=True
        )
        
        if start_analysis:
            st.info(f"Analysiere Flächen mit Filter für Typen {feature_filter} und Score > {min_score}...")
            # Hier kann das Team im Hackathon eigene Berechnungen anstellen!
            st.balloons()
    else:
        st.warning("⚠️ Keine lokalen Testdaten gefunden under `/data/sample_data.gpkg`. Bitte zuerst `prepare_data.py` ausführen.")

st.markdown("---")
st.caption("Tobey GIS Open-Source Template | Bereitgestellt für den Hackathon")