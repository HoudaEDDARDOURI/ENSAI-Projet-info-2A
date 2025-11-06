import streamlit as st
import requests


# URL de l'API FastAPI
API_URL = "http://127.0.0.1:8000"

st.title("Sport Activities - Gestion Utilisateur")

# --- Session utilisateur ---
if "auth" not in st.session_state:
    st.session_state.auth = None  # stocke (username, password) après connexion

# --- Choix : se connecter ou créer un compte ---
action = st.sidebar.selectbox("Choisir une action", ["Se connecter", "Créer un compte"])

# --- Créer un compte ---
if action == "Créer un compte":
    st.header("Créer un nouveau compte")
    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Créer le compte"):
        if prenom and nom and username and password:
            payload = {
                "prenom": prenom,
                "nom": nom,
                "username": username,
                "password": password
            }
            response = requests.post(f"{API_URL}/users", data=payload)
            if response.status_code == 200:
                st.success(f"Compte créé avec succès pour {response.json()['username']}")
            else:
                st.error(f"Erreur: {response.json()['detail']}")
        else:
            st.warning("Veuillez remplir tous les champs.")

# --- Se connecter ---
elif action == "Se connecter":
    st.header("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username and password:
            response = requests.get(f"{API_URL}/users/me", auth=(username, password))

            if response.status_code == 200:
                st.success(f"Connecté en tant que {username}")
                st.session_state.auth = (username, password)

            else:
                try:
                    error_msg = response.json().get("detail", "Erreur inconnue")
                except:
                    error_msg = "Erreur serveur"
                st.error(error_msg)

        else:
            st.warning("Veuillez entrer vos identifiants.")



# --- Interface après connexion ---
if st.session_state.auth:
    auth = st.session_state.auth
    response = requests.get(f"{API_URL}/users/me", auth=auth)
    if response.status_code == 200:
        user = response.json()
        st.subheader("Vos informations")
        st.write(user)

        # Modifier
        st.subheader("Modifier vos informations")
        new_prenom = st.text_input("Prénom", value=user['prenom'])
        new_nom = st.text_input("Nom", value=user['nom'])
        new_username = st.text_input("Username", value=user['username'])
        new_password = st.text_input("Nouveau mot de passe (laisser vide pour ne pas changer)", type="password")

        if st.button("Modifier mon compte"):
            payload = {
                "prenom": new_prenom,
                "nom": new_nom,
                "username": new_username
            }
            if new_password:
                payload["mot_de_passe"] = new_password
            resp = requests.put(f"{API_URL}/users/me", data=payload, auth=auth)
            if resp.status_code == 200:
                st.success("Utilisateur modifié avec succès")
            else:
                st.error(f"Erreur: {resp.json()['detail']}")

        # Supprimer
        if st.button("Supprimer mon compte"):
            resp = requests.delete(f"{API_URL}/users/{user['id']}", auth=auth)
            if resp.status_code == 200:
                st.success("Compte supprimé")
                st.session_state.auth = None
            else:
                st.error(f"Erreur: {resp.json()['detail']}")
