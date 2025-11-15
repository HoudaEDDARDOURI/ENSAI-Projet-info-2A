from fastapi import APIRouter, Depends, HTTPException
from business_object.user import User
from service.user_service import UserService
from client.auth import get_current_user

user_service = UserService()

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
        
        # Formatter la réponse
        return {
            "activities": [
                {
                    "id_activite": act.id_activite,
                    "type": act.__class__.__name__,
                    "titre": act.titre,
                    "description": act.description,
                    "date": act.date.isoformat() if act.date else None,
                    "duree": act.duree,
                    "distance": getattr(act, 'distance', None),
                    "vitesse_moyenne": getattr(act, 'vitesse_moyenne', None),
                    "denivele": getattr(act, 'denivele', None),
                    "user": {
                        "id_user": act.user.id_user if hasattr(act, 'user') and act.user else act.id_user,
                        "username": act.user.username if hasattr(act, 'user') and act.user else None,
                        "prenom": act.user.prenom if hasattr(act, 'user') and act.user else None,
                        "nom": act.user.nom if hasattr(act, 'user') and act.user else None
                    }
                }
                for act in activities
            ],
            "count": len(activities)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la récupération du feed: {str(e)}"
        )