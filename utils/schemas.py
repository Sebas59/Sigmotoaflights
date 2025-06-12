from sqlmodel import SQLModel
from utils.models import *
from typing import Optional
from fastapi import Form, UploadFile, File



class UserCreate(SQLModel):
    nombre: str
    email: str
    have_mascota: bool




