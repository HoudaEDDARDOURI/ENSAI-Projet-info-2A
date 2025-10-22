import logging
from dao.db_connection import DBConnection
from utils.singleton import Singleton


class UserDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux utilissateurs de la base de données"""

    def creer(self, user) -> bool:
        """Creation d'un utilisateur dans la base de données

        Parameters
        ----------
        user : User

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO app.users(prenom, nom, username, mot_de_passe) VALUES        "
                        "(%(prenom)s, %(nom)s, %(username)s, %(mot_de_passe)s)             "
                        "  RETURNING id_user;                                                ",
                        {
                            "prenom": user.prenom,
                            "nom": user.nom,
                            "username": user.username,
                            "mot_de_passe": user.mot_de_passe,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            user.id_user = res["id_user"]
            created = True

        return created

    def update(self, user) -> bool:
        """Mise à jour d'un utilisateur"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE app.users
                        SET prenom = %(prenom)s,
                            nom = %(nom)s,
                            username = %(username)s,
                            mot_de_passe = %(mot_de_passe)s
                        WHERE id_user = %(id_user)s
                        RETURNING id_user;
                        """,
                        {
                            "prenom": user.prenom,
                            "nom": user.nom,
                            "username": user.username,
                            "mot_de_passe": user.mot_de_passe,
                            "id_user": user.id_user,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        updated = False
        if res:
            updated = True
        return updated

    def delete(self, id_user: int) -> bool:
        """Supprime un utilisateur par son ID"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM app.users WHERE id_user = %(id_user)s RETURNING id_user;",
                        {"id_user": id_user},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        deleted = False
        if res:
            deleted = True
        return deleted

    def read(self, id_user: int) -> User | None:
         """Récupère toutes les informations d'un utilisateur à partir de son ID"""
         res = None

        try:
            with DBConnection().connection as connection:
             with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM app.users WHERE id_user = %(id_user)s;",
                    {"id_user": id_user},
                )
                res = cursor.fetchone()
        except Exception as e:
        logging.info(e)

        user = None
        if res:
            user = User(
                id_user=res["id_user"],
                prenom=res["prenom"],
                nom=res["nom"],
                username=res["username"],
                mot_de_passe=res["mot_de_passe"],
            )
        return user