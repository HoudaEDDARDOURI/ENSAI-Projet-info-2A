from datetime import date, timedelta
from business_object.activite import Activite


class Course(Activite):
    def __init__(self, id_activite: int, id_user: int, date: date, distance: float,
                 duree: timedelta, trace: str, id_parcours: int,
                 titre: str, description: str, denivele: float):
        super().__init__(id_activite=id_activite,
                         id_user=id_user,
                         date=date,
                         type_sport="course",
                         distance=distance,
                         duree=duree,
                         trace=trace,
                         id_parcours=id_parcours,
                         titre=titre,
                         description=description)
        self.denivele = denivele
        self.vitesse_minkm = None

    def calculer_vitesse_course(self) -> float:
        """Calcule la vitesse moyenne en minutes par km."""
        if self.distance <= 0 or self.duree.total_seconds() <= 0:
            self.vitesse_minkm = 0.0
        else:
            duree_minutes = self.duree.total_seconds() / 60
            self.vitesse_minkm = round(duree_minutes / self.distance, 2)
        return self.vitesse_minkm

    def afficher_course(self):
        vitesse_str = f"{self.vitesse_minkm:.2f}" if self.vitesse_minkm is not None else "N/A"
        print(
            f"Course: {self.titre}, Distance: {self.distance} km, "
            f"Dénivelé: {self.denivele} m, Vitesse: {vitesse_str} min/km"
        )

    def afficher_details(self):
        self.calculer_vitesse_course()
        self.afficher_course()
