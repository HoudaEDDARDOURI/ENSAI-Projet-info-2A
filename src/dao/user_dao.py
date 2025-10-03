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
