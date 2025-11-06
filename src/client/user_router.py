from fastapi import APIRouter, Depends, Form, HTTPException
from typing import Optional
from business_object.user import User
from service.user_service import UserService
from client.auth import get_current_user  # ← Import depuis auth.py

user_service = UserService()

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# ═══════════════════════════════════════════
# ENDPOINT PUBLIC (sans authentification)
# ═══════════════════════════════════════════

@user_router.post("/")
def create_user(
    prenom: str = Form(...),
    nom: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    """Créer un nouveau compte utilisateur"""
    user = user_service.creer_user(prenom, nom, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Erreur création utilisateur")
    return {"id": user.id_user, "username": user.username}

# ═══════════════════════════════════════════
# ENDPOINTS PROTÉGÉS (authentification requise)
# ═══════════════════════════════════════════

@user_router.get("/me")
def lire_user_courant(current_user: User = Depends(get_current_user)):
    """Récupérer les informations de l'utilisateur connecté avec nombre de followers"""
    
    # Nombre de followers
    followers = user_service.lister_followers(current_user)
    followers_count = len(followers)
    
    # Nombre de suivis (followed) — si tu as une fonction similaire à lister_followers
    followed_count = len(user_service.lister_followed(current_user))  # à créer si nécessaire

    return {
        "id": current_user.id_user,
        "username": current_user.username,
        "nom": current_user.nom,
        "prenom": current_user.prenom,
        "followers_count": followers_count,
        "followed_count": followed_count
    }


@user_router.put("/me")
def modifier_user_api(
    prenom: Optional[str] = Form(None),
    nom: Optional[str] = Form(None),
    username: Optional[str] = Form(None),
    mot_de_passe: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """Modifier les informations de l'utilisateur connecté"""
    if prenom and prenom != "string":
        current_user.prenom = prenom
    if nom and nom != "string":
        current_user.nom = nom
    if username and username != "string":
        current_user.username = username

    success = user_service.modifier_user(current_user, mot_de_passe)
    if not success:
        raise HTTPException(status_code=500, detail="Erreur lors de la modification")
    return {"message": "Utilisateur modifié avec succès"}

@user_router.delete("/{id_user}")
def supprimer_user(id_user: int, current_user: User = Depends(get_current_user)):
    """Supprimer son propre compte"""
    # Sécurité : un utilisateur ne peut supprimer que son propre compte
    if id_user != current_user.id_user:
        raise HTTPException(status_code=403, detail="Non autorisé")
    
    success = user_service.supprimer_user(id_user)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"detail": "Utilisateur supprimé"}