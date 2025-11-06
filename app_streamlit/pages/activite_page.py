import streamlit as st
import requests
from datetime import datetime
import gpxpy

API_URL = "http://127.0.0.1:8000"

def calculer_distance_gpx(fichier_gpx):
    """Calcule la distance totale en km à partir d’un fichier GPX"""
    gpx = gpxpy.parse(fichier_gpx)
    distance_totale = 0.0
    for track in gpx.tracks:
        for segment in track.segments:
            distance_totale += segment.length_3d()  # en mètres
    return round(distance_totale / 1000, 2)  # convertir en km

def activites_page():
    st.header("🏃 Mes Activités")

    if not st.session_state.auth:
        st.warning("Veuillez vous connecter d'abord.")
        return

    # Afficher la liste des activités
    resp = requests.get(f"{API_URL}/activites/", auth=st.session_state.auth)
    if resp.status_code == 200:
        activites = resp.json() or []
        for act in activites:
            st.write(f"{act.get('titre')} - {act.get('type_sport')} - {act.get('distance')} km")
    else:
        st.error("Impossible de récupérer les activités")

    st.subheader("➕ Ajouter une activité")

    titre = st.text_input("Titre")
    type_sport = st.selectbox("Type de sport", ["Course", "Natation", "Cyclisme"])
    fichier_gpx = st.file_uploader("Télécharger fichier GPX (optionnel)", type=["gpx"])
    date_activite = st.date_input("Date", datetime.today())

    distance = 0.0
    if fichier_gpx:
        distance = calculer_distance_gpx(fichier_gpx)

    if st.button("Enregistrer"):
        # Si l'utilisateur n'a pas uploadé de GPX, il doit saisir la distance manuellement
        if distance == 0.0:
            distance = st.number_input("Distance (km)", min_value=0.0)

        data = {
            "titre": titre,
            "type_sport": type_sport,
            "distance": distance,
            "date_activite": str(date_activite),
            "id_parcours": 1,
            "trace": "",  # éventuellement sauvegarder le GPX sur serveur
            "description": ""
        }
        resp = requests.post(f"{API_URL}/activites/", data=data, auth=st.session_state.auth)
        if resp.status_code == 200:
            st.success("Activité enregistrée ✅")
        else:
            st.error(resp.json().get("detail", "Erreur"))
