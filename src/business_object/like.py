from business_object.user import User
from business_object.activite import Activite


class Like:
    def __init__(self, user: User, activite: Activite, date=None):
        self.user = user
        self.activite = activite
        self.date = date