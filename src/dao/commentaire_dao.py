import logging
import psycopg2
from dao.db_connection import DBConnection
from business_object.commentaire import Commentaire
from utils.singleton import Singleton


class CommentaireDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux commentaires de la base de données"""

    def creer(self, commentaire: Commentaire) -> bool:
        """Crée un nouveau commentaire dans la base."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO commentaire (
                            contenu, date, id_user, id_activite
                        )
                        VALUES (
                            %(contenu)s, %(date)s, %(id_user)s, %(id_activite)s
                        )
                        RETURNING id_commentaire;
                        """,
                        {
                            "contenu": commentaire.contenu,
                            "date": commentaire.date,
                            "id_user": commentaire.id_user,
                            "id_activite": commentaire.id_activite,
                        },
                    )
                    res = cursor.fetchone()
                    if res:
                        commentaire.id_commentaire = res["id_commentaire"]
                        return True
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL (CREATE commentaire) : {e.pgerror or e}")
        except Exception as e:
            logging.exception("Erreur inattendue (CREATE commentaire)")
        return False

    def lire(self, id_commentaire: int) -> Commentaire | None:
        """Récupère un commentaire avec son identifiant."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM commentaire
                        WHERE id_commentaire = %(id)s;
                        """,
                        {"id": id_commentaire},
                    )
                    res = cursor.fetchone()
                    if res:
                        return Commentaire(
                            id_commentaire=res["id_commentaire"],
                            contenu=res["contenu"],
                            date=res["date"],
                            id_user=res["id_user"],
                            id_activite=res["id_activite"],
                        )
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror or e}")
        except Exception as e:
            logging.exception("Erreur inattendue dans la lecture du commentaire")
        return None

    def modifier(self, commentaire: Commentaire) -> bool:
        """Met à jour le contenu ou la date d’un commentaire existant."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE commentaire
                        SET
                            contenu = %(contenu)s,
                            date = %(date)s
                        WHERE id_commentaire = %(id_commentaire)s;
                        """,
                        {
                            "id_commentaire": commentaire.id_commentaire,
                            "contenu": commentaire.contenu,
                            "date": commentaire.date,
                        },
                    )
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL (UPDATE commentaire) : {e.pgerror or e}")
        except Exception as e:
            logging.exception("Erreur inattendue (UPDATE commentaire)")
        return False

    def supprimer(self, id_commentaire: int) -> bool:
        """Supprime un commentaire."""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM commentaire WHERE id_commentaire = %(id)s;",
                        {"id": id_commentaire},
                    )
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL (DELETE commentaire) : {e.pgerror or e}")
        except Exception as e:
            logging.exception("Erreur inattendue (DELETE commentaire)")
        return False