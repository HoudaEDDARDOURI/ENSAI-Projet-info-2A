import pytest
from service.activite_service import ActiviteService
from business_object.course import Course
from business_object.like import Like
from datetime import date, timedelta
from dao.user_dao import UserDao
from business_object.user import User
from datetime import datetime, timedelta, date


# URL de ta base de test si tu en as une, sinon la base réelle
# TEST_DB_URL = "sqlite:///test.db"


@pytest.fixture(scope="module")
def activite_service():
    """Fixture pour le service avec DAO réel"""
    service = ActiviteService()  # le service crée lui-même son DAO
    return service



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



def test_creer_activite_in_db(activite_service, utilisateur_exemple):
    """Test d'intégration : créer une activité et vérifier en base"""
    
    date_activite = date(2025, 11, 5)
    type_sport = "Course"
    distance = 10.5
    duree = timedelta(minutes=50)
    trace = "trace_test.gpx"
    titre = "Course test intégration"
    description = "Activité test intégration"
    id_user = utilisateur_exemple.id_user

    # Créer l'activité
    activite = activite_service.creer_activite(
        date_activite,
        type_sport,
        distance,
        duree,
        trace,
        titre,
        description,
        id_user
    )

    assert activite is not None
    assert isinstance(activite, Course)
    assert activite.titre == titre

    # Vérification en base via lire_activites_par_user
    activites_utilisateur = activite_service.activiteDao.lire_activites_par_user(id_user)
    activite_recuperee = next(
        (a for a in activites_utilisateur if a.id_activite == activite.id_activite),
        None
    )

    print(activite_recuperee.id_activite if activite_recuperee else "Non trouvé")
    print(activite_recuperee)

    assert activite_recuperee is not None
    assert activite_recuperee.titre == titre



def test_supprimer_activite(activite_service, utilisateur_exemple):
    """Test d'intégration : créer puis supprimer une activité"""

    # 1️⃣ Créer une activité temporaire
    date_activite = date(2025, 11, 5)
    type_sport = "Course"
    distance = 10.5
    duree = timedelta(minutes=50)
    trace = "trace_test.gpx"
    titre = "Course à supprimer"
    description = "Activité temporaire pour test"
    id_user = utilisateur_exemple.id_user

    activite = activite_service.creer_activite(
        date_activite,
        type_sport,
        distance,
        duree,
        trace,
        titre,
        description,
        id_user
    )

    assert activite is not None
    assert isinstance(activite, Course)

    # 2️⃣ Supprimer l'activité
    resultat = activite_service.supprimer_activite(activite.id_activite)
    assert resultat is True

    # 3️⃣ Vérifier qu'elle n'existe plus en base
    activites_utilisateur = activite_service.activiteDao.lire_activites_par_user(id_user)
    activite_recuperee = next(
        (a for a in activites_utilisateur if a.id_activite == activite.id_activite),
        None
    )
    assert activite_recuperee is None



def test_modifier_activite(activite_service, utilisateur_exemple):
    """Test d'intégration : modification d'une activité"""
    
    #  Créer une activité temporaire
    date_activite = date(2025, 11, 5)
    type_sport = "Course"
    distance = 10.0
    duree = timedelta(minutes=60)
    trace = "trace_modif.gpx"
    titre = "Titre original"
    description = "Description originale"
    id_user = utilisateur_exemple.id_user


    activite = activite_service.creer_activite(
        date_activite, type_sport, distance, duree,
        trace, titre, description, id_user
    )

    assert activite is not None

    # Modifier certains attributs
    activite.titre = "Titre modifié"
    activite.description = "Description modifiée"

    # Appel de la méthode modifier
    resultat = activite_service.modifier_activite(activite)
    assert resultat is True

    # Vérifier les modifications en base via lire_activites_par_user
    activites = activite_service.activiteDao.lire_activites_par_user(id_user)
    activite_modifiee = next((a for a in activites if a.id_activite == activite.id_activite), None)

    assert activite_modifiee is not None
    assert activite_modifiee.titre == "Titre modifié"
    assert activite_modifiee.description == "Description modifiée"


def test_get_likes_activite(activite_service, utilisateur_exemple):
    """Test d'intégration : récupérer les likes d'une activité"""
    date_activite = date(2025, 11, 5)
    type_sport = "Course"
    distance = 10.5
    duree = timedelta(minutes=50)
    trace = "trace_test_likes.gpx"
    titre = "Course avec likes"
    description = "Activité pour test likes"
    id_user = utilisateur_exemple.id_user
    # Créer l'activité
    activite = activite_service.creer_activite(
        date_activite, type_sport, distance, duree,
        trace, titre, description, id_user
    )
    assert activite is not None

    # Ajouter un like via le DAO
    like = Like(id_user=id_user, id_activite=activite.id_activite)
    activite_service.likeDao.creer(like)  # Assure-toi que la méthode existe

    # Vérifier avec la méthode du service
    likes = activite_service.get_likes_activite(activite.id_activite)
    assert len(likes) > 0
    assert any(l.id_user == id_user for l in likes)
