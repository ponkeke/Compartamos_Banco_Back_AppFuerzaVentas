from sqlalchemy import Column, Integer, String, DateTime, Text, func
from app.core.cfg_database import Base


class SolicitudRegistroCliente(Base):
    __tablename__ = "solicitudes_registro_cliente"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dni = Column(String(8), nullable=False, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=False)
    correo = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    estado = Column(String(20), nullable=False, default="PENDIENTE")
    observacion = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
