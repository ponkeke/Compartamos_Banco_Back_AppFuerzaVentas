from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from app.core.cfg_database import Base


class FirmaCliente(Base):
    __tablename__ = "firmas_cliente"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_credito.id"), nullable=True)
    firma_base64 = Column(Text, nullable=True)
    fecha_firma = Column(DateTime(timezone=True), server_default=func.now())
