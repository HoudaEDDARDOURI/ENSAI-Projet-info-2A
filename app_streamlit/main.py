import streamlit as st
from pages.user_page import users_page
from pages.activite_page import activites_page
from pages.statistique_page import statistiques_page
from pages.feed_page import feed_page
from pages.parcours_page import parcours_page

st.set_page_config(
    page_title="Sport App 🏃",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de la session
if "auth" not in st.session_state:
    st.session_state.auth = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

# ===== SIDEBAR DESIGN =====
with st.sidebar:
    st.markdown("# 🏃 Sport App")
    st.markdown("---")
    
    # Affichage utilisateur connecté
    if st.session_state.get("username"):
        st.markdown(f"### 👤 Connecté en tant que")
        st.markdown(f"**@{st.session_state.username}**")
        st.markdown("---")
    
    # Navigation avec icônes
    st.markdown("### 🧭 Navigation")
    
    # Style des boutons de navigation
    pages_config = {
        "🏠 Feed": "Feed",
        "🏃 Mes Activités": "Activités",
        "📊 Statistiques": "Statistiques",
        "🗺️ Parcours": "Parcours",
        "👥 Utilisateurs": "Utilisateurs"
    }
    
    # Sélection de la page
    page_display = st.radio(
        "Choisir une page",
        options=list(pages_config.keys()),
        label_visibility="collapsed"
    )
    
    page = pages_config[page_display]
    
    st.markdown("---")
    
    # Section aide/info
    with st.expander("ℹ️ À propos"):
        st.write("""
        **Sport App** vous permet de :
        - 📝 Suivre vos activités sportives
        - 📊 Analyser vos performances
        - 👥 Suivre vos amis
        - 🗺️ Créer des parcours
        """)
    
    # Déconnexion
    if st.session_state.get("auth"):
        st.markdown("---")
        if st.button("🚪 Se déconnecter", use_container_width=True, type="secondary"):
            st.session_state.auth = None
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()

# ===== ROUTING DES PAGES =====
if page == "Feed":
    feed_page()
elif page == "Activités":
    activites_page()
elif page == "Statistiques":
    statistiques_page()
elif page == "Parcours":
    parcours_page()
elif page == "Utilisateurs":
    users_page()
else:
    feed_page()  # Page par défaut