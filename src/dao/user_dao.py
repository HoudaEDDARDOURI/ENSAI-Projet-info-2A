from dotenv import load_dotenv
import os

load_dotenv()  # charge les variables depuis le fichier .env

host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
database = os.environ['POSTGRES_DATABASE']


import logging
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from business_object.user import User

class UserDao(metaclass=Singleton):

    def creer(self, user: User) -> bool:
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO users(prenom, nom, username, mot_de_passe)
                        VALUES (%(prenom)s, %(nom)s, %(username)s, %(mot_de_passe)s)
                        RETURNING id_user, created_at;
                        """,
                        {
                            "prenom": user.prenom,
                            "nom": user.nom,
                            "username": user.username,
                            "mot_de_passe": user.mot_de_passe,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.error(f"Erreur lors de la création d'un utilisateur : {e}")

        if res:
            user.id_user = res["id_user"]
            user.created_at = res["created_at"]
            return True
        return False

    def lire(self, id_user: int) -> User | None:
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
            logging.error(f"Erreur lors de la lecture d'un utilisateur : {e}")

        if res:
            return User(
                id_user=res["id_user"],
                prenom=res["prenom"],
                nom=res["nom"],
                username=res["username"],
                mot_de_passe=res["mot_de_passe"],
                created_at=res["created_at"],
            )
        return None
