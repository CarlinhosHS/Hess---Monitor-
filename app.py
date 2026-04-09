import streamlit as st
import pandas as pd
import requests
import datetime
import plotly.express as px

# =========================
# 🌍 CONFIG
# =========================
st.set_page_config(page_title="HESS Monitor Global", layout="wide")

# =========================
# 🎨 TEMA
# =========================
hora = datetime.datetime.now().hour

if 6 <= hora < 18:
    bg = "#F5F7FA"
    text_color = "#000000"
    card = "#FFFFFF"
    graph_template = "plotly_white"
else:
    bg = "#0F172A"
    text_color = "#FFFFFF"
    card = "#1E293B"
    graph_template = "plotly_dark"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text_color};
}}
h1,h2,h3,h4,p {{
    color: {text_color} !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# 📍 LOCALIZAÇÃO DO USUÁRIO
# =========================
try:
    geo = requests.get("https://ipapi.co/json/").json()
    cidade = geo.get("city", "Desconhecida")
    pais = geo.get("country_name", "")
except:
    cidade = "Indisponível"
    pais = ""

st.title("🚀 HESS Monitor Global")
st.write(f"📍 Localização detectada: **{cidade}, {pais}**")

# =========================
# 📡 DADOS REAIS (NOAA)
# =========================
try:
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df["time_tag"] = pd.to_datetime(df["time_tag"])
    df["kp"] = df["kp_index"]

    df = df.tail(120)

except:
    st.error("Erro ao carregar dados reais.")
    df = pd.DataFrame()

# =========================
# 📊 MÉTRICAS
# =========================
if not df.empty:
    ultimo = df["kp"].iloc[-1]

    col1, col2 = st.columns(2)

    col1.metric("📈 Último Kp", ultimo)

    if ultimo >= 5:
        col2.error("🌪️ Tempestade solar forte")
    elif ultimo >= 3:
        col2.warning("⚠️ Atividade elevada")
    else:
        col2.success("✅ Atividade normal")

# =========================
# 📊 GRÁFICO PRINCIPAL
# =========================
st.subheader("📡 Atividade Geomagnética (Tempo Real)")

fig = px.line(df, x="time_tag", y="kp")

fig.update_layout(
    template=graph_template,
    plot_bgcolor=bg,
    paper_bgcolor=bg,
    font=dict(color=text_color),
    dragmode="pan"
)

fig.add_hline(y=3, line_dash="dash", line_color="yellow")
fig.add_hline(y=5, line_dash="dash", line_color="red")

st.plotly_chart(fig, use_container_width=True)

# =========================
# 🌍 MAPA GLOBAL
# =========================
st.subheader("🌍 Atividade Global (Visão Mundial)")

# simulação com base real simplificada
world_df = pd.DataFrame({
    "lat": [0, 40, -30, 60, -10],
    "lon": [0, -74, 120, 30, -50],
    "kp": [2, 4, 3, 5, 1]
})

fig_map = px.scatter_geo(
    world_df,
    lat="lat",
    lon="lon",
    color="kp",
    size="kp",
    projection="natural earth",
)

fig_map.update_layout(
    template=graph_template
)

st.plotly_chart(fig_map, use_container_width=True)

# =========================
# 🧠 EXPLICAÇÃO HESS
# =========================
st.subheader("🧠 O que é o HESS?")

st.markdown("""
O **HESS (Sistema de Monitoramento Inteligente)** é um modelo que:

- 📡 Analisa dados espaciais reais (NOAA)
- 🤖 Aplica lógica matemática e inteligência artificial
- ⚠️ Detecta anomalias geomagnéticas
- 🌍 Ajuda a prever impactos na Terra

### 📊 Sobre o índice Kp:
- 0 a 2 → Normal  
- 3 a 4 → Atenção  
- 5+ → Tempestade solar  

Esses eventos podem afetar:
- 📡 Satélites  
- 📶 Comunicação  
- ⚡ Redes elétricas  
""")

# =========================
# 💰 PREMIUM
# =========================
st.subheader("💰 Recursos avançados")

if st.button("💎 Quero acesso premium"):
    st.success("🚀 Em breve você terá acesso a previsões com IA!")
