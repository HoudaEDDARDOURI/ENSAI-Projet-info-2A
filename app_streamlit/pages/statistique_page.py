import streamlit as st
import requests
from datetime import date, timedelta, datetime

API_URL = "http://127.0.0.1:8000"

def statistiques_page():
    st.header("📊 Mes Statistiques")

    if not st.session_state.get('auth'):
        st.warning("Veuillez vous connecter d'abord.")
        return

    user_info = st.session_state.get('user')
    if not user_info or 'id' not in user_info:
        st.error("Impossible de récupérer les informations utilisateur.")
        return

    user_id = user_info['id']

    # Choix de la date
    date_reference = st.date_input(
        "Sélectionnez une date dans la semaine que vous souhaitez analyser :",
        value=date.today(),
        max_value=date.today(),
        key="stats_date_picker"
    )

    # Récupération des statistiques
    try:
        endpoint = f"{API_URL}/statistiques/{user_id}"
        params = {"reference_date": date_reference.isoformat()}
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        stats_data = response.json()

        stats = stats_data.get("Statistiques", {})
        periode = stats_data.get("Période", [date_reference.isoformat(), (date_reference + timedelta(days=6)).isoformat()])
        debut_semaine = datetime.fromisoformat(periode[0]).strftime("%d/%m/%Y")
        fin_semaine = datetime.fromisoformat(periode[1]).strftime("%d/%m/%Y")
        st.info(f"Période analysée : **Du {debut_semaine} au {fin_semaine}**")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Activités réalisées", stats.get("Nombre d'activités", 0))
        with col2:
            st.metric("Temps total d'activité", stats.get("Temps total d'activité", "00h 00min 00s"))
        with col3:
            distance = stats.get("Distance totale en kilomètres", 0)
            st.metric("Distance totale", f"{distance:,.2f} km")

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API : {e}")

    # Prédiction

    st.markdown("---")
    st.subheader("🔮 Prédiction d'Entraînement")

    # Choix du sport pour la prédiction
    sports = ['Course', 'Natation', 'Cyclisme']
    sport_choisi = st.selectbox(
        "Pour quel sport souhaitez-vous une recommandation de distance ?",
        sports
    )

    if st.button(f"Calculer la distance pour la {sport_choisi}"):
        try:
            # URL d'appel
            endpoint_pred = f"{API_URL}/statistiques/prediction/{user_id}"
            params_pred = {
                "type_sport": sport_choisi.lower()
            }

            response_pred = requests.get(endpoint_pred, params=params_pred)
            response_pred.raise_for_status()

            prediction_value = response_pred.json().get("distance_recommandee") 
            # Changement de nom de variable pour clarté

            # Affichage résultat
            unite = "m" if sport_choisi == "Natation" else "km"

            if sport_choisi == "Natation":
                # Si la valeur est en mètres (1100), on affiche sans décimale.
                distance_affichage = f"{prediction_value:,.0f}"
            else:
                # Pour les KM, on garde une décimale.
                distance_affichage = f"{prediction_value:,.1f}"

            st.success(
                f"🎉 Distance recommandée pour votre prochaine séance de **{sport_choisi}** : **{distance_affichage} {unite}**"
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors du calcul de la prédiction via l'API : {e}")
        except Exception as e:
            st.error(f"Erreur lors du traitement de la prédiction : {e}")
