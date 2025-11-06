import streamlit as st
import requests
from datetime import datetime

# URL de l'API FastAPI
API_URL = "http://127.0.0.1:8000"

# Configuration de la page
st.set_page_config(
    page_title="Sport Activities",
    page_icon="🏃",
    layout="wide"
)

st.title("🏃 Sport Activities - Gestion Utilisateur & Activités")

# --- Session utilisateur ---
if "auth" not in st.session_state:
    st.session_state.auth = None  # stocke (username, password) après connexion

# --- Fonction de déconnexion ---
def logout():
    st.session_state.auth = None
    st.rerun()

# --- Sidebar : Connexion / Inscription ---
with st.sidebar:
    st.header("🔐 Authentification")
    
    if st.session_state.auth:
        # Utilisateur connecté
        user_resp = requests.get(f"{API_URL}/users/me", auth=st.session_state.auth)
        if user_resp.status_code == 200:
            user = user_resp.json()
            st.success(f"Connecté : **{user['prenom']} {user['nom']}**")
            st.write(f"👤 @{user['username']}")
            if st.button("🚪 Se déconnecter", use_container_width=True):
                logout()
        else:
            st.error("Session expirée")
            logout()
    else:
        # Pas connecté
        action = st.selectbox("Choisir une action", ["Se connecter", "Créer un compte"])
        
        # --- Créer un compte ---
        if action == "Créer un compte":
            st.subheader("📝 Nouveau compte")
            with st.form("signup_form"):
                prenom = st.text_input("Prénom", placeholder="Jean")
                nom = st.text_input("Nom", placeholder="Dupont")
                username = st.text_input("Nom d'utilisateur", placeholder="jean.dupont")
                password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
                
                submit = st.form_submit_button("✅ Créer le compte", use_container_width=True)
                
                if submit:
                    if prenom and nom and username and password:
                        payload = {
                            "prenom": prenom,
                            "nom": nom,
                            "username": username,
                            "password": password
                        }
                        try:
                            response = requests.post(f"{API_URL}/users/", data=payload)
                            if response.status_code == 200:
                                st.success(f"✅ Compte créé : {response.json()['username']}")
                                st.info("👉 Vous pouvez maintenant vous connecter")
                            else:
                                st.error(f"❌ Erreur : {response.json().get('detail', 'Erreur inconnue')}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ Erreur de connexion à l'API : {e}")
                    else:
                        st.warning("⚠️ Veuillez remplir tous les champs")

        # --- Se connecter ---
        elif action == "Se connecter":
            st.subheader("🔑 Connexion")
            with st.form("login_form"):
                username = st.text_input("Nom d'utilisateur", placeholder="jean.dupont")
                password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
                
                submit = st.form_submit_button("🔓 Se connecter", use_container_width=True)
                
                if submit:
                    if username and password:
                        try:
                            response = requests.get(f"{API_URL}/users/me", auth=(username, password))
                            if response.status_code == 200:
                                st.session_state.auth = (username, password)
                                st.success("✅ Connexion réussie !")
                                st.rerun()
                            else:
                                st.error(f"❌ {response.json().get('detail', 'Erreur serveur')}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"❌ Erreur de connexion à l'API : {e}")
                    else:
                        st.warning("⚠️ Veuillez entrer vos identifiants")

# --- Interface principale (après connexion) ---
if st.session_state.auth:
    auth = st.session_state.auth

    # Récupérer les infos utilisateur
    try:
        user_resp = requests.get(f"{API_URL}/users/me", auth=auth)
        if user_resp.status_code == 200:
            user = user_resp.json()
            
            # Onglets
            tab1, tab2 = st.tabs(["📊 Mes Activités", "➕ Nouvelle Activité"])
            
            # ═══════════════════════════════════════════
            # TAB 1 : Afficher toutes les activités
            # ═══════════════════════════════════════════
            with tab1:
                st.header("📊 Toutes mes activités")
                
                try:
                    activites_resp = requests.get(f"{API_URL}/activites/", auth=auth)
                    if activites_resp.status_code == 200:
                        activites = activites_resp.json() 
                        
                        if len(activites) == 0:
                            st.info("🏃 Aucune activité enregistrée. Créez-en une dans l'onglet 'Nouvelle Activité' !")
                        else:
                            st.success(f"**{len(activites)}** activité(s) enregistrée(s)")
                            
                            # Affichage en colonnes
                            for i, act in enumerate(activites):
                                with st.container():
                                    col1, col2, col3 = st.columns([3, 2, 2])
                                    
                                    with col1:
                                        st.subheader(f"🏅 {act.get('titre', 'Sans titre')}")
                                        st.write(f"**Type :** {act.get('type_sport', 'N/A')}")
                                        st.write(f"📝 {act.get('description', 'Pas de description')}")
                                    
                                    with col2:
                                        st.metric("📏 Distance", f"{act.get('distance', 0)} km")
                                        st.write(f"📅 **Date :** {act.get('date_activite', 'N/A')}")
                                    
                                    with col3:
                                        st.metric("⏱️ Durée", act.get('duree', 'N/A'))
                                        st.write(f"🗺️ **Parcours ID :** {act.get('id_parcours', 'N/A')}")
                                    
                                    st.divider()
                    else:
                        st.error(f"❌ Impossible de récupérer les activités : {activites_resp.json().get('detail', 'Erreur')}")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Erreur de connexion à l'API : {e}")
            
            # ═══════════════════════════════════════════
            # TAB 2 : Créer une nouvelle activité
            # ═══════════════════════════════════════════
            with tab2:
                st.header("➕ Créer une nouvelle activité")
                
                with st.form("create_activity_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        titre = st.text_input("🏅 Titre de l'activité *", placeholder="Course matinale au parc")
                        type_sport = st.selectbox("🏃 Type de sport *", 
                            ["Course à pied", "Vélo", "Natation", "Randonnée", "Marche", "Autre"])
                        date_activite = st.date_input("📅 Date de l'activité *", value=datetime.today())
                        distance = st.number_input("📏 Distance (km) *", min_value=0.0, step=0.1, format="%.2f")
                    
                    with col2:
                        duree = st.text_input("⏱️ Durée (HH:MM:SS) *", placeholder="01:30:00")
                        id_parcours = st.number_input("🗺️ ID du parcours *", min_value=1, value=1, step=1)
                        trace = st.text_input("📍 Trace GPS / fichier", placeholder="trace.gpx (optionnel)")
                        description = st.text_area("📝 Description", placeholder="Belle séance sous le soleil...")
                    
                    st.info("ℹ️ Les champs marqués d'un * sont obligatoires")
                    
                    submit = st.form_submit_button("✅ Enregistrer l'activité", use_container_width=True)
                    
                    if submit:
                        # Validation
                        if not titre or not type_sport or not distance or not duree:
                            st.error("⚠️ Veuillez remplir tous les champs obligatoires")
                        else:
                            payload = {
                                "date_activite": str(date_activite),
                                "type_sport": type_sport,
                                "distance": distance,
                                "duree": duree,
                                "trace": trace if trace else "",
                                "titre": titre,
                                "description": description if description else "",
                                "id_parcours": id_parcours
                            }
                            
                            try:
                                resp = requests.post(f"{API_URL}/activites/", data=payload, auth=auth)
                                if resp.status_code == 200:
                                    st.success(f"✅ Activité '{resp.json()['titre']}' créée avec succès !")
                                    st.balloons()
                                    st.info("👉 Consultez l'onglet 'Mes Activités' pour voir votre nouvelle activité")
                                else:
                                    st.error(f"❌ Erreur : {resp.json().get('detail', 'Erreur création activité')}")
                            except requests.exceptions.RequestException as e:
                                st.error(f"❌ Erreur de connexion à l'API : {e}")
        
        else:
            st.error("❌ Impossible de récupérer vos informations. Veuillez vous reconnecter.")
            logout()
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erreur de connexion à l'API : {e}")
        st.info("💡 Vérifiez que l'API FastAPI est bien lancée sur http://127.0.0.1:8000")

else:
    # Message d'accueil quand pas connecté
    st.info("👈 Connectez-vous ou créez un compte dans la barre latérale pour commencer !")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 🏃 Suivez vos activités
        Enregistrez toutes vos séances sportives
        """)
    with col2:
        st.markdown("""
        ### 📊 Analysez vos performances
        Consultez vos statistiques
        """)
    with col3:
        st.markdown("""
        ### 🎯 Atteignez vos objectifs
        Progressez à votre rythme
        """)