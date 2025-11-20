from datetime import date, timedelta
from business_object.activite import Activite


class Cyclisme(Activite):
    def __init__(self, id_activite: int, id_user: int, date: date, distance: float,
                 duree: timedelta, trace: str,
                 titre: str, description: str):
        super().__init__(id_activite=id_activite,
                         id_user=id_user,
                         date=date,
                         type_sport="cyclisme",
                         distance=distance,
                         duree=duree,
                         trace=trace,
                         titre=titre,
                         description=description)
        self.vitesse_kmh = None

    def afficher_details(self):
        print(f"Cyclisme: {self.titre}, Distance: {self.distance} km, Vitesse: {self.vitesse_kmh}"
              "km/h")
              
    def calculer_vitesse_cyclisme(self) -> float:
        """Calcule la vitesse moyenne du cycliste en km/h."""
        duree_heures = self.duree.total_seconds() / 3600  # convertir la durée en heures
        if duree_heures > 0:
            self.vitesse_kmh = round(self.distance / duree_heures, 2)
        else:
            self.vitesse_kmh = 0.0
        return self.vitesse_kmh         
