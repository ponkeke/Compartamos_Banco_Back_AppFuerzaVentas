from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal


class SolicitudCreditoRequest(BaseModel):
    tipo_credito: str = Field(..., max_length=50)
    monto_solicitado: Decimal = Field(..., gt=0)
    numero_cuotas: int = Field(..., gt=0)
    motivo: str | None = None
    ingresos_mensuales: Decimal | None = Field(None, gt=0)
    actividad_economica: str | None = Field(None, max_length=100)


class SolicitudCreditoOut(BaseModel):
    id: int
    cliente_id: int
    tipo_credito: str
    monto_solicitado: Decimal
    numero_cuotas: int
    motivo: str | None = None
    ingresos_mensuales: Decimal | None = None
    actividad_economica: str | None = None
    tasa_interes: Decimal | None = None
    cuota_estimada: Decimal | None = None
    estado: str
    fecha_solicitud: datetime | None = None
    fecha_evaluacion: datetime | None = None
    empleado_evaluador_id: int | None = None
    observacion_evaluacion: str | None = None

    class Config:
        from_attributes = True


class SolicitudCreditoDetailOut(SolicitudCreditoOut):
    cliente_nombres: str | None = None
    cliente_apellidos: str | None = None
    cliente_dni: str | None = None
    evaluador_nombres: str | None = None
    evaluador_apellidos: str | None = None
    evaluador_codigo: str | None = None


class EvaluarSolicitudRequest(BaseModel):
    estado: str = Field(..., pattern="^(APROBADO|RECHAZADO)$")
    observacion: str | None = Field(None, max_length=500)


class DesembolsarResponse(BaseModel):
    credito_id: int
    mensaje: str


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
