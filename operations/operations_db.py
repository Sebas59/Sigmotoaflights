from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import and_, func
from fastapi import HTTPException, status
from typing import List, Optional,Dict
from utils.models import *
from utils.schemas import *
from fastapi import Form,File


async def crear_user_db(user_create, session:AsyncSession)->User:
    nuevo_user = User(**user_create.dict())
    session.add(nuevo_user)
    try:
        await session.commit()
        await session.refresh(nuevo_user)
        return nuevo_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Error al crear el Usuario")


def user_create_form(
        nombre: str = Form(...),
        email: str = Form(...),
        have_mascota: bool = Form(...),


) -> UserCreate:
    return UserCreate(
        nombre=nombre,
        email=email,
        have_mascota=have_mascota,
    )