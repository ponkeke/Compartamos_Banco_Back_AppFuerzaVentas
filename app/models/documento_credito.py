from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from app.core.cfg_database import Base


class DocumentoCredito(Base):
    __tablename__ = "documentos_credito"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes_credito.id"), nullable=True)
    tipo_documento = Column(String(100), nullable=True)
    archivo_url = Column(Text, nullable=True)
    fecha_subida = Column(DateTime(timezone=True), server_default=func.now())
