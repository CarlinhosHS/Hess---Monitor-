import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# =========================
# 🎨 CONFIG DA PÁGINA
# =========================
st.set_page_config(page_title="HESS Monitor", layout="wide")

# =========================
# 🎨 TEMA PROFISSIONAL
# =========================
hora = datetime.datetime.now().hour

if 6 <= hora < 18:
    # 🌤️ MODO CLARO (PROFISSIONAL)
    bg = "#F5F7FA"
    text_color = "#1F2937"
    card = "#FFFFFF"
    accent = "#2563EB"
else:
    # 🌙 MODO ESCURO (PADRÃO TOP)
    bg = "#0F172A"
    text_color = "#E2E8F0"
    card = "#1E293B"
    accent = "#38BDF8"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text_color};
}}

div[data-testid="stMetric"] {{
    background-color: {card};
    padding: 15px;
    border-radius: 12px;
}}

section[data-testid="stSidebar"] {{
    background-color: {card};
}}

</style>
""", unsafe_allow_html=True)

# =========================
# 🎯 TÍTULO
# =========================
st.markdown(f"""
# 🚀 HESS Monitor
### {tema} — Monitoramento Inteligente em Tempo Real
""")

st.divider()

# =========================
# 📡 DADOS SIMULADOS (BASE REALISTA)
# =========================
tempo = pd.date_range(end=pd.Timestamp.now(), periods=200, freq="min")
valores = np.sin(np.linspace(0, 10, 200)) + np.random.normal(0, 0.2, 200)

df = pd.DataFrame({
    "tempo": tempo,
    "kp": valores
})

# =========================
# 🎛️ CONTROLE DO USUÁRIO
# =========================
st.sidebar.header("⚙️ Configurações")

janela = st.sidebar.slider("Quantidade de pontos", 50, 200, 150)
df = df.tail(janela)

mostrar_anomalia = st.sidebar.checkbox("Mostrar anomalias", True)

# =========================
# 🔍 DETECÇÃO SIMPLES
# =========================
hess = df[df["kp"] > 0.8]
ia = df[df["kp"] < -0.8]

# =========================
# 📊 MÉTRICAS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("🔷 HESS", len(hess))
col2.metric("🤖 IA", len(ia))
col3.metric("📈 Último Kp", round(df["kp"].iloc[-1], 2))

# =========================
# 📊 GRÁFICO PRINCIPAL (INTERATIVO)
# =========================
st.subheader("📡 Atividade Geomagnética")

fig = px.line(df, x="tempo", y="kp")

fig.update_layout(
    template="plotly_dark" if hora >= 18 else "plotly_white",
    plot_bgcolor=bg,
    paper_bgcolor=bg,
    font=dict(color=text_color),
)

# linhas de referência
fig.add_hline(y=0.8, line_color="orange")
fig.add_hline(y=-0.8, line_color="red")

# anomalias
if mostrar_anomalia:
    fig.add_scatter(
        x=hess["tempo"],
        y=hess["kp"],
        mode="markers",
        name="HESS",
        marker=dict(size=8)
    )

    fig.add_scatter(
        x=ia["tempo"],
        y=ia["kp"],
        mode="markers",
        name="IA",
        marker=dict(size=8)
    )

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "scrollZoom": True,  # agora pode navegar melhor
        "displayModeBar": True
    }
)

# =========================
# 📚 EXPLICAÇÃO
# =========================
st.info("""
📊 Como ler:

- Linha = comportamento da atividade geomagnética
- Pontos = eventos fora do padrão
- Quanto mais alto → mais atividade solar

🔴 acima de 0.8 → alerta  
🔵 abaixo de -0.8 → comportamento incomum  
""")

# =========================
# 💰 FUTURO (PREMIUM)
# =========================
st.divider()

st.subheader("💰 Recursos avançados")

st.write("Previsão, alertas e análise inteligente em breve.")

if st.button("📩 Quero acesso antecipado"):
    st.success("Você entrou na lista 🚀")
