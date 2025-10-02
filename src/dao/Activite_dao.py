import logging
from dao.db_connection import DBConnection
from business_object.activite import Activite
from utils.singleton import Singleton

class ActiviteDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux activités de la base de données"""

    def creer(self, activite: Activite) -> bool:
        """Création d'une activité dans la base de données"""
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO app.activite(
                            id_user, type_sport, distance, duree, trace, id_parcours, titre, description
                        ) VALUES (
                            %(id_user)s, %(type_sport)s, %(distance)s, %(duree)s, %(trace)s,
                            %(id_parcours)s, %(titre)s, %(description)s
                        )
                        RETURNING id_activite;
                        """,
                        {
                            "id_user": activite.id_user,
                            "type_sport": activite.type_sport,
                            "distance": activite.distance,
                            "duree": activite.duree,
                            "trace": activite.trace,
                            "id_parcours": activite.id_parcours,
                            "titre": activite.titre,
                            "description": activite.description,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la création de l'activité : {e}")

        created = False
        if res:
            activite.id_activite = res["id_activite"]
            created = True

        return created
