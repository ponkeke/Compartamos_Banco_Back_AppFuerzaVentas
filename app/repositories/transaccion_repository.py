from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.transaccion import Transaccion
from decimal import Decimal


class TransaccionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cuenta_id: int, tipo: str, descripcion: str | None, monto: Decimal, saldo_resultante: Decimal) -> Transaccion:
        transaccion = Transaccion(
            cuenta_id=cuenta_id,
            tipo=tipo,
            descripcion=descripcion,
            monto=monto,
            saldo_resultante=saldo_resultante,
        )
        self.db.add(transaccion)
        self.db.flush()
        return transaccion

    def get_by_cuenta_id(self, cuenta_id: int, limit: int = 10):
        return (
            self.db.query(Transaccion)
            .filter(Transaccion.cuenta_id == cuenta_id)
            .order_by(desc(Transaccion.fecha))
            .limit(limit)
            .all()
        )

    def list_by_cuenta_id(self, cuenta_id: int):
        return (
            self.db.query(Transaccion)
            .filter(Transaccion.cuenta_id == cuenta_id)
            .order_by(desc(Transaccion.fecha))
            .all()
        )
