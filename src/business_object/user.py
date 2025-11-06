from __future__ import annotations
from datetime import datetime


class User():

    def __init__(self, nom: str, prenom: str, username: str, mot_de_passe: str,
                 id_user: int = None, created_at: datetime = None):
        self.id_user = id_user
        self.prenom = prenom
        self.nom = nom
        self.username = username
        self.mot_de_passe = mot_de_passe
        self.created_at = created_at

        self.activites = []
        self.parcours = []

        self.following: set[int] = set()
        self.followers: set[int] = set()

    def suivre(self, autre_user: "User"):
        """Ajoute un utilisateur à la liste des suivis"""
        if autre_user.id_user == self.id_user:
            raise ValueError("Un utilisateur ne peut pas se suivre lui-même.")
        self.following.add(autre_user.id_user)

    def ajouter_activite(self, activite):
        """Ajoute une activité à la liste locale"""
        self.activites.append(activite)

    def ajouter_parcours(self, parcours):
        """Ajoute un parcours à la liste locale"""
        self.parcours.append(parcours)
