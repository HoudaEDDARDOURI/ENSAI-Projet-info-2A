import streamlit as st
import requests
import streamlit.components.v1 as components

API_URL = "http://127.0.0.1:8000"

def parcours_page():
    st.header("🗺️ Gestion des Parcours")

    # Vérification login
    if not st.session_state.get("auth"):
        st.warning("⚠️ Veuillez vous connecter d'abord.")
        return

    user = st.session_state.get("user")
    user_id = user.get("id")

    st.markdown("---")

    # ==================================================
    # SECTION 1 — CRÉER UN PARCOURS
    # ==================================================

    st.subheader("➕ Créer un nouveau parcours")

    col1, col2 = st.columns(2)

    with col1:
        depart = st.text_input("📍 Adresse de départ", placeholder="Ex: Paris, France")
    with col2:
        arrivee = st.text_input("🏁 Adresse d'arrivée", placeholder="Ex: Lyon, France")

    if st.button("✅ Créer le parcours", type="primary", use_container_width=True):
        # Validation
        if not depart or not arrivee:
            st.error("⚠️ Veuillez renseigner les adresses de départ et d'arrivée")
        else:
            try:
                with st.spinner("🔄 Création du parcours en cours..."):
                    payload = {
                        "depart": depart,
                        "arrivee": arrivee,
                        "id_user": user_id
                    }

                    # Création du parcours
                    response = requests.post(f"{API_URL}/parcours/", params=payload)
                    response.raise_for_status()
                    result = response.json()
                    parcours_id_created = result.get("id_parcours")

                    st.success("🎉 Parcours créé avec succès !")

                    # Visualisation automatique
                    if parcours_id_created is not None:
                        with st.spinner("🗺️ Génération de la carte..."):
                            vis_response = requests.get(
                                f"{API_URL}/parcours/{parcours_id_created}/visualiser",
                                timeout=15
                            )
                            vis_response.raise_for_status()
                            html_content = vis_response.json().get("html_content")

                            if html_content:
                                st.markdown("---")
                                st.info("🗺️ Visualisation du parcours créé")
                                # Affichage de la carte avec hauteur augmentée
                                components.html(html_content, height=650, scrolling=False)
                            else:
                                st.warning("⚠️ Le parcours a été créé, mais le contenu HTML est vide.")
                    else:
                        st.warning("⚠️ Le parcours a été créé, mais l'API n'a pas renvoyé d'ID.")

            except requests.exceptions.HTTPError as http_err:
                st.error(f"❌ Erreur HTTP : {http_err.response.status_code}")
                try:
                    error_detail = http_err.response.json()
                    st.error(f"Détails : {error_detail.get('detail', 'Erreur inconnue')}")
                except:
                    st.error(f"Réponse : {http_err.response.text}")

            except Exception as e:
                st.error(f"❌ Erreur : {e}")

    st.markdown("---")

    # ==================================================
    # SECTION 2 — PRÉVISUALISER UN FICHIER GPX
    # ==================================================

    st.subheader("📂 Prévisualiser un fichier GPX")

    gpx_file = st.file_uploader(
        "Téléchargez un fichier GPX",
        type=["gpx"],
        help="Visualisez rapidement un fichier GPX sans créer de parcours"
    )

    if gpx_file is not None:
        try:
            gpx_content = gpx_file.read().decode('utf-8')
            
            with st.spinner("🗺️ Génération de la carte..."):
                viz_resp = requests.post(
                    f"{API_URL}/parcours/visualiser-gpx",
                    json={"gpx_content": gpx_content},
                    timeout=15
                )
                viz_resp.raise_for_status()
                html_content = viz_resp.json().get("html_content")

                if html_content:
                    st.success("✅ Fichier GPX chargé avec succès")
                    st.markdown("---")
                    # Affichage de la carte GPX
                    components.html(html_content, height=650, scrolling=False)
                else:
                    st.warning("⚠️ Contenu HTML vide")

        except requests.exceptions.HTTPError as http_err:
            st.error(f"❌ Erreur HTTP : {http_err.response.status_code}")
            try:
                error_detail = http_err.response.json()
                st.error(f"Détails : {error_detail.get('detail', 'Erreur inconnue')}")
            except:
                st.error(f"Réponse : {http_err.response.text}")

        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture du fichier : {e}")

    st.markdown("---")