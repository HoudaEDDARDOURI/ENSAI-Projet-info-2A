import os
import pytest

from unittest.mock import patch
from dotenv import load_dotenv
from utils.reset_database import ResetDatabase
from dao.user_dao import UserDao
from business_object.user import User
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
load_dotenv(dotenv_path)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield

def test_creer_ok():
    """Création d'utilisateur réussie"""

    # GIVEN
    user = User(prenom="clara", nom="beauvais", username="123456789", mot_de_passe="secret123")

    # WHEN
    creation_ok = UserDao().creer(user)

    # THEN
    assert creation_ok
    assert user.id_user
