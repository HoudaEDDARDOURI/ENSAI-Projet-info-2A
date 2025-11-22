from fastapi import APIRouter, HTTPException, Query
from datetime import date
from service.Statistique_service import StatistiqueService
from service.user_service import UserService

statistiques_router = APIRouter(
    prefix="/statistiques",
    tags=["Statistiques"]
)

user_service = UserService()


@statistiques_router.get("/{user_id}")
def get_statistiques(user_id: int, reference_date: date = date.today()):
    user = user_service.lire_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    service = StatistiqueService(user)
    return service.afficherStats(reference_date)


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


@statistiques_router.get("/{user_id}/distance_sport")
def get_distance_par_sport_route(
    user_id: int,
    reference_date: date = Query(..., description="Date de référence dans la semaine à analyser")
):
    """
    Retourne la distance totale parcourue pour chaque sport durant la semaine.
    Utilisé pour le graphique de répartition (Pie Chart).
    """
    user = user_service.lire_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    stats_service = StatistiqueService(user)

    distances_par_sport = stats_service.get_distances_par_sport_semaine(reference_date)

    return distances_par_sport


@statistiques_router.get("/{user_id}/duree_journaliere")
def get_duree_par_jour_route(
    user_id: int,
    reference_date: date = Query(..., description="Date de référence dans la semaine à analyser")
):
    """
    Retourne la durée totale d'activité (en minutes) pour chaque jour de la semaine.
    Utilisé pour le graphique de charge (Bar Chart).
    """
    user = user_service.lire_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    stats_service = StatistiqueService(user)

    duree_par_jour = stats_service.get_duree_par_jour_semaine(reference_date)

    return duree_par_jour