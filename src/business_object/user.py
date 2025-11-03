from business_object.activite import Activite
from business_object.like import Like
from business_object.commentaire import Commentaire
from business_object.parcours import Parcours
from datetime import date


class User():
    def __init__(self, nom: str, prenom: str, username: str, mot_de_passe: str,
                 email: str, date_creation: date, id_user: int = None):
        self.id_user = id_user
        self.prenom = prenom
        self.nom = nom
        self.username = username
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.date_creation = date_creation

        # self.photo = photo

        self.following: set[int] = set()
        self.followers: set[int] = set()

        self.activites: list[Activite] = []
        self.parcours: list[Parcours] = []
