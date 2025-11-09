from fastapi import APIRouter, HTTPException
from datetime import date
from service.Statistique_service import StatistiqueService
from business_object.user import User
from service.user_service import UserService

statistiques_router = APIRouter(
    prefix="/statistiques",
    tags=["Statistiques"]
)

user_service = UserService()


@statistiques_router.get("/{user_id}")
def get_statistiques(user_id: int, reference_date: date = date.today()):
    """
    Endpoint qui renvoie les statistiques hebdomadaires d'un utilisateur.
    """
    try:
        user = user_service.lire_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

        service = StatistiqueService(user)
        stats = service.afficherStats(reference_date)
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@statistiques_router.get("/prediction/{user_id}")
def get_prediction(user_id: int, type_sport: str):
    """
    Endpoint qui renvoie une prédiction de distance pour un sport donné.
    """
    try:
        user = user_service.lire_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

        service = StatistiqueService(user)

        distance_recommandee = service.predire(type_sport)

        if distance_recommandee is None:
            raise HTTPException(status_code=404, detail="Aucune donnée suffisante pour la prédiction.")

        return {"distance_recommandee": distance_recommandee}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")
