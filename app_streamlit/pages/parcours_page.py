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
    # ✔ SECTION 2 — VISUALISER UN PARCOURS
    # ==================================================

    st.subheader("🔍 Visualiser un parcours")

    # Demander l'ID du parcours à l'utilisateur
    parcours_id = st.number_input("Entrez l'ID du parcours à visualiser :", min_value=1, step=1)

    # Bouton pour visualiser la carte
    if st.button("Visualiser la carte HTML"):
        if parcours_id:
            try:
                # Envoie une requête à l'API pour générer la carte
                response = requests.get(f"{API_URL}/parcours/{parcours_id}/visualiser")
                response.raise_for_status()

                # Récupère le contenu HTML directement
                html_content = response.json().get("html_content")
                
                if html_content:
                    st.success("Carte générée ✔")
                    
                    # Affiche la carte directement dans Streamlit
                    components.html(html_content, height=600, scrolling=True)
                else:
                    st.error("Le contenu HTML n'a pas pu être récupéré.")
                    
            except requests.exceptions.HTTPError as e:
                st.error(f"Erreur HTTP : {e.response.status_code} - {e.response.text}")
            except Exception as e:
                st.error(f"Erreur lors de la visualisation du parcours : {e}")
        else:
            st.error("Veuillez entrer un ID valide pour le parcours.")

    # ==================================================
    # ✔ SECTION 3 — COORDONNÉES DU PARCOURS
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
