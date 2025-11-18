import logging
import psycopg2
from dao.db_connection import DBConnection
from business_object.commentaire import Commentaire
from utils.singleton import Singleton


class CommentaireDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux commentaires de la base de données"""

    def creer(self, commentaire: Commentaire) -> bool:
        """
        Crée un nouveau commentaire dans la base.
        created_at est géré automatiquement par la BD (DEFAULT CURRENT_TIMESTAMP)
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO commentaire (
                            contenu, id_user, id_activite
                        )
                        VALUES (
                            %(contenu)s, %(id_user)s, %(id_activite)s
                        )
                        RETURNING id_commentaire, created_at;
                        """,
                        {
                            "contenu": commentaire.contenu,
                            "id_user": commentaire.id_user,
                            "id_activite": commentaire.id_activite,
                        },
                    )
                    res = cursor.fetchone()
                    if res:
                        commentaire.id_commentaire = res["id_commentaire"]
                        commentaire.created_at = res["created_at"]  # Récupérer created_at de la BD
                        return True
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL (CREATE commentaire) : {e.pgerror or e}")
        except Exception:
            logging.exception("Erreur inattendue (CREATE commentaire)")
        return False

    def lire_par_activite(self, id_activite: int) -> list[Commentaire]:
        """Récupère tous les commentaires associés à une activité."""
        commentaires = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM commentaire
                        WHERE id_activite = %(id_activite)s
                        ORDER BY created_at ASC;
                        """,
                        {"id_activite": id_activite},
                    )
                    results = cursor.fetchall()
                    for res in results:
                        commentaires.append(
                            Commentaire(
                                id_commentaire=res["id_commentaire"],
                                contenu=res["contenu"],
                                created_at=res["created_at"],
                                id_user=res["id_user"],
                                id_activite=res["id_activite"],
                            )
                        )
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror or e}")
        except Exception as e:
            logging.exception(f"Erreur inattendue dans la lecture des commentaires : {e}")
        return commentaires

    def modifier(self, commentaire: Commentaire) -> bool:
        """
        Met à jour le contenu d'un commentaire existant.
        created_at n'est pas modifiable.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE commentaire
                        SET contenu = %(contenu)s
                        WHERE id_commentaire = %(id_commentaire)s;
                        """,
                        {
                            "id_commentaire": commentaire.id_commentaire,
                            "contenu": commentaire.contenu,
                        },
                    )
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            logging.error(f"Erreur SQL (UPDATE commentaire) : {e.pgerror or e}")
        except Exception:
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
        except Exception:
            logging.exception("Erreur inattendue (DELETE commentaire)")
        return False
    
    def compter_commentaires(self, id_activite: int) -> int:
        """
        Compte le nombre de commentaires pour une activité.
        
        Parameters:
        - id_activite: ID de l'activité
        
        Returns:
        - Nombre de commentaires
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT COUNT(*) as count
                        FROM commentaire
                        WHERE id_activite = %(id_activite)s;
                        """,
                        {"id_activite": id_activite}
                    )
                    res = cursor.fetchone()
                    return res["count"] if res else 0
        except Exception as e:
            logging.error(f"Erreur lors du comptage des commentaires pour l'activité {id_activite}: {e}")
            return 0