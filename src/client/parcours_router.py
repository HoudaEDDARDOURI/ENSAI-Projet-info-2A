from fastapi import APIRouter, HTTPException
from service.parcours_service import ParcoursService
from dao.parcours_dao import ParcoursDao
from business_object.parcours import Parcours

parcours_router = APIRouter(
    prefix="/parcours",
    tags=["Parcours"]
)

parcours_service = ParcoursService()
parcours_dao = ParcoursDao()


@parcours_router.post("/")
def creer_parcours(depart: str, arrivee: str, id_user: int, id_activite: int | None = None):
    """
    Crée un nouveau parcours.
    """
    try:
        created = parcours_service.creer_parcours(depart, arrivee, id_activite, id_user)
        if not created:
            raise HTTPException(status_code=500, detail="Erreur lors de la création du parcours.")
        return {"message": "Parcours créé avec succès."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@parcours_router.get("/{id_parcours}")
def lire_parcours(id_parcours: int):
    """
    Lit un parcours et renvoie ses informations.
    """
    try:
        parcours = parcours_dao.lire(id_parcours)
        if not parcours:
            raise HTTPException(status_code=404, detail="Parcours non trouvé.")
        return parcours.__dict__

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@parcours_router.get("/{id_parcours}/coordonnees")
def get_coordonnees(id_parcours: int):
    """
    Renvoie les coordonnées du parcours (issues du GPX ou géocodage).
    """
    try:
        parcours = parcours_dao.lire(id_parcours)
        if not parcours:
            raise HTTPException(status_code=404, detail="Parcours non trouvé.")

        coords = parcours_service.get_coordinates(parcours)
        return {"coordonnees": coords}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@parcours_router.get("/{id_parcours}/visualiser")
def visualiser_parcours(id_parcours: int):
    """
    Génère la carte HTML du parcours.
    """
    try:
        file_path = parcours_service.visualiser_parcours(id_parcours)
        return {"fichier_html": file_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

