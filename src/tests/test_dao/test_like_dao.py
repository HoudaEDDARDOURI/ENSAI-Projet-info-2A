import pytest
from dao.like_dao import LikeDao
from business_object.like import Like
from dotenv import load_dotenv
from dao.user_dao import UserDao
from business_object.user import User
from datetime import datetime, timedelta, date
from business_object.course import Course
from dao.activite_dao import ActiviteDao

load_dotenv()


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


@pytest.fixture
def activite_course_exemple(utilisateur_exemple):
    activite = Course(
        id_activite=None,
        id_user=utilisateur_exemple.id_user,
        date=datetime.now(),
        distance=10.0,
        duree=timedelta(minutes=60),
        trace="trace_course",
        titre="Course test",
        description="Test course"
    )
    # Création dans la DB pour que id_activite soit généré
    ActiviteDao().creer(activite)
    return activite



def test_creer_like_ok(utilisateur_exemple, activite_course_exemple):
    user = utilisateur_exemple
    activite = activite_course_exemple
    like = Like(user.id_user, activite.id_activite)
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


def test_supprimer_like_ok(utilisateur_exemple, activite_course_exemple):
    user = utilisateur_exemple
    activite = activite_course_exemple
    like = Like(user.id_user, activite.id_activite)
    LikeDao().creer(like)

    deleted = LikeDao().supprimer(like.id_like)
    assert deleted is True

    like_db = LikeDao().lire(like.id_like)
    assert like_db is None


def test_supprimer_like_inexistant():
    deleted = LikeDao().supprimer(99999)
    assert deleted is False
