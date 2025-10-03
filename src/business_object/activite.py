from datetime import date, timedelta
from abc import ABC, abstractmethod
from business_object.user import User
from business_object.parcours import Parcours


class Activite(ABC):
    def __init__(self, user: User, date: date, typeSport: str, distance: float, duree: timedelta,
                 trace: str, parcours: Parcours, titre: str, description: str,
                 id_activite: int = None):
        self.id_activite = id_activite
        self.user = user
        self.date = date
        self.typeSport = typeSport
        self.distance = distance
        self.duree = duree
        self.trace = trace
        self.parcours = parcours
        self.titre = titre
        self.description = description

    @abstractmethod
    def afficher_details(self):
        pass
