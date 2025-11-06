# users_page.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def users_page():
    st.header("🔐 Gestion Utilisateur")

    # Si connecté
    if st.session_state.auth:
        resp = requests.get(f"{API_URL}/users/me", auth=st.session_state.auth)

        if resp.status_code == 200:
            user = resp.json()
            # Stockage des infos user dans la session pour accès par d'autres pages (Statistiques)
            st.session_state.user = user

            st.success(f"Connecté : {user['prenom']} {user['nom']}")
            st.write(f"@{user['username']}")

            st.write(f"👥 Followers : **{user['followers_count']}**")
            st.write(f"➡️ Suivis : **{user['followed_count']}**")

            # --- Suggestions d'utilisateurs à suivre ---
            st.subheader("🔥 Suggestions d'amis")

            suggestions_resp = requests.get(f"{API_URL}/users/suggestions", auth=st.session_state.auth)

            if suggestions_resp.status_code == 200:
                suggestions = suggestions_resp.json()

                for s in suggestions:
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**{s['prenom']} {s['nom']}** (@{s['username']})")

                    with col2:
                        if st.button("Suivre", key=f"follow_{s['id_user']}"):
                            follow = requests.post(
                                f"{API_URL}/users/{s['id_user']}/follow",
                                auth=st.session_state.auth
                            )
                            if follow.status_code == 200:
                                st.success(f"✅ Vous suivez maintenant {s['prenom']} !")
                                st.rerun()
                            else:
                                st.error(follow.json().get("detail", "Erreur"))
            else:
                st.write("Aucune suggestion pour le moment 😢.")

            # Bouton déconnexion
            if st.button("Se déconnecter"):
                st.session_state.auth = None
                st.session_state.user = None
                st.rerun()
            return

        else:
            st.error("Erreur d'authentification")
            st.session_state.auth = None
            st.session_state.user = None
            return

    # -------------------------
    # FORMULAIRE CONNEXION/CRÉATION
    # -------------------------
    action = st.radio("Action", ["Se connecter", "Créer un compte"])

    if action == "Se connecter":
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Connexion"):
            resp = requests.get(f"{API_URL}/users/me", auth=(username, password))
            if resp.status_code == 200:
                user_data = resp.json()
                st.session_state.auth = (username, password)
                # Stockage des infos user après la connexion
                st.session_state.user = user_data 
                st.success("Connexion réussie ✅")
                st.rerun()
            else:
                st.error(resp.json().get("detail", "Identifiants incorrects"))

    else:  # Créer un compte
        prenom = st.text_input("Prénom")
        nom = st.text_input("Nom")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Créer mon compte"):
            data = {"prenom": prenom, "nom": nom, "username": username, "password": password}
            resp = requests.post(f"{API_URL}/users/", data=data)
            if resp.status_code == 200:
                st.success("Compte créé ✅ Vous pouvez vous connecter.")
            else:
                st.error(resp.json().get("detail", "Erreur"))