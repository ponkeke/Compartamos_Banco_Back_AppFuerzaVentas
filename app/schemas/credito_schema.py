from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal


class SolicitudCreditoRequest(BaseModel):
    tipo_credito: str = Field("CrediChamba", max_length=50)
    monto_solicitado: Decimal = Field(..., gt=0)
    numero_cuotas: int = Field(..., gt=0)
    motivo: str | None = None
    ingreso_mensual: Decimal | None = Field(None, gt=0)
    gasto_mensual: Decimal | None = Field(None, gt=0)
    actividad_economica: str | None = Field(None, max_length=100)
    garantia: str | None = Field(None, max_length=100)
    destino: str | None = Field(None, max_length=100)
    destino_credito: str | None = Field(None, max_length=100)
    plazo: int | None = None
    ingresos_mensuales: Decimal | None = Field(None, gt=0)

    class Config:
        extra = "allow"


class SolicitudCreditoOut(BaseModel):
    id: int
    cliente_id: int
    tipo_credito: str
    monto_solicitado: Decimal
    numero_cuotas: int
    motivo: str | None = None
    estado: str
    fecha_solicitud: datetime | None = None
    plazo: int | None = None
    tea: Decimal | None = None
    garantia: str | None = None
    destino: str | None = None
    ingreso_mensual: Decimal | None = None
    gasto_mensual: Decimal | None = None
    actividad_economica: str | None = None
    canal: str | None = None
    numero_expediente: str | None = None

    class Config:
        from_attributes = True


class SolicitudCreditoDetailOut(SolicitudCreditoOut):
    cliente_nombres: str | None = None
    cliente_apellidos: str | None = None
    cliente_dni: str | None = None


class CreditoOut(BaseModel):
    id: int
    cliente_id: int
    solicitud_id: int
    tipo_credito: str
    monto_desembolsado: Decimal
    saldo_pendiente: Decimal
    tasa_interes: Decimal
    numero_cuotas: int
    cuota_actual: int
    estado: str
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class CreditoDetailOut(CreditoOut):
    cliente_nombres: str | None = None
    cliente_apellidos: str | None = None
    cliente_dni: str | None = None
