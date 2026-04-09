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
### 📊 Monitoramento Inteligente em Tempo Real
""")
st.title("🚀 Monitor HESS")
st.subheader("Monitoramento em Tempo Real")

# dados simulados
tempo = np.arange(0,500)
dados = np.sin(tempo * 0.5)

df = pd.DataFrame({
    "tempo": tempo,
    "x_t": dados
})

fig = px.line(df, x="tempo", y="x_t")
fig.update_layout(
    template="plotly_dark",
    title="📡 Monitoramento Inteligente",
    xaxis_title="Tempo",
    yaxis_title="Sinal",
)

df = get_data()

# criar anomalias primeiro
hess = df[df["x_t"] > 0.8]
ia = df[df["x_t"] < -0.8]

# depois mostrar métricas
col1, col2, col3 = st.columns(3)

col1.metric("🔷 Anomalias HESS", len(hess))
col2.metric("🤖 Anomalias IA", len(ia))
col3.metric("📈 Último valor", round(df["x_t"].iloc[-1], 2))
import plotly.express as px

fig = px.line(df, x="tempo", y="x_t", title="Monitoramento em Tempo Real")

fig.add_scatter(x=hess["tempo"], y=hess["x_t"], mode='markers', name='HESS')
fig.add_scatter(x=ia["tempo"], y=ia["x_t"], mode='markers', name='IA')

st.plotly_chart(fig, use_container_width=True) 

from ai_model import aplicar_ia

df = aplicar_ia(df)
ia = df[df["anomalia_ia"] == 1]
