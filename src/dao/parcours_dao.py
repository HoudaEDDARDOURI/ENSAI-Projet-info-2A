import logging
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from business_object.parcours import Parcours


class ParcoursDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux parcours de la base de données"""

    def creer(self, parcours: Parcours) -> bool:
        """Création d'un parcours dans la base de données"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO app.parcours(depart, arrivee, id_activite, id_user) 
                        VALUES (%(depart)s, %(arrivee)s, %(id_activite)s, %(id_user)s) 
                        RETURNING id_parcours;
                        """,
                        {
                            "depart": parcours.depart,
                            "arrivee": parcours.arrivee,
                            "id_activite": parcours.id_activite if parcours.id_activite is not None else None,
                            "id_user": parcours.id_user,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la création du parcours : {e}")
            created = False
            if res:
                parcours.id_parcours = res["id_parcours"]
                created = True
        return created

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
