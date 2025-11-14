import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def parcours_page():
    st.header("🗺️ Gestion des Parcours")

    # Vérification login
    if not st.session_state.get("auth"):
        st.warning("Veuillez vous connecter d'abord.")
        return

    user = st.session_state.get("user")
    user_id = user.get("id")

    st.markdown("---")

    # ==================================================
    # ✔ SECTION 1 — CRÉER UN PARCOURS
    # ==================================================

    st.subheader("➕ Créer un nouveau parcours")

    col1, col2 = st.columns(2)

    with col1:
        depart = st.text_input("📍 Adresse de départ")
    with col2:
        arrivee = st.text_input("🏁 Adresse d'arrivée")

    id_activite = st.text_input(
        "ID d'activité associée (optionnel)", 
        value="", 
        placeholder="Laisser vide si géocodage"
    )

    if id_activite.strip() == "":
        id_activite = None
    else:
        id_activite = int(id_activite)

    if st.button("Créer le parcours"):
        try:
            payload = {
                "depart": depart,
                "arrivee": arrivee,
                "id_user": user_id,
                "id_activite": id_activite
            }

            response = requests.post(f"{API_URL}/parcours/", params=payload)
            response.raise_for_status()

            st.success("🎉 Parcours créé avec succès !")

        except Exception as e:
            st.error(f"Erreur : {e}")

    st.markdown("---")

    # ==================================================
    # ✔ SECTION 2 — LIRE / VISUALISER UN PARCOURS
    # ==================================================

    st.subheader("🔍 Rechercher un parcours")

    parcours_id = st.number_input("ID du parcours :", min_value=1, step=1)

    if st.button("Charger les informations"):
        try:
            response = requests.get(f"{API_URL}/parcours/{parcours_id}")
            response.raise_for_status()
            parcours = response.json()

            st.success("Parcours trouvé ✔")
            st.json(parcours)

        except Exception as e:
            st.error(f"Erreur : {e}")

    st.markdown("---")

    # ==================================================
    # ✔ SECTION 3 — VISUALISATION / TELECHARGEMENT
    # ==================================================

    st.subheader("🌍 Visualiser ou Télécharger le parcours")

    colA, colB = st.columns(2)

    with colA:
        if st.button("Visualiser la carte HTML"):
            try:
                response = requests.get(f"{API_URL}/parcours/{parcours_id}/visualiser")
                response.raise_for_status()
                file_path = response.json().get("fichier_html")

                st.success("Carte générée ✔")
                st.write(f"📄 Fichier : `{file_path}`")

                st.markdown(f"[👉 Ouvrir la carte]({file_path})", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erreur : {e}")

    with colB:
        if st.button("Télécharger le fichier"):
            try:
                response = requests.get(f"{API_URL}/parcours/{parcours_id}/telecharger")
                response.raise_for_status()
                file_path = response.json().get("fichier_telecharge")

                st.success("Téléchargement prêt ✔")
                st.write(f"📦 `{file_path}`")
                st.markdown(f"[⬇ Télécharger]({file_path})", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erreur : {e}")

    st.markdown("---")

    # ==================================================
    # ✔ SECTION 4 — COORDONNÉES DU PARCOURS
    # ==================================================

    st.subheader("📐 Coordonnées du parcours")

    if st.button("Afficher les coordonnées"):
        try:
            response = requests.get(f"{API_URL}/parcours/{parcours_id}/coordonnees")
            response.raise_for_status()
            coords = response.json().get("coordonnees")

            st.success("Coordonnées récupérées ✔")
            st.json(coords)

        except Exception as e:
            st.error(f"Erreur : {e}")
