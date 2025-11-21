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

    id_activite = st.text_input(
        "🔗 ID d'activité (optionnel)", 
        value="", 
        placeholder="Si renseigné, utilise le GPX de l'activité",
        help="Laissez vide pour créer un parcours basé sur les adresses"
    )

    if id_activite.strip() == "":
        id_activite = None
    else:
        try:
            id_activite = int(id_activite)
        except ValueError:
            st.error("⚠️ L'ID d'activité doit être un nombre")
            id_activite = None

    col_btn1, col_btn2 = st.columns([1, 3])
    
    with col_btn1:
        if st.button("✅ Créer le parcours", type="primary", use_container_width=True):
            # Validation
            if not id_activite and (not depart or not arrivee):
                st.error("⚠️ Veuillez renseigner soit un ID d'activité, soit les adresses de départ et d'arrivée")
            else:
                try:
                    with st.spinner("🔄 Création du parcours en cours..."):
                        payload = {
                            "depart": depart,
                            "arrivee": arrivee,
                            "id_user": user_id,
                            "id_activite": id_activite
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
                                    st.info("🗺️ Visualisation du parcours créé")
                                    components.html(html_content, height=600, scrolling=True)
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
    # SECTION 3 — PRÉVISUALISER UN FICHIER GPX
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
                    components.html(html_content, height=600, scrolling=True)
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
 