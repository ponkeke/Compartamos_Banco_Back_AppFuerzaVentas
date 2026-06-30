from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.solicitud_credito import SolicitudCredito
from app.models.credito import Credito
from app.models.cronograma_cuota import CronogramaCuota


class SolicitudCreditoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente_id: int, tipo_credito: str, monto_solicitado, numero_cuotas: int, **kwargs) -> SolicitudCredito:
        solicitud = SolicitudCredito(
            cliente_id=cliente_id,
            tipo_credito=tipo_credito,
            monto_solicitado=monto_solicitado,
            numero_cuotas=numero_cuotas,
            estado="PENDIENTE",
            canal="APP_CLIENTES",
        )
        for k, v in kwargs.items():
            if v is not None and hasattr(solicitud, k):
                setattr(solicitud, k, v)
        print("        >>> ANTES DE DB.ADD (solicitud)")
        self.db.add(solicitud)
        print("        >>> DESPUES DE DB.ADD (solicitud)")
        print("        >>> ANTES DE DB.FLUSH (solicitud)")
        self.db.flush()
        print("        >>> DESPUES DE DB.FLUSH (solicitud)")
        return solicitud

    def get_by_id(self, solicitud_id: int) -> SolicitudCredito | None:
        return self.db.query(SolicitudCredito).filter(SolicitudCredito.id == solicitud_id).first()

    def get_by_cliente_id(self, cliente_id: int):
        return (
            self.db.query(SolicitudCredito)
            .filter(SolicitudCredito.cliente_id == cliente_id)
            .order_by(desc(SolicitudCredito.fecha_solicitud))
            .all()
        )

    def get_all(self):
        return (
            self.db.query(SolicitudCredito)
            .order_by(desc(SolicitudCredito.fecha_solicitud))
            .all()
        )

    def get_pendientes(self):
        return (
            self.db.query(SolicitudCredito)
            .filter(SolicitudCredito.estado.in_(["PENDIENTE", "EN_EVALUACION"]))
            .order_by(desc(SolicitudCredito.fecha_solicitud))
            .all()
        )

    def update_estado(self, solicitud: SolicitudCredito, estado: str, numero_expediente: str | None = None):
        solicitud.estado = estado
        if numero_expediente:
            solicitud.numero_expediente = numero_expediente
        self.db.flush()
        return solicitud


class CreditoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, credito_id: int) -> Credito | None:
        return self.db.query(Credito).filter(Credito.id == credito_id).first()

    def get_by_cliente_id(self, cliente_id: int):
        return (
            self.db.query(Credito)
            .filter(Credito.cliente_id == cliente_id)
            .order_by(desc(Credito.created_at))
            .all()
        )

    def get_all(self):
        return (
            self.db.query(Credito)
            .order_by(desc(Credito.created_at))
            .all()
        )

    def create(self, cliente_id: int, solicitud_id: int, tipo_credito: str, monto_desembolsado, tasa_interes, numero_cuotas: int, fecha_inicio) -> Credito:
        credito = Credito(
            cliente_id=cliente_id,
            solicitud_id=solicitud_id,
            tipo_credito=tipo_credito,
            monto_desembolsado=monto_desembolsado,
            saldo_pendiente=monto_desembolsado,
            tasa_interes=tasa_interes,
            numero_cuotas=numero_cuotas,
            cuota_actual=0,
            estado="ACTIVO",
            fecha_inicio=fecha_inicio,
        )
        self.db.add(credito)
        self.db.flush()
        return credito


class CronogramaCuotaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_credito_id(self, credito_id: int):
        return (
            self.db.query(CronogramaCuota)
            .filter(CronogramaCuota.credito_id == credito_id)
            .order_by(CronogramaCuota.numero_cuota)
            .all()
        )

    def bulk_create(self, cuotas: list[dict]):
        for c in cuotas:
            cuota = CronogramaCuota(
                credito_id=c["credito_id"],
                numero_cuota=c["numero_cuota"],
                fecha_vencimiento=c["fecha_vencimiento"],
                capital=c["capital"],
                interes=c["interes"],
                seguro=c["seguro"],
                monto_total=c["monto_total"],
            )
            self.db.add(cuota)
        self.db.flush()
