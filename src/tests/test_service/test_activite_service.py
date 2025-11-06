import pytest
from service.activite_service import ActiviteService
from business_object.course import Course
from business_object.like import Like
from datetime import date, timedelta


# URL de ta base de test si tu en as une, sinon la base réelle
# TEST_DB_URL = "sqlite:///test.db"


@pytest.fixture(scope="module")
def activite_service():
    """Fixture pour le service avec DAO réel"""
    service = ActiviteService()  # le service crée lui-même son DAO
    return service


def test_creer_activite_in_db(activite_service):
    """Test d'intégration : créer une activité et vérifier en base"""
    
    date_activite = date(2025, 11, 5)
    type_sport = "Course"
    distance = 10.5
    duree = timedelta(minutes=50)
    trace = "trace_test.gpx"
    titre = "Course test intégration"
    description = "Activité test intégration"
    id_user = 1
    id_parcours = 1

    # Créer l'activité
    activite = activite_service.creer_activite(
        date_activite,
        type_sport,
        distance,
        duree,
        trace,
        titre,
        description,
        id_user,
        id_parcours
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



def test_supprimer_activite(activite_service):
    """Test d'intégration : créer puis supprimer une activité"""

    # 1️⃣ Créer une activité temporaire
    date_activite = date(2025, 11, 5)
    type_sport = "Course"
    distance = 10.5
    duree = timedelta(minutes=50)
    trace = "trace_test.gpx"
    titre = "Course à supprimer"
    description = "Activité temporaire pour test"
    id_user = 1
    id_parcours = 1

    activite = activite_service.creer_activite(
        date_activite,
        type_sport,
        distance,
        duree,
        trace,
        titre,
        description,
        id_user,
        id_parcours
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



def test_afficher_toutes_activites(activite_service, capsys):
    """Test d'intégration : vérifier l'affichage de toutes les activités d'un utilisateur"""

    # ID de l'utilisateur pour le test
    id_user = 1

    # Créer une activité de test
    date_activite = date(2025, 11, 5)
    activite = activite_service.creer_activite(
        date_activite,
        "Course",
        5.0,
        timedelta(minutes=30),
        "trace_affichage.gpx",
        "Activite affichage",
        "Description affichage",
        id_user,  # id_user
        1         # id_parcours
    )
    assert activite is not None

    # Appel de la fonction à tester
    # On capture la sortie pour vérifier l'affichage
    import sys
    from io import StringIO

    captured_output = StringIO()
    sys.stdout = captured_output  # redirige stdout

    activite_service.afficher_toutes_activites(id_user)

    sys.stdout = sys.__stdout__  # rétablit stdout
    output = captured_output.getvalue()

    # Vérifier que la sortie contient le titre et la description
    assert "Activite affichage" in output
    assert "Description affichage" in output



def test_modifier_activite(activite_service):
    """Test d'intégration : modification d'une activité"""
    
    #  Créer une activité temporaire
    date_activite = date(2025, 11, 5)
    type_sport = "Course"
    distance = 10.0
    duree = timedelta(minutes=60)
    trace = "trace_modif.gpx"
    titre = "Titre original"
    description = "Description originale"
    id_user = 1
    id_parcours = 1

    activite = activite_service.creer_activite(
        date_activite, type_sport, distance, duree,
        trace, titre, description, id_user, id_parcours
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


def test_get_likes_activite(activite_service):
    """Test d'intégration : récupérer les likes d'une activité"""
    date_activite = date(2025, 11, 5)
    type_sport = "Course"
    distance = 10.5
    duree = timedelta(minutes=50)
    trace = "trace_test_likes.gpx"
    titre = "Course avec likes"
    description = "Activité pour test likes"
    id_user = 1
    id_parcours = 1

    # Créer l'activité
    activite = activite_service.creer_activite(
        date_activite, type_sport, distance, duree,
        trace, titre, description, id_user, id_parcours
    )
    assert activite is not None

    # Ajouter un like via le DAO
    like = Like(id_user=id_user, id_activite=activite.id_activite)
    activite_service.likeDao.creer(like)  # Assure-toi que la méthode existe

    # Vérifier avec la méthode du service
    likes = activite_service.get_likes_activite(activite.id_activite)
    assert len(likes) > 0
    assert any(l.id_user == id_user for l in likes)
