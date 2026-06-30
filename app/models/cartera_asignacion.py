from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from app.core.cfg_database import Base

class CarteraAsignacion(Base):
    __tablename__ = "cartera_asignaciones"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_credito.id"), nullable=False)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=False)
    estado_visita = Column(String(20), nullable=False, default="PENDIENTE")
    tipo_gestion = Column(String(50), nullable=True)
    prioridad = Column(String(10), nullable=True)
    score_prioridad = Column(Integer, nullable=True, default=0)
    monto_credito = Column(Numeric(12, 2), nullable=True)
    fecha_asignacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_visita = Column(DateTime(timezone=True), nullable=True)
    observacion = Column(String(500), nullable=True)
    latitud = Column(Numeric(10, 7), nullable=True)
    longitud = Column(Numeric(10, 7), nullable=True)
