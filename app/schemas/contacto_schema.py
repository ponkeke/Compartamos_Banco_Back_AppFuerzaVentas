from pydantic import BaseModel, Field
from datetime import datetime


class ContactoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    telefono: str = Field(..., min_length=7, max_length=15)


class ContactoOut(BaseModel):
    id: int
    cliente_id: int
    nombre: str
    apellido: str
    telefono: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True
