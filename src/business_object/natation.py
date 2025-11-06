from datetime import date, timedelta
from business_object.activite import Activite


class Natation(Activite):
    def __init__(self, id_activite: int, id_user: int, date: date, distance: float,
                 duree: timedelta, trace: str, id_parcours: int,
                 titre: str, description: str, denivele: float = 0.0):
        super().__init__(id_activite=id_activite,
                         id_user=id_user,
                         date=date,
                         type_sport="natation",
                         distance=distance,
                         duree=duree,
                         trace=trace,
                         id_parcours=id_parcours,
                         titre=titre,
                         description=description)
        self.denivele = denivele
        self.vitesse_min100m = None  # reste None jusqu'au calcul

    def calculer_vitesse_natation(self) -> float:
        """
        Calcule la vitesse moyenne de la natation en minutes par 100 mètres.
        :return: vitesse en minutes pour 100 mètres
        """
        if self.distance <= 0 or self.duree.total_seconds() <= 0:
            self.vitesse_min100m = 0.0
        else:
            # Convertir la durée en minutes
            duree_minutes = self.duree.total_seconds() / 60
            # Temps pour 100 m
            vitesse_100m = (duree_minutes / self.distance) * 100
            self.vitesse_min100m = round(vitesse_100m, 2)
        return self.vitesse_min100m

    def afficher_details(self):
        # Gérer le cas où la vitesse n'a pas encore été calculée
        vitesse_str = f"{self.vitesse_min100m:.2f}" if self.vitesse_min100m is not None else "N/A"
        print(f"Natation: {self.titre}, Distance: {self.distance} m, "
              f"Vitesse: {vitesse_str} min/100m")
