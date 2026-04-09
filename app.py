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

col1.metric("🔷 HESS", len(hess))
col2.metric("🤖 IA", len(ia))
col3.metric("📊 Último Kp", round(df["x_t"].iloc[-1], 2))

fig = px.line(df, x="tempo", y="x_t", title="Monitoramento em Tempo Real")

fig.add_scatter(x=hess["tempo"], y=hess["x_t"], mode='markers', name='HESS')
fig.add_scatter(x=ia["tempo"], y=ia["x_t"], mode='markers', name='IA')

st.plotly_chart(fig, use_container_width=True) 

from ai_model import aplicar_ia

df = aplicar_ia(df)
ia = df[df["anomalia_ia"] == 1]

st.divider()

st.subheader("📊 Detecção de Anomalias")

fig2 = px.line(df, x="tempo", y="x_t")

fig2.add_scatter(
    x=hess["tempo"],
    y=hess["x_t"],
    mode="markers",
    name="HESS",
)

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

st.plotly_chart(fig2, use_container_width=True, config={
    "scrollZoom": False,
    "displayModeBar": False
})

st.write("Receba alertas automáticos e previsões inteligentes.")

if st.button("📩 Quero acesso premium"):
    st.success("Entraremos em contato com você!")
