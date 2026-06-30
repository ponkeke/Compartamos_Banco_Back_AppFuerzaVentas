from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class EvaluacionPreRequest(BaseModel):
    solicitud_id: int
    resultado: str = Field(..., max_length=50)
    capacidad_pago: Decimal | None = Field(None, gt=0)
    observaciones: str | None = None


class EvaluacionBuroRequest(BaseModel):
    solicitud_id: int
    resultado: str = Field(..., max_length=50)
    observaciones: str | None = None


class EvaluacionOut(BaseModel):
    id: int
    solicitud_id: int | None = None
    empleado_id: int | None = None
    resultado_pre_evaluacion: str | None = None
    resultado_buro: str | None = None
    capacidad_pago: Decimal | None = None
    observaciones: str | None = None
    fecha_evaluacion: datetime | None = None

    class Config:
        from_attributes = True
