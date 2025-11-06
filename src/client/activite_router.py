from fastapi import APIRouter, Depends, Form, HTTPException
from service.activite_service import ActiviteService
from client.auth import get_current_user  # ← Import depuis auth.py

activite_service = ActiviteService()

activite_router = APIRouter(
    prefix="/activites",
    tags=["activites"]
)

@activite_router.post("/")
def creer_activite(
    date_activite: str = Form(...),
    type_sport: str = Form(...),
    distance: float = Form(...),
    duree: str = Form(...),
    trace: str = Form(...),
    titre: str = Form(...),
    description: str = Form(...),
    id_parcours: int = Form(...),
    current_user = Depends(get_current_user)  # ← Authentification requise
):
    """Créer une nouvelle activité pour l'utilisateur connecté"""
    activite = activite_service.creer_activite(
        date_activite, type_sport, distance, duree,
        trace, titre, description, current_user.id_user, id_parcours
    )
    if not activite:
        raise HTTPException(status_code=400, detail="Erreur création activité")
    return {"id": activite.id_activite, "titre": activite.titre}

@activite_router.get("/")
def get_user_activites(current_user = Depends(get_current_user)):
    """Récupérer toutes les activités de l'utilisateur connecté"""
    # Retourne uniquement les activités de l'utilisateur connecté
    return activite_service.afficher_toutes_activites(current_user.id_user)
    