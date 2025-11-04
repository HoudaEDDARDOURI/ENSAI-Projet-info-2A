import os
import pytest

from unittest.mock import patch
from dotenv import load_dotenv

load_dotenv()  

from dao.user_dao import UserDao

from business_object.user import User


def test_creer_ok():
    """Création d'utilisateur réussie"""

    # GIVEN
    user = User(prenom="clara", nom="beauvais", username="123456789", mot_de_passe="secret123")

    # WHEN
    creation_ok = UserDao().creer(user)

    # THEN
    assert creation_ok
    assert user.id_user
