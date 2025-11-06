import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

def activites_page():
    st.header("🏃 Mes Activités")

    if not st.session_state.auth:
        st.warning("Veuillez vous connecter d'abord.")
        return

    # Afficher la liste
    resp = requests.get(f"{API_URL}/activites/", auth=st.session_state.auth)
    if resp.status_code == 200:
        activites = resp.json()
        for act in activites:
            st.write(f"{act.get('titre')} - {act.get('type_sport')} - {act.get('distance')} km")
    else:
        st.error("Impossible de récupérer les activités")

    # Formulaire création activité
    st.subheader("➕ Ajouter une activité")
    titre = st.text_input("Titre")
    type_sport = st.text_input("Sport")
    distance = st.number_input("Distance (km)", min_value=0.0)
    duree = st.text_input("Durée (HH:MM:SS)")
    date_activite = st.date_input("Date", datetime.today())

    if st.button("Enregistrer"):
        data = {
            "titre": titre,
            "type_sport": type_sport,
            "distance": distance,
            "duree": duree,
            "date_activite": str(date_activite),
            "id_parcours": 1,
            "trace": "",
            "description": ""
        }
        resp = requests.post(f"{API_URL}/activites/", data=data, auth=st.session_state.auth)
        if resp.status_code == 200:
            st.success("Activité enregistrée ✅")
        else:
            st.error(resp.json().get("detail", "Erreur"))
