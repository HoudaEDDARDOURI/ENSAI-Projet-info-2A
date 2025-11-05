import os
import pytest
from unittest.mock import patch
from dotenv import load_dotenv
from dao.user_dao import UserDao
from business_object.user import User


def test_creer_ok():
    """Création d'utilisateur réussie"""

    # GIVEN
    user = User(prenom="clara", nom="beauvais", username="1234", mot_de_passe="secret123")

    # Si l'utilisateur existe déjà, on le supprime
    existing_user = UserDao().trouver_par_username(user.username)
    if existing_user:
        UserDao().supprimer(existing_user.id_user)

    # WHEN
    creation_ok = UserDao().creer(user)

    # THEN
    assert creation_ok
    assert user.id_user
