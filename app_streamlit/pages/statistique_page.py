import streamlit as st
import requests
from datetime import date, timedelta, datetime
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"


def formater_vitesse_min_sec(vitesse_minutes_decimal: float) -> str:
    """
    Convertit une vitesse en format décimal de minutes (ex: 4.76)
    en format minutes et secondes (ex: 4'46").
    """
    if vitesse_minutes_decimal <= 0:
        return "N/A"

    minutes = int(vitesse_minutes_decimal)

    secondes_decimales = vitesse_minutes_decimal - minutes
    secondes = round(secondes_decimales * 60)

    if secondes >= 60:
        minutes += 1
        secondes -= 60

    return f"{minutes:01}'{secondes:02}\""


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

        st.markdown("---")
        st.subheader("⚡ Vitesses Moyennes Hebdomadaires")

        v_col1, v_col2, v_col3 = st.columns(3)

        vitesse_course = stats.get("Vitesse moyenne course (min/km)", 0.0)
        with v_col1:
            if vitesse_course > 0:
                vitesse_course_formattee = formater_vitesse_min_sec(vitesse_course)
                st.metric("Course (min/km)", vitesse_course_formattee)
            else:
                st.metric("Course (min/km)", "N/A", delta_color="off")

        vitesse_cyclisme = stats.get("Vitesse moyenne cyclisme (km/h)", 0.0)
        with v_col2:
            if vitesse_cyclisme > 0:
                st.metric("Cyclisme (km/h)", f"{vitesse_cyclisme:.2f}")
            else:
                st.metric("Cyclisme (km/h)", "N/A", delta_color="off")

        vitesse_natation = stats.get("Vitesse moyenne natation (min/100m)", 0.0)
        with v_col3:
            if vitesse_natation > 0:
                vitesse_natation_formattee = formater_vitesse_min_sec(vitesse_natation)
                st.metric("Natation (min/100m)", vitesse_natation_formattee)
            else:
                st.metric("Natation (min/100m)", "N/A", delta_color="off")

    except requests.exceptions.RequestException as e:
        st.error(f"Erreur API lors de la récupération des statistiques principales : {e}")
        return

    # GRAPHIQUES

    st.markdown("---")
    st.subheader("📈 Visualisation de la Charge d'Entraînement")

    graph_col1, graph_col2 = st.columns(2)

    # GRAPHIQUE 1 : Durée par jour
    with graph_col1:
        try:
            endpoint_duree = f"{API_URL}/statistiques/{user_id}/duree_journaliere" 
            params_duree = {"reference_date": date_reference.isoformat()}
            response_duree = requests.get(endpoint_duree, params=params_duree)
            response_duree.raise_for_status()

            duree_data = response_duree.json() 
            df_duree = pd.DataFrame(duree_data) 

            if not df_duree.empty and df_duree['Durée (min)'].sum() > 0:
                fig_duree = px.bar(
                    df_duree,
                    x='Jour',
                    y='Durée (min)',
                    title="Durée totale d'activité par jour",
                    color_discrete_sequence=px.colors.qualitative.Prism
                )
                fig_duree.update_layout(xaxis_title="", yaxis_title="Durée (min)")
                st.plotly_chart(fig_duree, use_container_width=True)
            else:
                st.caption("Pas de données de durée quotidienne pour cette semaine.")

        except requests.exceptions.RequestException:
            st.warning("Graphique Durée: Endpoint de durée journalière non accessible.")

    # GRAPHIQUE 2 : DIstance par sport
    with graph_col2:
        try:
            endpoint_distance = f"{API_URL}/statistiques/{user_id}/distance_sport" 
            params_distance = {"reference_date": date_reference.isoformat()}
            response_distance = requests.get(endpoint_distance, params=params_distance)
            response_distance.raise_for_status()

            distances_data = response_distance.json()

            df_distance = pd.DataFrame(list(distances_data.items()), columns=['Sport', 'Distance (km)'])

            df_distance = df_distance[df_distance['Distance (km)'] > 0]
            
            if not df_distance.empty:
                fig_dist = px.pie(
                    df_distance, 
                    values='Distance (km)', 
                    names='Sport', 
                    title='Répartition de la distance hebdomadaire',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_dist.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_dist, use_container_width=True)
            else:
                st.caption("Pas de données de distance pour cette semaine.")

        except requests.exceptions.RequestException:
            st.warning("Graphique Distance: Endpoint de répartition des distances non accessible.")

    # PRÉDICTION

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

            unite = "m" if sport_choisi == "Natation" else "km"

            if sport_choisi == "Natation":
                distance_affichage = f"{prediction_value:,.0f}"
            else:
                distance_affichage = f"{prediction_value:,.1f}"

            st.success(
                f"🎉 Distance recommandée pour votre prochaine séance de **{sport_choisi}** : **{distance_affichage} {unite}**"
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors du calcul de la prédiction via l'API : {e}")
        except Exception as e:
            st.error(f"Erreur lors du traitement de la prédiction : {e}")