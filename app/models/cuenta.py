from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from app.core.cfg_database import Base


class Cuenta(Base):
    __tablename__ = "cuentas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    numero_cuenta = Column(String(20), unique=True, nullable=False)
    tipo = Column(String(50), nullable=False)
    moneda = Column(String(3), nullable=False, default="PEN")
    saldo = Column(Numeric(12, 2), nullable=False, default=0.00)
    tea = Column(Numeric(5, 2), nullable=False, default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
