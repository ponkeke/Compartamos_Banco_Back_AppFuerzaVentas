from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, func
from app.core.cfg_database import Base


class Credito(Base):
    __tablename__ = "creditos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_credito.id"), nullable=False)
    tipo_credito = Column(String(50), nullable=False)
    monto_desembolsado = Column(Numeric(12, 2), nullable=False)
    saldo_pendiente = Column(Numeric(12, 2), nullable=False)
    tasa_interes = Column(Numeric(5, 2), nullable=False)
    numero_cuotas = Column(Integer, nullable=False)
    cuota_actual = Column(Integer, nullable=False, default=0)
    estado = Column(String(20), nullable=False, default="ACTIVO")
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
