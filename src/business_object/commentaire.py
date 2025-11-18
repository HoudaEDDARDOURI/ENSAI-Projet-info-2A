class Commentaire:    
    def __init__(
        self, 
        id_user: int, 
        id_activite: int, 
        contenu: str,
        id_commentaire: int = None,
        created_at=None  # Géré automatiquement par la BD
    ):
        self.id_commentaire = id_commentaire
        self.id_user = id_user
        self.id_activite = id_activite
        self.contenu = contenu
        self.created_at = created_at  # Timestamp de création (auto par la BD)