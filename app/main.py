from fastapi import FastAPI
from app.routers.climate_router import router

# Cria a aplicação.
app = FastAPI()

# Registra as rotas GET e POST.
app.include_router(router)