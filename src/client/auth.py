from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from business_object.user import User
from service.user_service import UserService
from utils.securite import verify_password

security = HTTPBasic()
user_service = UserService()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    """Vérifie les credentials et retourne l'utilisateur authentifié"""
    user = user_service.get_user_par_username(credentials.username)
    
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