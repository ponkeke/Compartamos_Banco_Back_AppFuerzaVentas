from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class VisitaCarteraRequest(BaseModel):
    resultado: str = Field(..., max_length=30)
    observacion: str | None = None
    lat: float | None = None
    lng: float | None = None

class CarteraOut(BaseModel):
    id: int
    solicitud_id: int
    empleado_id: int
    estado_visita: str
    tipo_gestion: str | None = None
    prioridad: str | None = None
    score_prioridad: int | None = None
    monto_credito: Decimal | None = None
    fecha_asignacion: datetime | None = None
    class Config:
        from_attributes = True

class CarteraDetalleOut(CarteraOut):
    cliente_nombre: str | None = None
    documento: str | None = None
    cliente_id: int | None = None
