from business_object.activite import Activite


class User():
    def __init__(self, nom: str, prenom: str, username: str, mot_de_passe: str,
                 id_user: int = None):
        self.id_user = id_user
        self.prenom = prenom
        self.nom = nom
        self.username = username
        self.mot_de_passe = mot_de_passe
        # self.photo = photo
        self.activites: list[Activite] = []   # composition
        # self.commentaires: List[Commentaire] = []
        # self.likes: List[Like] = []
        # self.parcours: List[Parcours] = []
