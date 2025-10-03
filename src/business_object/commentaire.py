from business_object.user import User
from business_object.activite import Activite


class Commentaire:
    def __init__(self, user: User, activite: Activite, contenu: str, date=None):
        self.user = user
        self.activite = activite
        self.contenu = contenu
        self.date = date
