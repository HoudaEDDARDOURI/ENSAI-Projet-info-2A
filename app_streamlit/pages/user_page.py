# users_page.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def users_page():
    st.header("🔐 Gestion Utilisateur")

    if st.session_state.auth:
        # Profil
        resp = requests.get(f"{API_URL}/users/me", auth=st.session_state.auth)
        if resp.status_code == 200:
            user = resp.json()
            st.success(f"Connecté : {user['prenom']} {user['nom']}")
            st.write(f"@{user['username']}")
            if st.button("Se déconnecter"):
                st.session_state.auth = None
                st.rerun()
            return

    # Formulaire connexion / création
    action = st.radio("Action", ["Se connecter", "Créer un compte"])

    if action == "Se connecter":
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Connexion"):
            resp = requests.get(f"{API_URL}/users/me", auth=(username, password))
            if resp.status_code == 200:
                st.session_state.auth = (username, password)
                st.success("Connexion réussie ✅")
                st.rerun()
            else:
                st.error(resp.json().get("detail", "Erreur"))

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
