from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from app.core.cfg_database import Base


class CronogramaCuota(Base):
    __tablename__ = "cronograma_cuotas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    credito_id = Column(Integer, ForeignKey("creditos.id"), nullable=False)
    numero_cuota = Column(Integer, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    capital = Column(Numeric(12, 2), nullable=False)
    interes = Column(Numeric(12, 2), nullable=False)
    seguro = Column(Numeric(12, 2), nullable=False, default=0.00)
    monto_total = Column(Numeric(12, 2), nullable=False)
    estado = Column(String(20), nullable=False, default="PENDIENTE")
