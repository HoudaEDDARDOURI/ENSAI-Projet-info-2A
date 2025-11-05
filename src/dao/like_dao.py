import logging
from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.like import Like


class LikeDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux likes de la base de données"""

    def creer(self, like: Like) -> bool:
        """Création d'un like dans la base de données"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO likes (
                            id_user, id_activite
                        ) VALUES (
                            %(id_user)s, %(id_activite)s
                        )
                        RETURNING id_like;
                        """,
                        {
                            "id_user": like.id_user,
                            "id_activite": like.id_activite,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la création du like : {e}")

        created = False
        if res:
            like.id_like = res["id_like"]
            created = True

        return created
    
    def lire_par_activite(self, id_activite: int) -> list[Like]:
        """Récupère tous les likes associés à une activité."""
        likes = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM likes WHERE id_activite = %(id_activite)s;",
                        {"id_activite": id_activite},
                    )
                    results = cursor.fetchall()
                    for res in results:
                        likes.append(
                            Like(
                                id_like=res["id_like"],
                                id_user=res["id_user"],
                                id_activite=res["id_activite"],
                                created_at=res["created_at"],
                            )
                        )
        except Exception as e:
            logging.error(f"Erreur lors de la lecture des likes pour l'activité {id_activite}:{e}")

        return likes

    def supprimer(self, id_like: int) -> bool:
        """Supprime un like par son ID"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM likes WHERE id_like = %(id_like)s RETURNING id_like;",
                        {"id_like": id_like},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du like : {e}")

        deleted = False
        if res:
            deleted = True
        return deleted

    
