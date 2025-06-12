from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import and_, func
from fastapi import HTTPException, status
from typing import List, Optional,Dict
from utils.models import *
from utils.schemas import *
from fastapi import Form,File


async def crear_usero_db(usuario:UserCreate, session:AsyncSession)->User:
    nuevo_user = User(nombre=usuario.nombre, email=usuario.email, have_mascota=usuario.have_mascota)
    session.add(nuevo_user)
    try:
        await session.commit()
        await session.refresh(nuevo_user)
        return nuevo_user
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=404, detail="Error al crear el Usuario ")


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


async def obtener_user_db(
        session: AsyncSession,
        nombre: Optional[str] = None,
        email: Optional[str] = None,
        user_id: Optional[int] = None
) -> List[User]:
    query = select(User)
    condition = []
    if nombre:
        condition.append(User.nombre.ilike(f"%{nombre}"))
    if email:
        condition.append(User.email.ilike(f"%{email}"))
    if user_id:
        condition.append(User.id == user_id)

    if condition:
        query = query.where(and_(*condition))

    result = await session.execute(query)
    usuarios = result.scalars().all()
    return usuarios