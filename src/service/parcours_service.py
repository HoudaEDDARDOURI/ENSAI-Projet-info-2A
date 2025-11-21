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
import io
from typing import List, Tuple


class ParcoursService:
    """
    Service pour gérer les parcours : création, modification, suppression, lecture et visualisation.
    """

    def __init__(self):
        self.parcours_dao = ParcoursDao()
        self.activite_dao = ActiviteDao()
        self.user_dao = UserDao()

    def creer_parcours(self, depart: str, arrivee: str, id_activite: int | None, id_user: int) -> int:
        """
        Crée un nouveau parcours en validant et en passant la responsabilité de la persistance au ParcoursDao.
        """
        parcours = Parcours(depart, arrivee, id_activite, id_user)
        return self.parcours_dao.creer(parcours)

    def get_coordinates(self, parcours: Parcours) -> List[Tuple[float, float]]:
        """
        Récupère les coordonnées du parcours soit via le contenu GPX de l'activité,
        soit via un géocodage des adresses.
        """
        if parcours.id_activite:
            activite = self.activite_dao.lire(parcours.id_activite)
            if activite:
                gpx_content = activite.trace  # Contenu GPX stocké en base
                if gpx_content:
                    return self.extraire_coordonnees_de_gpx_content(gpx_content)
                else:
                    raise ValueError(f"Aucun contenu GPX trouvé pour l'activité {parcours.id_activite}")
            else:
                raise ValueError(f"Aucune activité trouvée pour l'ID {parcours.id_activite}")
        else:
            # Géocodage des adresses
            geolocator = Nominatim(user_agent="parcours_service", timeout=10)

            try:
                depart_location = geolocator.geocode(parcours.depart)
                sleep(1)  # Pause requise par Nominatim
                arrivee_location = geolocator.geocode(parcours.arrivee)

                if not depart_location or not arrivee_location:
                    raise ValueError("Impossible de géocoder les adresses de départ ou d'arrivée")

                depart_coords = (depart_location.latitude, depart_location.longitude)
                arrivee_coords = (arrivee_location.latitude, arrivee_location.longitude)

                return [depart_coords, arrivee_coords]

            except Exception as e:
                raise ValueError(f"Erreur lors du géocodage : {str(e)}")

    def extraire_coordonnees_de_gpx_content(self, gpx_content: str) -> List[Tuple[float, float]]:
        """
        Extrait toutes les coordonnées depuis le contenu GPX (string).
        Gère les cas : contenu GPX, chemin fichier (ancien système), ou contenu vide.
        """
        if not gpx_content or gpx_content.strip() == "":
            raise ValueError("Aucun contenu GPX disponible pour cette activité")
        
        # CAS 1 : Ancien système avec chemin de fichier
        if gpx_content.startswith("uploads/") or (gpx_content.endswith(".gpx") and len(gpx_content) < 200):
            logging.warning(f"Ancien format détecté (chemin fichier) : {gpx_content}")
            
            # Essayer de lire le fichier s'il existe encore
            import os
            if os.path.exists(gpx_content):
                logging.info(f"Lecture du fichier GPX : {gpx_content}")
                with open(gpx_content, 'r', encoding='utf-8') as f:
                    gpx_content = f.read()
            else:
                raise ValueError(
                    f"L'activité contient un ancien chemin de fichier ({gpx_content}) "
                    "qui n'existe plus. Veuillez re-télécharger le fichier GPX pour cette activité."
                )
        
        # CAS 2 : Vérifier que c'est bien du XML
        if not (gpx_content.strip().startswith("<?xml") or gpx_content.strip().startswith("<gpx")):
            raise ValueError(
                f"Le contenu ne semble pas être du XML/GPX valide. "
                f"Début : {gpx_content[:100]}"
            )
        
        # CAS 3 : Parser le GPX
        try:
            gpx = gpxpy.parse(gpx_content)
        except Exception as e:
            raise ValueError(f"Erreur lors du parsing du contenu GPX : {str(e)}")

        # Extraire les coordonnées
        parcours_coords = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat, lon = point.latitude, point.longitude
                    parcours_coords.append((lat, lon))

        if not parcours_coords:
            raise ValueError("Aucun point de parcours trouvé dans le contenu GPX.")

        return parcours_coords

    def visualiser_parcours(self, id_parcours: int) -> str:
        """
        Récupère un parcours à partir de son ID et génère le HTML de la carte.
        Retourne directement le HTML (pas de fichier créé).
        """
        try:
            parcours = self.parcours_dao.lire(id_parcours)
            if not parcours:
                raise ValueError(f"Le parcours avec l'ID {id_parcours} n'existe pas")

            logging.info(f"Parcours trouvé : {parcours}")

            # Récupérer les coordonnées
            parcours_coords = self.get_coordinates(parcours)

            # Calculer le centre de la carte
            map_center = [
                (parcours_coords[0][0] + parcours_coords[-1][0]) / 2,
                (parcours_coords[0][1] + parcours_coords[-1][1]) / 2
            ]
            
            # Créer la carte
            map_ = folium.Map(location=map_center, zoom_start=13)

            # Marqueur de départ
            folium.Marker(
                location=parcours_coords[0],
                popup="Départ",
                icon=folium.Icon(color="green", icon="play", prefix="fa")
            ).add_to(map_)

            # Marqueur d'arrivée
            folium.Marker(
                location=parcours_coords[-1],
                popup="Arrivée",
                icon=folium.Icon(color="red", icon="flag-checkered", prefix="fa")
            ).add_to(map_)

            # Tracer le parcours
            folium.PolyLine(
                parcours_coords, 
                color="blue", 
                weight=3, 
                opacity=0.8
            ).add_to(map_)
            
            # Ajouter le mode plein écran
            plugins.Fullscreen().add_to(map_)

            # Générer le HTML en mémoire (pas de fichier créé)
            html_content = map_._repr_html_()

            return html_content

        except Exception as e:
            logging.error(f"Erreur dans la génération de la carte : {str(e)}")
            raise e

    def visualiser_parcours_depuis_gpx(self, gpx_content: str) -> str:
        """
        Génère directement le HTML d'une carte depuis du contenu GPX.
        Utile pour visualiser rapidement sans créer de parcours en base.
        """
        try:
            # Extraire les coordonnées
            parcours_coords = self.extraire_coordonnees_de_gpx_content(gpx_content)

            # Calculer le centre
            map_center = [
                sum(coord[0] for coord in parcours_coords) / len(parcours_coords),
                sum(coord[1] for coord in parcours_coords) / len(parcours_coords)
            ]
            
            # Créer la carte
            map_ = folium.Map(location=map_center, zoom_start=13)

            # Marqueurs
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

            # Tracer le parcours
            folium.PolyLine(
                parcours_coords, 
                color="blue", 
                weight=3, 
                opacity=0.8
            ).add_to(map_)
            
            plugins.Fullscreen().add_to(map_)

            # Retourner le HTML
            return map_._repr_html_()

        except Exception as e:
            logging.error(f"Erreur génération carte depuis GPX : {str(e)}")
            raise e