import os
import pytest
from dotenv import load_dotenv
from dao.db_connection import DBConnection

# Chargement du .env si nécessaire
load_dotenv()

# Fixture pour changer dynamiquement le schéma avant chaque test
@pytest.fixture(scope="function", autouse=True)
def set_test_schema():
    """Changer le schéma pour les tests sans toucher aux variables .env"""
    # Sauvegarde du schéma actuel (avant changement)
    original_schema = os.environ.get("POSTGRES_SCHEMA", "public")
    
    # Modification du schéma pour utiliser le schéma de test
    os.environ["POSTGRES_SCHEMA"] = "test"
    # Connexion à la base de données
    db_connection = DBConnection()
    connection = db_connection.connection

    # Activation du schéma test
    with connection.cursor() as cursor:
        cursor.execute("SET search_path TO test;")
        
    # Exécution avant le test
    yield
    
    # Nettoyage après le test 
    try:
        with connection.cursor() as cursor:
            # Récupérer toutes les tables du schéma test
            cursor.execute("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'test';
            """)
            tables = cursor.fetchall()

            # Désactiver les contraintes pour pouvoir tout supprimer
            cursor.execute("SET session_replication_role = 'replica';")

            for (table,) in tables:
                cursor.execute(f"TRUNCATE TABLE test.{table} RESTART IDENTITY CASCADE;")

            # Réactiver les contraintes
            cursor.execute("SET session_replication_role = 'origin';")

        connection.commit()
    except Exception as e:
        print(f"⚠️ Erreur lors du nettoyage de la base de test : {e}")
        connection.rollback()
    # Par exemple, restaurer l'état initial de la base de données, ou supprimer des données créées.
    
    # Restaurer le schéma d'origine après le test
    os.environ["POSTGRES_SCHEMA"] = original_schema
