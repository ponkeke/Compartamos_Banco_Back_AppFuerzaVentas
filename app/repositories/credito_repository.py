from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.solicitud_credito import SolicitudCredito
from app.models.credito import Credito
from app.models.cronograma_cuota import CronogramaCuota
from decimal import Decimal


class SolicitudCreditoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente_id: int, tipo_credito: str, monto_solicitado, numero_cuotas: int, motivo: str | None, ingresos_mensuales=None, actividad_economica=None, cuota_estimada=None, tasa_interes=None) -> SolicitudCredito:
        solicitud = SolicitudCredito(
            cliente_id=cliente_id,
            tipo_credito=tipo_credito,
            monto_solicitado=monto_solicitado,
            numero_cuotas=numero_cuotas,
            motivo=motivo,
            ingresos_mensuales=ingresos_mensuales,
            actividad_economica=actividad_economica,
            cuota_estimada=cuota_estimada,
            tasa_interes=tasa_interes,
            estado="PENDIENTE",
        )
        self.db.add(solicitud)
        self.db.flush()
        return solicitud

    def get_by_cliente_id(self, cliente_id: int):
        return (
            self.db.query(SolicitudCredito)
            .filter(SolicitudCredito.cliente_id == cliente_id)
            .order_by(desc(SolicitudCredito.fecha_solicitud))
            .all()
        )

    def get_by_id(self, solicitud_id: int) -> SolicitudCredito | None:
        return self.db.query(SolicitudCredito).filter(SolicitudCredito.id == solicitud_id).first()

    def get_pendientes(self):
        return (
            self.db.query(SolicitudCredito)
            .filter(SolicitudCredito.estado.in_(["PENDIENTE", "EN_EVALUACION"]))
            .order_by(desc(SolicitudCredito.fecha_solicitud))
            .all()
        )

    def update_estado(self, solicitud: SolicitudCredito, estado: str, empleado_evaluador_id: int | None = None, observacion: str | None = None):
        solicitud.estado = estado
        solicitud.fecha_evaluacion = func.now()
        if empleado_evaluador_id is not None:
            solicitud.empleado_evaluador_id = empleado_evaluador_id
        if observacion is not None:
            solicitud.observacion_evaluacion = observacion
        self.db.flush()
        return solicitud


class CreditoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_cliente_id(self, cliente_id: int):
        return (
            self.db.query(Credito)
            .filter(Credito.cliente_id == cliente_id)
            .order_by(desc(Credito.created_at))
            .all()
        )

    def create(self, cliente_id: int, solicitud_id: int, tipo_credito: str, monto_desembolsado: Decimal, tasa_interes: Decimal, numero_cuotas: int, fecha_inicio) -> Credito:
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
