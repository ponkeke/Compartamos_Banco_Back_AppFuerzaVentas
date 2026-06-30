from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SolicitudRegistroRequest(BaseModel):
    dni: str = Field(..., min_length=8, max_length=8)
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    celular: str = Field(..., min_length=6, max_length=15)
    correo: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6)


class SolicitudRegistroOut(BaseModel):
    id: int
    dni: str
    nombres: str
    apellidos: str
    celular: str
    correo: str
    estado: str
    created_at: datetime | None = None
    observacion: str | None = None

    class Config:
        from_attributes = True


class RechazarRequest(BaseModel):
    observacion: str = Field(..., min_length=1)
