from business_object.user import User
from business_object.activite import Activite
from dao.user_dao import UserDao
from src.dao.activite_dao import ActiviteDao
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
        self.activiteDao = ActiviteDao()
        self.commentaireDao = CommentaireDao()
        self.likeDao = LikeDao()

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

    # creer activite 
    def creer_activite(self, date, type_sport, distance, duree, trace, titre, description, id_user,
                       id_parcours) -> Activite:

        """Création d'une activité à partir de ses attributs"""
        # Choix de la classe concrète selon le type de sport
        if type_sport.lower() == "course":
            nouvelle_activite = Course(
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
        elif type_sport.lower() == "natation":
            nouvelle_activite = Natation(
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
        elif type_sport.lower() == "cyclisme":
            nouvelle_activite = Cyclisme(
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
        else:
            raise ValueError(f"Type de sport inconnu : {type_sport}")

        # Appel du DAO pour sauvegarder
        return nouvelle_activite if self.activiteDao.creer(nouvelle_activite) else None
    # afficher all activities 

    def afficher_toutes(self):
        """
        Affiche toutes les activités en utilisant la méthode 'lire' du DAO.
        """
        try:
            # Étape 1 : récupérer tous les IDs
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id_activite FROM activite;")
                    ids = [row["id_activite"] for row in cursor.fetchall()]

            if not ids:
                print("Aucune activité trouvée.")
                return

            # Étape 2 et 3 : récupérer chaque activité et l'afficher
            for id_activite in ids:
                activite = self.activiteDao.lire(id_activite)
                if activite:
                    activite.afficher_details()
    
        except Exception as e:
            import logging
            logging.exception(f"Erreur lors de l'affichage de toutes les activités: {e}")

    # modifier activite 

    def modifier(self, activite: Activite) -> bool:
        """
        Modifie une activité existante.
        :param activite: objet Activite (ou Natation/Cyclisme/Course) avec les nouvelles valeurs
        :return: True si la modification a réussi, False sinon
        """

        # Appel à la méthode modifier du DAO
        return self.activiteDao.modifier(activite)
    # supprimer activite 

    def supprimer_activite(self, id_activite: int) -> bool:
        return self.activiteDao.supprimer(id_activite)

    # consulter une activite            
    # get all comments d'une activite
    def get_commentaires_activite(self, id_activite: int):
        """Retourne tous les commentaires d'une activité."""
        return self.commentaireDao.lire_par_activite(id_activite)

    # get all likes d'une activite

    def get_likes_activite(self, id_activite: int):
        return self.likeDao.par_activite(id_activite)

    # ------------------------- parcours 

    # CRUD parcours 