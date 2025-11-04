import os
import logging
import dotenv

from utils.log_decorator import log
from utils.singleton import Singleton
from dao.db_connection import DBConnection

from service.user_service import UserService


class ResetDatabase(metaclass=Singleton):
    """Réinitialisation de la base de données à partir de init_db.sql"""

    @log
    def lancer(self, test_dao=False):
        """Réinitialise la base de données. Si test_dao=True, utilise le schéma de test."""
        dotenv.load_dotenv()

        schema_name = "projet_test_dao" if test_dao else os.environ.get("POSTGRES_SCHEMA", "public")
        create_schema = f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; CREATE SCHEMA {schema_name};"

        # Charger le fichier init_db.sql
        init_db_path = "data/init_db.sql"
        with open(init_db_path, encoding="utf-8") as f:
            init_db_as_string = f.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
        except Exception as e:
            logging.error(e)
            raise

        user_service = UserService()
        for u in user_service.lister_tous(inclure_mdp=True):
            user_service.modifier(u)

        return True

if __name__ == "__main__":
    ResetDatabase().lancer()
    ResetDatabase().lancer(True)
