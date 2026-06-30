from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class CronogramaCuotaOut(BaseModel):
    id: int
    credito_id: int
    numero_cuota: int
    fecha_vencimiento: date
    capital: Decimal
    interes: Decimal
    seguro: Decimal
    monto_total: Decimal
    estado: str

    class Config:
        from_attributes = True
