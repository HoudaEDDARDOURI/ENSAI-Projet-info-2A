import secrets
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status, Form, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from business_object.user import User
from service.user_service import UserService
from utils.securite import verify_password

# --- Initialisation FastAPI ---
app = FastAPI(title="Sport Activities API", root_path="/proxy/8000")
security = HTTPBasic()
service = UserService()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    user = service.get_user_par_username(credentials.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )

    if not verify_password(credentials.password, user.mot_de_passe):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe incorrect"
        )

    return user

# --- Router pour les endpoints utilisateurs protégés ---
user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]  # Auth obligatoire pour tous les endpoints
)

# --- Endpoint public (création de compte) ---
@app.post("/users")
def create_user(
    prenom: str = Form(...),
    nom: str = Form(...),
    username: str = Form(...),
    password: str = Form(...)
):
    user = service.creer_user(prenom, nom, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Erreur création utilisateur")
    return {"id": user.id_user, "username": user.username}

# --- Endpoints protégés ---
@user_router.get("/me")
def lire_user_courant(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id_user,
        "username": current_user.username,
        "nom": current_user.nom,
        "prenom": current_user.prenom
    }

@user_router.put("/me")
def modifier_user_api(
    prenom: Optional[str] = Form(None),
    nom: Optional[str] = Form(None),
    username: Optional[str] = Form(None),
    mot_de_passe: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    if prenom and prenom != "string":
        current_user.prenom = prenom
    if nom and nom != "string":
        current_user.nom = nom
    if username and username != "string":
        current_user.username = username

    success = service.modifier_user(current_user, mot_de_passe)
    if not success:
        raise HTTPException(status_code=500, detail="Erreur lors de la modification")
    return {"message": "Utilisateur modifié avec succès"}

@user_router.delete("/{id_user}")
def supprimer_user(id_user: int):
    success = service.supprimer_user(id_user)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"detail": "Utilisateur supprimé"}

# --- Inclure le router dans l'app ---
app.include_router(user_router)
