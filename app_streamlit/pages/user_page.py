# users_page.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def users_page():
    st.header("🔐 Gestion Utilisateur")

    # -------------------------
    # 🎨 STYLE INSTAGRAM
    # -------------------------
    st.markdown("""
    <style>
    /* Bouton bleu Instagram-like */
    div.stButton > button:first-child {
        background-color: #0095F6;
        color: white;
        border-radius: 8px;
        padding: 6px 18px;
        border: none;
        font-weight: 600;
    }
    div.stButton > button:first-child:hover {
        background-color: #1877F2;
        color: white;
    }

    /* Ligne utilisateur */
    .user-row {
        padding: 12px 0;
        border-bottom: 1px solid #e6e6e6;
    }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------
    # 🌐 UTILISATEUR CONNECTÉ
    # -------------------------
    if st.session_state.auth:
        resp = requests.get(f"{API_URL}/users/me", auth=st.session_state.auth)

        if resp.status_code == 200:
            user = resp.json()
            st.session_state.user = user  # stocké pour d'autres pages

            st.success(f"Connecté : {user['prenom']} {user['nom']}")
            st.write(f"@{user['username']}")

            st.write(f"👥 Followers : **{user.get('followers_count', 0)}**")
            st.write(f"➡️ Suivis : **{user.get('followed_count', 0)}**")

            st.markdown("---")
            st.subheader("🔥 Suggestions d'amis")

            # -------------------------
            # 🔍 SUGGESTIONS A SUIVRE
            # -------------------------
            suggestions_resp = requests.get(f"{API_URL}/users/suggestions", auth=st.session_state.auth)

            if suggestions_resp.status_code == 200:
                suggestions = suggestions_resp.json()

                if not suggestions:
                    st.info("Aucune suggestion pour le moment 😢.")

                for s in suggestions:
                    with st.container():
                        st.markdown('<div class="user-row">', unsafe_allow_html=True)

                        col1, col2 = st.columns([4, 1])

                        with col1:
                            st.write(f"**{s['prenom']} {s['nom']}**")
                            st.caption(f"@{s['username']}")

                        with col2:
                            if st.button("Suivre", key=f"follow_{s['id_user']}"):
                                follow = requests.post(
                                    f"{API_URL}/users/{s['id_user']}/follow",
                                    auth=st.session_state.auth
                                )
                                if follow.status_code == 200:
                                    st.success(f"🤝 Vous suivez maintenant {s['prenom']} !")
                                    st.rerun()
                                else:
                                    st.error(follow.json().get("detail", "Erreur"))

                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Impossible de récupérer les suggestions.")

            st.markdown("---")

            # -------------------------
            # 🚪 BOUTON DÉCONNEXION
            # -------------------------
            if st.button("Se déconnecter"):
                st.session_state.auth = None
                st.session_state.user = None
                st.rerun()

            return

        else:
            st.error("Erreur d'authentification.")
            st.session_state.auth = None
            st.session_state.user = None
            return

    # -------------------------
    # 🔑 PAS CONNECTÉ → LOGIN / SIGNUP
    # -------------------------
    action = st.radio("Action", ["Se connecter", "Créer un compte"])

    if action == "Se connecter":
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Connexion"):
            resp = requests.get(f"{API_URL}/users/me", auth=(username, password))
            if resp.status_code == 200:
                st.session_state.auth = (username, password)
                st.session_state.user = resp.json()
                st.success("Connexion réussie ✅")
                st.rerun()
            else:
                try:
                    st.error(resp.json().get("detail", "Identifiants incorrects"))
                except:
                    st.error("Identifiants incorrects.")

    else:  # Création de compte
        prenom = st.text_input("Prénom")
        nom = st.text_input("Nom")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Créer mon compte"):
            data = {"prenom": prenom, "nom": nom, "username": username, "password": password}
            resp = requests.post(f"{API_URL}/users/", data=data)

            if resp.status_code == 200:
                st.success("Compte créé 🎉 Vous pouvez maintenant vous connecter.")
            else:
                st.error(resp.json().get("detail", "Erreur lors de la création du compte."))
