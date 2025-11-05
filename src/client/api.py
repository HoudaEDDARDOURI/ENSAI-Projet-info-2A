import secrets
from fastapi import FastAPI, HTTPException, Depends, status, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from business_object.user import User
from service.user_service import UserService

app = FastAPI(
    title="Sport Activities API",
    root_path="/proxy/8000"  # utile si tu déploies derrière un proxy (ex: Onyxia)
)

# --- Authentification basique (temporaire)
security = HTTPBasic()
service = UserService()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = service.get_user_par_username(username)
    if not user or not secrets.compare_digest(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"username": username}


# --- ROUTES UTILISATEUR ---

@app.post("/users")
def create_user(
    prenom: str = Form(...),
    nom: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """Créer un nouvel utilisateur"""
    user = service.creer(prenom, nom, username, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Erreur création utilisateur")
    return {"id": user.id_user, "username": user.username}


@app.get("/users/{id_user}")
def get_user(id_user: int):
    """Récupérer un utilisateur par son ID"""
    user = service.get_user(id_user)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"id": user.id_user, "username": user.username}


@app.put("/users/{id_user}")
def modifier_user(
    id_user: int,
    prenom: str = Form(...),
    nom: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """Modifier un utilisateur existant"""
    user = User(
        id_user=id_user,
        prenom=prenom,
        nom=nom,
        username=username,
        email=email,
        password=password
    )
    updated_user = service.modifier_user(user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"id": updated_user.id_user, "username": updated_user.username}


@app.delete("/users/{id_user}")
def supprimer_user(id_user: int):
    """Supprimer un utilisateur"""
    success = service.supprimer_user(id_user)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"detail": "Utilisateur supprimé"}
