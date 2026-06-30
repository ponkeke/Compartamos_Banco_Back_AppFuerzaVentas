from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.contacto_repository import ContactoRepository
from decimal import Decimal


class OperacionService:
    def __init__(self, db: Session):
        self.db = db
        self.cuenta_repo = CuentaRepository(db)
        self.transaccion_repo = TransaccionRepository(db)
        self.contacto_repo = ContactoRepository(db)

    def listar_movimientos(self, cliente_id: int):
        cuenta = self.cuenta_repo.get_by_cliente_id(cliente_id)
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        return self.transaccion_repo.get_by_cuenta_id(cuenta.id, limit=50)

    def registrar_movimiento(self, cuenta_id: int, tipo: str, descripcion: str | None, monto: Decimal):
        cuenta = self.cuenta_repo.get_by_id(cuenta_id)
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        if tipo in ("YAPEO_ENVIADO", "RETIRO", "PAGO"):
            nuevo_saldo = cuenta.saldo - monto
            if nuevo_saldo < 0:
                raise HTTPException(status_code=400, detail="Saldo insuficiente")
        else:
            nuevo_saldo = cuenta.saldo + monto

        transaccion = self.transaccion_repo.create(
            cuenta_id=cuenta_id,
            tipo=tipo,
            descripcion=descripcion,
            monto=monto,
            saldo_resultante=nuevo_saldo,
        )
        self.cuenta_repo.update_saldo(cuenta_id, nuevo_saldo)
        return transaccion

    def listar_movimientos_global(self):
        return self.transaccion_repo.list_all()
