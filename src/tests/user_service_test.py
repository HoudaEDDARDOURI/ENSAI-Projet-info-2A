from unittest.mock import MagicMock
from datetime import date
from service.user_service import UserService
from dao.activite_dao import ActiviteDao
from business_object.activite import Activite


def test_creer_activite_ok():
    """Test de la création d'une activité réussie"""

    # GIVEN : les paramètres d'entrée
    date_activite = date(2025, 11, 4)
    type_sport = "Course"
    distance = 10.5
    duree = "00:50:00"
    trace = "trace_test.gpx"
    titre = "Course test unitaire"
    description = "Activité de test unitaire"
    id_user = 1
    id_parcours = 1

    # On mocke la méthode creer() du DAO
    ActiviteDao().creer = MagicMock(return_value=True)

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
    assert isinstance(activite, Activite)
    assert activite.titre == titre
    assert activite.type_sport == type_sport
    assert activite.id_user == id_user
