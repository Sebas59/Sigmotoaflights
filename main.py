from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

import home

app = FastAPI(
    title="Gestion de Vuelos y reservas para mascotas y sus dueños",
    description="Aplicacion web para gestionar mascotas, vuelos, reservas y dueños"
)

app.mount("/statics", StaticFiles(directory="statics"), name="statics")

app.include_router(home.router)

templates = Jinja2Templates(directory="templates")