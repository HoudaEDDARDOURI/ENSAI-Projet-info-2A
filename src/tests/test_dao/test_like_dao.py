import pytest
from dao.like_dao import LikeDao
from business_object.like import Like
from utils.reset_database import ResetDatabase
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Réinitialise la base de données avant chaque test DAO."""
    ResetDatabase().lancer(test_dao=True)


def test_creer_like_ok():
    like = Like(id_user=1, id_activite=1)
    created = LikeDao().creer(like)

    assert created is True
    assert like.id_like is not None

    like_db = LikeDao().lire(like.id_like)
    assert like_db is not None
    assert like_db.id_user == like.id_user
    assert like_db.id_activite == like.id_activite


def test_lire_like_inexistant():
    like = LikeDao().lire(99999)
    assert like is None


def test_supprimer_like_ok():
    like = Like(id_user=1, id_activite=1)
    LikeDao().creer(like)

    deleted = LikeDao().supprimer(like.id_like)
    assert deleted is True

    like_db = LikeDao().lire(like.id_like)
    assert like_db is None


def test_supprimer_like_inexistant():
    deleted = LikeDao().supprimer(99999)
    assert deleted is False
