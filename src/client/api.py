from fastapi import FastAPI
from client.user_router import user_router
from client.activite_router import activite_router


# Création de l'application FastAPI
app = FastAPI(title="Sport Activities API", root_path="/proxy/8000")

# Inclusion des routers
app.include_router(user_router)
app.include_router(activite_router)