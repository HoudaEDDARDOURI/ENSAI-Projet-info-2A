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
    
    # Créer une nouvelle connexion DB pour tester sur le schéma modifié
    db_connection = DBConnection()
    connection = db_connection.connection
    cursor = connection.cursor()
    
    # Ici, vous pouvez ajouter des actions supplémentaires si nécessaire pour
    # préparer votre schéma avant les tests (par exemple, créer des tables, insérer des données, etc.)
    
    # Exécution avant le test
    yield
    
    # Nettoyage après le test (optionnel)
    # Par exemple, restaurer l'état initial de la base de données, ou supprimer des données créées.
    
    # Restaurer le schéma d'origine après le test
    os.environ["POSTGRES_SCHEMA"] = original_schema
