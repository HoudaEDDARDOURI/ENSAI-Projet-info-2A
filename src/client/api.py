from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from service.user_service import UserService

app = FastAPI(
    title="Sport Activities API",
    root_path="/proxy/8000"
)


# --- Authentification basique (exemple simple à garder temporairement)
security = HTTPBasic()

USERS = {
    "admin": {"password": "1234", "roles": ["admin"]},
    "user": {"password": "abcd", "roles": ["user"]},
}


service = UserService()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = USERS.get(username)
    if not user or not secrets.compare_digest(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"username": username, "roles": user["roles"]}


@app.post("/users")
def create_user(prenom: str, nom: str, username: str, email: str, password: str):
    service = UserService()
    user = service.creer(prenom, nom, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Erreur création utilisateur")
    return {"id": user.id_user, "username": user.username}


@app.get("/users/{id_user}")
def get_user(id_user: int):
    user = service.get_user(id_user)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"id": user.id_user, "username": user.username}


@app.put("/users/{id_user}")
def modifier_user(id_user: int):
    updated_user = service.update_user(id_user, user_data.dict(exclude_none=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"id": updated_user.id_user, "username": updated_user.username}


@app.delete("/users/{id_user}")
def supprimer_user(id_user: int):
    success = service.delete_user(id_user)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"detail": "Utilisateur supprimé"}