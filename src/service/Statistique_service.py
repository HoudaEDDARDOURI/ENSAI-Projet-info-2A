from business_object.user import User
from datetime import date, timedelta
import statistics


class StatistiqueService():

    def __init__(self, user):
        if not isinstance(user, User):
            raise TypeError("L'attribut 'user' doit être une instance de la classe User.")
        self.user = user

    def _safe_date_comparison(self, activite_date, debut_semaine: date, fin_semaine: date) -> bool:
        """
        Convertit activite_date en objet date si nécessaire et effectue la comparaison.
        Retourne False si la date est None ou non convertible.
        """
        if activite_date is None:
            return False

        if isinstance(activite_date, date):
            date_a_comparer = activite_date
        elif isinstance(activite_date, str):
            try:
                # Tenter la conversion depuis le format ISO
                date_a_comparer = date.fromisoformat(activite_date)
            except ValueError:
                # La chaîne n'est pas un format de date valide. On ignore l'activité.
                return False
        else:
            return False

        return debut_semaine <= date_a_comparer <= fin_semaine

    def get_nombre_services_semaine(self, date_reference):
        """Calcule et retourne le nombre d'activités (services)
        de l'utilisateur au cours de la semaine de la date_reference."""

        debut_semaine, fin_semaine = self._get_bornes_semaine(date_reference)

        activites_semaine = [
            a for a in self.user.activites
            if self._safe_date_comparison(a.date, debut_semaine, fin_semaine)
        ]

        return len(activites_semaine)

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

        jour_de_la_semaine = date_reference.isoweekday()  # 1 pour Lundi, 7 pour Dimanche
        date_debut_semaine = date_reference - timedelta(days=jour_de_la_semaine - 1)
        date_fin_semaine = date_debut_semaine + timedelta(days=6)
        return date_debut_semaine, date_fin_semaine

    def calculer_temps_sport_par_semaine(self, date_reference):
        """
        Calcule la durée totale de sport (en minutes) effectuée par l'utilisateur
        pendant la semaine où se situe la date_reference.
        """
        date_debut_semaine, date_fin_semaine = self._get_bornes_semaine(date_reference)
        total_duree_minutes = 0.0
        for activite in self.user.activites:

            if self._safe_date_comparison(activite.date, date_debut_semaine, date_fin_semaine):

                if isinstance(activite.duree, timedelta):

                    total_duree_minutes += activite.duree.total_seconds() / 60

        return total_duree_minutes

    """def _convertir_duree_vers_minutes(self, duree_str: str) -> float:
        """"""Convertit une durée de HH:MM:SS en minutes (float).""""""
        if not duree_str:
            return 0.0

        try:
            heures, minutes, secondes = map(int, duree_str.split(':'))
            total_minutes = heures * 60 + minutes + secondes / 60
            return total_minutes
        except ValueError:
            # Gérer le cas où la chaîne est mal formatée
            try:
                # Tente de convertir directement si ce n'est pas HH:MM:SS
                return float(duree_str) 
            except (ValueError, TypeError):
                return 0.0  # Retourne 0 si la conversion échoue"""

    def calculer_kilometres_par_semaine(self, date_reference):
        """
        Calcule le nombre total de kilomètres parcourus par l'utilisateur
        pendant la semaine où se situe la date_reference.
        """
        # Utilise la méthode utilitaire pour obtenir les bornes de la semaine
        date_debut_semaine, date_fin_semaine = self._get_bornes_semaine(date_reference)

        total_kilometres = 0.0
        for activite in self.user.activites:
            if self._safe_date_comparison(activite.date, date_debut_semaine, date_fin_semaine):
                distance_value = activite.distance if activite.distance is not None else 0.0
                try:
                    total_kilometres += float(distance_value)
                except (ValueError, TypeError):
                    pass
        return total_kilometres

    def get_vitesse_moyenne_par_sport(self, date_reference: date, type_sport: str) -> float:
        """
        Calcule la vitesse moyenne pour un type de sport donné pendant la semaine
        où se situe la date_reference. L'unité est déterminée par la classe d'activité
        (ex: course en min/km, cyclisme en km/h, natation en min/100m).
        """
        date_debut_semaine, date_fin_semaine = self._get_bornes_semaine(date_reference)

        activites_filtrees = [
            a for a in self.user.activites
            if self._safe_date_comparison(a.date, date_debut_semaine, date_fin_semaine) and a.type_sport.lower() == type_sport.lower()
        ]

        vitesses = []
        for activite in activites_filtrees:

            if hasattr(activite, 'calculer_vitesse'):
                vitesse = activite.calculer_vitesse()
                if vitesse > 0:
                    vitesses.append(vitesse)

        if not vitesses:
            return 0.0

        vitesse_moyenne = statistics.mean(vitesses)

        return round(vitesse_moyenne, 2)

    # Partie graphique

    def get_distances_par_sport_semaine(self, date_reference: date) -> dict:
        """
        Calcule et retourne la distance totale par type de sport pour la semaine sélectionnée.
        Les distances sont retournées en KM (l'unité de base dans vos Activite).
        """
        date_debut_semaine, date_fin_semaine = self._get_bornes_semaine(date_reference)
        distances = {}

        for activite in self.user.activites:
            if self._safe_date_comparison(activite.date, date_debut_semaine, date_fin_semaine):
                sport = activite.type_sport.lower()
                distance_value = activite.distance if activite.distance is not None else 0.0

                try:
                    distances[sport] = distances.get(sport, 0.0) + float(distance_value)
                except (ValueError, TypeError):
                    continue

        return {k: round(v, 2) for k, v in distances.items()}

    def get_duree_par_jour_semaine(self, date_reference: date) -> list[dict]:
        """
        Calcule et retourne la durée totale d'activité (en minutes) pour chaque jour de la semaine.
        Retourne une liste de dictionnaires pour faciliter l'utilisation avec pandas/Streamlit.
        """
        date_debut_semaine, date_fin_semaine = self._get_bornes_semaine(date_reference)

        jours_semaine = {
            (date_debut_semaine + timedelta(days=i)): 0.0 for i in range(7)
        }

        for activite in self.user.activites:
            if isinstance(activite.duree, timedelta) and self._safe_date_comparison(activite.date, date_debut_semaine, date_fin_semaine):

                if isinstance(activite.date, str):
                    date_cle = date.fromisoformat(activite.date)
                else:
                    date_cle = activite.date

                duree_minutes = activite.duree.total_seconds() / 60

                if date_cle in jours_semaine:
                    jours_semaine[date_cle] += duree_minutes

        NOMS_JOURS = ["Lun.", "Mar.", "Mer.", "Jeu.", "Ven.", "Sam.", "Dim."]

        data_graph = []
        for i in range(7):
            jour_date = date_debut_semaine + timedelta(days=i)
            data_graph.append({
                "Jour": NOMS_JOURS[i],
                "Durée (min)": round(jours_semaine[jour_date], 1)
            })

        return data_graph

    # Partie prédiction

    def predire(self, type_sport, nb_entrainements=10):
        """
        Prédit une distance recommandée pour le prochain entraînement.

        Parameters:
            type_sport (str): Type de sport (Course, Natation, Cyclisme)
            nb_entrainements (int): Nombre d'entraînements à analyser (par défaut 10)

        Returns:
            float: Distance recommandée en km (ou m pour natation)
        """
        # Récupére les dernières activités pour ce type de sport
        dernieres_activites = self._recuperer_dernieres_activites(
            type_sport,
            nb_entrainements
        )

        # Si pas d'historique, retourne une distance par défaut
        if not dernieres_activites:
            return self._get_distance_defaut(type_sport)

        # Extrait les distances
        distances = [activite.distance for activite in dernieres_activites]

        # Calcule la moyenne
        moyenne_distance = statistics.mean(distances)

        # Calcule le coefficient de progression adaptatif
        coefficient = self._calculer_coefficient_progression(dernieres_activites)

        # Calcule la distance proposée
        distance_proposee = moyenne_distance * coefficient

        # Arrondit selon le sport
        return self._arrondir_distance(distance_proposee, type_sport)

    def _recuperer_dernieres_activites(self, type_sport, limite):
        """
        Récupère les N dernières activités de l'utilisateur pour un sport donné.
        """
        # Filtre les activités par type de sport
        activites_filtrees = [
            a for a in self.user.activites
            if a.type_sport.lower() == type_sport.lower()
        ]

        # Sécuriser et convertir la date avant le tri (méthode de sécurité)

        activites_valides = []
        DATE_MINIMALE = date(1900, 1, 1)  # Date de secours pour les entrées manquantes

        for a in activites_filtrees:
            date_obj = None
            if isinstance(a.date, str):
                try:
                    date_obj = date.fromisoformat(a.date)
                except ValueError:
                    # La date n'est pas convertible, on attribue la date minimale
                    date_obj = DATE_MINIMALE
            elif isinstance(a.date, date):
                date_obj = a.date

            # S'assurer qu'on a une date pour le tri
            if date_obj:
                a._sort_date = date_obj
                activites_valides.append(a)

        # 3. Trier par la nouvelle clé sécurisée
        activites_valides.sort(key=lambda a: a._sort_date, reverse=True)
        return activites_valides[:limite]

    def _calculer_coefficient_progression(self, activites):
        """
        Calcule un coefficient de progression adaptatif selon la tendance.

        Parameters:
            activites (list): Liste des activités récentes

        Returns:
            float: Coefficient multiplicateur (entre 1.03 et 1.10)
        """
        if len(activites) < 3:
            return 1.05  # Débutant : progression douce

        # Analyser la tendance sur les 3 derniers entraînements
        tendance = self._calculer_tendance(activites[:3])

        if tendance > 0.1:  # Progression > 10%
            return 1.10  # En forte progression : on peut pousser
        elif tendance < -0.1:  # Régression > 10%
            return 1.03  # En baisse : on y va doucement
        else:
            return 1.07  # Stable : progression standard

    def _calculer_tendance(self, activites):
        """
        Calcule la tendance de progression (positif = amélioration).

        Parameters:
            activites (list): Liste de 3 activités minimum

        Returns:
            float: Taux de progression (ex: 0.15 = +15%)
        """
        if len(activites) < 2:
            return 0.0

        # Comparer la distance la plus récente avec la plus ancienne
        distance_recente = activites[0].distance
        distance_ancienne = activites[-1].distance

        if distance_ancienne == 0:
            return 0.0

        return (distance_recente - distance_ancienne) / distance_ancienne

    def _get_distance_defaut(self, type_sport):
        """
        Retourne une distance de démarrage par défaut selon le sport.

        Parameters:
            type_sport (str): Type de sport

        Returns:
            float: Distance en km (ou m pour natation)
        """
        distances_defaut = {
            'course': 5.0,
            'natation': 500.0,
            'cyclisme': 20.0
        }
        return distances_defaut.get(type_sport.lower(), 5.0)

    def _arrondir_distance(self, distance, type_sport):
        """
        Arrondit la distance selon le sport.

        ATTENTION: Assurez-vous que la 'distance' reçue est toujours en KM,
        conformément à votre stockage BDD.
        """
        if type_sport.lower() == 'natation':
            distance_en_m = distance * 1000
            # Arrondi à 50m près
            distance_arrondie_m = round(distance_en_m / 50) * 50
            return distance_arrondie_m 

        elif type_sport.lower() == 'cyclisme':
            # Arrondi au km près
            return round(distance)
        else:
            # Arrondi à 0.5 km près
            return round(distance * 2) / 2

    def _formater_duree(self, total_minutes: float) -> str:
        """Convertit le temps total en minutes (float) en une chaîne formatée (HHh MMmin SSs)."""
        if total_minutes is None or total_minutes < 0:
            return "00h 00min 00s"

        total_secondes = int(total_minutes * 60)

        heures = total_secondes // 3600
        total_secondes %= 3600

        minutes = total_secondes // 60
        secondes = total_secondes % 60

        return f"{heures:02}h {minutes:02}min {secondes:02}s"

    def afficherStats(self, date_reference: date) -> dict:
        """
        Retourne les statistiques hebdomadaires de l'utilisateur.
        """
        if not isinstance(date_reference, date):
            raise TypeError("date_reference doit être un objet datetime.date")

        nb_activites = self.get_nombre_services_semaine(date_reference)
        temps_total_minutes = self.calculer_temps_sport_par_semaine(date_reference)
        distance_totale = self.calculer_kilometres_par_semaine(date_reference)
        temps_total_formatte = self._formater_duree(temps_total_minutes)

        vitesse_course = self.get_vitesse_moyenne_par_sport(date_reference, 'course')
        vitesse_cyclisme = self.get_vitesse_moyenne_par_sport(date_reference, 'cyclisme')
        vitesse_natation = self.get_vitesse_moyenne_par_sport(date_reference, 'natation')

        return {
            "Utilisateur": self.user.username,
            "Période": self._get_bornes_semaine(date_reference),
            "Statistiques": {
                "Nombre d'activités": nb_activites,
                "Temps total d'activité": temps_total_formatte,
                "Distance totale en kilomètres": round(distance_totale, 2),
                "Vitesse moyenne course (min/km)": vitesse_course,
                "Vitesse moyenne cyclisme (km/h)": vitesse_cyclisme,
                "Vitesse moyenne natation (min/100m)": vitesse_natation,
            }
        }