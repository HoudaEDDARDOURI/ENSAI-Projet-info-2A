# app_streamlit.py
import streamlit as st
import requests
import gpxpy
from datetime import datetime
from typing import Tuple

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

# ---------- page connexion ----------
def login_page():
    st.header("🔑 Connexion")
    
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        try:
            # Appel API /login ou /users/me selon ton backend
            resp = requests.get(f"{API_URL}/users/me", auth=(username, password), timeout=10)
            if resp.status_code == 200:
                user_data = resp.json()
                st.session_state.user_id = user_data["id_user"]
                st.session_state.auth = (username, password)
                st.success(f"Connecté en tant que {user_data['nom']}")
                st.experimental_rerun()  # recharge la page après connexion
            else:
                st.error("Identifiants incorrects")
        except Exception as e:
            st.error(f"Erreur réseau: {e}")

# ---------- page activités ----------
def activites_page():
    st.header("🏃 Mes Activités")

    # ---------- Initialisation session ----------
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "auth" not in st.session_state:
        st.session_state.auth = None
    if "modif_id" not in st.session_state:
        st.session_state.modif_id = None
    if "modif_data" not in st.session_state:
        st.session_state.modif_data = {}

    # Auth check
    if not st.session_state.user_id or not st.session_state.auth:
        st.warning("Veuillez vous connecter d'abord.")
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
        st.error(f"Erreur connexion API: {e}")
        activites = []

    # --- List activities ---
    st.subheader("📋 Liste des activités")
    if not activites:
        st.info("Aucune activité trouvée.")
    else:
        for act in activites:
            act_id = act.get("id_activite")
            title = act.get("titre", "Sans titre")
            t_sport = act.get("type_sport", "N/A")
            dist = act.get("distance", 0.0)

            with st.container():
                st.markdown(f"**{title}** — {t_sport.capitalize()} — {dist} km")
                col1, col2 = st.columns([1, 1])

                # Modifier
                if col1.button("✏️ Modifier", key=f"mod_{act_id}"):
                    st.session_state.modif_id = act_id
                    st.session_state.modif_data = act

                # Supprimer
                if col2.button("🗑️ Supprimer", key=f"del_{act_id}"):
                    try:
                        del_resp = requests.delete(
                            f"{API_URL}/activites/{act_id}",
                            auth=st.session_state.auth,
                            timeout=10
                        )
                        if del_resp.status_code == 200:
                            st.success("✅ Activité supprimée")
                            st.rerun()
                        else:
                            msg = del_resp.json().get("detail", del_resp.text)
                            st.error(f"Erreur suppression: {msg}")
                    except Exception as e:
                        st.error(f"Erreur suppression: {e}")

    st.markdown("---")
    st.subheader("➕ Ajouter / Modifier une activité")

    # --- Prefill if modifying ---
    modif_data = st.session_state.get("modif_data") or {}
    if st.session_state.get("modif_id"):
        st.info("✏️ Mode modification")
        titre_default = modif_data.get("titre", "")
        type_sport_default = (modif_data.get("type_sport") or "Course").capitalize()
        date_default = datetime.fromisoformat(modif_data.get("date")).date() if modif_data.get("date") else datetime.today().date()
        distance_default = float(modif_data.get("distance", 0.0))
        duree_default = modif_data.get("duree", "")
    else:
        titre_default = ""
        type_sport_default = "Course"
        date_default = datetime.today().date()
        distance_default = 0.0
        duree_default = ""

    titre = st.text_input("Titre", value=titre_default)
    type_sport_list = ["Course", "Natation", "Cyclisme"]
    type_sport = st.selectbox(
        "Type de sport",
        type_sport_list,
        index=type_sport_list.index(type_sport_default) if type_sport_default in type_sport_list else 0
    )
    fichier_gpx = st.file_uploader("Télécharger fichier GPX (optionnel)", type=["gpx"])

    # Distance calculée ou manuelle
    if fichier_gpx:
        distance, duree = extraire_info_gpx(fichier_gpx)
        st.info(f"Distance calculée: {distance} km • Durée: {duree or 'N/A'}")
    else:
        distance = st.number_input("Distance (km) — si pas de GPX", min_value=0.0, value=distance_default)
        duree = duree_default

    date_activite = st.date_input("Date", value=date_default)

    # --- Save ---
    if st.button("✅ Enregistrer"):
        payload = {
            "titre": titre,
            "type_sport": type_sport.lower(),
            "distance": distance,
            "date": str(date_activite),
            "trace": fichier_gpx.name if fichier_gpx else modif_data.get("trace", ""),
            "description": modif_data.get("description", "") if modif_data else "",
            "duree": duree,
            "id_user": st.session_state.user_id
        }

        try:
            if st.session_state.get("modif_id"):
                # Modification
                act_id = st.session_state["modif_id"]
                payload["id_activite"] = act_id
                put_resp = requests.put(f"{API_URL}/activites/{act_id}", json=payload, auth=st.session_state.auth, timeout=10)
                if put_resp.status_code == 200:
                    st.success("✅ Activité modifiée")
                    st.session_state.modif_id = None
                    st.session_state.modif_data = {}
                    st.rerun()
                else:
                    st.error(f"Erreur modification: {put_resp.json().get('detail', put_resp.text)}")
            else:
                # Création
                post_resp = requests.post(f"{API_URL}/activites/", json=payload, auth=st.session_state.auth, timeout=10)
                if post_resp.status_code == 200:
                    st.success("✅ Activité enregistrée")
                    st.rerun()
                else:
                    st.error(f"Erreur création: {post_resp.json().get('detail', post_resp.text)}")
        except Exception as e:
            st.error(f"Erreur réseau: {e}")

# ---------- MAIN ----------
def main():
    if "user_id" not in st.session_state or not st.session_state.user_id:
        login_page()
    else:
        activites_page()

if __name__ == "__main__":
    main()
