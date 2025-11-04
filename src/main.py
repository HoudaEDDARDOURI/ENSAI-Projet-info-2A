import gpxpy
from datetime import timedelta, date

from business_object.course import Course
from service.user_service import UserService
from dao.Activite_dao import ActiviteDao
from datetime import date

from dao.db_connection import DBConnection





def importer_activite_gpx(chemin_fichier: str, id_user: int):
    """Lit un fichier GPX et crée une activité associée à l'utilisateur."""
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)

    # === Extraction des infos principales ===
    distance_m = gpx.length_3d()  # en mètres
    up_m, down_m = gpx.get_uphill_downhill()
    duration_s = gpx.get_duration()
    moving = gpx.get_moving_data()

    # === Création de l’activité ===
    activite = Course(
        id_activite=None,
        id_user=id_user,
        date=date.today(),
        distance=distance_m / 1000,  # en km
        duree=timedelta(seconds=duration_s),
        trace=chemin_fichier,
        id_parcours=None,
        titre=gpx.tracks[0].name if gpx.tracks else "Activité sans nom",
        description=f"D+ {up_m:.1f} m / D- {down_m:.1f} m | vitesse moyenne : {moving.moving_distance/moving.moving_time*3.6:.2f} km/h",
        denivele=up_m
    )


    print("\n=== Résumé activité ===")
    print(f"Nom:   {activite.titre}")
    print(f"Type:  {activite.type_sport}")
    print(f"Distance: {activite.distance:.2f} km")
    print(f"D+: {up_m:.1f} m / D-: {down_m:.1f} m")
    print(f"Durée: {duration_s/60:.1f} min")
    print(f"Vitesse moyenne: {moving.moving_distance/moving.moving_time*3.6:.2f} km/h")

    return activite


if __name__ == "__main__":
    print("=== Test de création d’un utilisateur et d’une activité ===")

    # 1Créer un utilisateur
    user_service = UserService()
    date_inscription = date(2025, 10, 26)
    user = user_service.creer("Houda", "Edd", "user14", "motdepassefort")

    if user:
        print(f"Utilisateur créé : {user.username} (id={user.id_user})")
    else:
        print("⚠️ Erreur lors de la création de l'utilisateur.")
        exit()

    # 2Importer une activité depuis un fichier GPX
    chemin_gpx = "/home/onyxia/work/ENSAI-Projet-info-2A/data/strava_activities.gpx"  # adapte le chemin
    activite = importer_activite_gpx(chemin_gpx, user.id_user)

    # Enregistrer l’activité dans la base via le DAO
    dao = ActiviteDao()
    succes = dao.creer(activite)

    if succes:
        print(f"\nActivité enregistrée en base avec id={activite.id_activite}")
    else:
        print("\nErreur lors de la sauvegarde de l’activité.")

    # 4Vérification : lecture depuis la base
    if succes:
        activite_lue = dao.lire(activite.id_activite)
        print("\nActivité relue depuis la base :")
        print(activite_lue)


    # Fermer la connexion avant de modifier la BD
db = DBConnection()
db.close()
