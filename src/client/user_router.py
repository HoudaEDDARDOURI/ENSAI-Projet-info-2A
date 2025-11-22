from fastapi import APIRouter, Depends, Form, HTTPException
from typing import Optional
from business_object.user import User
from service.user_service import UserService
from client.auth import get_current_user 
from service.activite_service import ActiviteService
import logging

user_service = UserService()
activite_service = ActiviteService()

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
    try:
        # Vérifier d'abord si le username existe déjà
        if user_service.pseudo_deja_utilise(username):
            raise HTTPException(
                status_code=400, 
                detail=f"Le nom d'utilisateur '{username}' est déjà utilisé"
            )
        
        user = user_service.creer_user(prenom, nom, username, password)
        
        if not user:
            raise HTTPException(
                status_code=400, 
                detail="Erreur lors de la création de l'utilisateur"
            )
        
        return {"id": user.id_user, "username": user.username}
    
    except HTTPException:
        # Re-lever les HTTPException pour qu'elles soient gérées par FastAPI
        raise
    
    except ValueError as e:
        # Erreurs de validation
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # Erreur générique
        logging.error(f"Erreur inattendue lors de la création d'utilisateur : {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erreur interne du serveur lors de la création du compte"
        )

# ═══════════════════════════════════════════
# ENDPOINTS PROTÉGÉS (authentification requise)
# ═══════════════════════════════════════════

@user_router.get("/me")
def lire_user_courant(current_user: User = Depends(get_current_user)):
    """Récupérer les informations de l'utilisateur connecté avec nombre de followers"""
    
    # Nombre de followers
    followers = user_service.lister_followers(current_user)
    followers_count = len(followers)
    
    # Nombre de suivis (followed)
    followed_count = len(user_service.lister_followed(current_user))

    # Nombre d'activités pratiquées par le user actuel 
    nombre_activites = len(activite_service.get_toutes_activites(current_user.id_user))

    return {
        "id": current_user.id_user,
        "username": current_user.username,
        "nom": current_user.nom,
        "prenom": current_user.prenom,
        "followers_count": followers_count,
        "followed_count": followed_count,
        "nombre_activites": nombre_activites
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
    try:
        # Vérifier si le nouveau username est déjà pris (par quelqu'un d'autre)
        if username and username != current_user.username:
            if user_service.pseudo_deja_utilise(username):
                raise HTTPException(
                    status_code=400,
                    detail=f"Le nom d'utilisateur '{username}' est déjà utilisé"
                )
        
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
    
    except HTTPException:
        raise
    
    except Exception as e:
        logging.error(f"Erreur lors de la modification de l'utilisateur : {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur interne lors de la modification"
        )


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


@user_router.get("/suggestions")
def suggestions(current_user: User = Depends(get_current_user)):
    users = user_service.lister_tous_les_users()

    suggestions = [
        u for u in users
        if u.id_user != current_user.id_user   # exclure soi-même
        and not user_service.est_suivi(current_user, u)  # pas déjà suivi
    ]

    return [
        {
            "id_user": u.id_user,
            "prenom": u.prenom,
            "nom": u.nom,
            "username": u.username
        }
        for u in suggestions[:10]
    ]


@user_router.post("/{id}/follow")
def suivre_user(id: int, current_user: User = Depends(get_current_user)):
    autre_user = user_service.lire_user(id)
    if not autre_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    try:
        result = user_service.suivre(current_user, autre_user)
        if result == "deja_suivi":
            return {"message": "Déjà suivi"}
        return {"message": "Suivi effectué"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.delete("/{id}/follow")
def ne_plus_suivre_user(id: int, current_user: User = Depends(get_current_user)):
    """Arrêter de suivre un utilisateur (unfollow)"""
    autre_user = user_service.lire_user(id)
    if not autre_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    try:
        success = user_service.ne_plus_suivre(current_user, autre_user)
        if success:
            return {"message": "Vous ne suivez plus cet utilisateur"}
        else:
            raise HTTPException(status_code=400, detail="Vous ne suiviez pas cet utilisateur")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/{id}/is-following")
def verifier_si_suivi(id: int, current_user: User = Depends(get_current_user)):
    """Vérifie si l'utilisateur connecté suit un autre utilisateur"""
    autre_user = user_service.lire_user(id)
    if not autre_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    
    is_following = user_service.est_suivi(current_user, autre_user)
    return {"is_following": is_following}


@user_router.get("/me/following")
def get_my_following(current_user: User = Depends(get_current_user)):
    followed = user_service.lister_followed(current_user)
    return [
        {
            "id_user": u.id_user,
            "prenom": u.prenom,
            "nom": u.nom,
            "username": u.username
        }
        for u in followed
    ]