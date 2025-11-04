import logging
from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.follows import Follow


class FollowDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux relations de suivi (follow)"""

    def creer(self, follow: Follow) -> bool:
        """Création d'une relation follow dans la base de données"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO follow (id_followed, id_follower)
                        VALUES (%(id_followed)s, %(id_follower)s)
                        RETURNING id_follow;
                        """,
                        {
                            "id_followed": follow.id_followed,
                            "id_follower": follow.id_follower,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la création du follow : {e}")
        created = False
        if res:
            follow.id_follow = res["id_follow"]
            created = True
        return created

    def lire(self, id_follow: int) -> Follow | None:
        """Récupère toutes les informations d'une relation follow par son ID"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM follow WHERE id_follow = %(id_follow)s;",
                        {"id_follow": id_follow},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la lecture du follow : {e}")
        follow = None
        if res:
            follow = Follow(
                id_follow=res["id_follow"],
                id_followed=res["id_followed"],
                id_follower=res["id_follower"],
                created_at=res["created_at"],
            )
        return follow

    def supprimer(self, id_follow: int) -> bool:
        """Supprime une relation follow par son ID"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM follow WHERE id_follow = %(id_follow)s RETURNING id_follow;",
                        {"id_follow": id_follow},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du follow : {e}")

        deleted = False
        if res:
            deleted = True
        return deleted
