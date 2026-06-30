from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.cfg_database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dni = Column(String(8), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    clave = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    estado_registro = Column(String(20), default="ACTIVO")
