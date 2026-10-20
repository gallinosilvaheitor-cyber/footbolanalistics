"""Football Analytics Hub — Plataforma Profissional de Inteligência Esportiva e BI do Futebol."""

import os
import streamlit as st
from dotenv import load_dotenv

# Carrega variáveis locais se existirem
load_dotenv()

# Configuração da página Streamlit (deve ser o primeiro comando Streamlit)
st.set_page_config(
    page_title="Football Analytics Hub | Inteligência Esportiva",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.api.client import get_football_client
from src.utils.config import SUPPORTED_COMPETITIONS, APP_NAME, APP_TAGLINE, APP_VERSION
from src.views import (
    render_dashboard_view,
    render_competitions_view,
    render_teams_view,
    render_players_view,
    render_matches_view,
    render_advanced_analytics_view,
    render_mobile_install_view
)

# Injeção de Meta Tags PWA (Progressive Web App) e CSS Global
st.markdown(
    """
    <!-- Metatags para funcionamento como App no Android, iOS e PC -->
    <link rel="manifest" href="/app/static/manifest.json">
    <link rel="apple-touch-icon" href="/app/static/apple-touch-icon.png">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="FootballHub">
    <meta name="theme-color" content="#0d1117">

    <script>
      // Registro do Service Worker para suporte PWA
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
          navigator.serviceWorker.register('/app/static/service-worker.js').catch(function(err) {
            console.log('Service Worker registro ignorado em dev:', err);
          });
        });
      }
    </script>

    <style>
        /* Tipografia e Fundo */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Ajuste do container principal */
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }
        
        /* Sidebar estilizada */
        section[data-testid="stSidebar"] {
            background-color: #12171f;
            border-right: 1px solid #21262d;
        }
        
        /* Botões customizados */
        .stButton > button {
            background-color: #21262d;
            color: #f0f6fc;
            border: 1px solid #30363d;
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #00e676;
            color: #0d1117;
            border-color: #00e676;
            transform: translateY(-1px);
        }
        
        /* Abas e caixas de seleção */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #161b22;
            border-radius: 6px;
            padding: 8px 16px;
            color: #8b949e;
            border: 1px solid #30363d;
        }
        .stTabs [aria-selected="true"] {
            background-color: #00e676 !important;
            color: #0d1117 !important;
            font-weight: 700;
        }
        
        /* Estilização de métricas nativas */
        [data-testid="stMetricValue"] {
            color: #00e676;
            font-weight: 700;
        }
        
        /* Rodapé customizado */
        .footer-container {
            margin-top: 50px;
            padding: 20px 0;
            border-top: 1px solid #21262d;
            text-align: center;
            color: #8b949e;
            font-size: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Inicialização do estado de sessão
    if "api_key" not in st.session_state:
        env_key = os.getenv("FOOTBALL_DATA_API_KEY", "")
        secret_key = ""
        try:
            if hasattr(st, "secrets") and "FOOTBALL_DATA_API_KEY" in st.secrets:
                secret_key = st.secrets["FOOTBALL_DATA_API_KEY"]
        except Exception:
            secret_key = ""
        st.session_state.api_key = secret_key or env_key or ""

    if "force_demo" not in st.session_state:
        st.session_state.force_demo = not bool(st.session_state.api_key)

    # BARRA LATERAL (Sidebar)
    with st.sidebar:
        # Branding do App
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                <span style="font-size: 1.8rem;">⚽</span>
                <span style="font-size: 1.25rem; font-weight: 800; color: #f0f6fc; letter-spacing: -0.5px;">
                    {APP_NAME}
                </span>
            </div>
            <div style="font-size: 0.75rem; color: #8b949e; margin-bottom: 20px;">
                {APP_TAGLINE} v{APP_VERSION}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.divider()

        # Navegação Principal
        st.markdown("### 🧭 Navegação")
        menu_options = [
            "🏠 Visão Geral",
            "🏆 Campeonatos & Tabela",
            "🛡️ Raio-X das Equipes",
            "🎯 Artilharia & Atletas",
            "📅 Calendário de Jogos",
            "🔬 BI & Análise Avançada",
            "📱 Como Usar como App (Celular/PC)"
        ]
        selected_menu = st.radio("Selecione a Tela:", menu_options, label_visibility="collapsed")

        st.divider()

        # Seleção da Competição
        st.markdown("### 🌍 Competição Ativa")
        comp_keys = list(SUPPORTED_COMPETITIONS.keys())
        comp_labels = [f"{SUPPORTED_COMPETITIONS[k]['flag']} {SUPPORTED_COMPETITIONS[k]['name']}" for k in comp_keys]
        
        selected_comp_idx = st.selectbox(
            "Campeonato:",
            range(len(comp_keys)),
            format_func=lambda i: comp_labels[i]
        )
        active_comp_code = comp_keys[selected_comp_idx]

        st.divider()

        # Controle de Conexão e Chave de API
        st.markdown("### ⚙️ Conexão & Dados")
        
        # Modo Demonstração Toggle
        use_demo_toggle = st.checkbox(
            "Modo Demonstração (Offline)",
            value=st.session_state.force_demo,
            help="Ative para explorar o app com dados sintéticos offline sem consumir sua cota da API."
        )
        st.session_state.force_demo = use_demo_toggle

        # Entrada de Chave de API se não estiver em modo demo forçado
        if not use_demo_toggle:
            api_key_input = st.text_input(
                "Chave API football-data.org:",
                value=st.session_state.api_key,
                type="password",
                help="Cadastre-se gratuitamente em football-data.org para obter uma chave de 10 req/min."
            )
            if api_key_input != st.session_state.api_key:
                st.session_state.api_key = api_key_input
                st.rerun()

        # Botão de Sincronização / Limpeza de Cache
        if st.button("🔄 Atualizar / Limpar Cache", use_container_width=True):
            st.cache_data.clear()
            st.toast("Cache reiniciado com sucesso!", icon="🧹")
            st.rerun()

        # Status do Cliente e Rate Limit
        client = get_football_client(api_key=st.session_state.api_key)
        is_blocked, wait_s = client.is_rate_limited()
        if is_blocked:
            st.warning(f"⏳ Cota por minuto da API ativa. Aguarde {wait_s}s para nova chamada.", icon="⏳")

        # Badges informativos na barra lateral
        if st.session_state.force_demo:
            st.caption("🟡 Status: Modo Demonstração (Sem requisições externas)")
        elif client.has_api_key():
            st.caption("🟢 Status: Chave configurada (football-data.org)")
        else:
            st.caption("⚠️ Sem chave informada. Usando demonstração automática.")

    # ROTEAMENTO DE TELAS
    use_demo = st.session_state.force_demo or not client.has_api_key()

    if selected_menu == "🏠 Visão Geral":
        render_dashboard_view(client, active_comp_code, use_demo=use_demo)
    elif selected_menu == "🏆 Campeonatos & Tabela":
        render_competitions_view(client, active_comp_code, use_demo=use_demo)
    elif selected_menu == "🛡️ Raio-X das Equipes":
        render_teams_view(client, active_comp_code, use_demo=use_demo)
    elif selected_menu == "🎯 Artilharia & Atletas":
        render_players_view(client, active_comp_code, use_demo=use_demo)
    elif selected_menu == "📅 Calendário de Jogos":
        render_matches_view(client, active_comp_code, use_demo=use_demo)
    elif selected_menu == "🔬 BI & Análise Avançada":
        render_advanced_analytics_view(client, active_comp_code, use_demo=use_demo)
    elif selected_menu == "📱 Como Usar como App (Celular/PC)":
        render_mobile_install_view()

    # RODAPÉ (Footer)
    st.markdown(
        """
        <div class="footer-container">
            <b>Football Analytics Hub</b> — Desenvolvido com Python, Streamlit, Pandas, NumPy e Plotly.<br>
            Integração com a API <a href="https://www.football-data.org/" target="_blank" style="color: #00e676; text-decoration: none;">football-data.org</a>.
            As marcas, nomes e escudos pertencem às suas respectivas entidades esportivas.<br>
            <span style="font-size: 0.75rem; color: #6e7681;">Código aberto sob licença MIT. Pronto para implantação no Streamlit Community Cloud.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
