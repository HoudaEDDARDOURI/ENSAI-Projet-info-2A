import logging
import psycopg2
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
                        INSERT INTO activite(
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
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror}")
        except Exception as e:
            logging.exception("Erreur inattendue lors de la création de l'activité")

        created = False
        if res:
            activite.id_activite = res["id_activite"]
            created = True

        return created

    def lire(self, id_activite: int) -> Activite | None:
        """Récupère une activité par son identifiant."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM activite
                        WHERE id_activite = %(id)s;
                        """,
                        {"id": id_activite},
                    )
                    res = cursor.fetchone()
                    if res:
                        return Activite(
                            id_activite=res["id_activite"],
                            id_user=res["id_user"],
                            type_sport=res["type_sport"],
                            distance=res["distance"],
                            duree=res["duree"],
                            trace=res["trace"],
                            id_parcours=res["id_parcours"],
                            titre=res["titre"],
                            description=res["description"],
                        )
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror}")
        except Exception as e:
            logging.exception("Erreur inattendue lors de la lecture de l'activité")
        return None

    def modifier(self, activite: Activite) -> bool:
        """Met à jour les informations d’une activité existante."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE activite
                        SET
                            type_sport = %(type_sport)s,
                            distance = %(distance)s,
                            duree = %(duree)s,
                            trace = %(trace)s,
                            id_parcours = %(id_parcours)s,
                            titre = %(titre)s,
                            description = %(description)s
                        WHERE id_activite = %(id_activite)s;
                        """,
                        {
                            "id_activite": activite.id_activite,
                            "type_sport": activite.type_sport,
                            "distance": activite.distance,
                            "duree": activite.duree,
                            "trace": activite.trace,
                            "id_parcours": activite.id_parcours,
                            "titre": activite.titre,
                            "description": activite.description,
                        },
                    )
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror}")
        except Exception as e:
            logging.exception("Erreur inattendue lors de la modification de l'activité")
        return False

    def supprimer(self, id_activite: int) -> bool:
        """Supprime une activité."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM activite WHERE id_activite = %(id)s;",
                        {"id": id_activite},
                    )
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror}")
        except Exception as e:
            logging.exception("Erreur inattendue lors de la suppression de l'activité")
        return False