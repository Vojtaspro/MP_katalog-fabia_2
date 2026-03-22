import streamlit as st
import pandas as pd
import base64

# 1. FUNKCE PRO NAČTENÍ OBRÁZKU POZADÍ
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# Nastavení stránky
st.set_page_config(
    page_title="Fabia Katalog 2.0 - Detail vozu",
    page_icon="🚗",
    layout="wide"
)

# 2. KOMPLETNÍ CSS STYLING
img_base64 = get_base64_of_bin_file('2.png')

style = f'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700;900&display=swap');

.stApp {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-attachment: fixed;
    font-family: 'Quicksand', sans-serif !important;
}}

.header-container {{
    width: 100%;
    text-align: center;
    margin-top: -20px;
    margin-bottom: 20px;
}}
.main-title {{
    color: #ffffff !important;
    font-size: 60px !important;
    font-weight: 900;
    text-transform: uppercase;
    text-shadow: 0 0 25px rgba(0,0,0,0.9);
}}

.custom-card {{
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    color: #1e1e1e;
}}

.motor-card {{ min-height: 366px; }}

.card-title {{
    font-weight: 900;
    font-size: 22px;
    color: #000;
    margin-bottom: 10px;
    border-bottom: 2px solid #ddd;
    padding-bottom: 5px;
}}

/* SIDEBAR STYLING */
[data-testid="stSidebar"] {{
    background-color: rgba(0, 0, 0, 0.7) !important;
    backdrop-filter: blur(15px);
}}
[data-testid="stSidebar"] h2 {{ color: white !important; font-weight: 900 !important; }}
[data-testid="stSidebar"] label p {{ color: white !important; font-weight: 700 !important; }}

[data-testid="stSidebar"] summary p {{
    color: #ffffff !important;
    font-weight: 700 !important;
}}
[data-testid="stSidebar"] .st-expanderIcon {{ fill: #ffffff !important; }}

.legal-text {{ 
    font-size: 11px !important; 
    color: #ffffff !important; 
    text-align: justify;
    line-height: 1.4;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}}
.legal-text b, .legal-text strong {{ color: #ffffff !important; font-weight: 800; }}

.motor-grid {{ display: flex; justify-content: space-between; gap: 20px; }}
.motor-col {{ flex: 1; }}

.top-card {{
    background: rgba(0, 0, 0, 0.75);
    text-align: center;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 30px;
}}
.top-card h1, .top-card p, .top-card b {{
    color: #ffffff !important;
    text-shadow: 2px 2px 10px rgba(0,0,0,1) !important;
}}

.price-container {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
}}
.price-item {{
    flex: 0 1 auto;
    background: rgba(0,0,0,0.05);
    padding: 10px 20px;
    border-radius: 12px;
    border: 1px solid rgba(0,0,0,0.1);
    min-width: 140px;
    text-align: center;
}}
</style>
'''
st.markdown(style, unsafe_allow_html=True)

# 3. NAČTENÍ DAT
try:
    df_origin = pd.read_excel("Py_F_data_2.xlsx")
    df = df_origin.copy()

    # 4. SIDEBAR
    with st.sidebar:
        st.markdown("## 🔍 Filtr vozů")
        vybrana_generace = st.selectbox("1. Vyberte generaci", ["Vše"] + sorted(df['generace'].unique().tolist()))
        if vybrana_generace != "Vše":
            df = df[df['generace'] == vybrana_generace]
            
        poradi_karoserie = {"Hatchback": 1, "Combi": 2, "Sedan": 3}
        seznam_karoserii = sorted(df['karoserie'].unique().tolist(), key=lambda x: poradi_karoserie.get(x, 99))
        vybrana_karoserie = st.selectbox("2. Vyberte karoserii", ["Vše"] + seznam_karoserii)
        if vybrana_karoserie != "Vše":
            df = df[df['karoserie'] == vybrana_karoserie]
            
        vybrana_motorizace = st.selectbox("3. Vyberte motorizaci", ["Vše"] + sorted(df['Motor'].unique().tolist()))
        if vybrana_motorizace != "Vše":
            df = df[df['Motor'] == vybrana_motorizace]

        for _ in range(25):
            st.write("")

        with st.expander("⚖️ Právní doložka a prohlášení"):
            st.markdown(f'''
            <div class="legal-text">
            <strong>Právní doložka a prohlášení:</strong> Tento web je neoficiální projekt vytvořený výhradně pro účely maturitní práce a edukaci v oblasti analýzy dat. Projekt je vytvořen v souladu s § 35 odst. 3 zákona č. 121/2000 Sb. (Autorský zákon) o užití školního díla pro potřeby školy a pro účely výuky.<br><br>
            <b>Zdroje dat:</b> Veškeré technické parametry a dobové ceny byly čerpány z veřejně dostupných archivů a oficiálních materiálů Škoda Auto.<br><br>
            <b>Aktualita:</b> Data mají informativní charakter a mohou se lišit od reálných historických nabídek. Autor neručí za případné chyby v datech.<br><br>
            <b>Autorská práva:</b> Užití ochranných známek slouží výhradně k identifikaci produktů a nepředstavuje spojení s držitelem práv. Ochranná známka Škoda a názvy modelů jsou majetkem společnosti Škoda Auto a.s.<br><br>
            <b>Neziskovost:</b> Projekt není využíván ke komerčním účelům ani k žádné formě výdělku.<br><br>
            <strong>Autor:</strong> Vojtěch Hendrych<br>
            <strong>Škola:</strong> SPŠ strojnická, Betlémská 287/4, Praha 1<br>
            <strong>Školní rok:</strong> 2025/2026
            </div>
            ''', unsafe_allow_html=True)

    # 5. HLAVNÍ PLOCHA
    st.markdown('<div class="header-container"><span class="main-title">KATALOG FABIA</span></div>', unsafe_allow_html=True)

    if len(df) > 0:
        car = df.iloc[0]
        # DOPLNĚNÍ ROKU DO TOP KARTY
        st.markdown(f'''
            <div class="custom-card top-card">
                <h1>{car['Motor']}</h1>
                <p>Generace: <b>{car['generace']}</b> | Rok: <b>{car.get('Rok', '-')}</b> | Karoserie: <b>{car['karoserie']}</b></p>
            </div>
        ''', unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.markdown(f'''
                <div class="custom-card motor-card">
                    <div class="card-title">⚙️ Motor</div>
                    <div class="motor-grid">
                        <div class="motor-col">
                            <p>Objem: <b>{car.get('Objem [l]', '-')} l</b></p>
                            <p>Výkon: <b>{car.get('Výkon [kW]', '-')} kW</b></p>
                            <p>Točivý moment: <b>{car.get('Točivý moment [Nm]', '-')} Nm</b></p>
                            <p>Zdvihový objem: <b>{car.get('Zdvihový objem v [cm³]', '-')} cm³</b></p>
                            <p>Počet válců: <b>{car.get('Počet válců', '-')}</b></p>
                        </div>
                        <div class="motor-col">
                            <p>Typ: <b>{car.get('Typ', '-')}</b></p> 
                            <p>Pohon: <b>{car.get('Pohon', '-')}</b></p>
                            <p>Převodovka: <b>{car.get('Převodovka', '-')}</b></p>
                            <p>Spojka: <b>{car.get('Spojka', '-')}</b></p>
                        </div>
                    </div>
                </div>
                <div class="custom-card">
                    <div class="card-title">🚀 Rychlosti</div>
                    <p>Nejvyšší rychlost: <b>{car.get('Nejvyšší rychlost [km/h]', '-')} km/h</b></p>
                    <p>Zrychlení 0-100 km/h: <b>{car.get('Zrychlení 0 - 100 km/h', '-')} s</b></p>
                </div>
            ''', unsafe_allow_html=True)

        with col_right:
            st.markdown(f'''
                <div class="custom-card">
                    <div class="card-title">⛽ Palivo</div>
                    <p>Typ paliva: <b>{car.get('Typ paliva', '-')}</b></p>
                    <p>Kombinovaná spotřeba paliva: <b>{car.get('Kombinovaná spotřeba paliva [l/100 km]', '-')} l/100 km</b></p>
                    <p>Emisní hodnoty CO2: <b>{car.get('Emisní hodnoty CO2 [g/km]', '-')} g/km</b></p>
                    <p>Exhalační norma: <b>{car.get('Exhalační norma', '-')}</b></p>
                </div>
                <div class="custom-card">
                    <div class="card-title">⚖️ Hmotnosti</div>
                    <p>Celková hmotnost: <b>{car.get('Celková hmotnost [kg]', '-')} kg</b></p>
                    <p>Pohotovostní hmotnost: <b>{car.get('Pohotovostní hmotnost [kg]', '-')} kg</b></p>
                </div>
                <div class="custom-card">
                    <div class="card-title">📦 Objemy</div>
                    <p>Objem zavazadlového prostoru: <b>{car.get('Objem zavazadlového prostoru [l]', '-')} l</b></p>
                    <p>Objem palivové nádrže: <b>{car.get('Objem palivové nádrže [l]', '-')} l</b></p>
                </div>
            ''', unsafe_allow_html=True)

        # KOMPLETNÍ SEZNAM VÝBAV Z EXCELU
        vybavy_cols = [
            'Easy', 'Classic', 'Comfort', 'Elegance', 'RS', 'Ambient', 'Scout', 
            'Sport', 'Monte Carlo', 'Active', 'Ambition', 'Style', 'Selection', 
            'Top Selection', '130 Let', '130 Premium', 'Dynamic', 'R5'
        ]
        
        nalezené_ceny = []
        for col in vybavy_cols:
            if col in car and pd.notnull(car[col]):
                val = car[col]
                # Formátování čísla (mezera jako oddělovač tisíců)
                formatted_val = f"{int(val):,}".replace(",", " ") if isinstance(val, (int, float)) else str(val)
                nalezené_ceny.append(f'<div class="price-item">{col}:<br><b>{formatted_val} Kč</b></div>')

        ceny_html = f'<div class="price-container">{" ".join(nalezené_ceny)}</div>' if nalezené_ceny else "Ceny nejsou k dispozici."

        st.markdown(f'''
            <div class="custom-card">
                <div class="card-title">💰 Dobové ceny a výbavy</div>
                {ceny_html}
            </div>
        ''', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Chyba při zpracování dat: {e}")
