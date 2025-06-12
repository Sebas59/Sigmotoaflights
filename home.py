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


@router.get("/Users", tags=["Usuario"])
async def usuario_list_html(
        request: Request,
        session: AsyncSession = Depends(get_session),
        nombre: Optional[str] = Query(None, description="Filtrar por nombre del usuario(opcional)"),
        email: Optional[str] = Query(None, description="Filtrar por email del usuario(opcional)"),
        user_id: Optional[int] = Query(None, description="Filtrar por ID del usuario(opcional)"),
        have_mascota: Optional[bool] = Query(None, description="Filtrar por ID del vehiculo(opcional)")
):
    current_nombre = nombre if nombre else None
    current_email = email if email else None

    current_user_id = int(user_id) if user_id and user_id.isdigit() else None

    try:
        usuarios = await obtener_user_db(
            session=session,
            nombre=current_nombre,
            email=current_email,
            user_id=current_user_id
        )
        error_message = None
        if not usuarios and (current_nombre or current_email or current_user_id):
            error_message = "No se encontraron usuarios con los criterios de búsqueda"

        return templades.TemplateResponse(
            "User.html",
            {
                "request": request,
                "usuarios": usuarios,
                "have_mascota" : have_mascota,
                "current_nombre": current_nombre,
                "current_email": current_email,
                "id_buscado": current_user_id,
                "error_mensage": error_message
            }
        )
    except HTTPException as e:
        return templades.TemplateResponse(
            "User.html",
            {
                "request": request,
                "usuarios": [],
                "have_mascota" : have_mascota,
                "current_nombre": current_nombre,
                "current_email": current_email,
                "id_buscado": current_user_id,
                "error_mensage": e.detail
            },
            status_code=e.status_code
        )
    except Exception as e:
        return templades.TemplateResponse(
            "User.html",
            {
                "request": request,
                "usuarios": [],
                "have_mascota" : have_mascota,
                "current_nombre": current_nombre,
                "current_email": current_email,
                "id_buscado": current_user_id,
                "error_mensage": f"Error inesperado: {e}"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




@router.get("/usuario/crear", tags=["Usuario"])
async def usuario_create_html(request: Request, session: AsyncSession = Depends(get_session)):
    return templades.TemplateResponse("user_create.html", {
        "request": request,
        "title": "Crear usuario"
    })


@router.post("/usuario/crear", tags=["Usuario"])
async def create_user(
    user_data: UserCreate = Depends(user_create_form),
    session: AsyncSession = Depends(get_session)
):
    try:
        nuevo_user = await crear_usero_db(user_data,session)
        return RedirectResponse(url="/Users", status_code=status.HTTP_303_SEE_OTHER)
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