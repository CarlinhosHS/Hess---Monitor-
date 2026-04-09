import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="HESS Monitor", layout="wide")

st.title("🚀 HESS Monitor")

# dados simulados
tempo = np.arange(0, 100)
dados = np.sin(tempo * 0.1)

df = pd.DataFrame({
    "tempo": tempo,
    "x_t": dados
})

fig = px.line(df, x="tempo", y="x_t", title="Monitoramento em Tempo Real")

st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)

col1.metric("Anomalias HESS", len(hess))
col2.metric("Anomalias IA", len(ia))
col3.metric("Último valor", round(df["x_t"].iloc[-1],2))

import plotly.express as px

fig = px.line(df, x="tempo", y="x_t", title="Monitoramento em Tempo Real")

fig.add_scatter(x=hess["tempo"], y=hess["x_t"], mode='markers', name='HESS')
fig.add_scatter(x=ia["tempo"], y=ia["x_t"], mode='markers', name='IA')

st.plotly_chart(fig, use_container_width=True)

from lstm_model import preparar_dados, treinar_lstm, prever

X, y, scaler = preparar_dados(df)

model = treinar_lstm(X, y)

pred = prever(model, X, scaler)

df = df.iloc[-len(pred):]
df["previsao"] = pred

ax.plot(df["tempo"], df["previsao"], label="Previsão IA", linestyle="--")
