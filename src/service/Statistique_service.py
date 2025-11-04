# Importations nécessaires
from business_object.user import User
from datetime import date, timedelta


class StatistiqueService():

    def __init__(self, user):
        if not isinstance(user, User):
            raise TypeError("L'attribut 'user' doit être une instance de la classe User.")
        self.user = user

    def get_nombre_services(self):
        """
        Calcule et retourne le nombre d'activités (services) de l'utilisateur.
        """
        return len(self.user.activites)

    # Nouvelle méthode utilitaire pour déterminer les bornes de la semaine
    def _get_bornes_semaine(self, date_reference):
        """
        Méthode utilitaire interne pour déterminer le début et la fin de la semaine
        à partir d'une date de référence. La semaine va du lundi au dimanche.

        Args:
            date_reference (datetime.date): Une date quelconque dans la semaine.

        Returns:
            tuple: Un tuple (date_debut_semaine, date_fin_semaine).
        """
        if not isinstance(date_reference, date):
            raise TypeError("date_reference doit être un objet datetime.date")

        jour_de_la_semaine = date_reference.isoweekday() # 1 pour Lundi, 7 pour Dimanche
        date_debut_semaine = date_reference - timedelta(days=jour_de_la_semaine - 1)
        date_fin_semaine = date_debut_semaine + timedelta(days=6)
        return date_debut_semaine, date_fin_semaine

    def calculer_temps_sport_par_semaine(self, date_reference):
        """
            Calcule la durée totale de sport (en minutes) effectuée par l'utilisateur
            pendant la semaine où se situe la date_reference.
        """
        # Utilise la méthode utilitaire pour obtenir les bornes de la semaine
        date_debut_semaine, date_fin_semaine = self._get_bornes_semaine(date_reference)

        total_duree_minutes = 0.0
        for activite in self.user.activites:
            if date_debut_semaine <= activite.date <= date_fin_semaine:
                total_duree_minutes += activite.duree
        return total_duree_minutes

    def calculer_kilometres_par_semaine(self, date_reference):
        """
        Calcule le nombre total de kilomètres parcourus par l'utilisateur
        pendant la semaine où se situe la date_reference.
        """
        # Utilise la méthode utilitaire pour obtenir les bornes de la semaine
        date_debut_semaine, date_fin_semaine = self._get_bornes_semaine(date_reference)

        total_kilometres = 0.0
        for activite in self.user.activites:
            if date_debut_semaine <= activite.date <= date_fin_semaine:
                total_kilometres += activite.distance
        return total_kilometres

