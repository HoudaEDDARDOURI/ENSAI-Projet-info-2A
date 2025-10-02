from typing import Optional, Tuple


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
    def __init__(
        self,
        idParcours: int,
        depart: Tuple[float, float], 
        arrivee: Tuple[float, float], 
        idActivite: int,
        idUser: int
    ):
        self.idParcours = idParcours
        self.depart = depart
        self.arrivee = arrivee
        self.idActivite = idActivite
        self.idUser = idUser