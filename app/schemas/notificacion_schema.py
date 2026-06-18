from pydantic import BaseModel
from datetime import datetime


class NotificacionOut(BaseModel):
    id: int
    cliente_id: int
    tipo: str
    titulo: str
    descripcion: str | None = None
    leida: bool
    fecha: datetime | None = None

    class Config:
        from_attributes = True
