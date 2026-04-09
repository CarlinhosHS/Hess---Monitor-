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
# =========================
# 🎨 TEMA PROFISSIONAL PADRÃO
# =========================
hora = datetime.datetime.now().hour

if 6 <= hora < 18:
    # ☀️ MODO CLARO
    bg = "#F5F7FA"
    text_color = "#000000"   # TEXTO PRETO
    card = "#FFFFFF"
    graph_template = "plotly_white"
else:
    # 🌙 MODO ESCURO
    bg = "#0F172A"
    text_color = "#FFFFFF"   # TEXTO BRANCO
    card = "#1E293B"
    graph_template = "plotly_dark"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
    color: {text_color};
}}

/* textos gerais */
h1, h2, h3, h4, h5, h6, p, span, label {{
    color: {text_color} !important;
}}

/* cards */
div[data-testid="stMetric"] {{
    background-color: {card};
    padding: 15px;
    border-radius: 12px;
}}

/* sidebar */
section[data-testid="stSidebar"] {{
    background-color: {card};
}}

/* botão premium */
button[kind="primary"] {{
    background-color: #2563EB !important;
    color: white !important;
    border-radius: 10px;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# 🎯 TÍTULO
# =========================
if 6 <= hora < 12:
    tema = "🌥️ Manhã"
elif 12 <= hora < 18:
    tema = "☀️ Tarde"
elif 18 <= hora < 22:
    tema = "🌆 Noite"
else:
    tema = "🌌 Madrugada"

st.markdown(f"""
# 🚀 HESS Monitor
### {tema}
📡 Monitoramento Inteligente em Tempo Real

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
    template=graph_template,
    plot_bgcolor=bg,
    paper_bgcolor=bg,
    font=dict(color=text_color),
    dragmode="pan"
)

# linhas de referência
fig.add_hline(y=0.8, line_color="orange", line_dash="dash")
fig.add_hline(y=-0.8, line_color="red", line_dash="dash")

# pontos HESS
fig.add_scatter(
    x=hess["tempo"],
    y=hess["kp"],
    mode="markers",
    name="HESS",
    marker=dict(size=8, color="orange")
)

# pontos IA
fig.add_scatter(
    x=ia["tempo"],
    y=ia["kp"],
    mode="markers",
    name="IA",
    marker=dict(size=8, color="cyan")
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "scrollZoom": True,
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

if st.button("💎 Quero acesso premium"):
    st.success("🚀 Você entrou na lista premium!")
