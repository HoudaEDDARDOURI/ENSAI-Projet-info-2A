from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from service.user_service import UserService

app = FastAPI(title="Sport Activities API")

# --- Authentification basique (exemple simple à garder temporairement)
security = HTTPBasic()

USERS = {
    "admin": {"password": "1234", "roles": ["admin"]},
    "user": {"password": "abcd", "roles": ["user"]},
}


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
