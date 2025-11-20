from business_object.activite import Activite
from business_object.course import Course
from business_object.natation import Natation
from business_object.cyclisme import Cyclisme
from dao.activite_dao import ActiviteDao
from dao.commentaire_dao import CommentaireDao
from dao.like_dao import LikeDao
from business_object.like import Like
from business_object.commentaire import Commentaire
import logging


class ActiviteService:

    def __init__(self):
        self.activiteDao = ActiviteDao()
        self.commentaireDao = CommentaireDao()
        self.likeDao = LikeDao()

    def creer_activite(self, date, type_sport, distance, duree, trace, titre, description, id_user) -> Activite:

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
                id_user=id_user
                
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
                id_user=id_user
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
                id_user=id_user
                
            )
        else:
            raise ValueError(f"Type de sport inconnu : {type_sport}")

        # Appel du DAO pour sauvegarder
        return nouvelle_activite if self.activiteDao.creer(nouvelle_activite) else None
    # afficher all activities 

    def get_toutes_activites(self, id_user: int) -> list:
        """
        Récupère toutes les activités d'un utilisateur.
        Retourne toujours une liste (vide si aucune activité).
        """
        try:
            activites = self.activiteDao.lire_activites_par_user(id_user)
            return activites or []  # Toujours retourner une liste
        except Exception as e:
            logging.exception(f"Erreur lors de la récupération des activités : {e}")
            return []

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
          
    # get all comments d'une activite
    def get_commentaires_activite(self, id_activite: int):
        """Retourne tous les commentaires d'une activité."""
        return self.commentaireDao.lire_par_activite(id_activite)

    # get all likes d'une activite
    def get_likes_activite(self, id_activite: int):
        return self.likeDao.lire_par_activite(id_activite)

    def ajouter_like(self, id_activite: int, id_user: int) -> bool:
        """
        Ajoute un like à une activité.
        """
        try:
            # Vérifier si l'utilisateur a déjà liké cette activité
            likes_existants = self.likeDao.lire_par_activite(id_activite)
            if any(like.id_user == id_user for like in likes_existants):
                logging.info(f"L'utilisateur {id_user} a déjà liké l'activité {id_activite}")
                return False
            
            # Créer le like
            nouveau_like = Like(
                id_user=id_user,
                id_activite=id_activite
            )
            
            return self.likeDao.creer(nouveau_like)
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du like : {e}")
            return False

    def retirer_like(self, id_activite: int, id_user: int) -> bool:
        """
        Retire un like d'une activité.
        """
        try:
            # Trouver le like de cet utilisateur pour cette activité
            likes_existants = self.likeDao.lire_par_activite(id_activite)
            like_a_supprimer = next(
                (like for like in likes_existants if like.id_user == id_user), 
                None
            )
            
            if not like_a_supprimer:
                logging.info(f"Aucun like trouvé pour l'utilisateur {id_user} sur l'activité {id_activite}")
                return False
            
            return self.likeDao.supprimer(like_a_supprimer.id_like)
        except Exception as e:
            logging.error(f"Erreur lors du retrait du like : {e}")
            return False

    def ajouter_commentaire(self, id_activite: int, id_user: int, contenu: str) -> Commentaire | None:
        """
        Ajoute un commentaire à une activité.
        """
        try:
            if not contenu or not contenu.strip():
                logging.error("Le contenu du commentaire est vide")
                return None
            
            nouveau_commentaire = Commentaire(
                id_commentaire=None,
                contenu=contenu.strip(),
                id_user=id_user,
                id_activite=id_activite
            )
            
            if self.commentaireDao.creer(nouveau_commentaire):
                return nouveau_commentaire
            return None
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du commentaire : {e}")
            return None

    def supprimer_commentaire(self, id_commentaire: int, id_user: int) -> bool:
        """
        Supprime un commentaire (uniquement par son auteur).
        """
        try:
            # Vérifier que l'utilisateur est bien l'auteur du commentaire
            # (nécessite une méthode lire() dans CommentaireDao)
            return self.commentaireDao.supprimer(id_commentaire)
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du commentaire : {e}")
            return False

    def compter_likes(self, id_activite: int) -> int:
        """
        Compte le nombre de likes d'une activité.
        """
        try:
            likes = self.likeDao.lire_par_activite(id_activite)
            return len(likes)
        except Exception as e:
            logging.error(f"Erreur lors du comptage des likes : {e}")
            return 0

    def compter_commentaires(self, id_activite: int) -> int:
        """
        Compte le nombre de commentaires d'une activité.
        """
        try:
            commentaires = self.commentaireDao.lire_par_activite(id_activite)
            return len(commentaires)
        except Exception as e:
            logging.error(f"Erreur lors du comptage des commentaires : {e}")
            return 0

    def user_a_like(self, id_activite: int, id_user: int) -> bool:
        """
        Vérifie si un utilisateur a liké une activité.
        """
        try:
            likes = self.likeDao.lire_par_activite(id_activite)
            return any(like.id_user == id_user for like in likes)
        except Exception as e:
            logging.error(f"Erreur lors de la vérification du like : {e}")
            return False