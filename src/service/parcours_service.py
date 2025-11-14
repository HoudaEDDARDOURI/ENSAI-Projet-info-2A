import logging
import folium
from folium import plugins
from geopy.geocoders import Nominatim
from business_object.parcours import Parcours
from dao.parcours_dao import ParcoursDao
from dao.activite_dao import ActiviteDao  
from dao.user_dao import UserDao
from time import sleep


import gpxpy
import os
from typing import List, Tuple
import folium
import tempfile
from folium import plugins


class ParcoursService:
    """
    Service pour gérer les parcours : création, modification, suppression, lecture et téléchargement.
    """

    def __init__(self):
        self.parcours_dao = ParcoursDao()
        self.activite_dao = ActiviteDao()
        self.user_dao = UserDao()

    def creer_parcours(self, depart: str, arrivee: str, id_activite: int | None, id_user: int) -> bool:
        """
        Crée un nouveau parcours en validant et en passant la responsabilité de la persistance au ParcoursDao.
        """
        parcours = Parcours(depart, arrivee, id_activite, id_user)
        return self.parcours_dao.creer(parcours)

    def get_coordinates(self, parcours: Parcours) -> List[Tuple[float, float]]:
        """
        Récupère les coordonnées du parcours soit via un fichier GPX si l'activité est associée,
        soit via un géocodage des adresses.
        """
        if parcours.id_activite:
            activite = self.activite_dao.lire(parcours.id_activite)
            if activite:
                gpx_file_path = activite.trace
                return self.extraire_coordonnees_de_gpx(gpx_file_path)
            else:
                raise ValueError(f"Aucune activité trouvée pour l'ID {parcours.id_activite}")
        else:
            geolocator = Nominatim(user_agent="parcours_service", timeout=10)

            try:
                depart_location = geolocator.geocode(parcours.depart)
                sleep(1)  # Pause de 1 seconde entre les requêtes (requis par Nominatim)
                arrivee_location = geolocator.geocode(parcours.arrivee)

                if not depart_location or not arrivee_location:
                    raise ValueError("Impossible de géocoder les adresses de départ ou d'arrivée")

                depart_coords = (depart_location.latitude, depart_location.longitude)
                arrivee_coords = (arrivee_location.latitude, arrivee_location.longitude)

                return [depart_coords, arrivee_coords]

            except Exception as e:
                raise ValueError(f"Erreur lors du géocodage : {str(e)}")

    def extraire_coordonnees_de_gpx(self, gpx_file_path: str) -> List[Tuple[float, float]]:
        """
        Extrait toutes les coordonnées d'un fichier GPX en récupérant les points dans la trace.
        Le chemin d'accès au fichier GPX est fourni localement.
        """
        if not os.path.exists(gpx_file_path):
            raise FileNotFoundError(f"Le fichier GPX à l'emplacement {gpx_file_path} n'a pas été trouvé.")

        with open(gpx_file_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        parcours_coords = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat, lon = point.latitude, point.longitude
                    parcours_coords.append((lat, lon))

        if not parcours_coords:
            raise ValueError("Aucun point de parcours trouvé dans le fichier GPX.")

        return parcours_coords

    def visualiser_parcours(self, id_parcours):
        """
        Récupère un parcours à partir de son ID et génère une carte avec le tracé du parcours.
        """
        try:
            parcours = self.parcours_dao.lire(id_parcours)
            if not parcours:
                raise ValueError(f"Le parcours avec l'ID {id_parcours} n'existe pas")

            print(f"Parcours trouvé : {parcours}")

            parcours_coords = self.get_coordinates(parcours)

            map_center = [
                (parcours_coords[0][0] + parcours_coords[-1][0]) / 2,
                (parcours_coords[0][1] + parcours_coords[-1][1]) / 2
            ]
            map_ = folium.Map(location=map_center, zoom_start=13)

            folium.Marker(
                location=parcours_coords[0],
                popup="Départ",
                icon=folium.Icon(color="green", icon="play", prefix="fa")
            ).add_to(map_)

            folium.Marker(
                location=parcours_coords[-1],
                popup="Arrivée",
                icon=folium.Icon(color="red", icon="flag-checkered", prefix="fa")
            ).add_to(map_)

            folium.PolyLine(parcours_coords, color="blue", weight=2.5, opacity=1).add_to(map_)
            plugins.Fullscreen().add_to(map_)

            file_path = f"parcours_{id_parcours}.html"
            print(f"Sauvegarde de la carte dans : {file_path}")

            map_.save(file_path)

            return file_path

        except Exception as e:
            print(f"Erreur dans la génération de la carte : {str(e)}")
            raise e
