from pydantic import BaseModel, Field
from decimal import Decimal

class AccionCobranzaRequest(BaseModel):
    cliente_id: str
    cod_cuenta_credito: str | None = None
    tipo_gestion: str = Field(..., max_length=50)
    resultado: str = Field(..., max_length=50)
    monto_pagado: float | None = None
    fecha_compromiso: str | None = None
    monto_compromiso: float | None = None
    observaciones: str | None = None
    lat: float | None = None
    lng: float | None = None
