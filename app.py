import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
from datetime import datetime
import plotly.graph_objects as go

# =========================
# ⚙️ CONFIG
# =========================
st.set_page_config(page_title="HESS Monitor", layout="wide")

# =========================
# 🧠 CACHE (SEM ERRO)
# =========================
@st.cache_data(ttl=300)
def get_kp_data():
    url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df["time_tag"] = pd.to_datetime(df["time_tag"])
    df["kp"] = pd.to_numeric(df["kp"], errors="coerce")

    return df.tail(100)


@st.cache_data(ttl=600)
def get_location():
    try:
        data = requests.get("https://ipapi.co/json").json()
        return data.get("city", "Desconhecido"), data.get("country_name", "Desconhecido")
    except:
        return "Desconhecido", "Desconhecido"


# =========================
# 🔐 BANCO
# =========================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# =========================
# 🔐 AUTH
# =========================
def login(user, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user=? AND password=?", (user, password))
    result = c.fetchone()
    conn.close()
    return result


def register(user, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (user, password) VALUES (?, ?)", (user, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# =========================
# 🎨 TEMA DINÂMICO
# =========================
hora = datetime.now().hour

if 6 <= hora < 18:
    bg = "#F5F7FA"
    text = "#000000"
    chart_theme = "plotly_white"
else:
    bg = "#0E1117"
    text = "#FFFFFF"
    chart_theme = "plotly_dark"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text};
}}
</style>
""", unsafe_allow_html=True)


# =========================
# 🔐 LOGIN UI
# =========================
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:

    st.title("🔐 Login HESS")

    aba1, aba2 = st.tabs(["Login", "Cadastro"])

    with aba1:
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if login(user, password):
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Credenciais inválidas")

    with aba2:
        new_user = st.text_input("Novo usuário")
        new_pass = st.text_input("Nova senha", type="password")

        if st.button("Cadastrar"):
            if register(new_user, new_pass):
                st.success("Usuário criado!")
            else:
                st.error("Usuário já existe")

    st.stop()


# =========================
# 🌍 LOCALIZAÇÃO
# =========================
cidade, pais = get_location()

# =========================
# 📊 DADOS
# =========================
df = get_kp_data()

# =========================
# 📊 DASHBOARD
# =========================
st.title("🚀 HESS Monitor")
st.caption(f"📍 {cidade}, {pais}")

# =========================
# 📈 MÉTRICAS
# =========================
col1, col2, col3 = st.columns(3)

kp_atual = df["kp"].iloc[-1]
kp_max = df["kp"].max()
kp_min = df["kp"].min()

col1.metric("📊 KP Atual", round(kp_atual, 2))
col2.metric("📈 Máximo", round(kp_max, 2))
col3.metric("📉 Mínimo", round(kp_min, 2))

# =========================
# 🚨 ALERTA
# =========================
if kp_atual >= 5:
    st.error("🌋 Tempestade Solar Forte")
elif kp_atual >= 3:
    st.warning("⚠️ Atividade Elevada")
else:
    st.success("✅ Normal")

# =========================
# 📊 GRÁFICO PRINCIPAL
# =========================
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["time_tag"],
    y=df["kp"],
    mode='lines+markers',
    name="KP Index",
    line=dict(width=2)
))

# linhas referência
fig.add_hline(y=3, line_dash="dash", line_color="yellow")
fig.add_hline(y=5, line_dash="dash", line_color="red")

fig.update_layout(
    template=chart_theme,
    title="Atividade Geomagnética",
    xaxis_title="Tempo",
    yaxis_title="KP Index",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 🤖 PREVISÃO SIMPLES IA
# =========================
st.subheader("🧠 Previsão IA")

# previsão simples (média móvel)
df["prev"] = df["kp"].rolling(5).mean()

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df["time_tag"],
    y=df["kp"],
    name="Real"
))

fig2.add_trace(go.Scatter(
    x=df["time_tag"],
    y=df["prev"],
    name="Previsão IA",
    line=dict(dash="dot")
))

fig2.update_layout(
    template=chart_theme,
    title="Previsão de Tendência",
    height=400
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# 📘 EXPLICAÇÃO
# =========================
st.markdown("""
### 📘 O que é HESS?

HESS é um sistema de monitoramento geomagnético baseado em dados reais (NOAA).

Ele analisa:
- 🌍 Campo magnético da Terra  
- ☀️ Atividade solar  
- 📡 Possíveis impactos em tecnologia  

### 🚨 Interpretação:
- 0 a 2 → Normal  
- 3 a 4 → Atenção  
- 5+ → Tempestade solar  

""")


# =========================
# 🚀 PREMIUM
# =========================
st.divider()
st.subheader("💰 Recursos Avançados")

if st.button("Quero acesso premium"):
    st.success("Em breve entraremos em contato 🚀")
