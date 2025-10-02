from datetime import date, timedelta
from abc import ABC, abstractmethod
class Activite(ABC):
    def __init__(self, id_activite: int, id_user: int, date: date, typeSport: str, distance: float,duree: timedelta,trace: str, idParcours:int,
    titre: str,
    description: str):
        self.id_activite = id_activite
        self.id_user = id_user
        self.date = date
        self.typeSport = typeSport
        self.distance = distance
        self.duree = duree
        self.trace = trace
        self.idParcours = idParcours
        self.titre = titre
        self.description = description
    @abstractmethod
    def afficher_details(self):
        pass

