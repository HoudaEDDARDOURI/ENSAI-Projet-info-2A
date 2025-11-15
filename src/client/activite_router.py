from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from service.activite_service import ActiviteService
from client.auth import get_current_user

activite_service = ActiviteService()

activite_router = APIRouter(
    prefix="/activites",
    tags=["activites"]
)

# ----------------- SCHEMA -----------------
class ActiviteSchema(BaseModel):
    id_activite: Optional[int] = None
    date: str
    type_sport: str
    distance: float
    duree: str
    trace: Optional[str] = None
    titre: Optional[str] = None
    description: Optional[str] = None
    id_user: int

# ----------------- CREATION -----------------
from fastapi import UploadFile, File
import os
from fastapi.responses import JSONResponse

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@activite_router.post("/upload_gpx/")
def upload_gpx(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return {"file_path": file_path}

@activite_router.post("/", response_model=ActiviteSchema)
def creer_activite(activite: ActiviteSchema, current_user=Depends(get_current_user)):
    """Créer une nouvelle activité pour l'utilisateur connecté"""
    a = activite_service.creer_activite(
        date=activite.date,
        type_sport=activite.type_sport,
        distance=activite.distance,
        duree=activite.duree,
        trace=activite.trace,
        titre=activite.titre,
        description=activite.description,
        id_user=current_user.id_user
    )
    if not a:
        raise HTTPException(status_code=400, detail="Erreur création activité")
    return ActiviteSchema(
        id_activite=a.id_activite,
        date=a.date,
        type_sport=a.type_sport,
        distance=a.distance,
        duree=a.duree,
        trace=a.trace,
        titre=a.titre,
        description=a.description,
        id_user=a.id_user
    )

# ----------------- LECTURE -----------------
@activite_router.get("/", response_model=List[ActiviteSchema])
def get_user_activites(id_user: int, current_user=Depends(get_current_user)):
    """Récupérer toutes les activités d'un utilisateur"""
    activites = activite_service.get_toutes_activites(id_user)
    return [
        ActiviteSchema(
            id_activite=act.id_activite,
            date=str(act.date),
            type_sport=act.type_sport,
            distance=act.distance,
            duree=str(act.duree),
            trace=act.trace,
            titre=act.titre,
            description=getattr(act, "description", ""),
            id_user=act.id_user
        )
        for act in activites
    ]

# ----------------- MODIFICATION -----------------
@activite_router.put("/{id_activite}", response_model=ActiviteSchema)
def modifier_activite(id_activite: int, activite: ActiviteSchema, current_user=Depends(get_current_user)):
    """Modifier une activité existante"""
    # Création d'un objet concret
    class ActiviteConcrète:
        def __init__(self, id_activite, date, type_sport, distance, duree, trace, titre, description, id_user):
            self.id_activite = id_activite
            self.date = date
            self.type_sport = type_sport
            self.distance = distance
            self.duree = duree
            self.trace = trace
            self.titre = titre
            self.description = description
            self.id_user = id_user

    a = ActiviteConcrète(
        id_activite=id_activite,
        date=activite.date,
        type_sport=activite.type_sport,
        distance=activite.distance,
        duree=activite.duree,
        trace=activite.trace,
        titre=activite.titre,
        description=activite.description,
        id_user=current_user.id_user
    )
    ok = activite_service.modifier_activite(a)
    if not ok:
        raise HTTPException(status_code=400, detail="Erreur modification activité")
    return ActiviteSchema(
        id_activite=a.id_activite,
        date=a.date,
        type_sport=a.type_sport,
        distance=a.distance,
        duree=a.duree,
        trace=a.trace,
        titre=a.titre,
        description=a.description,
        id_user=a.id_user
    )

# ----------------- SUPPRESSION -----------------
@activite_router.delete("/{id_activite}")
def supprimer_activite(id_activite: int, current_user=Depends(get_current_user)):
    """Supprimer une activité"""
    ok = activite_service.supprimer_activite(id_activite)
    if not ok:
        raise HTTPException(status_code=400, detail="Erreur suppression activité")
