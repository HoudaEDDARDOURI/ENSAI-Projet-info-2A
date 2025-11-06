from typing import Optional
from business_object.user import User
from business_object.activite import Activite


class Parcours:
    """
    Représente un parcours ou un itinéraire enregistré.

    Attributs basés sur le diagramme UML :
    - idParcours: INTEGER (int)
    - depart: STRING (str) - Description ou adresse du point de départ
    - arrivee: STRING (str) - Description ou adresse du point d'arrivée
    - idActivite: INTEGER - L'activité associée (peut être nulle)
    - idUser: INTEGER (int)
    """
    def __init__(self, depart: str, arrivee: str,
                 id_activite: Optional[int], id_user: int, id_parcours: int = None):
        self.id_parcours = id_parcours
        self.depart = depart
        self.arrivee = arrivee
        self.id_activite = id_activite  # Peut être None si aucune activité associée
        self.id_user = id_user