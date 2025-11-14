from dotenv import load_dotenv
import os
import logging
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from business_object.user import User
from psycopg import errors
from typing import List

load_dotenv()  # charge les variables depuis le fichier .env
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
database = os.environ['POSTGRES_DATABASE']


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
        except errors.UniqueViolation as e:
            logging.error(f"Erreur : username déjà utilisé : {e}")
            return False
        except errors.Error as e:
            logging.error(f"Erreur base de données SQL : {e}")
            return False

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
                        "SELECT * FROM users WHERE id_user = %(id_user)s;",
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

    def supprimer(self, id_user: int) -> bool:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM users WHERE id_user = %(id_user)s;",
                        {"id_user": id_user}
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de l'utilisateur {id_user} : {e}")
            return False

    def se_connecter(self, username: str, mot_de_passe: str) -> tuple[User | None, str]:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE username = %(username)s;",
                        {"username": username}
                    )
                    res = cursor.fetchone()
                    if not res:
                        return None, "Utilisateur non trouvé"
                    
                    # Vérifier le mot de passe
                    from utils.securite import verify_password
                    if not verify_password(mot_de_passe, res["mot_de_passe"]):
                        return None, "Mot de passe incorrect"

                    # Tout est OK
                    user = User(
                        id_user=res["id_user"],
                        prenom=res["prenom"],
                        nom=res["nom"],
                        username=res["username"],
                        mot_de_passe=res["mot_de_passe"],
                        created_at=res["created_at"],
                    )
                    return user, "Connexion réussie"

        except errors.ConnectionException:
            return None, "Erreur de connexion à la base de données"
        except errors.Error as e:
            return None, f"Erreur SQL : {e}"
        except Exception as e:
            return None, f"Erreur inattendue : {e}"

    def trouver_par_username(self, username: str) -> User | None:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE username = %(username)s;",
                        {"username": username}
                    )
                    res = cursor.fetchone()
                    if res:
                        return User(
                            id_user=res["id_user"],
                            prenom=res["prenom"],
                            nom=res["nom"],
                            username=res["username"],
                            mot_de_passe=res["mot_de_passe"],
                            created_at=res["created_at"],
                        )
        except Exception as e:
            logging.error(f"Erreur lors de la recherche d'un utilisateur par username : {e}")
        return None

    def ajouter_suivi(self, id_user: int, id_autre_user: int) -> str:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO app.follow (id_follower, id_followed)
                        VALUES (%(id_user)s, %(id_autre_user)s)
                        ON CONFLICT DO NOTHING
                        RETURNING id_follow;
                        """,
                        {"id_user": id_user, "id_autre_user": id_autre_user}
                    )
                    res = cursor.fetchone()
                    if res:
                        return "suivi_ajoute"
                    else:
                        return "deja_suivi"
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout d'un suivi : {e}")
            return "erreur"

    def lister_followers(self, user: User) -> list[User]:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT u.*
                        FROM app.follow f
                        JOIN app.users u ON u.id_user = f.id_follower
                        WHERE f.id_followed = %(id_user)s;
                        """,
                        {"id_user": user.id_user}
                    )
                    resultats = cursor.fetchall()
                    return [
                        User(
                            id_user=r["id_user"],
                            prenom=r["prenom"],
                            nom=r["nom"],
                            username=r["username"],
                            mot_de_passe=r["mot_de_passe"],
                            created_at=r["created_at"]
                        )
                        for r in resultats
                    ]
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des followers : {e}")
            return []

    def modifier(self, user: User) -> bool:
        """Modification d'un utilisateur dans la base de données

        Parameters
        ----------
        user : User

        Returns
        -------
        success : bool
            True si la modification est un succès, False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE app.users
                        SET prenom      = %(prenom)s,
                            nom         = %(nom)s,
                            username    = %(username)s,
                            mot_de_passe = %(mot_de_passe)s
                        WHERE id_user = %(id_user)s;
                        """,
                        {
                            "prenom": user.prenom,
                            "nom": user.nom,
                            "username": user.username,
                            "mot_de_passe": user.mot_de_passe,
                            "id_user": user.id_user,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.error(f"Erreur lors de la modification de l'utilisateur : {e}")

        return res == 1

    def lister_followed(self, user: User) -> list[User]:
        """Liste les utilisateurs que l'utilisateur suit (followed)"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT u.*
                        FROM app.follow f
                        JOIN app.users u ON u.id_user = f.id_followed
                        WHERE f.id_follower = %(id_user)s;
                        """,
                        {"id_user": user.id_user}
                    )
                    resultats = cursor.fetchall()
                    return [
                        User(
                            id_user=r["id_user"],
                            prenom=r["prenom"],
                            nom=r["nom"],
                            username=r["username"],
                            mot_de_passe=r["mot_de_passe"],
                            created_at=r["created_at"]
                        )
                        for r in resultats
                    ]
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des followed : {e}")
            return []

    def lister_tous_les_users(self) -> List[User]:
        """Récupère tous les utilisateurs de la base de données."""
        users: List[User] = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_user, prenom, nom, username, mot_de_passe
                        FROM app.users;
                        """
                    )
                    results = cursor.fetchall()

                    for res in results:
                        users.append(
                            User(
                                id_user=res["id_user"],
                                prenom=res["prenom"],
                                nom=res["nom"],
                                username=res["username"],
                                password=res["mot_de_passe"],
                            )
                        )
        except errors.Error as e:
            logging.error(f"Erreur SQL : {e.pgerror}")
        except Exception:
            logging.exception("Erreur inattendue lors de la récupération des utilisateurs")

        return users
