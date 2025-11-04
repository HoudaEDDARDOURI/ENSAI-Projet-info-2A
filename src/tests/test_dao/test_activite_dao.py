import os
import pytest
from datetime import datetime
from unittest.mock import patch
from utils.reset_database import ResetDatabase
from dao.activite_dao import ActiviteDao
from business_object.activite import Activite
from business_object.course import Course
from business_object.natation import Natation
from business_object.cyclisme import Cyclisme


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


@pytest.fixture
def activite_course_exemple():
    """Fixture qui crée une Course et retourne son ID"""
    course = Course(
        id_user=1,
        date=datetime.now(),
        distance=10.0,
        duree=60,
        trace="trace_course",
        id_parcours=None,
        titre="Course test",
        description="Test course",
        denivele=150.0
    )
    ActiviteDao().creer(course)
    return course.id_activite


@pytest.fixture
def activite_natation_exemple():
    """Fixture qui crée une Natation et retourne son ID"""
    natation = Natation(
        id_user=1,
        date=datetime.now(),
        distance=1.5,
        duree=45,
        trace=None,
        id_parcours=None,
        titre="Piscine test",
        description="Test natation"
    )
    ActiviteDao().creer(natation)
    return natation.id_activite


@pytest.fixture
def activite_cyclisme_exemple():
    """Fixture qui crée un Cyclisme et retourne son ID"""
    cyclisme = Cyclisme(
        id_user=1,
        date=datetime.now(),
        distance=40.0,
        duree=120,
        trace="trace_velo",
        id_parcours=None,
        titre="Sortie vélo",
        description="Test cyclisme",
        denivele=300.0
    )
    ActiviteDao().creer(cyclisme)
    return cyclisme.id_activite


def test_lire_activite_non_existante():
    """Recherche par id d'une activité n'existant pas"""
    # GIVEN
    id_activite = 9999999999999

    # WHEN
    activite = ActiviteDao().lire(id_activite)

    # THEN
    assert activite is None


def test_lire_activite_type_course(activite_course_creee):
    """Vérifie que la lecture d'une Course retourne bien un objet Course"""
    # GIVEN
    id_course = activite_course_creee

    # WHEN
    activite_lue = ActiviteDao().lire(id_course)

    # THEN
    assert activite_lue is not None
    assert isinstance(activite_lue, Course)
    assert hasattr(activite_lue, 'denivele')
    assert activite_lue.denivele == 150.0


def test_lire_activite_type_natation(activite_natation_creee):
    """Vérifie que la lecture d'une Natation retourne bien un objet Natation"""
    # GIVEN
    id_natation = activite_natation_creee

    # WHEN
    activite_lue = ActiviteDao().lire(id_natation)

    # THEN
    assert activite_lue is not None
    assert isinstance(activite_lue, Natation)
    assert activite_lue.distance == 1.5


def test_lire_activite_type_cyclisme(activite_cyclisme_creee):
    """Vérifie que la lecture d'un Cyclisme retourne bien un objet Cyclisme"""
    # GIVEN
    id_cyclisme = activite_cyclisme_creee

    # WHEN
    activite_lue = ActiviteDao().lire(id_cyclisme)

    # THEN
    assert activite_lue is not None
    assert isinstance(activite_lue, Cyclisme)
    assert hasattr(activite_lue, 'denivele')
    assert activite_lue.denivele == 300.0


def test_creer_activite_ok():
    """Création d'activité réussie"""
    # GIVEN
    activite = Activite(
        id_user=1,
        date=datetime.now(),
        type_sport="Course",
        distance=5.0,
        duree=30,
        trace="trace_test",
        id_parcours=None,
        titre="Test création",
        description="Activité de test"
    )

    # WHEN
    creation_ok = ActiviteDao().creer(activite)

    # THEN
    assert creation_ok
    assert activite.id_activite is not None


def test_creer_activite_ko():
    """Création d'activité échouée"""
    # GIVEN
    activite = Activite(
        id_user="invalide",  # Type incorrect
        date=datetime.now(),
        type_sport="Course",
        distance=5.0,
        duree=30,
        trace="trace_test",
        id_parcours=None,
        titre="Test échec",
        description="Doit échouer"
    )

    # WHEN
    creation_ok = ActiviteDao().creer(activite)

    # THEN
    assert not creation_ok


def test_modifier_activite_ok():
    """Modification d'activité réussie"""
    # GIVEN
    activite = Activite(
        id_user=1,
        date=datetime.now(),
        type_sport="Course",
        distance=5.0,
        duree=30,
        trace="trace_test",
        id_parcours=None,
        titre="Avant modification",
        description="Description avant"
    )
    ActiviteDao().creer(activite)

    activite.titre = "Titre modifié"
    activite.description = "Description modifiée"
    activite.distance = 12.5

    # WHEN
    modification_ok = ActiviteDao().modifier(activite)

    # THEN
    assert modification_ok

    # Vérification de la modification
    activite_modifiee = ActiviteDao().lire(activite.id_activite)
    assert activite_modifiee.titre == "Titre modifié"
    assert activite_modifiee.distance == 12.5


def test_modifier_activite_avec_denivele_ok(activite_course_creee):
    """Modification d'une activité avec dénivelé réussie"""
    # GIVEN
    course = ActiviteDao().lire(activite_course_creee)
    course.titre = "Course modifiée"
    course.denivele = 200.0
    course.distance = 15.0

    # WHEN
    modification_ok = ActiviteDao().modifier(course)

    # THEN
    assert modification_ok


def test_modifier_activite_ko():
    """Modification d'activité échouée (id inconnu)"""
    # GIVEN
    activite = Activite(
        id_activite=9999999,
        id_user=1,
        date=datetime.now(),
        type_sport="Course",
        distance=5.0,
        duree=30,
        trace="trace",
        id_parcours=None,
        titre="Inexistant",
        description="Ne doit pas fonctionner"
    )

    # WHEN
    modification_ok = ActiviteDao().modifier(activite)

    # THEN
    assert not modification_ok


def test_supprimer_activite_ok():
    """Suppression d'activité réussie"""
    # GIVEN
    activite = Activite(
        id_user=1,
        date=datetime.now(),
        type_sport="Course",
        distance=5.0,
        duree=30,
        trace="trace_a_supprimer",
        id_parcours=None,
        titre="À supprimer",
        description="Test suppression"
    )
    ActiviteDao().creer(activite)
    id_a_supprimer = activite.id_activite

    # WHEN
    suppression_ok = ActiviteDao().supprimer(id_a_supprimer)

    # THEN
    assert suppression_ok
    assert ActiviteDao().lire(id_a_supprimer) is None


def test_supprimer_activite_ko():
    """Suppression d'activité échouée (id inconnu)"""
    # GIVEN
    id_activite = 9999999

    # WHEN
    suppression_ok = ActiviteDao().supprimer(id_activite)

    # THEN
    assert not suppression_ok


if __name__ == "__main__":
    pytest.main([__file__])
