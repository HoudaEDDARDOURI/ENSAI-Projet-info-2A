import streamlit as st
import requests
from datetime import datetime
import streamlit.components.v1 as components

API_URL = "http://127.0.0.1:8000"

def get_sport_emoji(type_sport: str) -> str:
    """Retourne un emoji selon le type de sport"""
    emojis = {"course": "🏃", "natation": "🏊", "cyclisme": "🚴"}
    return emojis.get(type_sport.lower(), "🏃")

def format_duree(duree: str) -> str:
    """Formate la durée pour l'affichage"""
    if not duree or duree == "N/A":
        return "N/A"
    return duree

def feed_page():
    st.title("🏠 Feed - Activités de vos amis")

    # ---------- Initialisation session ----------
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "auth" not in st.session_state:
        st.session_state.auth = None

    # Auth check
    if not st.session_state.user_id or not st.session_state.auth:
        st.warning("⚠️ Veuillez vous connecter d'abord.")
        st.stop()

    # --- Paramètres du feed ---
    col1, col2 = st.columns([3, 1])
    with col2:
        limit = st.number_input("📊 Nombre d'activités", min_value=5, max_value=50, value=20, step=5)
        if st.button("🔄 Rafraîchir", use_container_width=True):
            st.rerun()

    # --- GET feed from API ---
    try:
        resp = requests.get(
            f"{API_URL}/feed/",
            params={"limit": limit},
            auth=st.session_state.auth,
            timeout=10
        )
        resp.raise_for_status()
        feed_data = resp.json()
        activites = feed_data.get("activities", [])
        message = feed_data.get("message", "")
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 404:
            st.error("❌ Endpoint /feed/ non trouvé. Vérifiez que le feed_router est bien enregistré.")
        else:
            st.error(f"❌ Erreur HTTP: {http_err.response.status_code} - {http_err.response.text}")
        activites = []
        message = ""
    except Exception as e:
        st.error(f"❌ Erreur connexion API: {e}")
        activites = []
        message = ""

    st.markdown("---")

    # --- Message si pas d'activités ---
    if not activites:
        st.info(message or "ℹ️ Aucune activité dans votre feed. Suivez des utilisateurs pour voir leurs activités !")
        
        # Suggestions d'utilisateurs à suivre
        st.subheader("👥 Suggestions d'utilisateurs à suivre")
        try:
            sugg_resp = requests.get(
                f"{API_URL}/users/suggestions",
                auth=st.session_state.auth,
                timeout=10
            )
            sugg_resp.raise_for_status()
            suggestions = sugg_resp.json()
            
            if suggestions:
                for user in suggestions[:5]:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{user['prenom']} {user['nom']}** (@{user['username']})")
                    with col2:
                        if st.button("➕ Suivre", key=f"follow_{user['id_user']}"):
                            try:
                                follow_resp = requests.post(
                                    f"{API_URL}/users/{user['id_user']}/follow",
                                    auth=st.session_state.auth,
                                    timeout=10
                                )
                                follow_resp.raise_for_status()
                                st.success(f"✅ Vous suivez maintenant @{user['username']}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur: {e}")
            else:
                st.info("Aucune suggestion disponible")
        except Exception as e:
            st.warning(f"Impossible de charger les suggestions: {e}")
        
        st.stop()

    # --- Statistiques du feed ---
    st.subheader("📊 Aperçu du feed")
    col1, col2, col3, col4 = st.columns(4)
    
    total_activites = len(activites)
    users_uniques = len(set(act.get("user", {}).get("id_user") for act in activites if act.get("user")))
    total_distance = sum(act.get("distance", 0) or 0 for act in activites)
    sports_types = {}
    for act in activites:
        sport = act.get("type", "Inconnu")
        sports_types[sport] = sports_types.get(sport, 0) + 1
    
    with col1:
        st.metric("📝 Activités", total_activites)
    with col2:
        st.metric("👥 Amis actifs", users_uniques)
    with col3:
        st.metric("🏃 Distance totale", f"{total_distance:.1f} km")
    with col4:
        sport_le_plus_pratique = max(sports_types.items(), key=lambda x: x[1])[0] if sports_types else "N/A"
        st.metric("🏅 Sport populaire", sport_le_plus_pratique)

    st.markdown("---")

    # --- Affichage des activités (style carte) ---
    st.subheader("📰 Activités récentes")
    
    for idx, act in enumerate(activites):
        user_info = act.get("user", {})
        username = user_info.get("username", "Inconnu")
        prenom = user_info.get("prenom", "")
        nom = user_info.get("nom", "")
        user_display = f"{prenom} {nom}" if prenom and nom else username
        
        type_sport = act.get("type", "Activité")
        titre = act.get("titre", "Sans titre")
        description = act.get("description", "")
        date_act = act.get("date", "")
        distance = act.get("distance", 0) or 0
        duree = format_duree(act.get("duree", "N/A"))
        vitesse_moyenne = act.get("vitesse_moyenne")
        denivele = act.get("denivele")
        
        # Formater la date
        try:
            date_obj = datetime.fromisoformat(date_act)
            date_formatted = date_obj.strftime("%d/%m/%Y à %H:%M")
            date_relative = get_relative_time(date_obj)
        except:
            date_formatted = date_act
            date_relative = ""
        
        emoji = get_sport_emoji(type_sport)
        
        # Carte d'activité
        with st.container():
            st.markdown(f"""
            <div style="
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                background-color: #f9f9f9;
            ">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <div style="font-size: 2em; margin-right: 10px;">{emoji}</div>
                    <div>
                        <strong style="font-size: 1.1em;">@{username}</strong> • {type_sport}
                        <br/>
                        <span style="color: #666; font-size: 0.9em;">{date_relative or date_formatted}</span>
                    </div>
                </div>
                <h3 style="margin: 10px 0;">{titre}</h3>
                {f'<p style="color: #555;">{description}</p>' if description else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # Statistiques de l'activité
            cols = st.columns(4)
            with cols[0]:
                st.metric("📏 Distance", f"{distance:.2f} km")
            with cols[1]:
                st.metric("⏱️ Durée", duree)
            with cols[2]:
                if vitesse_moyenne:
                    st.metric("⚡ Vitesse moy.", f"{vitesse_moyenne:.1f} km/h")
                else:
                    st.metric("⚡ Vitesse moy.", "N/A")
            
            # Actions sur l'activité (likes, commentaires)
            act_id = act.get("id_activite")
            likes_count = act.get("likes_count", 0)
            comments_count = act.get("comments_count", 0)
            user_has_liked = act.get("user_has_liked", False)
            
            col1, col2, col3 = st.columns([1, 1, 3])
            
            with col1:
                like_button_text = f"❤️ {likes_count}" if user_has_liked else f"🤍 {likes_count}"
                if st.button(like_button_text, key=f"like_{act_id}"):
                    try:
                        if user_has_liked:
                            # Unlike
                            unlike_resp = requests.delete(
                                f"{API_URL}/activites/{act_id}/like",
                                auth=st.session_state.auth,
                                timeout=10
                            )
                        else:
                            # Like
                            like_resp = requests.post(
                                f"{API_URL}/activites/{act_id}/like",
                                auth=st.session_state.auth,
                                timeout=10
                            )
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur : {e}")
            
            with col2:
                if st.button(f"💬 {comments_count}", key=f"comment_{act_id}"):
                    st.session_state[f"show_comments_{act_id}"] = not st.session_state.get(f"show_comments_{act_id}", False)
                    st.rerun()
            
            # Section commentaires (affichée si activée)
            if st.session_state.get(f"show_comments_{act_id}", False):
                st.markdown("---")
                st.markdown("### 💬 Commentaires")
                
                # Récupérer les commentaires
                try:
                    comments_resp = requests.get(
                        f"{API_URL}/activites/{act_id}/commentaires",
                        auth=st.session_state.auth,
                        timeout=10
                    )
                    
                    if comments_resp.status_code == 200:
                        comments_data = comments_resp.json()
                        commentaires = comments_data.get("commentaires", [])
                        
                        # Afficher les commentaires existants
                        if commentaires:
                            for comment in commentaires:
                                st.markdown(f"""
                                <div style="
                                    background-color: #f8f9fa;
                                    border-radius: 8px;
                                    padding: 10px;
                                    margin: 5px 0;
                                ">
                                    <strong>Utilisateur {comment.get('id_user')}</strong>
                                    <br/>
                                    {comment.get('contenu')}
                                    <br/>
                                    <small style="color: #999;">{comment.get('created_at', '')[:16] if comment.get('created_at') else ''}</small>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("Aucun commentaire pour le moment. Soyez le premier à commenter !")
                        
                        # Formulaire pour ajouter un commentaire
                        st.markdown("#### ✍️ Ajouter un commentaire")
                        with st.form(key=f"comment_form_{act_id}"):
                            comment_text = st.text_area(
                                "Votre commentaire",
                                key=f"comment_input_{act_id}",
                                placeholder="Écrivez votre commentaire ici...",
                                label_visibility="collapsed"
                            )
                            
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                submitted = st.form_submit_button("📤 Publier", use_container_width=True)
                            with col_btn2:
                                cancelled = st.form_submit_button("❌ Annuler", use_container_width=True)
                            
                            if cancelled:
                                st.session_state[f"show_comments_{act_id}"] = False
                                st.rerun()
                            
                            if submitted and comment_text:
                                try:
                                    post_comment_resp = requests.post(
                                        f"{API_URL}/activites/{act_id}/commentaire",
                                        data={"contenu": comment_text},
                                        auth=st.session_state.auth,
                                        timeout=10
                                    )
                                    
                                    if post_comment_resp.status_code == 200:
                                        st.success("✅ Commentaire publié !")
                                        st.rerun()
                                    else:
                                        st.error("Erreur lors de la publication")
                                except Exception as e:
                                    st.error(f"Erreur : {e}")
                    else:
                        st.error("Impossible de charger les commentaires")
                        
                except Exception as e:
                    st.error(f"Erreur : {e}")
            
            st.markdown("---")

def get_relative_time(date_obj: datetime) -> str:
    """Retourne une date relative (il y a X heures/jours)"""
    now = datetime.now()
    diff = now - date_obj
    
    if diff.days == 0:
        hours = diff.seconds // 3600
        if hours == 0:
            minutes = diff.seconds // 60
            return f"Il y a {minutes} minute{'s' if minutes > 1 else ''}"
        return f"Il y a {hours} heure{'s' if hours > 1 else ''}"
    elif diff.days == 1:
        return "Hier"
    elif diff.days < 7:
        return f"Il y a {diff.days} jours"
    else:
        return date_obj.strftime("%d/%m/%Y")