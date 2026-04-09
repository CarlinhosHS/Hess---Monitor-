import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import plotly.express as px

# =========================
# 🔐 SISTEMA DE LOGIN
# =========================
class Auth:
    def __init__(self):
        if "logado" not in st.session_state:
            st.session_state.logado = False

    def login(self):
        st.title("🔐 Login HESS")
        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if user == "admin" and senha == "123":
                st.session_state.logado = True
                st.success("Login realizado!")
                st.rerun()
            else:
                st.error("Credenciais inválidas")

    def check(self):
        return st.session_state.logado


# =========================
# 🌍 DADOS NOAA
# =========================
class DataLoader:

    @st.cache_data(ttl=60)
    def get_kp_data(self):
        url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
        r = requests.get(url)
        data = r.json()

        df = pd.DataFrame(data)
        df["time_tag"] = pd.to_datetime(df["time_tag"])
        df = df.rename(columns={"kp_index": "kp"})

        return df.tail(100)


# =========================
# 🧠 IA DE PREVISÃO
# =========================
class IA:
    def prever(self, df):
        modelo = SimpleExpSmoothing(df["kp"]).fit()
        previsao = modelo.forecast(10)

        previsao = np.clip(previsao, 0, 9)
        return previsao


# =========================
# 📊 DASHBOARD
# =========================
class Dashboard:

    def grafico_principal(self, df, previsao):
        fig = px.line(df, x="time_tag", y="kp",
                      title="📡 Atividade Geomagnética em Tempo Real")

        # previsão
        futuro = pd.date_range(df["time_tag"].iloc[-1], periods=10, freq="T")
        fig.add_scatter(x=futuro, y=previsao, mode="lines", name="Previsão IA")

        # linhas de referência
        fig.add_hline(y=3, line_dash="dash", line_color="yellow")
        fig.add_hline(y=5, line_dash="dash", line_color="red")

        fig.update_layout(
            template="plotly_dark" if st.session_state.tema == "escuro" else "plotly_white",
            xaxis_title="Tempo",
            yaxis_title="Índice Kp",
        )

        st.plotly_chart(fig, use_container_width=True)

    def metricas(self, df):
        col1, col2, col3 = st.columns(3)

        ultimo = round(df["kp"].iloc[-1], 2)

        col1.metric("📈 Último Kp", ultimo)
        col2.metric("⚠️ Alertas", len(df[df["kp"] > 3]))
        col3.metric("🚨 Críticos", len(df[df["kp"] > 5]))

        if ultimo >= 5:
            st.error("🚨 Tempestade Solar")
        elif ultimo >= 3:
            st.warning("⚠️ Atividade Elevada")
        else:
            st.success("✅ Normal")


# =========================
# 🌍 LOCALIZAÇÃO
# =========================
class Geo:

    @st.cache_data(ttl=300)
    def get_location(self):
        try:
            data = requests.get("https://ipapi.co/json").json()
            return data["city"], data["country_name"]
        except:
            return "Desconhecido", "Desconhecido"


# =========================
# 🚀 APP PRINCIPAL
# =========================
class HessApp:

    def __init__(self):
        st.set_page_config(layout="wide", page_title="HESS PRO")

        self.auth = Auth()
        self.data = DataLoader()
        self.ia = IA()
        self.dashboard = Dashboard()
        self.geo = Geo()

        if "tema" not in st.session_state:
            st.session_state.tema = "escuro"

        self.run()

    def run(self):

        if not self.auth.check():
            self.auth.login()
            return

        # LOCALIZAÇÃO
        cidade, pais = self.geo.get_location()

        # SIDEBAR
        st.sidebar.title("⚙️ Configurações")
        st.session_state.tema = st.sidebar.radio("Tema", ["escuro", "claro"])

        # TABS
        tab1, tab2, tab3 = st.tabs([
            "📊 Monitoramento",
            "🧠 IA & Previsão",
            "⚙️ Sistema"
        ])

        df = self.data.get_kp_data()
        previsao = self.ia.prever(df)

        # -------------------
        # 📊 MONITORAMENTO
        # -------------------
        with tab1:
            st.title("🚀 HESS Monitor")
            st.caption(f"📍 {cidade}, {pais}")

            self.dashboard.metricas(df)
            self.dashboard.grafico_principal(df, previsao)

        # -------------------
        # 🧠 IA
        # -------------------
        with tab2:
            st.subheader("🧠 Previsão Inteligente")

            futuro = pd.DataFrame({
                "tempo": range(len(previsao)),
                "kp": previsao
            })

            fig = px.line(futuro, x="tempo", y="kp", title="Previsão IA")
            st.plotly_chart(fig, use_container_width=True)

        # -------------------
        # ⚙️ SISTEMA
        # -------------------
        with tab3:
            st.subheader("ℹ️ Sobre o HESS")

            st.markdown("""
            O HESS é um sistema inteligente de monitoramento geomagnético que:

            - Usa dados reais da NOAA
            - Detecta anomalias solares
            - Aplica IA para previsão
            - Pode alertar eventos extremos

            🎯 Objetivo:
            Antecipar tempestades solares e proteger sistemas sensíveis.
            """)

            if st.button("🚪 Sair"):
                st.session_state.logado = False
                st.rerun()


# =========================
# 🚀 EXECUÇÃO
# =========================
HessApp()
