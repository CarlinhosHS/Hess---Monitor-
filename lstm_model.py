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
