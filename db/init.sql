-- 1. PostGIS Erweiterung aktivieren (falls noch nicht geschehen)
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Tabelle für die rohen Import-Daten (z.B. ALKIS / FIS-Broker Flurstücke)
CREATE TABLE IF NOT EXISTS raw_plots (
    id SERIAL PRIMARY KEY,
    gml_id VARCHAR(100),
    land_use VARCHAR(100),       -- z.B. "Wohnbaufläche", "Verkehrsfläche"
    sealing_rate NUMERIC,        -- Versiegelungsgrad in % (0 - 100)
    owner_type VARCHAR(50),      -- "public", "private", "unknown"
    geom GEOMETRY(MultiPolygon, 25833) -- UTM Zone 33N (Standard für Berlin/Brandenburg)
);

-- Räumlichen Index erstellen für schnelle Verschneidungen
CREATE INDEX IF NOT EXISTS idx_raw_plots_geom ON raw_plots USING GIST(geom);


-- 3. Tabelle für die Ergebnisse der Studenten (Entsiegelungspotenziale)
CREATE TABLE IF NOT EXISTS de_sealing_potentials (
    id SERIAL PRIMARY KEY,
    raw_plot_id INT REFERENCES raw_plots(id) ON DELETE CASCADE,
    area_sqm NUMERIC,            -- Berechnete Fläche in m²
    priority_score NUMERIC,      -- Dein MCE-Score (wird von Studenten berechnet)
    geom GEOMETRY(MultiPolygon, 25833)
);

CREATE INDEX IF NOT EXISTS idx_potentials_geom ON de_sealing_potentials USING GIST(geom);


-- 4. Hilfs-View / Trigger-Entwurf für den Geometrie-Check (QA/QC)
-- Dieser Befehl dient als Spickzettel für die Studenten, wie fehlerhafte Geometrien repariert werden
-- (ST_MakeValid fängt Selbstdurchdringungen ab)
-- SQL-Beispiel für das README:
-- UPDATE raw_plots SET geom = ST_Multi(ST_MakeValid(geom)) WHERE NOT ST_IsValid(geom);