from business_object.activite import Activite
from business_object.like import Like
from business_object.commentaire import Commentaire
from business_object.parcours import Parcours


class User():
    def __init__(self, nom: str, prenom: str, username: str, mot_de_passe: str,
                 id_user: int = None):
        self.id_user = id_user
        self.prenom = prenom
        self.nom = nom
        self.username = username
        self.mot_de_passe = mot_de_passe
        # self.photo = photo

        self.following: set[User] = set()
        self.followers: set[User] = set()

        self.activites: list[Activite] = []  
        self.commentaires: list[Commentaire] = []
        self.likes: list[Like] = []
        self.parcours: list[Parcours] = []
