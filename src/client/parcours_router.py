from fastapi import APIRouter, HTTPException, Body
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
    Crée un nouveau parcours et renvoie l'ID créé.
    """
    try:
        id_parcours = parcours_service.creer_parcours(depart, arrivee, id_activite, id_user)
        
        if id_parcours is None:
            raise HTTPException(status_code=500, detail="Erreur lors de la création du parcours.")
        
        return {
            "message": "Parcours créé avec succès.",
            "id_parcours": id_parcours
        }

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
    Renvoie les coordonnées du parcours (issues du GPX en base ou géocodage).
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
    Génère et retourne le contenu HTML de la carte du parcours.
    Le HTML est généré en mémoire, aucun fichier n'est créé.
    """
    try:
        html_content = parcours_service.visualiser_parcours(id_parcours)
        return {"html_content": html_content}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la carte : {str(e)}")


@parcours_router.post("/visualiser-gpx")
def visualiser_depuis_gpx(gpx_content: str = Body(..., embed=True)):
    """
    Visualise directement un parcours depuis du contenu GPX.
    Utile pour prévisualiser un GPX sans créer de parcours en base.
    
    Body example:
    {
        "gpx_content": "<gpx>...</gpx>"
    }
    """
    try:
        html_content = parcours_service.visualiser_parcours_depuis_gpx(gpx_content)
        return {"html_content": html_content}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la carte : {str(e)}")