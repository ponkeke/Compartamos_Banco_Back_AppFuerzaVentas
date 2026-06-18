from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from app.core.cfg_database import Base


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    leida = Column(Boolean, nullable=False, default=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
