from datetime import date, timedelta

class Natation(Activite):
    def __init__(self, id_activite: int, id_user: int, date: date, type_sport: str,
                 distance: float, duree: timedelta, trace: str, id_parcours: int,
                 titre: str, description: str,
                 id_natation: int, vitesse_min100m: float = 0):
        super().__init__(id_activite, id_user, date, type_sport, distance, duree,
                         trace, id_parcours, titre, description)
        self.id_natation = id_natation
        self.vitesse_min100m = vitesse_min100m
    def afficher_details(self):
        print(f"Natation: {self.titre}, Distance: {self.distance} m, "
              f"Vitesse: {self.vitesse_min100m:.2f} min/100m")