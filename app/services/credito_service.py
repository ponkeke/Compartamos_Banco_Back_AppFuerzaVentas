from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.credito_repository import SolicitudCreditoRepository, CreditoRepository, CronogramaCuotaRepository
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.repositories.notificacion_repository import NotificacionRepository
from app.core.tarifario import obtener_tasa_producto, obtener_seguro_producto, calcular_cuota_estimada
from datetime import date, timedelta
from decimal import Decimal
import random
import string


def _generar_expediente() -> str:
    year = date.today().year
    num = "".join(random.choices(string.digits, k=6))
    return f"CB-{year}-{num}"


class CreditoService:
    def __init__(self, db: Session):
        self.db = db
        self.cliente_repo = ClienteRepository(db)
        self.solicitud_repo = SolicitudCreditoRepository(db)
        self.credito_repo = CreditoRepository(db)
        self.cronograma_repo = CronogramaCuotaRepository(db)
        self.cuenta_repo = CuentaRepository(db)
        self.transaccion_repo = TransaccionRepository(db)
        self.empleado_repo = EmpleadoRepository(db)
        self.notificacion_repo = NotificacionRepository(db)

    def solicitar(self, cliente_id: int, tipo_credito: str, monto_solicitado: Decimal, numero_cuotas: int, **kwargs):
        print("  └─ CreditoService.solicitar()")
        print(f"     cliente_id={cliente_id}, tipo_credito={tipo_credito}, monto={monto_solicitado}, cuotas={numero_cuotas}")

        print("     >>> ANTES DE BUSCAR CLIENTE")
        cliente = self.cliente_repo.get_by_id(cliente_id)
        print(f"     >>> CLIENTE OBTENIDO: {cliente.id if cliente else 'NONE'}")
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        print("     >>> ANTES DE OBTENER TASA")
        tasa = obtener_tasa_producto(tipo_credito)
        print(f"     >>> TASA OBTENIDA: {tasa}")

        print("     >>> ANTES DE SOLICITUD_REPO.CREATE")
        solicitud = self.solicitud_repo.create(
            cliente_id=cliente_id,
            tipo_credito=tipo_credito,
            monto_solicitado=monto_solicitado,
            numero_cuotas=numero_cuotas,
            tea=tasa,
            motivo=kwargs.pop("motivo", None),
            ingreso_mensual=kwargs.pop("ingreso_mensual", None) or kwargs.pop("ingresos_mensuales", None),
            gasto_mensual=kwargs.pop("gasto_mensual", None),
            actividad_economica=kwargs.pop("actividad_economica", None),
            garantia=kwargs.pop("garantia", None),
            destino=kwargs.pop("destino", None) or kwargs.pop("destino_credito", None),
            plazo=kwargs.pop("plazo", None),
        )
        print(f"     >>> SOLICITUD REPO CREATE OK: id={solicitud.id}")

        expediente = _generar_expediente()
        solicitud.numero_expediente = expediente
        self.db.flush()
        print(f"     >>> EXPEDIENTE GENERADO: {expediente}")

        print("     >>> ANTES DE NOTIFICACION_REPO.CREATE")
        self.notificacion_repo.create(
            cliente_id=cliente_id,
            tipo="CREDITO",
            titulo="Solicitud de crédito registrada",
            descripcion=f"Tu solicitud de {tipo_credito} por S/ {monto_solicitado} está en revisión.",
        )
        print("     >>> NOTIFICACION REPO CREATE OK")

        print("     └─ CreditoService.solicitar() returning")
        return solicitud

    def listar_solicitudes(self):
        return self.solicitud_repo.get_all()

    def listar_pendientes(self):
        return self.solicitud_repo.get_pendientes()

    def obtener_detalle(self, solicitud_id: int):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")

        cliente = self.cliente_repo.get_by_id(solicitud.cliente_id)
        return {
            "id": solicitud.id,
            "cliente_id": solicitud.cliente_id,
            "tipo_credito": solicitud.tipo_credito,
            "monto_solicitado": solicitud.monto_solicitado,
            "numero_cuotas": solicitud.numero_cuotas,
            "motivo": solicitud.motivo,
            "estado": solicitud.estado,
            "fecha_solicitud": solicitud.fecha_solicitud,
            "plazo": solicitud.plazo,
            "tea": solicitud.tea,
            "garantia": solicitud.garantia,
            "destino": solicitud.destino,
            "ingreso_mensual": solicitud.ingreso_mensual,
            "gasto_mensual": solicitud.gasto_mensual,
            "actividad_economica": solicitud.actividad_economica,
            "canal": solicitud.canal,
            "numero_expediente": solicitud.numero_expediente,
            "cliente_nombres": cliente.nombres if cliente else None,
            "cliente_apellidos": cliente.apellidos if cliente else None,
            "cliente_dni": cliente.dni if cliente else None,
        }

    def aprobar(self, solicitud_id: int, empleado_id: int):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        if solicitud.estado != "PENDIENTE" and solicitud.estado != "EN_EVALUACION":
            raise HTTPException(status_code=400, detail=f"Estado actual: {solicitud.estado}. No se puede aprobar.")

        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        expediente = _generar_expediente()
        self.solicitud_repo.update_estado(solicitud, "APROBADO", numero_expediente=expediente)

        self.notificacion_repo.create(
            cliente_id=solicitud.cliente_id,
            tipo="CREDITO",
            titulo="Solicitud aprobada",
            descripcion=f"Tu solicitud de {solicitud.tipo_credito} fue aprobada. Próximo paso: desembolso.",
        )

        return solicitud

    def rechazar(self, solicitud_id: int, empleado_id: int):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        if solicitud.estado != "PENDIENTE" and solicitud.estado != "EN_EVALUACION":
            raise HTTPException(status_code=400, detail=f"No se puede rechazar. Estado actual: {solicitud.estado}")

        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        self.solicitud_repo.update_estado(solicitud, "RECHAZADO")

        self.notificacion_repo.create(
            cliente_id=solicitud.cliente_id,
            tipo="CREDITO",
            titulo="Solicitud rechazada",
            descripcion=f"Tu solicitud de {solicitud.tipo_credito} no fue aprobada.",
        )

        return solicitud

    def desembolsar(self, solicitud_id: int, empleado_id: int):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        if solicitud.estado != "APROBADO":
            raise HTTPException(status_code=400, detail=f"Debe estar APROBADO (actual: {solicitud.estado})")

        cliente = self.cliente_repo.get_by_id(solicitud.cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        cuenta = self.cuenta_repo.get_by_cliente_id(solicitud.cliente_id)
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cliente sin cuenta activa")

        tasa = solicitud.tea or obtener_tasa_producto(solicitud.tipo_credito) or Decimal("30.00")
        monto = solicitud.monto_solicitado
        hoy = date.today()

        credito = self.credito_repo.create(
            cliente_id=solicitud.cliente_id,
            solicitud_id=solicitud.id,
            tipo_credito=solicitud.tipo_credito,
            monto_desembolsado=monto,
            tasa_interes=tasa,
            numero_cuotas=solicitud.numero_cuotas,
            fecha_inicio=hoy,
        )

        seguro_pct = obtener_seguro_producto(solicitud.tipo_credito)
        tem = ((1 + float(tasa) / 100) ** (1 / 12)) - 1
        n = solicitud.numero_cuotas
        factor = (tem * (1 + tem) ** n) / ((1 + tem) ** n - 1) if tem > 0 else 1 / n
        cuota_total = round(float(monto) * factor, 2)

        cuotas = []
        saldo = float(monto)
        for i in range(1, n + 1):
            interes = round(saldo * tem, 2)
            capital = round(cuota_total - interes, 2)
            if i == n:
                capital = round(saldo, 2)
                cuota_total = round(capital + interes, 2)
            seguro = round(float(monto) * seguro_pct / 100, 2)
            monto_cuota = round(capital + interes + seguro, 2)
            fecha_venc = hoy + timedelta(days=30 * i)
            cuotas.append({
                "credito_id": credito.id,
                "numero_cuota": i,
                "fecha_vencimiento": fecha_venc,
                "capital": Decimal(str(capital)),
                "interes": Decimal(str(interes)),
                "seguro": Decimal(str(seguro)),
                "monto_total": Decimal(str(monto_cuota)),
            })
            saldo -= capital

        self.cronograma_repo.bulk_create(cuotas)

        nuevo_saldo = cuenta.saldo + monto
        self.cuenta_repo.update_saldo(cuenta.id, nuevo_saldo)

        self.transaccion_repo.create(
            cuenta_id=cuenta.id,
            tipo="DESEMBOLSO",
            descripcion=f"Desembolso {solicitud.tipo_credito} - Exp. {solicitud.numero_expediente or solicitud.id}",
            monto=monto,
            saldo_resultante=nuevo_saldo,
        )

        self.solicitud_repo.update_estado(solicitud, "DESEMBOLSADO")

        self.notificacion_repo.create(
            cliente_id=solicitud.cliente_id,
            tipo="CREDITO",
            titulo="¡Crédito desembolsado!",
            descripcion=f"Se desembolsó S/ {monto} de {solicitud.tipo_credito} a tu cuenta.",
        )

        return {"credito_id": credito.id, "mensaje": "Crédito desembolsado exitosamente"}

    def listar_creditos(self):
        return self.credito_repo.get_all()

    def obtener_credito(self, credito_id: int):
        credito = self.credito_repo.get_by_id(credito_id)
        if not credito:
            raise HTTPException(status_code=404, detail="Crédito no encontrado")
        cliente = self.cliente_repo.get_by_id(credito.cliente_id)
        cuotas = self.cronograma_repo.get_by_credito_id(credito_id)
        return {
            "id": credito.id,
            "cliente_id": credito.cliente_id,
            "solicitud_id": credito.solicitud_id,
            "tipo_credito": credito.tipo_credito,
            "monto_desembolsado": credito.monto_desembolsado,
            "saldo_pendiente": credito.saldo_pendiente,
            "tasa_interes": credito.tasa_interes,
            "numero_cuotas": credito.numero_cuotas,
            "cuota_actual": credito.cuota_actual,
            "estado": credito.estado,
            "fecha_inicio": credito.fecha_inicio,
            "fecha_fin": credito.fecha_fin,
            "cliente_nombres": cliente.nombres if cliente else None,
            "cliente_apellidos": cliente.apellidos if cliente else None,
            "cliente_dni": cliente.dni if cliente else None,
            "cronograma": [
                {
                    "id": c.id,
                    "numero_cuota": c.numero_cuota,
                    "fecha_vencimiento": c.fecha_vencimiento,
                    "capital": c.capital,
                    "interes": c.interes,
                    "seguro": c.seguro,
                    "monto_total": c.monto_total,
                    "estado": c.estado,
                }
                for c in cuotas
            ],
        }

    def get_cronograma(self, credito_id: int):
        credito = self.credito_repo.get_by_id(credito_id)
        if not credito:
            raise HTTPException(status_code=404, detail="Crédito no encontrado")
        return self.cronograma_repo.get_by_credito_id(credito_id)
