from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.notificacion_repository import NotificacionRepository
from decimal import Decimal


class OperacionService:
    def __init__(self, db: Session):
        self.db = db
        self.cuenta_repo = CuentaRepository(db)
        self.transaccion_repo = TransaccionRepository(db)
        self.notificacion_repo = NotificacionRepository(db)

    def yapeo(self, cliente_id: int, numero_destino: str, monto: Decimal):
        cuenta = self.cuenta_repo.get_by_cliente_id(cliente_id)
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        if cuenta.saldo < monto:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")

        nuevo_saldo = cuenta.saldo - monto
        self.cuenta_repo.update_saldo(cuenta.id, nuevo_saldo)

        transaccion = self.transaccion_repo.create(
            cuenta_id=cuenta.id,
            tipo="YAPEO",
            descripcion=f"Yapeo a {numero_destino}",
            monto=-monto,
            saldo_resultante=nuevo_saldo,
        )

        self.notificacion_repo.create(
            cliente_id=cliente_id,
            tipo="YAPEO",
            titulo="Yapeo realizado",
            descripcion=f"Realizaste un yapeo por S/ {monto} a {numero_destino}",
        )

        return {
            "comprobante": {
                "tipo": "YAPEO",
                "monto": -monto,
                "destino": numero_destino,
                "saldo_resultante": nuevo_saldo,
                "fecha": transaccion.fecha,
            }
        }

    def deposito(self, cliente_id: int, monto: Decimal, descripcion: str | None):
        cuenta = self.cuenta_repo.get_by_cliente_id(cliente_id)
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        nuevo_saldo = cuenta.saldo + monto
        self.cuenta_repo.update_saldo(cuenta.id, nuevo_saldo)

        transaccion = self.transaccion_repo.create(
            cuenta_id=cuenta.id,
            tipo="DEPOSITO",
            descripcion=descripcion or "Depósito en ventanilla",
            monto=monto,
            saldo_resultante=nuevo_saldo,
        )

        self.notificacion_repo.create(
            cliente_id=cliente_id,
            tipo="DEPOSITO",
            titulo="Depósito recibido",
            descripcion=f"Se realizó un depósito por S/ {monto}",
        )

        return {
            "mensaje": "Depósito exitoso",
            "saldo_resultante": nuevo_saldo,
            "fecha": transaccion.fecha,
        }

    def movimientos(self, cliente_id: int):
        cuenta = self.cuenta_repo.get_by_cliente_id(cliente_id)
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        return self.transaccion_repo.list_by_cuenta_id(cuenta.id)
