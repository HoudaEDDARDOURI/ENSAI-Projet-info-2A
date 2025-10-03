from typing import Tuple
from business_object.user import User
from business_object.activite import Activite


class Parcours:
    """
    Représente un parcours ou un itinéraire enregistré.

    Attributs basés sur le diagramme UML :
    - idParcours: INTEGER (int)
    - depart: TUPLE (Tuple[float, float])
    - arrivee: TUPLE (Tuple[float, float])
    - idActivite: INTEGER - L'activité associée (peut être nulle)
    - idUser: INTEGER (int)
    """
    def __init__(self, depart: Tuple[float, float], arrivee: Tuple[float, float],
                 activites: list[Activite], user: User, idParcours: int = None
                 ):
        self.idParcours = idParcours
        self.depart = depart
        self.arrivee = arrivee
        self.activites = activites
        self.user = user
