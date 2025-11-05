from __future__ import annotations
from datetime import date, timedelta
from abc import ABC, abstractmethod
 
 
class Activite(ABC):
    def __init__(self, id_user: int, date: date, type_sport: str, distance: float, duree: timedelta,
                 trace: str, id_parcours: int, titre: str, description: str,
                 id_activite: int = None):
        self.id_activite = id_activite
        self.id_user = id_user
        self.date = date
        self.type_sport = type_sport
        self.distance = distance
        self.duree = duree
        self.trace = trace
        self.id_parcours = id_parcours
        self.titre = titre
        self.description = description

    @abstractmethod
    def afficher_details(self):
        pass
