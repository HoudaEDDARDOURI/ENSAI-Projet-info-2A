from fastapi import APIRouter, HTTPException
from datetime import date
from service.Statistique_service import StatistiqueService
from business_object.user import User

statistiques_router = APIRouter(
    prefix="/statistiques",
    tags=["Statistiques"]
)


@statistiques_router.get("/{user_id}")
def get_statistiques(user_id: int, reference_date: date = date.today()):
    """
    Endpoint qui renvoie les statistiques hebdomadaires d'un utilisateur.
    """
    try:
        # Ici tu dois récupérer l'utilisateur à partir de la base ou d'une source en mémoire.
        # Exemple fictif :
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

        service = StatistiqueService(user)
        stats = service.afficherStats(reference_date)
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
