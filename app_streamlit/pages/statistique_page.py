import streamlit as st
import requests
from datetime import datetime, date, timedelta

API_URL = "http://127.0.0.1:8000"


def statistiques_page():
    st.header("📊 Mes Statistiques")

    if not st.session_state.get('auth'):
        st.warning("Veuillez vous connecter d'abord.")
        return

    # Infos user disponibles
    user_info = st.session_state.get('user')
    if not user_info or 'id_user' not in user_info:
        st.error("Impossible de récupérer les informations utilisateur.")
        return

    user_id = user_info['id_user']

    # Sélection de Période

    st.subheader("🗓️ Choisir la semaine")

    # Date de référence
    date_reference = st.date_input(
        "Sélectionnez une date dans la semaine que vous souhaitez analyser :",
        value=date.today(),
        max_value=date.today(),
        key="stats_date_picker"
    )

    date_str = date_reference.isoformat()

    # Affichage des Statistiques

    st.subheader("📈 Statistiques Hebdomadaires")

    # Récupération des statistiques
    try:
        # URL d'appel
        endpoint = f"{API_URL}/stats/hebdomadaires"
        params = {
            "user_id": user_id,
            "date_reference": date_str
        }

        # Récupération des données
        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        stats_data = response.json()

        # Affichage des données

        stats = stats_data.get("Statistiques", {})
        periode = stats_data.get("Période", (date_reference, date_reference + datetime.timedelta(days=6)))

        # Mise en forme de la période (le tuple de dates est converti en chaîne)
        debut_semaine = datetime.fromisoformat(periode[0]).strftime("%d/%m/%Y")
        fin_semaine = datetime.fromisoformat(periode[1]).strftime("%d/%m/%Y")
        st.info(f"Période analysée : **Du {debut_semaine} au {fin_semaine}**")

        # Utilisation de colonnes
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Activités réalisées",
                value=stats.get("Nombre d'activités", 0)
            )

        with col2:
            temps_minutes = stats.get("Temps total d'activité en minutes", 0)
            # Conversion minutes en HH:MM
            heures = int(temps_minutes // 60)
            minutes = int(temps_minutes % 60)
            temps_formatte = f"{heures}h {minutes}min"
            st.metric(
                label="Temps total d'activité",
                value=temps_formatte
            )

        with col3:
            distance = stats.get("Distance totale en kilomètres", 0)
            st.metric(
                label="Distance totale",
                value=f"{distance:,.2f} km"
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la communication avec l'API : {e}")
        st.warning("Assurez-vous que votre serveur API est bien lancé.")
    except Exception as e:
        st.error(f"Une erreur inattendue est survenue : {e}")

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
            endpoint_pred = f"{API_URL}/stats/prediction"
            params_pred = {
                "user_id": user_id,
                "type_sport": sport_choisi.lower()
            }

            response_pred = requests.get(endpoint_pred, params=params_pred)
            response_pred.raise_for_status()

            prediction_km = response_pred.json().get("distance_recommandee")

            # Affichage résultat
            unite = "m" if sport_choisi == "Natation" else "km"
            distance_affichage = f"{prediction_km:,.1f}" if sport_choisi == "Natation" else f"{prediction_km:,.1f}"

            st.success(
                f"🎉 Distance recommandée pour votre prochaine séance de **{sport_choisi}** : **{distance_affichage} {unite}**"
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors du calcul de la prédiction via l'API : {e}")
        except Exception as e:
            st.error(f"Erreur lors du traitement de la prédiction : {e}")
