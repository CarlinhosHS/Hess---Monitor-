import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="HESS Monitor", layout="wide")

st.title("🚀 Monitor HESS")
st.subheader("Monitoramento em Tempo Real")

# dados simulados
tempo = np.arange(0,900)
dados = np.sin(tempo * 0.1)

df = pd.DataFrame({
    "tempo": tempo,
    "x_t": dados
})

fig = px.line(df, x="tempo", y="x_t", title="Monitoramento em Tempo Real")

st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)

hess = df[df["x_t"] > 0.8]
ia = df[df["x_t"] < -0.8]
col1.metric("Anomalias HESS", len(hess))
col2.metric("Anomalias IA", len(ia))
col3.metric("Último valor", round(df["x_t"].iloc[-1],2))

import plotly.express as px

fig = px.line(df, x="tempo", y="x_t", title="Monitoramento em Tempo Real")

fig.add_scatter(x=hess["tempo"], y=hess["x_t"], mode='markers', name='HESS')
fig.add_scatter(x=ia["tempo"], y=ia["x_t"], mode='markers', name='IA')

st.plotly_chart(fig, use_container_width=True) 
