import streamlit as st
import requests
import streamlit.components.v1 as components


API_URL = "http://127.0.0.1:8000"  # L'URL de ton API

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
        "ID d'activité", 
        value="", 
        placeholder="Laisser vide si adresse de départ et d'arrivée renseignées"
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

            # 📌 1. Création du parcours
            response = requests.post(f"{API_URL}/parcours/", params=payload)
            response.raise_for_status()

            result = response.json()

            # 📌 Récupération de l'ID renvoyé par l'API
            parcours_id_created = result.get("id_parcours")

            st.success("🎉 Parcours créé avec succès !")

            # 📌 2. Visualisation automatique
            if parcours_id_created is not None:
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

