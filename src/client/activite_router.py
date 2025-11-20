from fastapi import APIRouter, Depends, HTTPException, Form
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
    description: Optional[str] = None  # Déjà présent
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
        description=activite.description,  # Description incluse
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
            description=getattr(act, "description", ""),  # Description incluse
            id_user=act.id_user
        )
        for act in activites
    ]

# ----------------- MODIFICATION -----------------
@activite_router.put("/{id_activite}", response_model=ActiviteSchema)
def modifier_activite(id_activite: int, activite: ActiviteSchema, current_user=Depends(get_current_user)):
    """Modifier une activité existante"""
    # Récupérer l'activité existante pour déterminer le type correct
    from business_object.course import Course
    from business_object.natation import Natation
    from business_object.cyclisme import Cyclisme
    
    type_sport_lower = activite.type_sport.lower()
    
    if type_sport_lower == "course":
        a = Course(
            id_activite=id_activite,
            date=activite.date,
            distance=activite.distance,
            duree=activite.duree,
            trace=activite.trace,
            titre=activite.titre,
            description=activite.description,  # Description incluse
            id_user=current_user.id_user,
            denivele=0.0
        )
    elif type_sport_lower == "natation":
        a = Natation(
            id_activite=id_activite,
            date=activite.date,
            distance=activite.distance,
            duree=activite.duree,
            trace=activite.trace,
            titre=activite.titre,
            description=activite.description,  # Description incluse
            id_user=current_user.id_user
        )
    elif type_sport_lower == "cyclisme":
        a = Cyclisme(
            id_activite=id_activite,
            date=activite.date,
            distance=activite.distance,
            duree=activite.duree,
            trace=activite.trace,
            titre=activite.titre,
            description=activite.description,  # Description incluse
            id_user=current_user.id_user,
            denivele=0.0
        )
    else:
        raise HTTPException(status_code=400, detail=f"Type de sport inconnu : {activite.type_sport}")
    
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
@activite_router.delete("/{id_activite}", status_code=204)
def supprimer_activite(id_activite: int, current_user=Depends(get_current_user)):
    """Supprimer une activité"""
    ok = activite_service.supprimer_activite(id_activite)
    if not ok:
        raise HTTPException(status_code=400, detail="Erreur suppression activité")

# ═══════════════════════════════════════════
# LIKES & COMMENTAIRES (inchangés)
# ═══════════════════════════════════════════

@activite_router.post("/{id_activite}/like")
def liker_activite(id_activite: int, current_user=Depends(get_current_user)):
    success = activite_service.ajouter_like(id_activite, current_user.id_user)
    if success:
        return {
            "message": "Activité likée avec succès",
            "likes_count": activite_service.compter_likes(id_activite)
        }
    else:
        raise HTTPException(status_code=400, detail="Vous avez déjà liké cette activité")

@activite_router.delete("/{id_activite}/like")
def unliker_activite(id_activite: int, current_user=Depends(get_current_user)):
    success = activite_service.retirer_like(id_activite, current_user.id_user)
    if success:
        return {
            "message": "Like retiré avec succès",
            "likes_count": activite_service.compter_likes(id_activite)
        }
    else:
        raise HTTPException(status_code=400, detail="Vous n'avez pas liké cette activité")

@activite_router.get("/{id_activite}/likes")
def get_likes_activite(id_activite: int, current_user=Depends(get_current_user)):
    likes = activite_service.get_likes_activite(id_activite)
    user_a_like = activite_service.user_a_like(id_activite, current_user.id_user)
    return {
        "likes": [
            {
                "id_like": like.id_like,
                "id_user": like.id_user,
                "created_at": like.created_at.isoformat() if like.created_at else None
            }
            for like in likes
        ],
        "count": len(likes),
        "user_has_liked": user_a_like
    }

@activite_router.post("/{id_activite}/commentaire")
def ajouter_commentaire(id_activite: int, contenu: str = Form(...), current_user=Depends(get_current_user)):
    commentaire = activite_service.ajouter_commentaire(id_activite, current_user.id_user, contenu)
    if commentaire:
        return {
            "message": "Commentaire ajouté avec succès",
            "commentaire": {
                "id_commentaire": commentaire.id_commentaire,
                "contenu": commentaire.contenu,
                "date": commentaire.created_at.isoformat() if commentaire.created_at else None,
                "id_user": commentaire.id_user,
                "username": current_user.username
            },
            "comments_count": activite_service.compter_commentaires(id_activite)
        }
    else:
        raise HTTPException(status_code=400, detail="Erreur lors de l'ajout du commentaire")

@activite_router.delete("/commentaire/{id_commentaire}")
def supprimer_commentaire(id_commentaire: int, current_user=Depends(get_current_user)):
    success = activite_service.supprimer_commentaire(id_commentaire, current_user.id_user)
    if success:
        return {"message": "Commentaire supprimé avec succès"}
    else:
        raise HTTPException(status_code=400, detail="Erreur lors de la suppression du commentaire")

@activite_router.get("/{id_activite}/commentaires")
def get_commentaires_activite(id_activite: int, current_user=Depends(get_current_user)):
    commentaires = activite_service.get_commentaires_activite(id_activite)
    return {
        "commentaires": [
            {
                "id_commentaire": com.id_commentaire,
                "contenu": com.contenu,
                "created_at": com.created_at.isoformat() if com.created_at else None,
                "id_user": com.id_user
            }
            for com in commentaires
        ],
        "count": len(commentaires)
    }

@activite_router.get("/{id_activite}/stats")
def get_stats_activite(id_activite: int, current_user=Depends(get_current_user)):
    return {
        "id_activite": id_activite,
        "likes_count": activite_service.compter_likes(id_activite),
        "comments_count": activite_service.compter_commentaires(id_activite),
        "user_has_liked": activite_service.user_a_like(id_activite, current_user.id_user)
    }