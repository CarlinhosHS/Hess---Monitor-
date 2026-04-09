app.py
import plotly.express as px
hess = df[df["anomalia_hess"] == 1]
ia = df[df["anomalia_ia"] == 1]

fig = px.line(df, x="tempo", y="x_t", title="Monitoramento em Tempo Real")

fig.add_scatter(x=hess["tempo"], y=hess["x_t"], mode='markers', name='HESS')
fig.add_scatter(x=ia["tempo"], y=ia["x_t"], mode='markers', name='IA')

st.plotly_chart(fig, use_container_width=True)
st.set_page_config(
    page_title="HESS Monitor",
    layout="wide"
)
col1, col2, col3 = st.columns(3)

col1.metric("Anomalias HESS", len(hess))
col2.metric("Anomalias IA", len(ia))
col3.metric("Último valor", round(df["x_t"].iloc[-1],2))
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

st.write("Anomalias HESS:", len(hess))
st.write("Anomalias IA:", len(ia))
from lstm_model import preparar_dados, treinar_lstm, prever

X, y, scaler = preparar_dados(df)

model = treinar_lstm(X, y)

pred = prever(model, X, scaler)

df = df.iloc[-len(pred):]
df["previsao"] = pred
ax.plot(df["tempo"], df["previsao"], label="Previsão IA", linestyle="--")
data.py
import requests
import pandas as pd

def get_data():
    url = "https://services.swpc.noaa.gov/experimental/json/geoelectric/geoelectric_scatterplots.json"
    response = requests.get(url)
    data = response.json()

    valores = []

    for item in data:
        if "value" in item:
            valores.append(item["value"])

    df = pd.DataFrame({
        "tempo": range(len(valores)),
        "x_t": valores
    })
    return df
hess.py
import numpy as np

def aplicar_hess(df):
    df["H"] = df["x_t"]

    df["H1"] = df["H"].shift(1)
    df["H2"] = df["H"].shift(2)

    df["media"] = (df["H1"] + df["H2"]) / 2
    df["delta_H"] = abs(df["H"] - df["media"])

    window = 20

    mediana = df["H"].rolling(window).median()
    mad = df["H"].rolling(window).apply(lambda x: np.median(abs(x - np.median(x))))

    k = 1.5
    df["tau"] = mediana + k * mad

    df["anomalia_hess"] = (df["delta_H"] > df["tau"]).astype(int)

    return df
ai_model.py
from sklearn.ensemble import IsolationForest

def aplicar_ia(df):
    model = IsolationForest(contamination=0.05)

    df["anomalia_ia"] = model.fit_predict(df[["x_t"]])
    df["anomalia_ia"] = df["anomalia_ia"].apply(lambda x: 1 if x == -1 else 0)

    return df
requirements.txt
streamlit
pandas
numpy
matplotlib
requests
scikit-learn
plotly
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
