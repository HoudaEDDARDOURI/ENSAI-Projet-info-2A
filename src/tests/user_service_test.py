import pytest
from datetime import date, timedelta
from service.user_service import UserService
from business_object.course import Course

# URL de ta base de test si tu en as une, sinon la base réelle
# TEST_DB_URL = "sqlite:///test.db"


@pytest.fixture(scope="module")
def user_service():
    """Fixture pour le service avec DAO réel"""
    service = UserService()  # le service crée lui-même son DAO
    return service


def test_creer_activite_in_db(user_service):
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
    activite = user_service.creer_activite(
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

    # Vérification en base
    activite_recuperee = user_service.activiteDao.lire(activite.id_activite)
    assert activite_recuperee is not None
    assert activite_recuperee.titre == titre
