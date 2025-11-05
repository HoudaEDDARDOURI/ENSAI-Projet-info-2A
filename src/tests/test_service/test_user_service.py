from unittest.mock import MagicMock
from service.user_service import UserService
from dao.user_dao import UserDao
from business_object.user import User


# Liste d'exemple pour les tests
liste_users = [
    User(prenom="Alice", nom="A", username="alice", mot_de_passe="pwd1"),
    User(prenom="Bob", nom="B", username="bob", mot_de_passe="pwd2"),
    User(prenom="Charlie", nom="C", username="charlie", mot_de_passe="pwd3"),
]


def test_creer_ok():
    """Création d'un utilisateur réussie"""
    # GIVEN
    prenom, nom, username, mot_de_passe = "Dave", "D", "dave", "1234"
    UserDao().creer = MagicMock(return_value=True)

    # WHEN
    user = UserService().creer(prenom, nom, username, mot_de_passe)

    # THEN
    assert user.username == username
    assert user.prenom == prenom


def test_creer_echec():
    """Création d'un utilisateur échouée"""
    # GIVEN
    prenom, nom, username, mot_de_passe = "Eve", "E", "eve", "1234"
    UserDao().creer = MagicMock(return_value=False)

    # WHEN
    user = UserService().creer(prenom, nom, username, mot_de_passe)

    # THEN
    assert user is None


def test_se_connecter_ok():
    """Connexion réussie"""
    # GIVEN
    username, mot_de_passe = "alice", "pwd1"
    UserDao().se_connecter = MagicMock(return_value=liste_users[0])

    # WHEN
    user = UserService().se_connecter(username, mot_de_passe)

    # THEN
    assert user.username == username


def test_se_connecter_echec():
    """Connexion échouée"""
    username, mot_de_passe = "unknown", "pwd"
    UserDao().se_connecter = MagicMock(return_value=None)

    user = UserService().se_connecter(username, mot_de_passe)
    assert user is None


def test_pseudo_deja_utilise_oui():
    """Le username est déjà utilisé"""
    UserDao().trouver_par_username = MagicMock(return_value=liste_users[0])
    assert UserService().pseudo_deja_utilise("alice") is True


def test_pseudo_deja_utilise_non():
    """Le username n'est pas utilisé"""
    UserDao().trouver_par_username = MagicMock(return_value=None)
    assert UserService().pseudo_deja_utilise("nouveau") is False


def test_supprimer_ok():
    """Suppression réussie"""
    UserDao().supprimer = MagicMock(return_value=True)
    assert UserService().supprimer(1) is True


def test_supprimer_echec():
    """Suppression échouée"""
    UserDao().supprimer = MagicMock(return_value=False)
    assert UserService().supprimer(999) is False


def test_suivre_ok():
    """Suivi d'un utilisateur réussi"""
    u1, u2 = liste_users[0], liste_users[1]

    # On leur donne des IDs différents pour ne pas déclencher l'erreur
    u1.id_user = 1
    u2.id_user = 2

    UserDao().ajouter_suivi = MagicMock(return_value=True)
    res = UserService().suivre(u1, u2)
    assert res is True


def test_suivre_echec_meme_user():
    """Erreur quand un utilisateur se suit lui-même"""
    u1 = liste_users[0]
    try:
        UserService().suivre(u1, u1)
        assert False, "Une exception aurait dû être levée"
    except ValueError as e:
        assert str(e) == "Un utilisateur ne peut pas se suivre lui-même."


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
