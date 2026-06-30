from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.credito_repository import CreditoRepository, SolicitudCreditoRepository


class ClienteService:
    def __init__(self, db: Session):
        self.db = db
        self.cliente_repo = ClienteRepository(db)
        self.cuenta_repo = CuentaRepository(db)
        self.transaccion_repo = TransaccionRepository(db)
        self.credito_repo = CreditoRepository(db)
        self.solicitud_repo = SolicitudCreditoRepository(db)

    def get_home(self, cliente_id: int):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            return None
        cuenta = self.cuenta_repo.get_by_cliente_id(cliente_id)
        creditos = self.credito_repo.get_by_cliente_id(cliente_id)
        transacciones = []
        if cuenta:
            transacciones = self.transaccion_repo.get_by_cuenta_id(cuenta.id)
        return {
            "cliente": {
                "id": cliente.id,
                "dni": cliente.dni,
                "nombres": cliente.nombres,
                "apellidos": cliente.apellidos,
            },
            "cuenta": {
                "id": cuenta.id,
                "numero_cuenta": cuenta.numero_cuenta,
                "tipo": cuenta.tipo,
                "moneda": cuenta.moneda,
                "saldo": cuenta.saldo,
            } if cuenta else None,
            "creditos": [
                {
                    "id": c.id,
                    "tipo_credito": c.tipo_credito,
                    "monto_desembolsado": c.monto_desembolsado,
                    "saldo_pendiente": c.saldo_pendiente,
                    "estado": c.estado,
                    "cuota_actual": c.cuota_actual,
                    "numero_cuotas": c.numero_cuotas,
                }
                for c in creditos
            ],
            "ultimos_movimientos": [
                {
                    "id": t.id,
                    "tipo": t.tipo,
                    "monto": t.monto,
                    "saldo_resultante": t.saldo_resultante,
                    "fecha": t.fecha,
                }
                for t in transacciones
            ],
        }

    def listar_clientes(self):
        clientes = self.cliente_repo.get_all()
        result = []
        for c in clientes:
            cuenta = self.cuenta_repo.get_by_cliente_id(c.id)
            result.append({
                "id": c.id,
                "dni": c.dni,
                "nombres": c.nombres,
                "apellidos": c.apellidos,
                "estado_registro": c.estado_registro,
                "saldo": cuenta.saldo if cuenta else 0,
            })
        return result

    def listar_pendientes(self):
        return self.cliente_repo.get_pendientes()

    def aprobar_cliente(self, cliente_id: int):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        if cliente.estado_registro != "PENDIENTE":
            raise HTTPException(status_code=400, detail=f"Solo se puede aprobar clientes PENDIENTE (actual: {cliente.estado_registro})")
        return self.cliente_repo.update_estado(cliente, "ACTIVO")

    def rechazar_cliente(self, cliente_id: int):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        if cliente.estado_registro != "PENDIENTE":
            raise HTTPException(status_code=400, detail=f"Solo se puede rechazar clientes PENDIENTE (actual: {cliente.estado_registro})")
        return self.cliente_repo.update_estado(cliente, "RECHAZADO")

    def obtener_cliente(self, cliente_id: int):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        cuenta = self.cuenta_repo.get_by_cliente_id(cliente_id)
        creditos = self.credito_repo.get_by_cliente_id(cliente_id)
        return {
            "id": cliente.id,
            "dni": cliente.dni,
            "nombres": cliente.nombres,
            "apellidos": cliente.apellidos,
            "estado_registro": cliente.estado_registro,
            "created_at": cliente.created_at,
            "cuenta": {
                "numero_cuenta": cuenta.numero_cuenta,
                "tipo": cuenta.tipo,
                "moneda": cuenta.moneda,
                "saldo": cuenta.saldo,
            } if cuenta else None,
            "creditos": [
                {
                    "id": c.id,
                    "tipo_credito": c.tipo_credito,
                    "monto_desembolsado": c.monto_desembolsado,
                    "saldo_pendiente": c.saldo_pendiente,
                    "estado": c.estado,
                }
                for c in creditos
            ],
        }
