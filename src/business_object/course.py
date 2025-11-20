from datetime import date, timedelta
from business_object.activite import Activite


class Course(Activite):
    def __init__(self, id_activite: int, id_user: int, date: date, distance: float,
                 duree: timedelta, trace: str,
                 titre: str, description: str):
        super().__init__(id_activite=id_activite,
                         id_user=id_user,
                         date=date,
                         type_sport="course",
                         distance=distance,
                         duree=duree,
                         trace=trace,
                         titre=titre,
                         description=description)
        self.vitesse_minkm = None

    def calculer_vitesse(self) -> float:
        """Calcule la vitesse moyenne en minutes par km."""
        if self.distance <= 0 or self.duree.total_seconds() <= 0:
            self.vitesse_minkm = 0.0
        else:
            duree_minutes = self.duree.total_seconds() / 60
            self.vitesse_minkm = round(duree_minutes / self.distance, 2)
        return self.vitesse_minkm

