from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from app.core.cfg_database import Base


class SolicitudCredito(Base):
    __tablename__ = "solicitudes_credito"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    tipo_credito = Column(String(50), nullable=False)
    monto_solicitado = Column(Numeric(12, 2), nullable=False)
    numero_cuotas = Column(Integer, nullable=False)
    motivo = Column(String(255), nullable=True)

    ingresos_mensuales = Column(Numeric(12, 2), nullable=True)
    actividad_economica = Column(String(100), nullable=True)

    tasa_interes = Column(Numeric(5, 2), nullable=True)
    cuota_estimada = Column(Numeric(12, 2), nullable=True)

    estado = Column(String(20), nullable=False, default="PENDIENTE")
    fecha_solicitud = Column(DateTime(timezone=True), server_default=func.now())
    fecha_evaluacion = Column(DateTime(timezone=True), nullable=True)
    empleado_evaluador_id = Column(Integer, ForeignKey("empleados.id"), nullable=True)
    observacion_evaluacion = Column(String(500), nullable=True)
