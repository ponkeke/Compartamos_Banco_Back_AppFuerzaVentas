from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.cfg_database import Base


class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo_empleado = Column(String(20), unique=True, nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    cargo = Column(String(100), nullable=False)
    estado = Column(String(20), nullable=False, default="ACTIVO")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
