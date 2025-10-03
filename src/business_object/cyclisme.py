from datetime import date, timedelta
from business_object.activite import Activite


class Cyclisme(Activite):
    def __init__(self, id_activite: int, id_user: int, date: date, type_sport: str,
                 distance: float, duree: timedelta, trace: str, id_parcours: int,
                 titre: str, description: str,
                 id_cyclisme: int, denivele: float, vitesse_kmh: float):
        super().__init__(id_activite, id_user, date, type_sport, distance, duree,
                         trace, id_parcours, titre, description)
        self.id_cyclisme = id_cyclisme
        self.denivele = denivele
        self.vitesse_kmh = vitesse_kmh

    def afficher_details(self):
        print(f"Cyclisme: {self.titre}, Distance: {self.distance} km, Vitesse: {self.vitesse_kmh}"
              "km/h")
