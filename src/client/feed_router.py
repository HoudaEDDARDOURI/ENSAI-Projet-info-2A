from fastapi import APIRouter, Depends, HTTPException
from business_object.user import User
from service.user_service import UserService
from service.activite_service import ActiviteService
from client.auth import get_current_user

user_service = UserService()
activite_service = ActiviteService()

feed_router = APIRouter(
    prefix="/feed",
    tags=["feed"]
)

@feed_router.get("/")
def get_feed(
    limit: int = 20,
    current_user: User = Depends(get_current_user)
):
    """
    Récupère le feed : les 20 activités les plus récentes des utilisateurs suivis
    avec likes, commentaires et informations utilisateur
    
    Parameters:
    - limit: Nombre d'activités à retourner (défaut: 20)
    """
    try:
        # Appel de la fonction dans UserService
        activities = user_service.get_feed_activites(current_user, limit=limit)
        
        if not activities:
            return {
                "activities": [],
                "count": 0,
                "message": "Aucune activité disponible. Suivez des utilisateurs pour voir leur contenu !"
            }
        
        # Formatter la réponse avec toutes les infos nécessaires
        formatted_activities = []
        
        for act in activities:
            # Récupérer les infos de l'utilisateur propriétaire de l'activité
            owner = user_service.get_user_by_id(act.id_user)
            
            # Récupérer les stats de l'activité (likes et commentaires)
            likes_count = activite_service.compter_likes(act.id_activite)
            comments_count = activite_service.compter_commentaires(act.id_activite)
            user_has_liked = activite_service.user_a_like(act.id_activite, current_user.id_user)
            
            # Calculer la vitesse moyenne si possible
            vitesse_moyenne = None
            if act.distance and act.duree:
                try:
                    duree_heures = act.duree.total_seconds() / 3600
                    if duree_heures > 0:
                        vitesse_moyenne = act.distance / duree_heures
                except:
                    pass
            
            formatted_activities.append({
                "id_activite": act.id_activite,
                "type": act.type_sport,
                "titre": act.titre,
                "description": getattr(act, 'description', ''),
                "date": act.date.isoformat() if act.date else None,
                "duree": str(act.duree) if act.duree else "N/A",
                "distance": act.distance,
                "vitesse_moyenne": round(vitesse_moyenne, 2) if vitesse_moyenne else None,
                "denivele": getattr(act, 'denivele', None),
                "trace": getattr(act, 'trace', None),  # Ajout de la trace GPX
                "user": {
                    "id_user": owner.id_user if owner else act.id_user,
                    "username": owner.username if owner else "Inconnu",
                    "prenom": owner.prenom if owner else "",
                    "nom": owner.nom if owner else ""
                },
                "likes_count": likes_count,
                "comments_count": comments_count,
                "user_has_liked": user_has_liked
            })
        
        return {
            "activities": formatted_activities,
            "count": len(formatted_activities)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la récupération du feed: {str(e)}"
        )