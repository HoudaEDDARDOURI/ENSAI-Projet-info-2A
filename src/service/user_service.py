from business_object.user import User
from business_object.activite import Activite
from dao.user_dao import UserDao
from dao.activite_dao import ActiviteDao
from utils.securite import hash_password
from datetime import datetime


class UserService:

    def __init__(self):
        self.userdao = UserDao()
        self.activiteDao = ActiviteDao()

    def creer(self, prenom, nom, username, mot_de_passe) -> User:
        """Création d'un utilisateur à partir de ses attributs"""

        nouveau_user = User(
            prenom=prenom,
            nom=nom,
            username=username,
            mot_de_passe=hash_password(mot_de_passe)
        )

        return nouveau_user if self.userdao.creer(nouveau_user) else None

    def supprimer(self, id_user: int) -> bool:
        return self.userdao.supprimer(id_user)

    def se_connecter(self, pseudo, mdp) -> User:
        return self.userdao.se_connecter(pseudo, hash_password(mdp, pseudo))

    def pseudo_deja_utilise(self, username) -> bool:
        user = self.userdao.trouver_par_username(username)
        return user is not None

    def suivre(self, user: User, autre_user: User) -> bool:
        if user.id_user == autre_user.id_user:
            raise ValueError("Un utilisateur ne peut pas se suivre lui-même.")
        user.suivre(autre_user)
        return self.userdao.ajouter_suivi(user.id_user, autre_user.id_user)

    # lister ses followers

    # trouver par id (pertinent de l'ajouter ?)

    # modifier user 


    # ---------------- activité 

    # creer activite 

    def creer_activite(self, date, type_sport, distance, duree, trace, titre, description, id_user, id_parcours) -> Activite:
        """Création d'une activité à partir de ses attributs"""
        nouvelle_activite = Activite(
            date=date,
            type_sport=type_sport,
            distance=distance,
            duree=duree,
            trace=trace,
            titre=titre,
            description=description,
            id_user=id_user,
            id_parcours=id_parcours
        )

        return nouvelle_activite if self.activiteDao.creer(nouvelle_activite) else None


    # afficher all activities 

    # modifier activite 

    # supprimer activite 

    # consulter une activite 

        
                    # get all likes d'une activite 

                    # get all comments 

    # ------------------------- parcours 

    # CRUD parcours 

    