import streamlit as st
import pandas as pd
import requests
from supabase import create_client, Client
import hashlib

# =========================
# 🔐 CONFIGURAÇÕES DE ACESSO (SUPABASE)
# =========================
# Obtenha estas chaves no painel do Supabase (Settings > API)
SUPABASE_URL = "SUA_URL_AQUI"
SUPABASE_KEY = "SUA_KEY_AQUI"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    st.error("Erro ao conectar ao banco de dados. Verifique as chaves.")

# Função para esconder a senha (Hash)
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# =========================
# 🧠 LÓGICA DE USUÁRIOS
# =========================
class AuthManager:
    @staticmethod
    def cadastrar_usuario(email, senha):
        hash_senha = make_hashes(senha)
        data, count = supabase.table("usuarios_hess").insert({"email": email, "senha": hash_senha}).execute()
        return data

    @staticmethod
    def verificar_login(email, senha):
        hash_senha = make_hashes(senha)
        res = supabase.table("usuarios_hess").select("*").eq("email", email).eq("senha", hash_senha).execute()
        return len(res.data) > 0

# =========================
# 🖥️ INTERFACE DE ACESSO
# =========================
def tela_autenticacao():
    st.title("🚀 HESS OS | Acesso")
    
    aba_login, aba_cadastro = st.tabs(["Entrar", "Criar Conta"])
    
    with aba_login:
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_pass")
        if st.button("Login"):
            if AuthManager.verificar_login(email, senha):
                st.session_state.logado = True
                st.session_state.usuario = email
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    with aba_cadastro:
        novo_email = st.text_input("Escolha um Email", key="reg_email")
        nova_senha = st.text_input("Escolha uma Senha", type="password", key="reg_pass")
        if st.button("Finalizar Cadastro"):
            try:
                AuthManager.cadastrar_usuario(novo_email, nova_senha)
                st.success("Conta criada! Vá para a aba de Login.")
            except:
                st.error("Este email já está cadastrado.")

# =========================
# 🚀 APP PRINCIPAL
# =========================
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    tela_autenticacao()
else:
    st.sidebar.success(f"Logado como: {st.session_state.usuario}")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()
    
    # AQUI ENTRA O RESTANTE DO SEU CÓDIGO DO DASHBOARD (Métricas, Gráficos, etc)
    st.title("📊 Bem-vindo ao HESS Monitor")
    st.write("Seu sistema está operando e protegido pelo banco de dados Supabase.")
