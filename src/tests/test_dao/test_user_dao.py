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

def test_lire_user_non_existant():
    """Recherche par id d'un user n'existant pas"""
    # GIVEN
    id_user = 9999999999999

    # WHEN
    user = UserDao().lire(id_user)

    # THEN
    assert user is None


@pytest.fixture
def utilisateur_exemple():
    """Fixture qui crée un utilisateur et retourne son ID"""
    user = User(
        id_user=None,  # L'ID est None au début car il sera généré lors de l'insertion
        prenom="Clara",
        nom="Beauvais",
        username="clara123",
        mot_de_passe="secret123",
        created_at=datetime.now()  # L'heure de création est automatiquement définie lors de l'instantiation
    )

    # Suppression d'un utilisateur avec le même username s'il existe
    existing_user = UserDao().trouver_par_username(user.username)
    if existing_user:
        UserDao().supprimer(existing_user.id_user)

    # Création de l'utilisateur dans la base de données
    creation_ok = UserDao().creer(user)
    
    # Retourne l'utilisateur créé pour les tests
    return user if creation_ok else None

    def test_creer_utilisateur(utilisateur_exemple):
    """Test de création d'un utilisateur"""

    # GIVEN : l'utilisateur est préparé dans la fixture utilisateur_exemple
    user = utilisateur_exemple

    # WHEN : On teste si l'utilisateur a bien été créé et si l'ID est défini
    assert user is not None  # Vérifie que l'utilisateur existe
    assert user.id_user is not None  # Vérifie que l'ID a été généré
    assert user.username == "clara123"  # Vérifie que le username correspond
    assert user.mot_de_passe == "secret123"  # Vérifie le mot de passe

    # Vous pouvez ajouter d'autres vérifications selon les propriétés de l'utilisateur

def test_lire_utilisateur(utilisateur_exemple):
    """Test de lecture d'un utilisateur par son ID"""

    # GIVEN : l'utilisateur est préparé dans la fixture utilisateur_exemple
    user = utilisateur_exemple

    # WHEN : On essaie de lire l'utilisateur depuis la base de données avec son ID
    user_lu = UserDao().lire(user.id_user)

    # THEN : Vérification que l'utilisateur a bien été récupéré
    assert user_lu is not None  # L'utilisateur doit être trouvé
    assert user_lu.id_user == user.id_user  # L'ID de l'utilisateur doit correspondre
    assert user_lu.username == user.username  # Vérification que le username correspond

def test_supprimer_utilisateur(utilisateur_exemple):
    """Test de suppression d'un utilisateur"""

    # GIVEN : l'utilisateur est préparé dans la fixture utilisateur_exemple
    user = utilisateur_exemple

    # WHEN : On essaie de supprimer l'utilisateur
    suppression_ok = UserDao().supprimer(user.id_user)

    # THEN : Vérification que la suppression a réussi
    assert suppression_ok is True  # La suppression doit être réussie
    # Vérification que l'utilisateur n'existe plus dans la base
    user_supprime = UserDao().lire(user.id_user)
    assert user_supprime is None  # L'utilisateur ne doit plus exister

