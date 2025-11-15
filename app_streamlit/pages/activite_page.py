import streamlit as st
import requests
import gpxpy
import pandas as pd
from datetime import datetime
from typing import Tuple
import os
import streamlit.components.v1 as components

API_URL = "http://127.0.0.1:8000"

# ---------- helpers GPX ----------
def extraire_info_gpx(fichier_gpx) -> Tuple[float, str]:
    """Retourne (distance_km, duree_str) depuis un fichier GPX"""
    try:
        gpx = gpxpy.parse(fichier_gpx)
        distance_km = round(gpx.length_3d() / 1000, 2)
        duree_s = gpx.get_duration() or 0
        duree_hms = str(datetime.utcfromtimestamp(int(duree_s)).time()) if duree_s else ""
        return distance_km, duree_hms
    except Exception as e:
        st.error(f"Impossible de parser le GPX: {e}")
        return 0.0, ""

def get_sport_emoji(type_sport: str) -> str:
    """Retourne un emoji selon le type de sport"""
    emojis = {"course": "🏃", "natation": "🏊", "cyclisme": "🚴"}
    return emojis.get(type_sport.lower(), "🏃")

# ---------- page ----------
def activites_page():
    st.title("🏃 Mes Activités Sportives")

    # ---------- Initialisation session ----------
    if "user_id" not in st.session_state: st.session_state.user_id = None
    if "auth" not in st.session_state: st.session_state.auth = None
    if "modif_id" not in st.session_state: st.session_state.modif_id = None
    if "modif_data" not in st.session_state: st.session_state.modif_data = {}

    # Auth check
    if not st.session_state.user_id or not st.session_state.auth:
        st.warning("⚠️ Veuillez vous connecter d'abord.")
        st.stop()

    # --- GET activities from API ---
    try:
        resp = requests.get(
            f"{API_URL}/activites/",
            params={"id_user": st.session_state.user_id},
            auth=st.session_state.auth,
            timeout=10
        )
        resp.raise_for_status()
        activites = resp.json() or []
    except Exception as e:
        st.error(f"❌ Erreur connexion API: {e}")
        activites = []

    # --- Statistiques globales ---
    if activites:
        col1, col2, col3 = st.columns(3)
        total_dist = sum(act.get("distance", 0) for act in activites)
        nb_course = sum(1 for act in activites if act.get("type_sport") == "course")
        nb_natation = sum(1 for act in activites if act.get("type_sport") == "natation")
        nb_cyclisme = sum(1 for act in activites if act.get("type_sport") == "cyclisme")
        with col1: st.metric("Distance totale", f"{total_dist:.1f} km")
        with col2: st.metric("Nombre d'activités", len(activites))
        with col3: st.metric("Sports pratiqués", f"🏃 {nb_course} | 🏊 {nb_natation} | 🚴 {nb_cyclisme}")
        st.markdown("---")

    # --- Tableau des activités ---
    st.subheader("📋 Liste des activités")
    if not activites:
        st.info("ℹ️ Aucune activité trouvée. Commencez par en ajouter une ci-dessous !")
    else:
        activites_triees = sorted(activites, key=lambda x: x.get("date", ""), reverse=True)
        data_tableau = []
        for act in activites_triees:
            act_id = act.get("id_activite")
            title = act.get("titre", "Sans titre")
            t_sport = act.get("type_sport", "N/A")
            dist = act.get("distance", 0.0)
            date_act = act.get("date", "")
            duree = act.get("duree", "N/A")
            try: date_formatted = datetime.fromisoformat(date_act).strftime("%d/%m/%Y")
            except: date_formatted = date_act
            emoji = get_sport_emoji(t_sport)
            data_tableau.append({
                "ID": act_id,
                "Sport": f"{emoji} {t_sport.capitalize()}",
                "Titre": title,
                "Distance (km)": f"{dist:.2f}",
                "Durée": duree,
                "Date": date_formatted
            })
        df = pd.DataFrame(data_tableau)
        st.dataframe(df.drop('ID', axis=1), use_container_width=True, hide_index=True)

        # --- Actions ---
        st.markdown("### Actions")
        col1, col2, col3 = st.columns([1, 1, 2])

        # --- Modifier ---
        with col1:
            activite_a_modifier = st.selectbox(
                "Sélectionner une activité à modifier",
                options=[""] + [f"{act.get('titre')} - {act.get('date')}" for act in activites_triees],
                key="select_modif"
            )
            if activite_a_modifier and st.button("✏️ Modifier cette activité"):
                for act in activites_triees:
                    if f"{act.get('titre')} - {act.get('date')}" == activite_a_modifier:
                        st.session_state.modif_id = act.get("id_activite")
                        st.session_state.modif_data = act
                        st.rerun()

        # --- Supprimer ---
        with col2:
            activite_a_supprimer = st.selectbox(
                "Sélectionner une activité à supprimer",
                options=[""] + [f"{act.get('titre')} - {act.get('date')}" for act in activites_triees],
                key="select_suppr"
            )
            if activite_a_supprimer and st.button("🗑️ Supprimer cette activité", type="secondary"):
                for act in activites_triees:
                    if f"{act.get('titre')} - {act.get('date')}" == activite_a_supprimer:
                        act_id = act.get("id_activite")
                        try:
                            del_resp = requests.delete(f"{API_URL}/activites/{act_id}",
                                                       auth=st.session_state.auth, timeout=10)
                            if del_resp.status_code == 200:
                                st.success("✅ Activité supprimée")
                                st.rerun()
                            else:
                                msg = del_resp.json().get("detail", del_resp.text)
                                st.error(f"❌ Erreur suppression: {msg}")
                        except Exception as e:
                            st.error(f"❌ Erreur suppression: {e}")

        # --- Visualiser parcours directement depuis l'activité ---
        with col3:
            st.markdown("#### 🔍 Créer / Visualiser un parcours")
            for act in activites_triees:
                act_id = act.get("id_activite")
                titre = act.get("titre", "Sans titre")
                if st.button(f"🗺️ {titre}", key=f"parcours_{act_id}"):
                    try:
                        payload = {
                            "depart": "",
                            "arrivee": "",
                            "id_user": st.session_state.user_id,
                            "id_activite": act_id
                        }

                        # Création du parcours via l'API
                        response = requests.post(f"{API_URL}/parcours/", params=payload)
                        response.raise_for_status()
                        result = response.json()
                        parcours_id_created = result.get("id_parcours")

                        st.success(f"🎉 Parcours créé pour l'activité '{titre}' !")

                        # Visualisation
                        if parcours_id_created:
                            vis_response = requests.get(f"{API_URL}/parcours/{parcours_id_created}/visualiser")
                            vis_response.raise_for_status()
                            html_content = vis_response.json().get("html_content")

                            if html_content:
                                st.info("🗺️ Visualisation automatique du parcours")
                                components.html(html_content, height=600, scrolling=True)
                            else:
                                st.warning("Le parcours a été créé, mais le contenu HTML est vide.")
                        else:
                            st.warning("Le parcours a été créé, mais l'API n'a pas renvoyé d'ID.")

                    except requests.exceptions.HTTPError as http_err:
                        st.error(f"Erreur HTTP : {http_err.response.status_code} - {http_err.response.text}")
                    except Exception as e:
                        st.error(f"Erreur : {e}")

    st.markdown("---")

    # --- Formulaire ajout / modification ---
    if st.session_state.get("modif_id"):
        st.subheader("✏️ Modifier une activité")
        modif_data = st.session_state.get("modif_data") or {}
        titre_default = modif_data.get("titre", "")
        type_sport_default = (modif_data.get("type_sport") or "Course").capitalize()
        date_default = datetime.fromisoformat(modif_data.get("date")).date() if modif_data.get("date") else datetime.today().date()
        distance_default = float(modif_data.get("distance", 0.0))
        duree_default = modif_data.get("duree", "")
        if st.button("❌ Annuler la modification"):
            st.session_state.modif_id = None
            st.session_state.modif_data = {}
            st.rerun()
    else:
        st.subheader("➕ Ajouter une nouvelle activité")
        titre_default = ""
        type_sport_default = "Course"
        date_default = datetime.today().date()
        distance_default = 0.0
        duree_default = ""

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            titre = st.text_input("📝 Titre de l'activité", value=titre_default, placeholder="Ex: Footing matinal")
            type_sport_list = ["Course", "Natation", "Cyclisme"]
            type_sport = st.selectbox("🏅 Type de sport", type_sport_list,
                                      index=type_sport_list.index(type_sport_default) if type_sport_default in type_sport_list else 0)
            date_activite = st.date_input("📅 Date de l'activité", value=date_default)
        with col2:
            fichier_gpx = st.file_uploader("📍 Fichier GPX (optionnel)", type=["gpx"])
            if fichier_gpx:
                distance, duree = extraire_info_gpx(fichier_gpx)
                st.success(f"✅ GPX analysé: {distance} km • Durée: {duree or 'N/A'}")
            else:
                distance = st.number_input("📏 Distance (km)", min_value=0.0, value=distance_default, step=0.1)
                duree = st.text_input("⏱️ Durée (HH:MM:SS)", value=duree_default or "")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("✅ Enregistrer", type="primary", use_container_width=True):
            if not titre:
                st.error("⚠️ Veuillez saisir un titre")
            elif distance <= 0:
                st.error("⚠️ La distance doit être supérieure à 0")
            else:
                try:
                    # --- Upload GPX si présent ---
                    if fichier_gpx:
                        files = {"file": (fichier_gpx.name, fichier_gpx.getvalue())}
                        resp_upload = requests.post(f"{API_URL}/activites/upload_gpx/", files=files)
                        resp_upload.raise_for_status()
                        trace_path = resp_upload.json()["file_path"]
                    else:
                        trace_path = st.session_state.modif_data.get("trace", "") if st.session_state.modif_data else ""

                    # --- Payload pour création / modification activité ---
                    payload = {
                        "titre": titre,
                        "type_sport": type_sport.lower(),
                        "distance": distance,
                        "date": str(date_activite),
                        "trace": trace_path,
                        "description": st.session_state.modif_data.get("description", "") if st.session_state.modif_data else "",
                        "duree": duree,
                        "id_user": st.session_state.user_id
                    }

                    # --- Modification ---
                    if st.session_state.get("modif_id"):
                        act_id = st.session_state["modif_id"]
                        put_resp = requests.put(
                            f"{API_URL}/activites/{act_id}",
                            json=payload,
                            auth=st.session_state.auth,
                            timeout=10
                        )
                        put_resp.raise_for_status()
                        st.success("✅ Activité modifiée avec succès")
                        st.session_state.modif_id = None
                        st.session_state.modif_data = {}
                        st.rerun()
                    else:
                        # --- Création ---
                        post_resp = requests.post(
                            f"{API_URL}/activites/",
                            json=payload,
                            auth=st.session_state.auth,
                            timeout=10
                        )
                        post_resp.raise_for_status()
                        st.success("✅ Activité enregistrée avec succès")
                        st.rerun()

                except requests.exceptions.HTTPError as http_err:
                    st.error(f"Erreur HTTP : {http_err.response.status_code} - {http_err.response.text}")
                except Exception as e:
                    st.error(f"❌ Erreur réseau ou API: {e}")

    with col2:
        if st.button("🔄 Réinitialiser", use_container_width=True):
            st.session_state.modif_id = None
            st.session_state.modif_data = {}
            st.rerun()
