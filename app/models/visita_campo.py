from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text, func
from app.core.cfg_database import Base


class VisitaCampo(Base):
    __tablename__ = "visitas_campo"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_credito.id"), nullable=True)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=True)
    estado_visita = Column(String(30), nullable=True)
    observacion = Column(Text, nullable=True)
    latitud = Column(Numeric(10, 7), nullable=True)
    longitud = Column(Numeric(10, 7), nullable=True)
    fecha_visita = Column(DateTime(timezone=True), server_default=func.now())
