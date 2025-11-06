# users_page.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def users_page():
    st.header("🔐 Gestion Utilisateur")

    # Si connecté
    if st.session_state.auth:
        try:
            resp = requests.get(f"{API_URL}/users/me", auth=st.session_state.auth)
            if resp.status_code == 200:
                user = resp.json()
                st.success(f"Connecté : {user['prenom']} {user['nom']}")
                st.write(f"@{user['username']}")

                # Ici tu peux appeler tes endpoints followers / followed
                followers_resp = requests.get(f"{API_URL}/users/{user['id']}/followers", auth=st.session_state.auth)
                followed_resp = requests.get(f"{API_URL}/users/{user['id']}/followed", auth=st.session_state.auth)

                try:
                    n_followers = len(followers_resp.json()) if followers_resp.status_code == 200 else 0
                    n_followed = len(followed_resp.json()) if followed_resp.status_code == 200 else 0
                except Exception:
                    n_followers = n_followed = 0

                st.write(f"Nombre de followers : {n_followers}")
                st.write(f"Nombre de followed : {n_followed}")

                if st.button("Se déconnecter"):
                    st.session_state.auth = None
                    st.rerun()
                return
            else:
                # Sécuriser le JSON decode
                try:
                    error_detail = resp.json().get("detail", "Erreur")
                except Exception:
                    error_detail = resp.text or "Erreur inconnue"
                st.error(f"Erreur connexion API : {error_detail}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur connexion API : {e}")
        return

    # Formulaire connexion / création
    action = st.radio("Action", ["Se connecter", "Créer un compte"])

    if action == "Se connecter":
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Connexion"):
            try:
                resp = requests.get(f"{API_URL}/users/me", auth=(username, password))
                if resp.status_code == 200:
                    st.session_state.auth = (username, password)
                    st.success("Connexion réussie ✅")
                    st.rerun()
                else:
                    try:
                        error_detail = resp.json().get("detail", "Erreur")
                    except Exception:
                        error_detail = resp.text or "Erreur inconnue"
                    st.error(error_detail)
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur connexion API : {e}")

    else:  # Créer un compte
        prenom = st.text_input("Prénom")
        nom = st.text_input("Nom")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")

        if st.button("Créer mon compte"):
            try:
                data = {"prenom": prenom, "nom": nom, "username": username, "password": password}
                resp = requests.post(f"{API_URL}/users/", data=data)
                if resp.status_code == 200:
                    st.success("Compte créé ✅ Vous pouvez vous connecter.")
                else:
                    try:
                        error_detail = resp.json().get("detail", "Erreur")
                    except Exception:
                        error_detail = resp.text or "Erreur inconnue"
                    st.error(error_detail)
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur connexion API : {e}")
