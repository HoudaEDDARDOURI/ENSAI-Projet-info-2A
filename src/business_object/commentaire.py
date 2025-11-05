class Commentaire:
    def __init__(self, id_user: int, id_activite: int, contenu: str, date=None,
                 id_commentaire=None):
        self.id_commentaire = id_commentaire
        self.id_user = id_user
        self.id_activite = id_activite
        self.contenu = contenu
        self.date = date
