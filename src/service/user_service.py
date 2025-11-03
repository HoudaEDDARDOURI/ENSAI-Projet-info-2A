from business_object.user import User
from dao.user_dao import UserDao
from utils.securite import hash_password
from datetime import datetime


class UserService:

    def __init__(self):
        self.dao = UserDao()

    def creer(self, prenom, nom, username, mot_de_passe) -> User:
        """Création d'un utilisateur à partir de ses attributs"""

        nouveau_user = User(
            prenom=prenom,
            nom=nom,
            username=username,
            mot_de_passe=hash_password(mot_de_passe)
        )

        return nouveau_user if self.dao.creer(nouveau_user) else None

    def supprimer(self, id_user: int) -> bool:
        return self.dao.supprimer(id_user)

    def se_connecter(self, pseudo, mdp) -> User:
        return self.dao.se_connecter(pseudo, hash_password(mdp, pseudo))

    def pseudo_deja_utilise(self, username) -> bool:
        user = self.dao.trouver_par_username(username)
        return user is not None

    def suivre(self, user: User, autre_user: User) -> bool:
        if user.id_user == autre_user.id_user:
            raise ValueError("Un utilisateur ne peut pas se suivre lui-même.")
        user.suivre(autre_user)
        return self.dao.ajouter_suivi(user.id_user, autre_user.id_user)

    # lister ses followers

    # trouver par id (pertinent de l'ajouter ?)

    # modifier

    # ajouter parcours
