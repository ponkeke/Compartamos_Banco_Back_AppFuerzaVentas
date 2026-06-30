from pydantic import BaseModel, Field
from datetime import datetime


class ClienteOut(BaseModel):
    id: int
    dni: str
    nombres: str
    apellidos: str
    estado_registro: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ClienteCreateIn(BaseModel):
    dni: str = Field(..., min_length=8, max_length=8)
    nombres: str = Field(..., min_length=1, max_length=100)
    apellidos: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6)
