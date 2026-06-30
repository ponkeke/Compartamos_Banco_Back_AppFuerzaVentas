from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class TransaccionOut(BaseModel):
    id: int
    cuenta_id: int
    tipo: str
    descripcion: str | None = None
    monto: Decimal
    saldo_resultante: Decimal
    fecha: datetime | None = None

    class Config:
        from_attributes = True


class MovimientoRequest(BaseModel):
    cuenta_id: int
    tipo: str = Field(..., max_length=50)
    descripcion: str | None = Field(None, max_length=255)
    monto: Decimal = Field(..., gt=0)
