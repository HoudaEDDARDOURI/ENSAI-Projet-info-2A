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
if "current_page" not in st.session_state:
    st.session_state.current_page = "Feed"

# Style CSS pour masquer les éléments Streamlit indésirables et styliser la sidebar
st.markdown("""
<style>
/* ✅ CACHER LE MENU DEBUG ET LES ÉLÉMENTS STREAMLIT */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Cacher le bouton "Deploy" en haut à droite */
.stDeployButton {display: none;}

/* Cacher la barre de développement */
.viewerBadge_container__1QSob {display: none;}

/* Style pour les boutons de navigation */
div.stButton > button {
    width: 100%;
    text-align: left;
    padding: 12px 16px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    background-color: white;
    font-weight: 500;
    transition: all 0.3s;
}

div.stButton > button:hover {
    background-color: #f5f5f5;
    border-color: #667eea;
    transform: translateX(5px);
}

/* Cacher les labels des boutons */
.stButton {
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR DESIGN =====
with st.sidebar:
    st.markdown("# 🏃 Sport App")
    st.markdown("---")
    
    # Affichage utilisateur connecté
    if st.session_state.get("username"):
        st.markdown(f"### 👤 Bienvenue")
        st.markdown(f"**@{st.session_state.username}**")
        st.markdown("---")
        
        # Navigation avec boutons stylisés
        st.markdown("### 🧭 Navigation")
        
        pages_config = [
            ("🏠 Feed", "Feed"),
            ("🏃 Mes Activités", "Activités"),
            ("📊 Statistiques", "Statistiques"),
            ("🗺️ Parcours", "Parcours"),
            ("👥 Utilisateurs", "Utilisateurs")
        ]
        
        for label, page_name in pages_config:
            if st.button(label, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.current_page = page_name
                st.rerun()
        
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
        st.markdown("---")
        if st.button("🚪 Se déconnecter", use_container_width=True, type="secondary"):
            st.session_state.auth = None
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.current_page = "Feed"
            st.rerun()
    else:
        # Message si non connecté
        st.info("👋 Connectez-vous pour accéder à l'application")

# ===== ROUTING DES PAGES =====
# Si pas connecté, toujours afficher la page utilisateurs (connexion)
if not st.session_state.get("auth"):
    users_page()
else:
    # Si connecté, router vers la page actuelle
    page = st.session_state.current_page
    
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