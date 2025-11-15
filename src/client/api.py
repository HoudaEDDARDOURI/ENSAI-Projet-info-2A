from fastapi import FastAPI
from client.user_router import user_router
from client.activite_router import activite_router
from client.statistiques_router import statistiques_router
from client.parcours_router import parcours_router
from client.feed_router import feed_router

# Création de l'application FastAPI
app = FastAPI(title="Sport Activities API")

# Inclusion des routers
app.include_router(user_router)
app.include_router(activite_router)
app.include_router(statistiques_router)
app.include_router(parcours_router)
app.include_router(feed_router)
