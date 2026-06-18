from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.credito_repository import SolicitudCreditoRepository, CreditoRepository, CronogramaCuotaRepository
from app.repositories.cuenta_repository import CuentaRepository
from app.repositories.transaccion_repository import TransaccionRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.repositories.notificacion_repository import NotificacionRepository
from app.core.tarifario import obtener_tasa_producto, obtener_seguro_producto, calcular_cuota_estimada
from datetime import date, timedelta
from decimal import Decimal


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

    def solicitar(self, cliente_id: int, tipo_credito: str, monto_solicitado: Decimal, numero_cuotas: int, motivo: str | None, ingresos_mensuales: Decimal | None = None, actividad_economica: str | None = None):
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        tasa = obtener_tasa_producto(tipo_credito)
        cuota_estimada = None
        if tasa and monto_solicitado:
            cuota_estimada = calcular_cuota_estimada(float(monto_solicitado), tasa, numero_cuotas)

        solicitud = self.solicitud_repo.create(
            cliente_id=cliente_id,
            tipo_credito=tipo_credito,
            monto_solicitado=monto_solicitado,
            numero_cuotas=numero_cuotas,
            motivo=motivo,
            ingresos_mensuales=ingresos_mensuales,
            actividad_economica=actividad_economica,
            cuota_estimada=cuota_estimada,
            tasa_interes=tasa,
        )

        self.notificacion_repo.create(
            cliente_id=cliente_id,
            tipo="CREDITO",
            titulo="Solicitud de crédito registrada",
            descripcion=f"Tu solicitud de {tipo_credito} por S/ {monto_solicitado} está en revisión.",
        )

        return solicitud

    def listar(self, cliente_id: int):
        solicitudes = self.solicitud_repo.get_by_cliente_id(cliente_id)
        creditos = self.credito_repo.get_by_cliente_id(cliente_id)
        return {
            "solicitudes": solicitudes,
            "creditos": creditos,
        }

    def listar_pendientes(self):
        return self.solicitud_repo.get_pendientes()

    def obtener_detalle(self, solicitud_id: int):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")

        cliente = self.cliente_repo.get_by_id(solicitud.cliente_id)
        empleado = None
        if solicitud.empleado_evaluador_id:
            empleado = self.empleado_repo.get_by_id(solicitud.empleado_evaluador_id)

        result = {
            "id": solicitud.id,
            "cliente_id": solicitud.cliente_id,
            "tipo_credito": solicitud.tipo_credito,
            "monto_solicitado": solicitud.monto_solicitado,
            "numero_cuotas": solicitud.numero_cuotas,
            "motivo": solicitud.motivo,
            "ingresos_mensuales": solicitud.ingresos_mensuales,
            "actividad_economica": solicitud.actividad_economica,
            "tasa_interes": solicitud.tasa_interes,
            "cuota_estimada": solicitud.cuota_estimada,
            "estado": solicitud.estado,
            "fecha_solicitud": solicitud.fecha_solicitud,
            "fecha_evaluacion": solicitud.fecha_evaluacion,
            "empleado_evaluador_id": solicitud.empleado_evaluador_id,
            "observacion_evaluacion": solicitud.observacion_evaluacion,
            "cliente_nombres": cliente.nombres if cliente else None,
            "cliente_apellidos": cliente.apellidos if cliente else None,
            "cliente_dni": cliente.dni if cliente else None,
            "evaluador_nombres": empleado.nombres if empleado else None,
            "evaluador_apellidos": empleado.apellidos if empleado else None,
            "evaluador_codigo": empleado.codigo_empleado if empleado else None,
        }
        return result

    def evaluar(self, solicitud_id: int, empleado_id: int, nuevo_estado: str, observacion: str | None):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        if solicitud.estado not in ("PENDIENTE", "EN_EVALUACION"):
            raise HTTPException(status_code=400, detail=f"La solicitud ya fue evaluada (estado: {solicitud.estado})")

        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado evaluador no encontrado")

        solicitud = self.solicitud_repo.update_estado(
            solicitud,
            estado=nuevo_estado,
            empleado_evaluador_id=empleado_id,
            observacion=observacion,
        )

        cliente = self.cliente_repo.get_by_id(solicitud.cliente_id)
        if nuevo_estado == "APROBADO":
            titulo = "Solicitud de crédito aprobada"
            desc = f"Tu solicitud de {solicitud.tipo_credito} fue aprobada. Pronto realizaremos el desembolso."
            if cliente:
                self.notificacion_repo.create(
                    cliente_id=cliente.id,
                    tipo="CREDITO",
                    titulo=titulo,
                    descripcion=desc,
                )

        if nuevo_estado == "RECHAZADO":
            razon = f" Motivo: {observacion}" if observacion else ""
            self.notificacion_repo.create(
                cliente_id=solicitud.cliente_id,
                tipo="CREDITO",
                titulo="Solicitud de crédito rechazada",
                descripcion=f"Tu solicitud de {solicitud.tipo_credito} no fue aprobada.{razon}",
            )

        return solicitud

    def desembolsar(self, solicitud_id: int, empleado_id: int):
        solicitud = self.solicitud_repo.get_by_id(solicitud_id)
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        if solicitud.estado != "APROBADO":
            raise HTTPException(status_code=400, detail=f"La solicitud debe estar APROBADO para desembolsar (actual: {solicitud.estado})")

        empleado = self.empleado_repo.get_by_id(empleado_id)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        cliente = self.cliente_repo.get_by_id(solicitud.cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        cuenta = self.cuenta_repo.get_by_cliente_id(solicitud.cliente_id)
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cliente no tiene cuenta activa")

        tasa = solicitud.tasa_interes or obtener_tasa_producto(solicitud.tipo_credito) or Decimal("30.00")
        monto = solicitud.monto_solicitado
        hoy = date.today()

        # 1. Crear credito
        credito = self.credito_repo.create(
            cliente_id=solicitud.cliente_id,
            solicitud_id=solicitud.id,
            tipo_credito=solicitud.tipo_credito,
            monto_desembolsado=monto,
            tasa_interes=tasa,
            numero_cuotas=solicitud.numero_cuotas,
            fecha_inicio=hoy,
        )

        # 2. Generar cronograma (sistema francés)
        seguro_pct = obtener_seguro_producto(solicitud.tipo_credito)
        tem = ((1 + float(tasa) / 100) ** (1 / 12)) - 1
        n = solicitud.numero_cuotas
        if tem > 0:
            factor = (tem * (1 + tem) ** n) / ((1 + tem) ** n - 1)
            cuota_total = round(float(monto) * factor, 2)
        else:
            cuota_total = round(float(monto) / n, 2)

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

        # 3. Actualizar saldo cuenta
        nuevo_saldo = cuenta.saldo + monto
        self.cuenta_repo.update_saldo(cuenta.id, nuevo_saldo)

        # 4. Crear transaccion DESEMBOLSO
        self.transaccion_repo.create(
            cuenta_id=cuenta.id,
            tipo="DESEMBOLSO",
            descripcion=f"Desembolso de crédito {solicitud.tipo_credito} - Solicitud #{solicitud.id}",
            monto=monto,
            saldo_resultante=nuevo_saldo,
        )

        # 5. Actualizar estado solicitud
        self.solicitud_repo.update_estado(
            solicitud,
            estado="DESEMBOLSADO",
            empleado_evaluador_id=empleado_id,
            observacion="Crédito desembolsado exitosamente",
        )

        # 6. Notificar cliente
        self.notificacion_repo.create(
            cliente_id=solicitud.cliente_id,
            tipo="CREDITO",
            titulo="¡Crédito desembolsado!",
            descripcion=f"Se desembolsó S/ {monto} de {solicitud.tipo_credito} a tu cuenta.",
        )

        return {"credito_id": credito.id, "mensaje": "Crédito desembolsado exitosamente"}
