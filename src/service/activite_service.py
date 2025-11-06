from business_object.activite import Activite
from business_object.course import Course
from business_object.natation import Natation
from business_object.cyclisme import Cyclisme
from dao.activite_dao import ActiviteDao
from dao.commentaire_dao import CommentaireDao
from dao.like_dao import LikeDao
import logging


class ActiviteService:

    def __init__(self):
        self.activiteDao = ActiviteDao()
        self.commentaireDao = CommentaireDao()
        self.likeDao = LikeDao()

    def creer_activite(self, date, type_sport, distance, duree, trace, titre, description, id_user,
                       id_parcours) -> Activite:

        """Création d'une activité à partir de ses attributs"""
        # Choix de la classe concrète selon le type de sport
        if type_sport.lower() == "course":
            nouvelle_activite = Course(
                id_activite=None,
                date=date,
                distance=distance,
                duree=duree,
                trace=trace,
                titre=titre,
                description=description,
                id_user=id_user,
                id_parcours=id_parcours,
                denivele=0.0
            )
        elif type_sport.lower() == "natation":
            nouvelle_activite = Natation(
                id_activite=None,
                date=date,
                distance=distance,
                duree=duree,
                trace=trace,
                titre=titre,
                description=description,
                id_user=id_user,
                id_parcours=id_parcours, 
            )
        elif type_sport.lower() == "cyclisme":
            nouvelle_activite = Cyclisme(
                id_activite=None,
                date=date,
                distance=distance,
                duree=duree,
                trace=trace,
                titre=titre,
                description=description,
                id_user=id_user,
                id_parcours=id_parcours,
                denivele=0.0
            )
        else:
            raise ValueError(f"Type de sport inconnu : {type_sport}")

        # Appel du DAO pour sauvegarder
        return nouvelle_activite if self.activiteDao.creer(nouvelle_activite) else None
    # afficher all activities 

    def afficher_toutes_activites(self, id_user: int):
        """Affiche toutes les activités d'un utilisateur en utilisant la méthode
         'lire_activites_par_user' du DAO.
        """
        try:
            # Récupérer toutes les activités de l'utilisateur
            activites = self.activiteDao.lire_activites_par_user(id_user)

            if not activites:
                print("Aucune activité trouvée pour cet utilisateur.")
                return

            # Afficher chaque activité
            for activite in activites:
                activite.afficher_details()

        except Exception as e:
            logging.exception(f"Erreur lors de l'affichage des activités : {e}")

    # modifier activite 

    def modifier_activite(self, activite: Activite) -> bool:
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
        return self.likeDao.lire_par_activite(id_activite)

    # ------------------------- parcours 

    # CRUD parcours