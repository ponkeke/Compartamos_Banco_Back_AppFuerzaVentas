from pydantic import BaseModel, Field
from datetime import datetime


class ContactoOut(BaseModel):
    id: int
    cliente_id: int
    nombre: str
    apellido: str
    telefono: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True
