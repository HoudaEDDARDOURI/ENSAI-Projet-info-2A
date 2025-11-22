import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from dao.activite_dao import ActiviteDao
from business_object.activite import Activite
from business_object.course import Course
from business_object.natation import Natation
from business_object.cyclisme import Cyclisme
from business_object.user import User
from dao.user_dao import UserDao


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
    return Course(
        id_activite=None,
        id_user=utilisateur_exemple.id_user,
        date=datetime.now(),
        distance=10.0,
        duree=timedelta(minutes=60),
        trace="trace_course",
        titre="Course test",
        description="Test course"
    )



@pytest.fixture
def activite_natation_exemple(utilisateur_exemple):
    """Fixture qui crée une Natation et retourne son ID"""
    
    # Conversion de la durée (minutes) en timedelta
    duree_minutes = 45
    duree_time = timedelta(minutes=duree_minutes)
    
    natation = Natation(
        id_activite=None,
        id_user=utilisateur_exemple.id_user,
        date=datetime.now(),
        distance=1.5,
        duree=duree_time,
        trace=None,
        titre="Piscine test",
        description="Test natation"
    )
    return natation


@pytest.fixture
def activite_cyclisme_exemple(utilisateur_exemple):
    """Fixture qui crée un Cyclisme et retourne son ID"""
    
    # Conversion de la durée (minutes) en timedelta
    duree_minutes = 120
    duree_time = timedelta(minutes=duree_minutes)
    
    cyclisme = Cyclisme(
        id_activite=None,
        id_user=utilisateur_exemple.id_user,
        date=datetime.now(),
        distance=40.0,
        duree=duree_time,
        trace="trace_velo",
        titre="Sortie vélo",
        description="Test cyclisme"
    )
    return cyclisme


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
    # GIVEN : Créer l'activité dans la base de données avant de la lire
    course = activite_course_exemple
    ActiviteDao().creer(course)

    # WHEN
    activite_lue = ActiviteDao().lire(course.id_activite)

    # THEN
    assert activite_lue is not None
    assert isinstance(activite_lue, Course)


def test_lire_activite_type_natation(activite_natation_exemple):
    """Vérifie que la lecture d'une Natation retourne bien un objet Natation"""
    # GIVEN
    natation = activite_natation_exemple
    ActiviteDao().creer(natation)

    # WHEN
    activite_lue = ActiviteDao().lire(natation.id_activite)

    # THEN
    assert activite_lue is not None
    assert isinstance(activite_lue, Natation)
    assert activite_lue.distance == 1.5


def test_lire_activite_type_cyclisme(activite_cyclisme_exemple):
    """Vérifie que la lecture d'un Cyclisme retourne bien un objet Cyclisme"""
    # GIVEN
    cyclisme = activite_cyclisme_exemple
    ActiviteDao().creer(cyclisme)

    # WHEN
    activite_lue = ActiviteDao().lire(cyclisme.id_activite)

    # THEN
    assert activite_lue is not None
    assert isinstance(activite_lue, Cyclisme)


def test_creer_activite_ok(activite_course_exemple):
    creation_ok = ActiviteDao().creer(activite_course_exemple)
    assert creation_ok
    assert activite_course_exemple.id_activite is not None


def test_creer_activite_ko():
    """Création d'activité échouée"""
    activite = Course(
        id_activite=None,
        id_user="invalide",  # Type incorrect
        date=datetime.now(),
        distance=5.0,
        duree=timedelta(minutes=30),
        trace="trace_test",
        titre="Test échec",
        description="Doit échouer"
    )

    # WHEN
    creation_ok = ActiviteDao().creer(activite)

    # THEN
    assert creation_ok is False
    assert activite.id_activite is None




def test_modifier_activite_ok(activite_course_exemple):
    """Modification d'activité réussie"""

    # GIVEN : L'activité est créée grâce à la fixture
    activite = activite_course_exemple
    ActiviteDao().creer(activite)

    # Modification de l'activité
    activite.titre = "Titre modifié"
    activite.description = "Description modifiée"
    activite.distance = 12.5

    # WHEN : Modification de l'activité dans la base de données
    modification_ok = ActiviteDao().modifier(activite)

    # THEN : Vérification que la modification a réussi
    assert modification_ok

    # Récupération de l'activité modifiée depuis la base de données
    activite_modifiee = ActiviteDao().lire(activite.id_activite)

    # Vérification des modifications
    assert activite_modifiee.titre == "Titre modifié"
    assert activite_modifiee.distance == 12.5
    assert activite_modifiee.description == "Description modifiée"



def test2_modifier_activite_ok(activite_course_exemple):
    """Modification d'une activité avec dénivelé réussie"""
    # GIVEN : Créer l'activité dans la base de données avant de la lire
    course = activite_course_exemple
    ActiviteDao().creer(course)

    # WHEN : Modification de l'activité dans la base de données
    course.titre = "Course modifiée"
    course.distance = 15.0
    modification_ok = ActiviteDao().modifier(course)

    # THEN : Vérification que la modification a réussi
    assert modification_ok


def test_modifier_activite_ko(utilisateur_exemple):
    """Modification d'activité échouée (id inconnu)"""
    # GIVEN
    activite = Course(
        id_activite=9999999,
        id_user=utilisateur_exemple.id_user,
        date=datetime.now(),
        distance=5.0,
        duree=timedelta(minutes=30),  # Utilisation de timedelta pour la durée
        trace="trace",
        titre="Inexistant",
        description="Ne doit pas fonctionner"
    )

    # WHEN
    modification_ok = ActiviteDao().modifier(activite)

    # THEN
    assert not modification_ok


def test_supprimer_activite_ok(activite_course_exemple):
    """Suppression d'activité réussie"""
    # GIVEN : Créer l'activité dans la base de données avant de la supprimer
    creation_ok = ActiviteDao().creer(activite_course_exemple)
    assert creation_ok
    assert activite_course_exemple.id_activite is not None  # Assurez-vous que l'ID est généré

    # WHEN : Suppression de l'activité
    suppression_ok = ActiviteDao().supprimer(activite_course_exemple.id_activite)

    # THEN : Vérification que la suppression a réussi
    assert suppression_ok

    # Vérification que l'activité a bien été supprimée
    activite_supprimee = ActiviteDao().lire(activite_course_exemple.id_activite)
    assert activite_supprimee is None
