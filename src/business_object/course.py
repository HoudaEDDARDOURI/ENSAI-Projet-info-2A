from datetime import date, timedelta

class Course(Activite):
    def __init__(self, id_activite: int, id_user: int, date: date, type_sport: str,
                 distance: float, duree: timedelta, trace: str, id_parcours: int,
                 titre: str, description: str,
                 id_course: int, denivele: float, vitesse_minkm: float = 0):
        super().__init__(id_activite, id_user, date, type_sport, distance, duree,
                         trace, id_parcours, titre, description)
        self.id_course = id_course
        self.denivele = denivele
        self.vitesse_minkm = vitesse_minkm

        def afficher_details(self):
          print(f"Course: {self.titre}, Distance: {self.distance} km, "
              f"Dénivelé: {self.denivele} m, Vitesse: {self.vitesse_minkm:.2f} min/km")