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


if _name_ == "_main_":
    import pytest
    pytest.main([_file_])