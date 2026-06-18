from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class CuentaOut(BaseModel):
    id: int
    cliente_id: int
    numero_cuenta: str
    tipo: str
    moneda: str
    saldo: Decimal
    tea: Decimal
    created_at: datetime | None = None

    class Config:
        from_attributes = True
