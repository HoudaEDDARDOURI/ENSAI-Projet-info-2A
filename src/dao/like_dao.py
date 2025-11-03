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
                        INSERT INTO app.likes (
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

    def lire(self, id_like: int) -> Like | None:
        """Récupère toutes les informations d'un like à partir de son ID"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM app.likes WHERE id_like = %(id_like)s;",
                        {"id_like": id_like},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du like : {e}")

        like = None
        if res:
            like = Like(
                id_like=res["id_like"],
                id_user=res["id_user"],
                id_activite=res["id_activite"],
                created_at=res["created_at"],
            )

        return like

    def supprimer(self, id_like: int) -> bool:
        """Supprime un like par son ID"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM app.likes WHERE id_like = %(id_like)s RETURNING id_like;",
                        {"id_like": id_like},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du like : {e}")

        deleted = False
        if res:
            deleted = True
        return deleted

    