from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, func
from app.core.cfg_database import Base


class EvaluacionCredito(Base):
    __tablename__ = "evaluaciones_credito"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_credito.id"), nullable=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=True)
    resultado_pre_evaluacion = Column(String(50), nullable=True)
    resultado_buro = Column(String(50), nullable=True)
    capacidad_pago = Column(Numeric(12, 2), nullable=True)
    observaciones = Column(Text, nullable=True)
    fecha_evaluacion = Column(DateTime(timezone=True), server_default=func.now())
