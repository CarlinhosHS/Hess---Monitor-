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
data.py


requirements.txt
streamlit
pandas
numpy
plotly
matplotlib
requests
scikit-learn

lstm_model.py
import streamlit as st
import matplotlib.pyplot as plt

from data import get_data
from hess import aplicar_hess
from ai_model import aplicar_ia

st.title("🚀 H.E.S.S. Monitor com IA")

# carregar dados
df = get_data()

# aplicar modelos
df = aplicar_hess(df)
df = aplicar_ia(df)

# gráfico
fig, ax = plt.subplots(figsize=(10,5))

ax.plot(df["tempo"], df["x_t"], label="Sinal")

# anomalias HESS
hess = df[df["anomalia_hess"] == 1]
ax.scatter(hess["tempo"], hess["x_t"], label="HESS", marker="o")

# anomalias IA
ia = df[df["anomalia_ia"] == 1]
ax.scatter(ia["tempo"], ia["x_t"], label="IA", marker="x")

ax.legend()
ax.set_title("Detecção de Anomalias")

st.pyplot(fig)

st.write("Anomalias HESS:", len(hess))
st.write("Anomalias IA:", len(ia))
