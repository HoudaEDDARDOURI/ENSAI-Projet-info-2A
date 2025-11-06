from business_object.user import User
from business_object.activite import Activite
from dao.user_dao import UserDao
from dao.activite_dao import ActiviteDao
from dao.like_dao import LikeDao
from dao.commentaire_dao import CommentaireDao
from utils.securite import hash_password
from dao.db_connection import DBConnection
from business_object.course import Course
from business_object.natation import Natation
from business_object.cyclisme import Cyclisme


class UserService:

    def __init__(self):
        self.userdao = UserDao()

    def creer_user(self, prenom, nom, username, mot_de_passe) -> User:
        """Création d'un utilisateur à partir de ses attributs"""

        nouveau_user = User(
            prenom=prenom,
            nom=nom,
            username=username,
            mot_de_passe=hash_password(mot_de_passe)
        )

        return nouveau_user if self.userdao.creer(nouveau_user) else None

    def supprimer_user(self, id_user: int) -> bool:
        return self.userdao.supprimer(id_user)

    def se_connecter(self, pseudo, mdp) -> User:
        return self.userdao.se_connecter(pseudo, hash_password(mdp))

    def pseudo_deja_utilise(self, username) -> bool:
        user = self.userdao.trouver_par_username(username)
        return user is not None

    def suivre(self, user: User, autre_user: User) -> bool:
        if user.id_user == autre_user.id_user:
            raise ValueError("Un utilisateur ne peut pas se suivre lui-même.")
        user.suivre(autre_user)
        return self.userdao.ajouter_suivi(user.id_user, autre_user.id_user)

    def lire_user(self, id_user: int) -> User | None:
        """Retourne un utilisateur selon son identifiant."""
        return self.userdao.lire(id_user)

    def modifier_user(self, user: User, nouveau_mot_de_passe: str | None = None) -> bool:
        """
        Met à jour les informations d'un utilisateur.
        Si un nouveau mot de passe est fourni, il sera hashé avant la mise à jour.

        Parameters
        ----------
        user : User
            L'utilisateur à modifier (doit déjà avoir son id_user)
        nouveau_mot_de_passe : str | None
            Le nouveau mot de passe en clair, s'il doit être changé

        Returns
        -------
        success : bool
            True si la modification a réussi, False sinon
        """
        if not user.id_user:
            print("Impossible de modifier : l'utilisateur n'a pas d'ID.")
            return False

        # Hash du mot de passe si un nouveau est fourni
        if nouveau_mot_de_passe:
            user.mot_de_passe = hash_password(nouveau_mot_de_passe)

        return self.userdao.modifier(user)

    def lister_followers(self, user: User):
        """Liste les followers de l'utilisateur"""
        return self.userdao.lister_followers(user)

    def lister_followed(self, user: User) -> list[User]:
        return self.userdao.lister_followed(user)

    def get_user_par_username(self, username: str):
        """Récupère l'utilisateur par son username"""
        return self.userdao.trouver_par_username(username)





        
