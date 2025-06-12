from sqlmodel import SQLModel, Field,Relationship
from typing import Optional
from sqlalchemy import Enum as SqlEnum,column,String



class User(SQLModel, table=True):
    __tablename__ = "Usuario"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    have_mascota: bool