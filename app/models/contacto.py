from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.core.cfg_database import Base


class Contacto(Base):
    __tablename__ = "contactos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
