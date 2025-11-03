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

    def afficher_details(self):
        print(f"Course: {self.titre}, Distance: {self.distance} km, "
                f"Dénivelé: {self.denivele} m, Vitesse: {self.vitesse_minkm:.2f} min/km")
