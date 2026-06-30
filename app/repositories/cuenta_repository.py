from sqlalchemy.orm import Session
from app.models.cuenta import Cuenta
from decimal import Decimal


class CuentaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_cliente_id(self, cliente_id: int) -> Cuenta | None:
        return self.db.query(Cuenta).filter(Cuenta.cliente_id == cliente_id).first()

    def get_by_id(self, cuenta_id: int) -> Cuenta | None:
        return self.db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()

    def create(self, cliente_id: int, numero_cuenta: str, tipo: str, moneda: str, saldo: float, tea: float) -> Cuenta:
        cuenta = Cuenta(
            cliente_id=cliente_id,
            numero_cuenta=numero_cuenta,
            tipo=tipo,
            moneda=moneda,
            saldo=saldo,
            tea=tea,
        )
        self.db.add(cuenta)
        self.db.flush()
        return cuenta

    def update_saldo(self, cuenta_id: int, nuevo_saldo: Decimal):
        cuenta = self.db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
        if cuenta:
            cuenta.saldo = nuevo_saldo
            self.db.flush()
            return cuenta
        return None
