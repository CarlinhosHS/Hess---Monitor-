from data import get_data
from ai_model import aplicar_ia
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import streamlit as st

st.set_page_config(
    page_title="HESS Monitor",
    layout="wide",
    page_icon="🚀"
)

st.markdown("""
# 🚀 HESS Monitor
### Monitoramento Inteligente em Tempo Real
""")
st.divider()
st.info("""
🧠 Este sistema monitora a atividade geomagnética da Terra em tempo real.

📡 Fonte: NOAA (dados espaciais reais)

🔷 HESS → detecção por regra matemática  
🤖 IA → detecção por aprendizado de máquina  

Valores altos indicam possíveis tempestades solares.
""")

intervalo = st.selectbox(
    "⏱️ Intervalo de atualização",
    ["Tempo real (1 min)", "A cada 5 minutos", "A cada 1 hora"]
)

import time

if intervalo == "Tempo real (1 min)":
    time.sleep(60)
    st.rerun()

elif intervalo == "A cada 5 minutos":
    time.sleep(300)
    st.rerun()

elif intervalo == "A cada 1 hora":
    time.sleep(3600)
    st.rerun()
    
df = get_data()

fig = px.line(df, x="tempo", y="x_t")

fig.update_layout(
    template="plotly_dark",
    title="📡 Atividade Geomagnética em Tempo Real",
    xaxis_title="Tempo",
    yaxis_title="Intensidade (Kp Index)",
    dragmode=False  # 🔥 remove zoom ao arrastar
)

st.plotly_chart(fig, use_container_width=True, config={
    "scrollZoom": False,   # 🔥 remove zoom com dedo
    "displayModeBar": False  # 🔥 remove botões chatos
})


# criar anomalias primeiro
hess = df[df["x_t"] > 0.8]
ia = df[df["x_t"] < -0.8]

# depois mostrar métricas
col1, col2, col3 = st.columns(3)

col1.metric("🔷 Eventos HESS", len(hess))
col2.metric("🤖 Eventos IA", len(ia))

ultimo = round(df["x_t"].iloc[-1], 2)
col3.metric("📊 Último índice Kp", ultimo)

if ultimo >= 5:
    st.error("🔴 Tempestade solar detectada!")
elif ultimo >= 3:
    st.warning("🟡 Atividade elevada")
else:
    st.success("🟢 Atividade normal")
fig = px.line(df, x="tempo", y="x_t", title="Monitoramento em Tempo Real")

fig.add_scatter(x=hess["tempo"], y=hess["x_t"], mode='markers', name='HESS')
fig.add_scatter(x=ia["tempo"], y=ia["x_t"], mode='markers', name='IA')

st.plotly_chart(fig, use_container_width=True) 

from ai_model import aplicar_ia

df = get_data()

df = aplicar_ia(df)

# anomalias
hess = df[df["x_t"] > 0.8]
ia = df[df["anomalia_ia"] == 1]

# =========================
# 📊 GRÁFICO PRINCIPAL
# =========================

st.subheader("📡 Atividade Geomagnética em Tempo Real")

fig.update_layout(
    template="plotly_dark",
    title="Atividade Geomagnética",
    xaxis_title="Tempo",
    yaxis_title="Kp Index",
    dragmode=False
)

# linhas de referência
fig.add_hline(y=3, line_dash="dash", line_color="yellow")
fig.add_hline(y=5, line_dash="dash", line_color="red")

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "scrollZoom": False,
        "displayModeBar": False
    }
)

# =========================
# 🔍 GRÁFICO DE ANOMALIAS
# =========================

st.subheader("🔍 Detecção de Anomalias")

# pontos HESS
fig2.add_scatter(
    x=hess["tempo"],
    y=hess["x_t"],
    mode="markers",
    name="HESS",
)

# pontos IA
fig2.add_scatter(
    x=ia["tempo"],
    y=ia["x_t"],
    mode="markers",
    name="IA",
)

fig2.update_layout(
    template="plotly_dark",
    dragmode=False
)

st.plotly_chart(
    fig2,
    use_container_width=True,
    config={
        "scrollZoom": False,
        "displayModeBar": False
    }
)
if st.button("📩 Quero acesso premium"):
    st.success("Entraremos em contato com você!")
