# activite_page.py
import streamlit as st
import requests
import gpxpy
from datetime import datetime
from typing import Tuple

API_URL = "http://127.0.0.1:8000"

# ---------- helpers GPX ----------
def extraire_info_gpx(fichier_gpx) -> Tuple[float, str]:
    """
    Prend un fichier-like GPX (ce que renvoie st.file_uploader)
    Retourne (distance_km, duree_str) où duree_str est "HH:MM:SS"
    """
    try:
        gpx = gpxpy.parse(fichier_gpx)
    except Exception as e:
        st.error(f"Impossible de parser le GPX: {e}")
        return 0.0, ""

    distance_m = gpx.length_3d() if gpx else 0.0
    duree_s = gpx.get_duration() or 0
    try:
        duree_hms = str(datetime.utcfromtimestamp(int(duree_s)).time())
    except Exception:
        duree_hms = ""
    distance_km = round(distance_m / 1000, 2)
    return distance_km, duree_hms

# ---------- page ----------
def activites_page():
    st.header("🏃 Mes Activités")

    # auth required
    if "auth" not in st.session_state or not st.session_state.auth:
        st.warning("Veuillez vous connecter d'abord.")
        return

    # init session keys
    if "modif_id" not in st.session_state:
        st.session_state.modif_id = None
    if "modif_data" not in st.session_state:
        st.session_state.modif_data = {}

    # --- GET activities from API ---
    try:
        resp = requests.get(f"{API_URL}/activites/", auth=st.session_state.auth, timeout=10)
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API: {e}")
        return

    if resp.status_code == 200:
        activites = resp.json() or []
    else:
        st.error(f"Impossible de récupérer les activités ({resp.status_code})")
        activites = []

    # --- list activities ---
    st.subheader("📋 Liste des activités")
    if not activites:
        st.info("Aucune activité trouvée.")
    else:
        for act in activites:
            title = act.get("titre", "Sans titre")
            t_sport = act.get("type_sport", "N/A")
            dist = act.get("distance", 0.0)
            act_id = act.get("id")  # backend doit renvoyer 'id'

            with st.container():
                st.markdown(f"**{title}** — {t_sport.capitalize()} — {dist} km")

                col1, col2 = st.columns([1, 1])
                if col1.button("✏️ Modifier", key=f"mod_{act_id}"):
                    st.session_state.modif_id = act_id
                    st.session_state.modif_data = act

                if col2.button("🗑️ Supprimer", key=f"del_{act_id}"):
                    try:
                        del_resp = requests.delete(f"{API_URL}/activites/{act_id}", auth=st.session_state.auth, timeout=10)
                        if del_resp.status_code == 200:
                            st.success("✅ Activité supprimée")
                            st.session_state.modif_id = None
                            st.session_state.modif_data = {}
                            st.experimental_rerun()
                        else:
                            msg = del_resp.json().get("detail", del_resp.text)
                            st.error(f"Erreur lors de la suppression: {msg}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Erreur suppression: {e}")

    st.markdown("---")
    st.subheader("➕ Ajouter / Modifier une activité")

    # --- Prefill if modifying ---
    modif_data = st.session_state.get("modif_data") or {}
    if st.session_state.get("modif_id"):
        st.info("✏️ Mode modification")
        titre_default = modif_data.get("titre", "")
        type_sport_default = (modif_data.get("type_sport") or "Course").capitalize()
        date_default = datetime.fromisoformat(modif_data.get("date_activite")).date() if modif_data.get("date_activite") else datetime.today().date()
        distance_default = float(modif_data.get("distance", 0.0))
    else:
        titre_default = ""
        type_sport_default = "Course"
        date_default = datetime.today().date()
        distance_default = 0.0

    titre = st.text_input("Titre", value=titre_default)

    type_sport_list = ["Course", "Natation", "Cyclisme"]
    idx = type_sport_list.index(type_sport_default) if type_sport_default in type_sport_list else 0
    type_sport = st.selectbox("Type de sport", type_sport_list, index=idx)

    fichier_gpx = st.file_uploader("Télécharger fichier GPX (optionnel)", type=["gpx"])

    # distance field
    if fichier_gpx is not None:
        distance_calc, duree_calc = extraire_info_gpx(fichier_gpx)
        distance = distance_calc
        duree = duree_calc
        st.info(f"Distance calculée depuis GPX: {distance} km • Durée: {duree or 'N/A'}")
    else:
        distance = st.number_input("Distance (km) — si pas de GPX", min_value=0.0, value=distance_default)
        duree = modif_data.get("duree", "") if st.session_state.get("modif_id") else ""

    date_activite = st.date_input("Date", value=date_default)

    # --- Save (create or update) ---
    if st.button("✅ Enregistrer"):
        payload = {
            "titre": titre,
            "type_sport": type_sport.lower(),
            "distance": distance,
            "date_activite": str(date_activite),
            "id_parcours": 1,
            "trace": fichier_gpx.name if (fichier_gpx is not None and hasattr(fichier_gpx, "name")) else (modif_data.get("trace", "") if modif_data else ""),
            "description": modif_data.get("description", "") if modif_data else "",
            "duree": duree
        }

        # modification
        if st.session_state.get("modif_id"):
            act_id = st.session_state["modif_id"]
            try:
                put_resp = requests.put(f"{API_URL}/activites/{act_id}", data=payload, auth=st.session_state.auth, timeout=10)
                if put_resp.status_code == 200:
                    st.success("✅ Activité modifiée")
                    st.session_state.modif_id = None
                    st.session_state.modif_data = {}
                    st.experimental_rerun()
                else:
                    msg = put_resp.json().get("detail", put_resp.text)
                    st.error(f"Erreur modification: {msg}")
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur modification: {e}")
            return

        # création
        try:
            post_resp = requests.post(f"{API_URL}/activites/", data=payload, auth=st.session_state.auth, timeout=10)
            if post_resp.status_code == 200:
                st.success("✅ Activité enregistrée")
                st.experimental_rerun()
            else:
                msg = post_resp.json().get("detail", post_resp.text)
                st.error(f"Erreur création: {msg}")
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur création: {e}")
