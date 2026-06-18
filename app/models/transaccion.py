from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from app.core.cfg_database import Base


class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cuenta_id = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    tipo = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=True)
    monto = Column(Numeric(12, 2), nullable=False)
    saldo_resultante = Column(Numeric(12, 2), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
