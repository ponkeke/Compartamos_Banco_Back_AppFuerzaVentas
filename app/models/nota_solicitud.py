from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from app.core.cfg_database import Base

class NotaSolicitud(Base):
    __tablename__ = "notas_solicitud"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_credito.id"), nullable=False)
    empleado_id = Column(Integer, ForeignKey("empleados.id"), nullable=False)
    contenido = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
