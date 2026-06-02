import streamlit as st
import geopandas as gpd
import folium
import rasterio
import requests
import pandas as pd
import plotly.graph_objects as go
import datetime
import os
from streamlit_folium import st_folium
from folium.plugins import MeasureControl, Fullscreen, MiniMap, MousePosition

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SIG Météo · Maroc",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DESIGN SYSTEM — ENTERPRISE BLACK & WHITE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    /* Light mode palette */
    --bg:          #f4f6f9;
    --black:       #f4f6f9;
    --black-2:     #ffffff;
    --black-3:     #f0f2f5;
    --black-4:     #e8ebf0;
    --gray-1:      #dde1e8;
    --gray-2:      #c8cdd6;
    --gray-3:      #8892a0;
    --gray-4:      #606878;
    --gray-5:      #3d4450;
    --gray-6:      #1e2530;
    --gray-7:      #111520;
    --white:       #1e2530;
    --pure-white:  #111520;
    --accent:      #1a5fe0;
    --border:      #dde1e8;
    --border-light:#c8cdd6;
    /* Brand colors */
    --blue:        #1a5fe0;
    --blue-light:  #e8f0fc;
    --teal:        #0d9488;
    --teal-light:  #e6f7f5;
    --amber:       #d97706;
    --amber-light: #fef3e2;
    --rose:        #e11d48;
    --rose-light:  #fde8ee;
    --sans:        'IBM Plex Sans', sans-serif;
    --mono:        'IBM Plex Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--sans) !important;
}

.stApp {
    background: var(--bg) !important;
    color: var(--gray-6) !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 2rem 3rem 2rem !important;
    max-width: 100% !important;
}

/* ── SIDEBAR TOUJOURS VISIBLE ── */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: none !important;
}
[data-testid="stSidebar"] {
    min-width: 260px !important;
    max-width: 260px !important;
    transform: none !important;
    visibility: visible !important;
}

/* ────────────────────────────
   SIDEBAR
──────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--black-2) !important;
    border-right: 1px solid var(--border) !important;
    width: 260px !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 0 !important;
}

.sb-brand {
    padding: 1.6rem 1.4rem 1.3rem;
    border-bottom: 1px solid var(--border);
}
.sb-brand-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--gray-3);
    margin-bottom: 0.4rem;
}
.sb-brand-name {
    font-size: 1rem;
    font-weight: 600;
    color: var(--pure-white);
    letter-spacing: -0.3px;
    line-height: 1.2;
}
.sb-brand-desc {
    font-size: 0.72rem;
    color: var(--gray-4);
    margin-top: 0.25rem;
    font-weight: 300;
}

.sb-section {
    padding: 1.1rem 1.4rem 0.9rem;
    border-bottom: 1px solid var(--border);
}
.sb-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--gray-3);
    margin-bottom: 0.9rem;
    display: block;
}

.sb-footer {
    padding: 1.2rem 1.4rem;
}
.sb-footer-title {
    font-family: var(--mono);
    font-size: 0.56rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--gray-3);
    margin-bottom: 0.7rem;
    display: block;
}
.sb-footer-item {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--gray-3);
    line-height: 2.1;
}

[data-testid="stSelectbox"] label {
    font-family: var(--mono) !important;
    font-size: 0.6rem !important;
    font-weight: 500 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--gray-4) !important;
}
[data-testid="stSelectbox"] > div > div {
    background: var(--black-3) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 3px !important;
    color: var(--gray-6) !important;
    font-family: var(--sans) !important;
    font-size: 0.85rem !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--gray-5) !important;
    box-shadow: none !important;
}
[data-testid="stSelectbox"] svg {
    color: var(--gray-4) !important;
}

[data-baseweb="popover"] {
    background: var(--black-3) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 3px !important;
}
[data-baseweb="menu"] {
    background: var(--black-3) !important;
}
[data-baseweb="option"] {
    background: var(--black-3) !important;
    color: var(--gray-6) !important;
    font-family: var(--sans) !important;
    font-size: 0.85rem !important;
}
[data-baseweb="option"]:hover {
    background: var(--black-4) !important;
}

[data-testid="stRadio"] label {
    font-family: var(--mono) !important;
    font-size: 0.6rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--gray-4) !important;
}
[data-testid="stRadio"] > div {
    gap: 0.3rem !important;
}
[data-testid="stRadio"] > div > label {
    background: var(--black-3) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 3px !important;
    padding: 0.55rem 1rem !important;
    width: 100% !important;
    transition: border-color 0.12s !important;
    color: var(--gray-5) !important;
}
[data-testid="stRadio"] > div > label:hover {
    border-color: var(--gray-5) !important;
}
[data-testid="stRadio"] > div > label[data-checked="true"],
[data-testid="stRadio"] > div > label[aria-checked="true"] {
    border-color: var(--gray-5) !important;
    background: var(--black-4) !important;
}

/* ────────────────────────────
   HEADER
──────────────────────────── */
.geo-header {
    background: var(--black-2);
    border-bottom: 1px solid var(--border);
    margin: 0 -2rem 2rem -2rem;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
}
.geo-header-left {
    display: flex;
    align-items: center;
    gap: 1.4rem;
}
.geo-header-divider-v {
    width: 1px;
    height: 28px;
    background: var(--border-light);
}
.geo-header-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--pure-white);
    letter-spacing: -0.2px;
}
.geo-header-sub {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--gray-3);
    margin-top: 0.15rem;
}
.geo-header-right {
    display: flex;
    align-items: center;
    gap: 2rem;
}
.geo-header-meta {
    text-align: right;
}
.geo-header-meta-label {
    font-family: var(--mono);
    font-size: 0.56rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--gray-3);
}
.geo-header-meta-value {
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--gray-5);
    margin-top: 0.1rem;
}
.geo-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--gray-4);
    border: 1px solid var(--border-light);
    padding: 0.35rem 0.8rem;
    border-radius: 2px;
}
.geo-status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4ade80;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* ────────────────────────────
   KPI GRID
──────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    margin-bottom: 1.8rem;
}
.kpi-card {
    background: var(--black-2);
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    padding: 1.3rem 1.5rem;
    border-top: 2px solid var(--kpi-accent, var(--border-light));
    transition: background 0.15s;
}
.kpi-card:hover {
    background: var(--black-3);
}
.kpi-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--gray-3);
    margin-bottom: 0.6rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 300;
    color: var(--pure-white);
    line-height: 1;
    letter-spacing: -1px;
    margin-bottom: 0.35rem;
}
.kpi-value span {
    font-size: 0.9rem;
    font-weight: 400;
    color: var(--gray-4);
    letter-spacing: 0;
}
.kpi-meta {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--gray-3);
}
.kpi-text {
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--gray-6);
    line-height: 1.4;
    margin-bottom: 0.35rem;
}

/* ────────────────────────────
   SECTION LABEL
──────────────────────────── */
.section-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--gray-3);
    margin-bottom: 0.8rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}

/* ────────────────────────────
   PANEL
──────────────────────────── */
.panel-head {
    background: var(--black-3);
    border: 1px solid var(--border);
    border-bottom: none;
    padding: 0.6rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.panel-head-title {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: var(--gray-5);
}
.panel-head-meta {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 1px;
    color: var(--gray-3);
}

/* ────────────────────────────
   DATAFRAME
──────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] th {
    background: var(--black-3) !important;
    font-family: var(--mono) !important;
    font-size: 0.6rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--gray-4) !important;
    border-bottom: 1px solid var(--border-light) !important;
}
[data-testid="stDataFrame"] td {
    font-family: var(--mono) !important;
    font-size: 0.76rem !important;
    color: var(--gray-5) !important;
    background: var(--black-2) !important;
    border-color: var(--border) !important;
}
[data-testid="stDataFrame"] tr:nth-child(even) td {
    background: var(--black-3) !important;
}

/* ────────────────────────────
   ALERT
──────────────────────────── */
[data-testid="stAlert"] {
    background: var(--black-3) !important;
    border: 1px solid var(--border-light) !important;
    border-left: 3px solid var(--gray-5) !important;
    color: var(--gray-5) !important;
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    border-radius: 2px !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--black); }
::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DONNÉES
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    path_r = os.path.join(data_dir, "Regions_WGS84.shp")
    path_p = os.path.join(data_dir, "Provinces_WGS84.shp")
    path_c = os.path.join(data_dir, "communes_WGS84.shp")
    
    for path in [path_r, path_p, path_c]:
        if not os.path.exists(path):
            st.error(f"❌ Fichier introuvable : `{path}`.")
            st.stop()
            
    r = gpd.read_file(path_r)
    p = gpd.read_file(path_p)
    c = gpd.read_file(path_c)
    return r, p, c

regions, provinces, communes = load_data()

# Uniformisation du nom ou filtre pour Béni Mellal-Khénifra
region_cible = "Béni Mellal-Khénifra"
# Au cas où l'accentuation diffère dans ton fichier SHP, on cherche une correspondance souple
regions_filtrees = regions[regions["libelle_fr"].str.contains("Mellal", case=False, na=False)]
if len(regions_filtrees) > 0:
    region_choisie = regions_filtrees.iloc[0]["libelle_fr"]
else:
    region_choisie = regions["libelle_fr"].unique()[0]

mes_regions = regions[regions["libelle_fr"] == region_choisie]

# ─────────────────────────────────────────────
# SIDEBAR (LOGIQUE MODIFIÉE SUR LES SELECTIONS)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-brand-label">Système d'information géographique</div>
      <div class="sb-brand-name">SIG Météo — Maroc</div>
      <div class="sb-brand-desc">Cartographie administrative &amp; prévisions</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-section">
      <span class="sb-label">Localisation</span>
    """, unsafe_allow_html=True)

    # La région reste affichée mais restreinte à ton choix unique
    st.selectbox("Région", [region_choisie], label_visibility="collapsed", disabled=True)

    # Récupération des provinces liées à cette région
    liste_provinces = provinces[
        provinces["code_reg"] == mes_regions.iloc[0]["code_reg"]
    ]["libelle_fr"].dropna().unique()
    
    # Ajout de l'état initial vide exigé pour la Province
    options_provinces = ["-- Sélectionner une province --"] + list(liste_provinces)
    province_choisie_raw = st.selectbox("Province", options_provinces, index=0, label_visibility="collapsed")

    # Logique conditionnelle pour les communes
    commune_choisie = None
    if province_choisie_raw != "-- Sélectionner une province --":
        province_choisie = province_choisie_raw
        liste_communes = communes[
            communes["FIRST_prov"] == province_choisie
        ]["FIRST_com_"].dropna().unique()
        
        # Ajout de l'état initial vide exigé pour la Commune
        options_communes = ["-- Sélectionner une commune --"] + list(liste_communes)
        commune_choisie_raw = st.selectbox("Commune", options_communes, index=0, label_visibility="collapsed")
        
        if commune_choisie_raw != "-- Sélectionner une commune --":
            commune_choisie = commune_choisie_raw
    else:
        province_choisie = None
        # Quand aucune province n'est cliquée, le champ commune affiche une liste vide / inactive
        st.selectbox("Commune", ["-- Sélectionner une commune --"], index=0, label_visibility="collapsed", disabled=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-section">
      <span class="sb-label">Indicateur météorologique</span>
    """, unsafe_allow_html=True)

    choix = st.radio(
        "Indicateur",
        ["Température", "Précipitations"],
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-footer">
      <span class="sb-footer-title">Sources</span>
      <div class="sb-footer-item">
        HCP Maroc — Découpages administratifs<br>
        Open-Meteo — Prévisions météorologiques<br>
        Terrestris — WMS SRTM30 Relief<br>
        Python · GeoPandas · Folium · Streamlit
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# GÉOMÉTRIE (DÉTERMINATION DU COUPLAGE GÉOGRAPHIQUE ACTIF)
# ─────────────────────────────────────────────
if commune_choisie:
    # Si une commune est explicitement sélectionnée
    ma_commune = communes[communes["FIRST_com_"] == commune_choisie]
    centre = ma_commune.geometry.centroid.iloc[0]
    zone_label = commune_choisie
    couche_geometrique = ma_commune
elif province_choisie:
    # Si seule la province est sélectionnée
    ma_province = provinces[provinces["libelle_fr"] == province_choisie]
    centre = ma_province.geometry.centroid.iloc[0]
    zone_label = province_choisie
    couche_geometrique = ma_province
else:
    # Par défaut : Unique affichage régional (Béni Mellal-Khénifra)
    centre = mes_regions.geometry.centroid.iloc[0]
    zone_label = region_choisie
    couche_geometrique = mes_regions

latitude  = centre.y
longitude = centre.x

# ─────────────────────────────────────────────
# MÉTÉO
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_meteo(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&forecast_days=15"
        f"&timezone=auto"
    )
    r = requests.get(url, timeout=10)
    d = r.json()
    df = pd.DataFrame({
        "Date":                 d["daily"]["time"],
        "Temp. max (°C)":       d["daily"]["temperature_2m_max"],
        "Temp. min (°C)":       d["daily"]["temperature_2m_min"],
        "Précipitations (mm)":  d["daily"]["precipitation_sum"],
    })
    df["Date"] = pd.to_datetime(df["Date"])
    return df

meteo_df  = fetch_meteo(latitude, longitude)
temp_max = meteo_df["Temp. max (°C)"].max()
temp_min = meteo_df["Temp. min (°C)"].min()

prec_auj = meteo_df["Précipitations (mm)"].iloc[0]
prec_tot = meteo_df["Précipitations (mm)"].sum()

mean_temp_max = meteo_df["Temp. max (°C)"].mean()
mean_temp_min = meteo_df["Temp. min (°C)"].mean()
mean_precip   = meteo_df["Précipitations (mm)"].mean()
today_str = datetime.date.today().strftime("%d %b %Y").upper()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="geo-header">
  <div class="geo-header-left">
    <div class="geo-header-divider-v"></div>
    <div>
      <div class="geo-header-title">Tableau de bord SIG &mdash; Météorologie</div>
      <div class="geo-header-sub">Cartographie administrative &middot; Maroc</div>
    </div>
    <div class="geo-header-divider-v"></div>
    <div>
      <div class="geo-header-meta-label">Zone active</div>
      <div class="geo-header-meta-value">{zone_label} &middot; {region_choisie}</div>
    </div>
  </div>
  <div class="geo-header-right">
    <div class="geo-header-meta">
      <div class="geo-header-meta-label">Coordonnées</div>
      <div class="geo-header-meta-value">{latitude:.4f}&deg; N &middot; {longitude:.4f}&deg; E</div>
    </div>
    <div class="geo-header-divider-v"></div>
    <div class="geo-header-meta">
      <div class="geo-header-meta-label">Date</div>
      <div class="geo-header-meta-value">{today_str}</div>
    </div>
    <div class="geo-header-divider-v"></div>
    <div class="geo-status">
      <div class="geo-status-dot"></div>
      Open-Meteo Live
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card" style="--kpi-accent:#1a5fe0;">
    <div class="kpi-label">Température maximale</div>
    <div class="kpi-value">{temp_max:.1f}<span> °C</span></div>
    <div class="kpi-meta">Minimum prévu — {temp_min:.1f} °C</div>
  </div>
  <div class="kpi-card" style="--kpi-accent:#0d9488;">
    <div class="kpi-label">Précipitations du jour</div>
    <div class="kpi-value">{prec_auj:.1f}<span> mm</span></div>
    <div class="kpi-meta">Cumul 15 jours — {prec_tot:.1f} mm</div>
  </div>
  <div class="kpi-card" style="--kpi-accent:#d97706;">
    <div class="kpi-label">Région administrative</div>
    <div class="kpi-text">{region_choisie}</div>
    <div class="kpi-meta">{province_choisie if province_choisie else "Aucune province active"}</div>
  </div>
  <div class="kpi-card" style="--kpi-accent:#e11d48;">
    <div class="kpi-label">Unité spatiale</div>
    <div class="kpi-text">{zone_label}</div>
    <div class="kpi-meta">{latitude:.4f}° N · {longitude:.4f}° E</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────
col_map, col_right = st.columns([3, 2], gap="large")

# ── CARTE ──
with col_map:
    st.markdown('<div class="section-label">Carte interactive — Couche administrative &amp; relief</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="panel-head">
      <span class="panel-head-title">{zone_label}</span>
      <span class="panel-head-meta">WGS84 · EPSG:4326 · Folium</span>
    </div>
    """, unsafe_allow_html=True)

    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=9 if (province_choisie or commune_choisie) else 8,
        control_scale=True,
        tiles=None,
    )

    # Fonds de carte
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="CartoDB", name="Positron (clair)", subdomains="abcd",
    ).add_to(m)
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="CartoDB", name="Dark Matter", subdomains="abcd",
    ).add_to(m)
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satellite Esri",
    ).add_to(m)
    folium.raster_layers.WmsTileLayer(
        url="https://ows.terrestris.de/osm/service?",
        layers="SRTM30-Colored", name="MNT Relief",
        fmt="image/png", transparent=True, overlay=True, control=True,
    ).add_to(m)

    # Contour administratif dynamique (Région, Province ou Commune active)
    folium.GeoJson(
        couche_geometrique,
        name="Délimitation administrative",
        style_function=lambda x: {
            "color": "#1a5fe0",
            "weight": 3,
            "fillOpacity": 0,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["FIRST_com_"] if commune_choisie else (["libelle_fr"] if province_choisie else ["libelle_fr"]),
            aliases=["Commune :" if commune_choisie else ("Province :" if province_choisie else "Région :")],
        ),
    ).add_to(m)
    
    Fullscreen(position="topright").add_to(m)
    minimap_layer = folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="&copy; CartoDB", name="minimap", subdomains="abcd",
    )
    MiniMap(toggle_display=True, position="bottomleft", tile_layer=minimap_layer).add_to(m)
    MousePosition(position="bottomright", separator=" · ", prefix="", num_digits=4).add_to(m)
    MeasureControl(position="topleft").add_to(m)
    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    # Titre carte
    m.get_root().html.add_child(folium.Element(f"""
    <div style="position:fixed;top:10px;left:50%;transform:translateX(-50%);z-index:9999;
                font-family:'IBM Plex Sans',sans-serif;font-size:12px;font-weight:600;
                letter-spacing:0.5px;
                background:rgba(10,10,10,0.88);color:#e8e8e8;
                padding:6px 16px;border:1px solid #333;
                box-shadow:0 2px 8px rgba(0,0,0,0.4);">
      {zone_label.upper()}
    </div>"""))

    # Légende
    m.get_root().html.add_child(folium.Element("""
    <div style="position:fixed;bottom:28px;right:12px;
                background:rgba(10,10,10,0.88);border:1px solid #333;
                padding:10px 14px;z-index:9999;
                font-family:'IBM Plex Mono',monospace;
                font-size:11px;color:#888;
                box-shadow:0 2px 8px rgba(0,0,0,0.4);min-width:150px;">
      <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;
                  color:#555;border-bottom:1px solid #2a2a2a;
                  padding-bottom:6px;margin-bottom:8px;">Légende</div>
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="width:18px;height:1.5px;background:#e8e8e8;"></div>
        <span>Délimitation active</span>
      </div>
    </div>"""))

    # Flèche Nord
    m.get_root().html.add_child(folium.Element("""
    <div style="position:fixed;top:80px;left:10px;z-index:9999;
                font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:600;
                background:rgba(10,10,10,0.88);color:#888;
                border:1px solid #333;
                width:34px;height:38px;
                display:flex;flex-direction:column;
                align-items:center;justify-content:center;
                line-height:1.1;box-shadow:0 2px 8px rgba(0,0,0,0.4);">
      &#8593;<span style="font-size:9px;letter-spacing:1px;">N</span>
    </div>"""))

    st_folium(m, width="100%", height=580, key=f"map_{zone_label}")

# ── PANNEAU DROIT (GRAPHIC ET DESIGN INTACTS) ──
with col_right:
    meteo_df["Date_str"] = meteo_df["Date"].dt.strftime("%d/%m")

    LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#f8fafd",
        font=dict(family="IBM Plex Sans", color="#606878", size=11),
        margin=dict(l=8, r=8, t=40, b=8),
        xaxis=dict(
            gridcolor="#e8ebf0",
            tickfont=dict(family="IBM Plex Mono", size=9, color="#8892a0"),
            linecolor="#dde1e8",
            tickangle=45,
            showgrid=True,
        ),
        yaxis=dict(
            gridcolor="#e8ebf0",
            tickfont=dict(family="IBM Plex Mono", size=9, color="#8892a0"),
            linecolor="#dde1e8",
            showgrid=True,
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#dde1e8",
            borderwidth=1,
            font=dict(family="IBM Plex Mono", size=9, color="#606878"),
            orientation="h", y=1.12,
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="#dde1e8",
            font=dict(family="IBM Plex Sans", size=11, color="#1e2530"),
        ),
    )

    if choix == "Température":
        st.markdown(f'<div class="section-label">Températures — {zone_label} — Prévision 15 jours</div>', unsafe_allow_html=True)
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=meteo_df["Date_str"], y=meteo_df["Temp. max (°C)"],
            name="T° max", mode="lines+markers",
            line=dict(color="#e11d48", width=2.5),
            marker=dict(size=5, color="#e11d48", line=dict(color="#fff", width=1.5)),
            fill="tonexty",
            fillcolor="rgba(26,95,224,0.08)",
        ))
        fig.add_trace(go.Scatter(
            x=meteo_df["Date_str"], y=meteo_df["Temp. min (°C)"],
            name="T° min", mode="lines+markers",
            line=dict(color="#1a5fe0", width=2.5),
            marker=dict(size=5, color="#1a5fe0", line=dict(color="#fff", width=1.5)),
        ))

        avg = meteo_df["Temp. max (°C)"].mean()
        fig.add_hline(
            y=avg, line_dash="dot", line_color="#d97706", line_width=1.2,
            annotation_text=f"Moy. {avg:.1f}°C",
            annotation_font=dict(family="IBM Plex Mono", size=9, color="#d97706"),
            annotation_position="top right",
        )

        fig.update_layout(**LAYOUT, height=265)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.markdown(f'<div class="section-label">Précipitations — {zone_label} — Prévision 15 jours</div>', unsafe_allow_html=True)
        precip_vals = meteo_df["Précipitations (mm)"]
        bar_colors = [
            "#1a5fe0" if v > 10 else
            "#0d9488" if v > 5  else
            "#60a5fa" if v > 1  else
            "#dde1e8"
            for v in precip_vals
        ]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=meteo_df["Date_str"],
            y=precip_vals,
            marker=dict(
                color=bar_colors,
                line=dict(color="rgba(0,0,0,0)", width=0),
                cornerradius=3,
            ),
            name="Précipitations",
            hovertemplate="<b>%{x}</b><br>%{y:.1f} mm<extra></extra>",
        ))

        mean_p = precip_vals.mean()
        if mean_p > 0:
            fig.add_hline(
                y=mean_p, line_dash="dot", line_color="#d97706", line_width=1.2,
                annotation_text=f"Moy. {mean_p:.1f} mm",
                annotation_font=dict(family="IBM Plex Mono", size=9, color="#d97706"),
                annotation_position="top right",
            )

        fig.update_layout(**LAYOUT, height=265)
        st.plotly_chart(fig, use_container_width=True)

    # ── Tableau ──
    st.markdown('<div class="section-label" style="margin-top:1rem;">Prévisions détaillées — Horizon 15 jours</div>', unsafe_allow_html=True)

    display_df = meteo_df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%a %d/%m").str.upper()
    display_df = display_df[[
        "Date", "Temp. max (°C)", "Temp. min (°C)", "Précipitations (mm)"
    ]].rename(columns={
        "Temp. max (°C)":      "T. MAX",
        "Temp. min (°C)":      "T. MIN",
        "Précipitations (mm)": "PLUIE mm",
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=265,
        column_config={
            "T. MAX":    st.column_config.NumberColumn(format="%.1f °C"),
            "T. MIN":    st.column_config.NumberColumn(format="%.1f °C"),
            "PLUIE mm":  st.column_config.ProgressColumn(
                format="%.1f mm",
                min_value=0,
                max_value=float(display_df["PLUIE mm"].max() or 1),
            ),
        },
    )