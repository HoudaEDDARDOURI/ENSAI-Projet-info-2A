from __future__ import annotations
from datetime import date, timedelta
from abc import ABC, abstractmethod


class Activite(ABC):
    def __init__(self, id_user: int, date: date, type_sport: str, distance: float, duree: timedelta,
                 trace: str, titre: str, description: str,
                 id_activite: int = None):
        self.id_activite = id_activite
        self.id_user = id_user
        self.date = date
        self.type_sport = type_sport
        self.distance = distance
        self.duree = duree
        self.trace = trace
        self.titre = titre
        self.description = description

    @abstractmethod
    def calculer_vitesse(self) -> float:
        pass


# Exemple de sous-classe concrète
class Course(Activite):
    def calculer_vitesse(self) -> float:
        if self.distance <= 0 or self.duree.total_seconds() <= 0:
            return 0.0
        duree_minutes = self.duree.total_seconds() / 60
        vitesse_minkm = round(duree_minutes / self.distance, 2)
        return vitesse_minkm
