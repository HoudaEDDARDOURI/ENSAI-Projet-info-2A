import logging
import psycopg2
from typing import List
from dao.db_connection import DBConnection
from business_object.activite import Activite
from business_object.course import Course
from business_object.natation import Natation
from business_object.cyclisme import Cyclisme
from business_object.user import User
from utils.singleton import Singleton
from typing import List


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
                            id_user, date_activite, type_sport, distance, duree, trace,
                            titre, description, denivele
                        ) VALUES (
                            %(id_user)s, %(date_activite)s, %(type_sport)s, %(distance)s, %(duree)s,
                            %(trace)s, %(titre)s, %(description)s, %(denivele)s
                        )
                        RETURNING id_activite;
                        """,
                        {
                            "id_user": activite.id_user,
                            "date_activite": activite.date,
                            "type_sport": activite.type_sport,
                            "distance": activite.distance,
                            "duree": activite.duree,
                            "trace": activite.trace,
                            "titre": activite.titre,
                            "description": activite.description,
                            "denivele": activite.denivele if hasattr(activite, 'denivele') else 0.0
                        },
                    )
                    res = cursor.fetchone()
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror}")
        except Exception:
            logging.exception("Erreur inattendue lors de la création de l'activité")

        created = False
        if res:
            activite.id_activite = res["id_activite"]
            created = True

        return created
    def lire(self, id_activite: int) -> Activite:
        """Récupère une activité par son ID."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM activite
                        WHERE id_activite = %(id_activite)s;
                        """,
                        {"id_activite": id_activite},
                    )
                    result = cursor.fetchone()

                    if result:
                        type_sport = result["type_sport"].lower()

                        # Sélectionner la sous-classe en fonction du type de sport
                        if type_sport == "course":
                            return Course(
                                id_activite=result["id_activite"],
                                id_user=result["id_user"],
                                date=result["date_activite"],
                                distance=result["distance"],
                                duree=result["duree"],
                                trace=result["trace"],
                                titre=result["titre"],
                                description=result["description"],
                                denivele=result.get("denivele", 0.0)
                            )
                        elif type_sport == "cyclisme":
                            return Cyclisme(
                                id_activite=result["id_activite"],
                                id_user=result["id_user"],
                                date=result["date_activite"],
                                distance=result["distance"],
                                duree=result["duree"],
                                trace=result["trace"],
                                titre=result["titre"],
                                description=result["description"],
                                denivele=result.get("denivele", 0.0)
                            )
                        elif type_sport == "natation":
                            return Natation(
                                id_activite=result["id_activite"],
                                id_user=result["id_user"],
                                date=result["date_activite"],
                                distance=result["distance"],
                                duree=result["duree"],
                                trace=result["trace"],
                                titre=result["titre"],
                                description=result["description"],
                                denivele=result.get("denivele", 0.0)
                            )
                        else:
                            logging.warning(f"Type d'activité inconnu : {type_sport}")
                            return None
                    else:
                        logging.warning(f"Aucune activité trouvée avec l'ID {id_activite}")
                        return None

        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror}")
        except Exception:
            logging.exception("Erreur inattendue lors de la récupération de l'activité")
        return None

    def lire_activites_par_user(self, id_user: int) -> List[Activite]:
        """Récupère toutes les activités d'un utilisateur par son ID."""
        activites: List[Activite] = []

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM activite
                        WHERE id_user = %(id_user)s
                        ORDER BY date_activite DESC;
                        """,
                        {"id_user": id_user},
                    )
                    results = cursor.fetchall()

                    for res in results:
                        type_sport = res["type_sport"].lower()

                        # Sélectionner la sous-classe en fonction du type de sport
                        if type_sport == "course":
                            activites.append(
                                Course(
                                    id_activite=res["id_activite"],
                                    id_user=res["id_user"],
                                    date=res["date_activite"],
                                    distance=res["distance"],
                                    duree=res["duree"],
                                    trace=res["trace"],
                                    titre=res["titre"],
                                    description=res["description"],
                                    denivele=res.get("denivele", 0.0)
                                )
                            )
                        elif type_sport == "cyclisme":
                            activites.append(
                                Cyclisme(
                                    id_activite=res["id_activite"],
                                    id_user=res["id_user"],
                                    date=res["date_activite"],
                                    distance=res["distance"],
                                    duree=res["duree"],
                                    trace=res["trace"],
                                    titre=res["titre"],
                                    description=res["description"],
                                    denivele=res.get("denivele", 0.0)
                                )
                            )
                        elif type_sport == "natation":
                            activites.append(
                                Natation(
                                    id_activite=res["id_activite"],
                                    id_user=res["id_user"],
                                    date=res["date_activite"],
                                    distance=res["distance"],
                                    duree=res["duree"],
                                    trace=res["trace"],
                                    titre=res["titre"],
                                    description=res["description"],
                                    denivele=res.get("denivele", 0.0)
                                )
                            )
                        else:
                            logging.warning(f"Type d'activité inconnu : {type_sport}")

        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror}")
        except Exception:
            logging.exception("Erreur inattendue lors de la lecture des activités")

        return activites


    def modifier(self, activite: Activite) -> bool:
        """Met à jour les informations d’une activité existante."""
        if activite.id_activite is None:
            logging.error("L'ID de l'activité est nécessaire pour la modification.")
            return False
        
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    sql = """
                        UPDATE activite
                        SET type_sport = %(type_sport)s,
                            distance = %(distance)s,
                            duree = %(duree)s,
                            trace = %(trace)s,
                            titre = %(titre)s,
                            description = %(description)s
                    """
                    params = {
                        "id_activite": activite.id_activite,
                        "type_sport": activite.type_sport,
                        "distance": activite.distance,
                        "duree": activite.duree,
                        "trace": activite.trace,
                        "titre": activite.titre,
                        "description": activite.description,
                    }

                    # Si l'activité a un dénivelé, on l'ajoute à la requête
                    if hasattr(activite, "denivele"):
                        sql += ", denivele = %(denivele)s"
                        params["denivele"] = activite.denivele

                    sql += " WHERE id_activite = %(id_activite)s;"

                    cursor.execute(sql, params)
                    if cursor.rowcount == 0:
                        logging.warning(f"Aucune modification effectuée pour l'activité {activite.id_activite}")
                        return False  # Aucune ligne modifiée
                    return True
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror}")
        except Exception:
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
        except Exception:
            logging.exception("Erreur inattendue lors de la suppression de l'activité")
        return False
