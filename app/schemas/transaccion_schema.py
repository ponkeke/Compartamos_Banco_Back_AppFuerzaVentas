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


class YapeoRequest(BaseModel):
    numero_destino: str = Field(..., min_length=9, max_length=20)
    monto: Decimal = Field(..., gt=0)


class DepositoRequest(BaseModel):
    monto: Decimal = Field(..., gt=0)
    descripcion: str | None = None
