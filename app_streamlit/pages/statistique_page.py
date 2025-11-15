import streamlit as st
import requests
from datetime import datetime, date, timedelta

API_URL = "http://127.0.0.1:8000"


def convertir_minutes_vers_hms(total_minutes: float) -> str:
    """Convertit un total de minutes (float) en HH:MM:SS."""
    if total_minutes is None or total_minutes < 0:
        return "00:00:00"

    total_secondes = int(total_minutes * 60)
    heures = total_secondes // 3600
    secondes_restantes = total_secondes % 3600
    minutes = secondes_restantes // 60
    secondes = secondes_restantes % 60

    # Utilisation de :02d pour garantir deux chiffres (ex: 01:05:30)
    return f"{heures:02d}h {minutes:02d}min {secondes:02d}s"


def statistiques_page():
    st.header("📊 Mes Statistiques")

    if not st.session_state.get('auth'):
        st.warning("Veuillez vous connecter d'abord.")
        return

    # Infos user disponibles
    user_info = st.session_state.get('user')
    if not user_info or 'id' not in user_info:
        st.error("Impossible de récupérer les informations utilisateur.")
        return

    user_id = user_info['id']

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
        endpoint = f"{API_URL}/statistiques/{user_id}"
        params = {
            "reference_date": date_str
        }

        # Récupération des données
        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        stats_data = response.json()

        # Affichage des données

        stats = stats_data.get("Statistiques", {})
        # Ajustement pour la compatibilité des types, car date_reference est un objet date
        periode = stats_data.get("Période", (date_reference.isoformat(), (date_reference + timedelta(days=6)).isoformat()))

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

            temps_formatte = convertir_minutes_vers_hms(temps_minutes) 

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
            # URL d'appel
            endpoint_pred = f"{API_URL}/statistiques/prediction/{user_id}"
            params_pred = {
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