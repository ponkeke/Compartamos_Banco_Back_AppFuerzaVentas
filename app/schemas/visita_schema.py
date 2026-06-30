from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class VisitaCampoRequest(BaseModel):
    solicitud_id: int
    estado_visita: str = Field(..., max_length=30)
    observacion: str | None = None
    latitud: Decimal | None = None
    longitud: Decimal | None = None


class VisitaCampoOut(BaseModel):
    id: int
    solicitud_id: int | None = None
    empleado_id: int | None = None
    estado_visita: str | None = None
    observacion: str | None = None
    latitud: Decimal | None = None
    longitud: Decimal | None = None
    fecha_visita: datetime | None = None

    class Config:
        from_attributes = True
