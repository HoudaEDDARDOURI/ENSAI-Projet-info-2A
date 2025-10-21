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
                        INSERT INTO app.parcours(
                             depart, arrivee, id_activite, id_user
                        ) VALUES (
                             %(depart)s, %(arrivee)s,%(id_activite)s,%(id_user)s
                        )
                        RETURNING id_parcours;
                        """,
                        {
                            "depart": parcours.depart,
                            "arrivee": parcours.arrivee,
                            "id_activite": parcours.id_activite,
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
