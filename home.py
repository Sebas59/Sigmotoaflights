from fastapi import APIRouter, Depends, HTTPException, status, Form, Query,UploadFile,File
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.future import select

from utils.models import *
from connections.connection_db import *
from utils.schemas import *
from operations.operations_db import *




@asynccontextmanager
async def lifespan(app: APIRouter):
    await init_db()
    yield

templades = Jinja2Templates(directory="templates")
router = APIRouter(lifespan=lifespan)


@router.get("/", response_class=HTMLResponse)
async def leer_home(request: Request):
    return templades.TemplateResponse("home.html", {"request": request})


@router.get("/usuario/crear", tags=["Usuario"])
async def usuario_create_html(request: Request, session: AsyncSession = Depends(get_session)):
    return templades.TemplateResponse("user_create.html", {
        "request": request,
        "title": "Crear Vehículo"
    })


@router.post("/usuario/crear", tags=["Usuario"])
async def create_user(
    user_data: UserCreate = Depends(user_create_form()),
    session: AsyncSession = Depends(get_session)
):
    try:
        nuevo_user = await crear_user_db(user_data,session)
        return RedirectResponse(url="/user_registro", status_code=status.HTTP_303_SEE_OTHER)
    except HTTPException as e:
         return templades.TemplateResponse(
            "user_create.html",
            {
                "request": Request(scope={"type": "http"}),
                "title": "Crear Usuario",
                "error_message": e.detail,
            },
            status_code=e.status_code
        )
    except Exception as e:
        print(f"Error inesperado al crear Usuario: {e}")
        return templades.TemplateResponse(
            "user_create.html",
            {
                "request": Request(scope={"type": "http"}),
                "title": "Crear Usuario",
                "error_message": f"Ocurrió un error inesperado al registrar el Usuario."
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )