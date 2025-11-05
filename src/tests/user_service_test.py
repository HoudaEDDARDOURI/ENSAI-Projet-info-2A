from datetime import date, timedelta
from unittest.mock import patch
from service.user_service import UserService
from business_object.course import Course


@patch("service.user_service.ActiviteDao")
def test_creer_activite_ok(mock_activite_dao):
    """Test de la création d'une activité réussie"""

    # GIVEN : les paramètres d'entrée
    mock_activite_dao.return_value.creer.return_value = True

    date_activite = date(2025, 11, 4)
    type_sport = "Course"
    distance = 10.5
    duree = timedelta(minutes=50)  # <-- ici c'est un timedelta
    trace = "trace_test.gpx"
    titre = "Course test unitaire"
    description = "Activité de test unitaire"
    id_user = 1
    id_parcours = 1

    # WHEN : appel du service
    activite = UserService().creer_activite(
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

    # THEN : vérifications
    assert activite is not None
    assert isinstance(activite, Course)
    assert activite.titre == titre
    assert activite.type_sport.lower() == type_sport.lower()
    assert activite.id_user == id_user
    mock_activite_dao.return_value.creer.assert_called_once()
