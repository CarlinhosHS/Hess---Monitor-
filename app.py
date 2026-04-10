import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import logging

# =================================================================
# 🛡️ CONFIGURAÇÃO DE SEGURANÇA E AMBIENTE
# =================================================================
st.set_page_config(page_title="HESS AI Pro", layout="wide", page_icon="🚀")

# Estilo CSS Avançado (Look & Feel Profissional)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #3B82F6; }
    .status-card { padding: 20px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 🧠 CLASSE DE PROCESSAMENTO (CONTROLLER/MODEL)
# =================================================================
class HESSDataEngine:
    """Gerencia a captura de dados e lógica de IA."""
    
    @staticmethod
    @st.cache_data(ttl=300)
    def fetch_noaa_data():
        try:
            url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            df = pd.DataFrame(response.json())
            df["time_tag"] = pd.to_datetime(df["time_tag"])
            df["kp"] = pd.to_numeric(df["kp_index"], errors="coerce")
            return df.tail(120)
        except Exception as e:
            logging.error(f"Erro na API NOAA: {e}")
            return pd.DataFrame()

    @staticmethod
    def run_ia_forecast(series, steps=20):
        """IA de Suavização Exponencial para séries temporais."""
        if len(series) < 10: return np.array([])
        model = SimpleExpSmoothing(series, initialization_method="estimated").fit()
        forecast = model.forecast(steps)
        return np.clip(forecast, 0, 9)

# =================================================================
# 🖥️ CLASSE DE INTERFACE (VIEW)
# =================================================================
class HESSInterface:
    def __init__(self):
        self.engine = HESSDataEngine()
        self.init_session()

    def init_session(self):
        if 'auth' not in st.session_state:
            st.session_state.auth = False

    def render_login(self):
        st.title("🔐 HESS OS v3.0")
        col_l, col_r = st.columns(2)
        with col_l:
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.button("Acessar Terminal", use_container_width=True):
                # Dica: Em produção, verifique contra o Supabase/Secrets
                if user == "admin" and pw == "admin": 
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Acesso Negado.")

    def render_dashboard(self):
        df = self.engine.fetch_noaa_data()
        if df.empty:
            st.warning("Aguardando sincronização com satélites NOAA...")
            return

        # --- HEADER ---
        st.title("🛰️ HESS | Monitoramento Global")
        
        # --- MÉTRICAS ---
        kp_atual = df["kp"].iloc[-1]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Kp Atual", f"{kp_atual:.2f}")
        c2.metric("Pico Recente", f"{df['kp'].max():.2f}")
        c3.metric("Média (2h)", f"{df['kp'].mean():.2f}")
        
        status = "CRÍTICO" if kp_atual >= 5 else "ALERTA" if kp_atual >= 3 else "NOMINAL"
        c4.write(f"**STATUS DO CAMPO:**\n# {status}")

        # --- TABS DE ANÁLISE ---
        tab_grafico, tab_ia, tab_raw = st.tabs(["📡 Telemetria", "🧠 IA Preditiva", "📄 Dados Brutos"])

        with tab_grafico:
            self.plot_main_chart(df)

        with tab_ia:
            self.render_ia_tab(df)

    def plot_main_chart(self, df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time_tag"], y=df["kp"], mode='lines', fill='tozeroy', line=dict(color='#3B82F6')))
        fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    def render_ia_tab(self, df):
        st.subheader("Predição por Suavização Exponencial (Holt-Winters)")
        horizonte = st.slider("Horizonte (minutos)", 5, 60, 20)
        
        preds = self.engine.run_ia_forecast(df["kp"], steps=horizonte)
        future_dates = pd.date_range(df["time_tag"].iloc[-1], periods=horizonte+1, freq='min')[1:]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time_tag"].tail(30), y=df["kp"].tail(30), name="Real"))
        fig.add_trace(go.Scatter(x=future_dates, y=preds, name="IA Forecast", line=dict(dash='dot', color='#EF4444')))
        fig.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig, use_container_width=True)

# --- EXECUÇÃO ---
app = HESSInterface()
if st.session_state.auth:
    app.render_dashboard()
else:
    app.render_login()
