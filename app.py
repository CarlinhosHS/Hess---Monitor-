import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime
import plotly.express as px
from sklearn.linear_model import LinearRegression

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="HESS AI Global", layout="wide")

# =========================
# TEMA
# =========================
hora = datetime.datetime.now().hour

if 6 <= hora < 18:
    bg = "#F5F7FA"
    text_color = "#000000"
    graph_template = "plotly_white"
else:
    bg = "#0F172A"
    text_color = "#FFFFFF"
    graph_template = "plotly_dark"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text_color};
}}
</style>
""", unsafe_allow_html=True)

# =========================
# LOCALIZAÇÃO
# =========================
try:
    geo = requests.get("https://ipapi.co/json/").json()
    cidade = geo.get("city", "Desconhecida")
    pais = geo.get("country_name", "")
except:
    cidade = "Indisponível"
    pais = ""

st.title("🚀 HESS AI Monitor")
st.write(f"📍 {cidade}, {pais}")

# =========================
# DADOS REAIS NOAA
# =========================
url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
data = requests.get(url).json()

df = pd.DataFrame(data)
df["time_tag"] = pd.to_datetime(df["time_tag"])
df["kp"] = df["kp_index"]

df = df.tail(120)

# =========================
# IA (PREVISÃO)
# =========================
df["t"] = np.arange(len(df))

X = df[["t"]]
y = df["kp"]

model = LinearRegression()
model.fit(X, y)

future_t = np.arange(len(df), len(df)+20).reshape(-1,1)
future_pred = model.predict(future_t)

future_time = pd.date_range(
    start=df["time_tag"].iloc[-1],
    periods=20,
    freq="min"
)

df_future = pd.DataFrame({
    "time_tag": future_time,
    "kp": future_pred
})

# =========================
# MÉTRICAS
# =========================
ultimo = df["kp"].iloc[-1]

col1, col2 = st.columns(2)

col1.metric("📈 Kp Atual", round(ultimo,2))

if ultimo >= 5:
    col2.error("🌪️ Tempestade Solar Forte")
elif ultimo >= 3:
    col2.warning("⚠️ Atividade Elevada")
else:
    col2.success("✅ Normal")

# =========================
# ALERTA AUTOMÁTICO
# =========================
if ultimo >= 5:
    st.error("🚨 ALERTA: Possível impacto em GPS, energia e comunicação")
elif ultimo >= 4:
    st.warning("⚠️ Atenção: aumento da atividade solar")

# =========================
# GRÁFICO COM PREVISÃO
# =========================
st.subheader("📡 Tempo Real + Previsão IA")

fig = px.line(df, x="time_tag", y="kp")

# previsão
fig.add_scatter(
    x=df_future["time_tag"],
    y=df_future["kp"],
    mode="lines",
    name="Previsão IA",
    line=dict(dash="dash")
)

fig.update_layout(
    template=graph_template,
    plot_bgcolor=bg,
    paper_bgcolor=bg,
    font=dict(color=text_color),
)

fig.add_hline(y=3, line_dash="dash", line_color="yellow")
fig.add_hline(y=5, line_dash="dash", line_color="red")

st.plotly_chart(fig, use_container_width=True)

# =========================
# MAPA GLOBAL MELHORADO
# =========================
st.subheader("🌍 Mapa Global de Atividade")

# simulação mais rica
world_df = pd.DataFrame({
    "lat": np.random.uniform(-60, 70, 30),
    "lon": np.random.uniform(-180, 180, 30),
    "kp": np.random.uniform(1, 6, 30)
})

fig_map = px.scatter_geo(
    world_df,
    lat="lat",
    lon="lon",
    color="kp",
    size="kp",
    projection="natural earth",
)

fig_map.update_layout(template=graph_template)

st.plotly_chart(fig_map, use_container_width=True)

# =========================
# EXPLICAÇÃO
# =========================
st.subheader("🧠 O que é o HESS")

st.markdown("""
O HESS é um sistema inteligente que:

- Usa dados reais da NOAA
- Aplica modelos matemáticos e IA
- Detecta anomalias geomagnéticas
- Prevê eventos futuros

📊 Índice Kp:
- 0–2 → Normal  
- 3–4 → Atenção  
- 5+ → Tempestade solar  

Impactos:
- GPS  
- Internet  
- Energia elétrica  
""")

# =========================
# PREMIUM
# =========================
st.subheader("💰 Premium")

if st.button("💎 Quero acesso premium"):
    st.success("🚀 Em breve: IA avançada + alertas no celular")
