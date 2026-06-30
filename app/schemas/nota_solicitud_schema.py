from pydantic import BaseModel, Field
from datetime import datetime

class NotaRequest(BaseModel):
    contenido: str = Field(..., min_length=1)

class NotaOut(BaseModel):
    id: int
    solicitud_id: int
    empleado_id: int
    contenido: str
    created_at: datetime | None = None
    class Config:
        from_attributes = True
