import logging
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from business_object.parcours import Parcours


class ParcoursDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux parcours de la base de données"""

    def creer(self, parcours: Parcours) -> bool:
        """Création d'un parcours dans la base de données"""
        try:
            # Validation : on doit avoir soit id_activite, soit depart et arrivee
            if not parcours.id_activite and (not parcours.depart or not parcours.arrivee):
                raise ValueError("Un parcours doit avoir soit un id_activite soit des informations de départ et d'arrivée.")

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO app.parcours(depart, arrivee, id_activite, id_user) 
                        VALUES (%(depart)s, %(arrivee)s, %(id_activite)s, %(id_user)s) 
                        RETURNING id_parcours;
                        """,
                        {
                            "depart": parcours.depart if parcours.depart else None,  # Utilise None si depart est vide
                            "arrivee": parcours.arrivee if parcours.arrivee else None,  # Utilise None si arrivee est vide
                            "id_activite": parcours.id_activite if parcours.id_activite else None,  # Accepte None si pas d'activité
                            "id_user": parcours.id_user,  # User id doit aussi être présent
                        },
                    )
                    # Récupérer l'ID du parcours créé
                    res = cursor.fetchone()
                    if res:
                        parcours.id_parcours = res["id_parcours"]
                        return True
                    return False
        except Exception as e:
            logging.error(f"Erreur lors de la création du parcours : {e}")
            return False

            
    def lire(self, id_parcours: int) -> Parcours | None:
        """Récupère un parcours à partir de son ID"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM app.parcours WHERE id_parcours = %(id_parcours)s;",
                        {"id_parcours": id_parcours},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du parcours : {e}")

        parcours = None
        if res:
            parcours = Parcours(
                id_parcours=res["id_parcours"],
                depart=res["depart"],
                arrivee=res["arrivee"],
                id_activite=res["id_activite"] if res["id_activite"] is not None else None,
                id_user=res["id_user"],
            )
        return parcours

    def modifier(self, parcours: Parcours) -> bool:
        """Mise à jour d'un parcours"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE app.parcours
                        SET depart = %(depart)s,
                            arrivee = %(arrivee)s,
                            id_activite = %(id_activite)s,
                            id_user = %(id_user)s
                        WHERE id_parcours = %(id_parcours)s
                        RETURNING id_parcours;
                        """,
                        {
                            "depart": parcours.depart,
                            "arrivee": parcours.arrivee,
                            "id_activite": parcours.id_activite if parcours.id_activite is not None else None,
                            "id_user": parcours.id_user,
                            "id_parcours": parcours.id_parcours,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour du parcours : {e}")

        updated = False
        if res:
            updated = True
        return updated

    def supprimer(self, id_parcours: int) -> bool:
        """Supprime un parcours par son ID"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """DELETE FROM app.parcours WHERE id_parcours = %(id_parcours)s
                        RETURNING id_parcours;""",
                        {"id_parcours": id_parcours},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du parcours : {e}")

        deleted = False
        if res:
            deleted = True
        return deleted
