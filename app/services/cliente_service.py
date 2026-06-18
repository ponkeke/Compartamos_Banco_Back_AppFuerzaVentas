from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.credito_repository import SolicitudCreditoRepository, CreditoRepository
from app.repositories.notificacion_repository import NotificacionRepository


class ClienteService:
    def __init__(self, db: Session):
        self.db = db
        self.cliente_repo = ClienteRepository(db)
        self.cuenta_repo = CuentaRepository(db)
        self.transaccion_repo = TransaccionRepository(db)
        self.solicitud_repo = SolicitudCreditoRepository(db)
        self.credito_repo = CreditoRepository(db)
        self.notificacion_repo = NotificacionRepository(db)

    def get_home(self, cliente_id: int):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            return None

        cuenta = self.cuenta_repo.get_by_cliente_id(cliente_id)
        ultimos_movimientos = []
        creditos = []
        solicitudes = []
        notificaciones = []

        if cuenta:
            ultimos_movimientos = self.transaccion_repo.get_by_cuenta_id(cuenta.id, limit=5)

        creditos = self.credito_repo.get_by_cliente_id(cliente_id)
        solicitudes = self.solicitud_repo.get_by_cliente_id(cliente_id)
        notificaciones = self.notificacion_repo.get_by_cliente_id(cliente_id)

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
                "tea": cuenta.tea,
            } if cuenta else None,
            "ultimos_movimientos": [
                {
                    "id": t.id,
                    "tipo": t.tipo,
                    "descripcion": t.descripcion,
                    "monto": t.monto,
                    "saldo_resultante": t.saldo_resultante,
                    "fecha": t.fecha,
                }
                for t in ultimos_movimientos
            ],
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
            "solicitudes": [
                {
                    "id": s.id,
                    "tipo_credito": s.tipo_credito,
                    "monto_solicitado": s.monto_solicitado,
                    "estado": s.estado,
                    "fecha_solicitud": s.fecha_solicitud,
                }
                for s in solicitudes
            ],
            "notificaciones": [
                {
                    "id": n.id,
                    "tipo": n.tipo,
                    "titulo": n.titulo,
                    "descripcion": n.descripcion,
                    "leida": n.leida,
                    "fecha": n.fecha,
                }
                for n in notificaciones
            ],
        }
