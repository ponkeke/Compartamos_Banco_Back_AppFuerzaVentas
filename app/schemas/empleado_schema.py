from pydantic import BaseModel
from datetime import datetime


class EmpleadoOut(BaseModel):
    id: int
    codigo_empleado: str
    nombres: str
    apellidos: str
    cargo: str
    estado: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True
