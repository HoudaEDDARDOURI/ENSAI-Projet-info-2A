import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def users_page():
    # -------------------------
    # 🎨 STYLE MODERNE
    # -------------------------
    st.markdown("""
    <style>
    /* Style principal */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Boutons */
    div.stButton > button {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    
    /* Bouton primaire (Suivre) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(45deg, #405DE6, #5B51D8, #833AB4, #C13584, #E1306C, #FD1D1D);
        color: white;
    }
    
    /* Bouton secondaire (Ne plus suivre) */
    .stButton > button[kind="secondary"] {
        background-color: #EFEFEF;
        color: #262626;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Cards utilisateurs */
    .user-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        border: 1px solid #DBDBDB;
        transition: all 0.3s;
    }
    
    .user-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    /* Stats */
    .stat-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .stat-number {
        font-size: 2em;
        font-weight: bold;
    }
    
    .stat-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    
    /* Profil header */
    .profile-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 30px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .profile-username {
        font-size: 1.8em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .profile-name {
        font-size: 1.1em;
        opacity: 0.9;
    }
    
    /* Tabs custom */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
    }
    
    /* Liste vide */
    .empty-state {
        text-align: center;
        padding: 40px;
        color: #8E8E8E;
    }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------
    # 🔑 INITIALISATION SESSION
    # -------------------------
    if "auth" not in st.session_state:
        st.session_state.auth = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    # -------------------------
    # 🌐 UTILISATEUR CONNECTÉ
    # -------------------------
    if st.session_state.auth:
        try:
            resp = requests.get(f"{API_URL}/users/me", auth=st.session_state.auth, timeout=10)
            
            if resp.status_code != 200:
                st.error("Erreur d'authentification.")
                st.session_state.auth = None
                st.rerun()
                return
            
            user = resp.json()
            st.session_state.user = user
            st.session_state.user_id = user.get("id_user") or user.get("id")
            st.session_state.username = user.get("username")
            
            # -------------------------
            # 📊 HEADER PROFIL
            # -------------------------
            st.markdown(f"""
            <div class="profile-header">
                <div style="display: flex; align-items: center; gap: 20px;">
                    <div style="font-size: 4em;">👤</div>
                    <div>
                        <div class="profile-username">@{user.get('username', '')}</div>
                        <div class="profile-name">{user.get('prenom', '')} {user.get('nom', '')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # -------------------------
            # 📈 STATISTIQUES
            # -------------------------
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="stat-container">
                    <div class="stat-number">{user.get('nombre_activites', 0)}</div>
                    <div class="stat-label">Activités</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-container">
                    <div class="stat-number">{user.get('followers_count', 0)}</div>
                    <div class="stat-label">Followers</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-container">
                    <div class="stat-number">{user.get('followed_count', 0)}</div>
                    <div class="stat-label">Suivis</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # -------------------------
            # 📑 ONGLETS
            # -------------------------
            tab1, tab2, tab3 = st.tabs(["👥 Mes Suivis", "💡 Suggestions", "⚙️ Paramètres"])
            # ═══════════════════════════════════
            # TAB 1 : MES SUIVIS
            # ═══════════════════════════════════
            with tab1:
                # Charger les données
                followed_users = []
                followers_users = []
                
                try:
                    # Récupérer abonnements
                    following_resp = requests.get(
                        f"{API_URL}/users/me/following", 
                        auth=st.session_state.auth,
                        timeout=10
                    )
                    if following_resp.status_code == 200:
                        followed_users = following_resp.json() or []
                    
                    # Récupérer abonnés
                    followers_resp = requests.get(
                        f"{API_URL}/users/me/followers", 
                        auth=st.session_state.auth,
                        timeout=10
                    )
                    if followers_resp.status_code == 200:
                        followers_users = followers_resp.json() or []
                        
                except Exception as e:
                    st.error(f"Erreur lors du chargement : {e}")
                
                # Sous-onglets
                subtab1, subtab2 = st.tabs([
                    f"👥 Abonnements ({len(followed_users)})", 
                    f"👤 Abonnés ({len(followers_users)})"
                ])
                
                # ─────────────────────────────────────
                # SOUS-ONGLET 1 : ABONNEMENTS
                # ─────────────────────────────────────
                with subtab1:
                    if not followed_users:
                        st.markdown("""
                        <div class="empty-state">
                            <div style="font-size: 3em;">🔍</div>
                            <h3>Vous ne suivez personne encore</h3>
                            <p>Découvrez des personnes dans l'onglet Suggestions !</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"### Vous suivez {len(followed_users)} personne(s)")
                        for followed in followed_users:
                            # relation_type="follow" pour les abonnements
                            render_user_card(
                                followed, 
                                is_following=True, 
                                key_prefix="following_", 
                                relation_type="follow"
                            )
                
                # ─────────────────────────────────────
                # SOUS-ONGLET 2 : ABONNÉS
                # ─────────────────────────────────────
                with subtab2:
                    if not followers_users:
                        st.markdown("""
                        <div class="empty-state">
                            <div style="font-size: 3em;">😔</div>
                            <h3>Personne ne vous suit encore</h3>
                            <p>Partagez vos activités pour attirer des abonnés !</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"### {len(followers_users)} personne(s) vous suit/suivent")
                        
                        for follower in followers_users:
                            # relation_type="follower" pour afficher le bouton "Retirer l'abonné"
                            render_user_card(
                                follower, 
                                is_following=False,  # Pas utilisé dans ce cas
                                key_prefix="followers_", 
                                relation_type="follower"
                            )
            # ═══════════════════════════════════
            # TAB 2 : SUGGESTIONS
            # ═══════════════════════════════════
            with tab2:
                st.subheader("💡 Suggestions pour vous")
                
                try:
                    suggestions_resp = requests.get(
                        f"{API_URL}/users/suggestions", 
                        auth=st.session_state.auth,
                        timeout=10
                    )
                    
                    if suggestions_resp.status_code == 200:
                        suggestions = suggestions_resp.json() or []
                        
                        if not suggestions:
                            st.markdown("""
                            <div class="empty-state">
                                <div style="font-size: 3em;">✨</div>
                                <h3>Aucune suggestion disponible</h3>
                                <p>Revenez plus tard pour découvrir de nouveaux profils !</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            for s in suggestions:
                                # ✅ Préfixe "suggestions_" pour les suggestions
                                render_user_card(s, is_following=False, key_prefix="suggestions_")
                    else:
                        st.error("Impossible de récupérer les suggestions")
                        
                except Exception as e:
                    st.error(f"Erreur : {e}")
            
            # ═══════════════════════════════════
            # TAB 3 : PARAMÈTRES
            # ═══════════════════════════════════
            with tab3:
                st.subheader("⚙️ Paramètres du compte")
                
                with st.expander("✏️ Modifier mon profil", expanded=False):
                    new_prenom = st.text_input("Prénom", value=user.get('prenom', ''))
                    new_nom = st.text_input("Nom", value=user.get('nom', ''))
                    new_username = st.text_input("Nom d'utilisateur", value=user.get('username', ''))
                    new_password = st.text_input("Nouveau mot de passe (laisser vide pour ne pas changer)", type="password")
                    
                    if st.button("💾 Enregistrer les modifications", type="primary"):
                        try:
                            data = {
                                "prenom": new_prenom,
                                "nom": new_nom,
                                "username": new_username
                            }
                            if new_password:
                                data["mot_de_passe"] = new_password
                            
                            update_resp = requests.put(
                                f"{API_URL}/users/me",
                                data=data,
                                auth=st.session_state.auth,
                                timeout=10
                            )
                            
                            if update_resp.status_code == 200:
                                st.success("✅ Profil mis à jour avec succès")
                                st.rerun()
                            else:
                                st.error(update_resp.json().get("detail", "Erreur lors de la mise à jour"))
                        except Exception as e:
                            st.error(f"Erreur : {e}")
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🚪 Se déconnecter", use_container_width=True):
                        st.session_state.auth = None
                        st.session_state.user = None
                        st.session_state.user_id = None
                        st.session_state.username = None
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ Supprimer mon compte", type="secondary", use_container_width=True):
                        if st.session_state.get("confirm_delete"):
                            try:
                                delete_resp = requests.delete(
                                    f"{API_URL}/users/{st.session_state.user_id}",
                                    auth=st.session_state.auth,
                                    timeout=10
                                )
                                if delete_resp.status_code == 200:
                                    st.success("Compte supprimé")
                                    st.session_state.auth = None
                                    st.rerun()
                                else:
                                    st.error("Erreur lors de la suppression")
                            except Exception as e:
                                st.error(f"Erreur : {e}")
                        else:
                            st.session_state.confirm_delete = True
                            st.warning("⚠️ Cliquez à nouveau pour confirmer la suppression")
            
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")
            st.session_state.auth = None
        
        return

    # -------------------------
    # 🔑 PAGE DE CONNEXION
    # -------------------------
    render_auth_page()

def render_user_card(user_data, is_following=False, key_prefix="", relation_type="follow"):
    """Affiche une carte utilisateur avec bouton follow/unfollow
    
    Args:
        user_data: Dictionnaire avec les infos de l'utilisateur
        is_following: True si on suit déjà cet utilisateur
        key_prefix: Préfixe pour rendre les clés uniques
        relation_type: "follow" (abonnements) ou "follower" (abonnés)
    """
    user_id = user_data.get('id_user')
    
    st.markdown('<div class="user-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 2])
    
    with col1:
        st.markdown('<div style="font-size: 3em; text-align: center;">👤</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**{user_data.get('prenom', '')} {user_data.get('nom', '')}**")
        st.caption(f"@{user_data.get('username', '')}")
    
    with col3:
        # ════════════════════════════════════════════
        # CAS 1 : Onglet ABONNÉS (followers)
        # ════════════════════════════════════════════
        if relation_type == "follower":
            if st.button("🚫 Retirer l'abonné", key=f"{key_prefix}remove_follower_{user_id}", type="secondary", use_container_width=True):
                try:
                    remove_resp = requests.delete(
                        f"{API_URL}/users/{user_id}/remove-follower",
                        auth=st.session_state.auth,
                        timeout=10
                    )
                    if remove_resp.status_code == 200:
                        st.success(f"@{user_data.get('username')} ne vous suit plus")
                        st.rerun()
                    else:
                        st.error(remove_resp.json().get("detail", "Erreur"))
                except Exception as e:
                    st.error(f"Erreur : {e}")
        
        # ════════════════════════════════════════════
        # CAS 2 : Onglet ABONNEMENTS ou SUGGESTIONS
        # ════════════════════════════════════════════
        else:
            if is_following:
                # Bouton "Ne plus suivre"
                if st.button("❌ Ne plus suivre", key=f"{key_prefix}unfollow_{user_id}", type="secondary", use_container_width=True):
                    try:
                        unfollow_resp = requests.delete(
                            f"{API_URL}/users/{user_id}/follow",
                            auth=st.session_state.auth,
                            timeout=10
                        )
                        if unfollow_resp.status_code == 200:
                            st.success(f"Vous ne suivez plus @{user_data.get('username')}")
                            st.rerun()
                        else:
                            st.error(unfollow_resp.json().get("detail", "Erreur"))
                    except Exception as e:
                        st.error(f"Erreur : {e}")
            else:
                # Bouton "Suivre"
                if st.button("➕ Suivre", key=f"{key_prefix}follow_{user_id}", type="primary", use_container_width=True):
                    try:
                        follow_resp = requests.post(
                            f"{API_URL}/users/{user_id}/follow",
                            auth=st.session_state.auth,
                            timeout=10
                        )
                        if follow_resp.status_code == 200:
                            st.success(f"Vous suivez maintenant @{user_data.get('username')}")
                            st.rerun()
                        else:
                            st.error(follow_resp.json().get("detail", "Erreur"))
                    except Exception as e:
                        st.error(f"Erreur : {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_auth_page():
    """Page de connexion/inscription"""
    st.markdown("""
    <div style="max-width: 400px; margin: 50px auto; text-align: center;">
        <h1 style="font-size: 3em;">🏃</h1>
        <h2>SporTrack</h2>
        <p style="color: #8E8E8E;">Connectez-vous pour suivre vos activités sportives</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Connexion", "✨ Inscription"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("Nom d'utilisateur", key="login_username")
        password = st.text_input("Mot de passe", type="password", key="login_password")
        
        if st.button("Se connecter", type="primary", use_container_width=True):
            if not username or not password:
                st.error("⚠️ Veuillez remplir tous les champs")
            else:
                try:
                    resp = requests.get(f"{API_URL}/users/me", auth=(username, password), timeout=10)
                    if resp.status_code == 200:
                        st.session_state.auth = (username, password)
                        st.session_state.user = resp.json()
                        st.session_state.user_id = st.session_state.user.get("id_user") or st.session_state.user.get("id")
                        st.session_state.username = username
                        st.success("✅ Connexion réussie")
                        st.rerun()
                    elif resp.status_code == 404:
                        st.error("❌ Utilisateur non trouvé")
                    elif resp.status_code == 401:
                        st.error("❌ Mot de passe incorrect")
                    else:
                        st.error("❌ Identifiants incorrects")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Impossible de se connecter au serveur. Vérifiez que l'API est démarrée.")
                except requests.exceptions.Timeout:
                    st.error("❌ Le serveur met trop de temps à répondre")
                except Exception as e:
                    st.error(f"❌ Erreur de connexion : {e}")
    
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        prenom = st.text_input("Prénom", key="signup_prenom")
        nom = st.text_input("Nom", key="signup_nom")
        username = st.text_input("Nom d'utilisateur", key="signup_username")
        password = st.text_input("Mot de passe", type="password", key="signup_password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="signup_confirm_password")
        
        if st.button("Créer mon compte", type="primary", use_container_width=True):
            # Validation côté client
            if not prenom or not nom or not username or not password:
                st.error("⚠️ Veuillez remplir tous les champs")
            elif len(username) < 3:
                st.error("⚠️ Le nom d'utilisateur doit contenir au moins 3 caractères")
            elif len(password) < 6:
                st.error("⚠️ Le mot de passe doit contenir au moins 6 caractères")
            elif password != confirm_password:
                st.error("⚠️ Les mots de passe ne correspondent pas")
            else:
                try:
                    data = {
                        "prenom": prenom, 
                        "nom": nom, 
                        "username": username, 
                        "password": password
                    }
                    resp = requests.post(f"{API_URL}/users/", data=data, timeout=10)
                    
                    if resp.status_code == 200:
                        st.success("🎉 Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
                        st.balloons()
                    elif resp.status_code == 400:
                        error_detail = resp.json().get("detail", "")
                        
                        # Gestion spécifique pour username déjà utilisé
                        if "username" in error_detail.lower() or "déjà utilisé" in error_detail.lower() or "already" in error_detail.lower():
                            st.error(f"❌ Le nom d'utilisateur '@{username}' est déjà pris. Veuillez en choisir un autre.")
                        else:
                            st.error(f"❌ {error_detail}")
                    else:
                        error_detail = resp.json().get("detail", "Erreur inconnue")
                        st.error(f"❌ Erreur lors de la création du compte : {error_detail}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Impossible de se connecter au serveur. Vérifiez que l'API est démarrée.")
                except requests.exceptions.Timeout:
                    st.error("❌ Le serveur met trop de temps à répondre")
                except Exception as e:
                    st.error(f"❌ Erreur : {e}")