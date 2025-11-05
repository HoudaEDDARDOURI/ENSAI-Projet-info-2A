import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from dao.activite_dao import ActiviteDao
from business_object.activite import Activite
from business_object.course import Course
from business_object.natation import Natation
from business_object.cyclisme import Cyclisme


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test (remplacée par le schéma dynamique)"""
    pass  # Cette fixture est maintenant gérée par conftest.py, donc plus besoin de cette logique ici.


@pytest.fixture
def activite_course_exemple():
    """Fixture qui crée une Course et retourne son ID"""
    
    # Conversion de la durée (minutes) en timedelta
    duree_minutes = 60
    duree_time = timedelta(minutes=duree_minutes)  # Utilisation de timedelta pour des durées supérieures à 59 minutes
    
    course = Course(
        id_activite=None,
        id_user=1,
        date=datetime.now(),
        distance=10.0,
        duree=duree_time,
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
    
    # Conversion de la durée (minutes) en timedelta
    duree_minutes = 45
    duree_time = timedelta(minutes=duree_minutes)
    
    natation = Natation(
        id_activite=None,
        id_user=1,
        date=datetime.now(),
        distance=1.5,
        duree=duree_time,
        trace=None,
        id_parcours=None,
        titre="Piscine test",
        description="Test natation",
        denivele=0.0  # Ajout du dénivelé
    )
    ActiviteDao().creer(natation)
    return natation.id_activite


@pytest.fixture
def activite_cyclisme_exemple():
    """Fixture qui crée un Cyclisme et retourne son ID"""
    
    # Conversion de la durée (minutes) en timedelta
    duree_minutes = 120
    duree_time = timedelta(minutes=duree_minutes)
    
    cyclisme = Cyclisme(
        id_activite=None,
        id_user=1,
        date=datetime.now(),
        distance=40.0,
        duree=duree_time,
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


def test_lire_activite_type_course(activite_course_exemple):
    """Vérifie que la lecture d'une Course retourne bien un objet Course"""
    # GIVEN
    id_course = activite_course_exemple

    # WHEN
    activite_lue = ActiviteDao().lire(id_course)

    # THEN
    assert activite_lue is not None
    assert isinstance(activite_lue, Course)
    assert hasattr(activite_lue, 'denivele')
    assert activite_lue.denivele == 150.0


def test_lire_activite_type_natation(activite_natation_exemple):
    """Vérifie que la lecture d'une Natation retourne bien un objet Natation"""
    # GIVEN
    id_natation = activite_natation_exemple

    # WHEN
    activite_lue = ActiviteDao().lire(id_natation)

    # THEN
    assert activite_lue is not None
    assert isinstance(activite_lue, Natation)
    assert activite_lue.distance == 1.5


def test_lire_activite_type_cyclisme(activite_cyclisme_exemple):
    """Vérifie que la lecture d'un Cyclisme retourne bien un objet Cyclisme"""
    # GIVEN
    id_cyclisme = activite_cyclisme_exemple

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
    activite = Course(
        id_activite=None,
        id_user=1,
        date=datetime.now(),
        distance=5.0,
        duree=timedelta(minutes=30),  # Utilisation de timedelta pour la durée
        trace="trace_test",
        id_parcours=None,
        titre="Test création",
        description="Activité de test",
        denivele=150.0
    )

    # WHEN
    creation_ok = ActiviteDao().creer(activite)

    # THEN
    assert creation_ok
    assert activite.id_activite is not None


def test_creer_activite_ko():
    """Création d'activité échouée"""
    # GIVEN
    activite = Course(
        id_activite=None,
        id_user="invalide",  # Type incorrect
        date=datetime.now(),
        distance=5.0,
        duree=timedelta(minutes=30),  # Utilisation de timedelta pour la durée
        trace="trace_test",
        id_parcours=None,
        titre="Test échec",
        description="Doit échouer",
        denivele=150.0
    )

    # WHEN
    creation_ok = ActiviteDao().creer(activite)

    # THEN
    assert not creation_ok


def test_modifier_activite_ok():
    """Modification d'activité réussie"""
    # GIVEN
    activite = Course(
        id_activite=None,
        id_user=1,
        date=datetime.now(),
        distance=5.0,
        duree=timedelta(minutes=30),  # Utilisation de timedelta pour la durée
        trace="trace_test",
        id_parcours=None,
        titre="Avant modification",
        description="Description avant",
        denivele=150.0
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


def test_modifier_activite_avec_denivele_ok(activite_course_exemple):
    """Modification d'une activité avec dénivelé réussie"""
    # GIVEN
    course = ActiviteDao().lire(activite_course_exemple)
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
    activite = Course(
        id_activite=9999999,
        id_user=1,
        date=datetime.now(),
        distance=5.0,
        duree=timedelta(minutes=30),  # Utilisation de timedelta pour la durée
        trace="trace",
        id_parcours=None,
        titre="Inexistant",
        description="Ne doit pas fonctionner",
        denivele=150.0
    )

    # WHEN
    modification_ok = ActiviteDao().modifier(activite)

    # THEN
    assert not modification_ok


def test_supprimer_activite_ok():
    """Suppression d'activité réussie"""
    # GIVEN
    activite = Course(
        id_activite=None,
        id_user=1,
        date=datetime.now(),
        distance=5.0,
        duree=timedelta(minutes=30),  # Utilisation de timedelta pour la durée
        trace="trace_a_supprimer",
        id_parcours=None,
        titre="À supprimer",
        description="Test suppression",
        denivele=150.0
    )
    ActiviteDao().creer(activite)

    # WHEN
    suppression_ok = ActiviteDao().supprimer(activite.id_activite)

    # THEN
    assert suppression_ok
