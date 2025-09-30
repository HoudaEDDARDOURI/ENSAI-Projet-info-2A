from business_object.user import User
from dao.user_dao import UserDao
from security import hash_password


class UserService():
    """Classe contenant les méthodes de service des users"""

    # créer user

    # lister tous les users

    # modifier users

    # lister les followers

    # trouver par id

    # modifier

    # supprimer

    # se connecter

    # @log
    def se_connecter(self, pseudo, mdp) -> User:
        """Se connecter à partir de pseudo et mdp"""
        return UserDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    # @log
    def pseudo_deja_utilise(self, pseudo) -> bool:
        """Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"""
        # User = UserDao().lister_tous()
        # return pseudo in [j.pseudo for j in joueurs]
        pass 
