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
    estado = Column(String(20), nullable=False, default="PENDIENTE")
    fecha_solicitud = Column(DateTime(timezone=True), server_default=func.now())
    plazo = Column(Integer, nullable=True)
    tea = Column(Numeric(5, 2), nullable=True)
    garantia = Column(String(100), nullable=True)
    destino = Column(String(100), nullable=True)
    ingreso_mensual = Column(Numeric(12, 2), nullable=True)
    gasto_mensual = Column(Numeric(12, 2), nullable=True)
    actividad_economica = Column(String(100), nullable=True)
    canal = Column(String(20), default="APP_CLIENTES")
    numero_expediente = Column(String(50), nullable=True)
