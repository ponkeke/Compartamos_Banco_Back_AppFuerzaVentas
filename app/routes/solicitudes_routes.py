from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.schemas.credito_schema import SolicitudCreditoOut, SolicitudCreditoDetailOut, SolicitudCreditoRequest
from app.schemas.nota_solicitud_schema import NotaRequest, NotaOut
from app.services.credito_service import CreditoService
from app.repositories.nota_repository import NotaRepository

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes (Fuerza de Ventas)"])


@router.get("", response_model=list[SolicitudCreditoOut])
def listar_solicitudes(empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    return service.listar_solicitudes()


@router.post("", response_model=SolicitudCreditoOut)
def crear_solicitud(body: SolicitudCreditoRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    from app.repositories.cliente_repository import ClienteRepository
    from fastapi import HTTPException
    cliente_repo = ClienteRepository(db)
    cliente = cliente_repo.get_by_dni(body.dni) if hasattr(body, 'dni') and body.dni else None
    if not cliente and hasattr(body, 'dni') and body.dni:
        from app.core.security import hash_password
        cliente = cliente_repo.create(dni=body.dni, nombres=body.nombres or "PENDIENTE", apellidos=body.apellidos or "PENDIENTE", clave=hash_password("temporal123"))
    if not cliente:
        raise HTTPException(status_code=400, detail="Cliente no identificado. Proporcione DNI valido.")
    service = CreditoService(db)
    solicitud = service.solicitar(
        cliente_id=cliente.id,
        tipo_credito=body.tipo_credito,
        monto_solicitado=body.monto_solicitado,
        numero_cuotas=body.numero_cuotas,
        motivo=body.motivo,
        ingreso_mensual=body.ingreso_mensual or body.ingresos_mensuales,
        gasto_mensual=body.gasto_mensual,
        actividad_economica=body.actividad_economica,
        garantia=body.garantia,
        destino=body.destino or body.destino_credito,
        plazo=body.plazo,
    )
    db.commit()
    db.refresh(solicitud)
    return solicitud


@router.get("/{solicitud_id}", response_model=SolicitudCreditoDetailOut)
def obtener_solicitud(solicitud_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    return service.obtener_detalle(solicitud_id)


@router.put("/{solicitud_id}/evaluar", response_model=SolicitudCreditoOut)
def evaluar_solicitud(solicitud_id: int, body: dict, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    estado = body.get("estado", "").upper()
    observacion = body.get("observacion", "")
    service = CreditoService(db)
    if estado == "APROBADO":
        result = service.aprobar(solicitud_id, empleado_id)
    elif estado == "RECHAZADO":
        result = service.rechazar(solicitud_id, empleado_id)
    else:
        raise HTTPException(status_code=400, detail="Estado debe ser APROBADO o RECHAZADO")
    db.commit()
    return result


@router.put("/{solicitud_id}/aprobar", response_model=SolicitudCreditoOut)
def aprobar_solicitud(solicitud_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    result = service.aprobar(solicitud_id, empleado_id)
    db.commit()
    return result


@router.put("/{solicitud_id}/rechazar", response_model=SolicitudCreditoOut)
def rechazar_solicitud(solicitud_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    result = service.rechazar(solicitud_id, empleado_id)
    db.commit()
    return result


@router.put("/{solicitud_id}/desembolsar")
def desembolsar_solicitud(solicitud_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    result = service.desembolsar(solicitud_id, empleado_id)
    db.commit()
    return result


@router.get("/{solicitud_id}/notas", response_model=list[NotaOut])
def listar_notas(solicitud_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    repo = NotaRepository(db)
    return repo.get_by_solicitud_id(solicitud_id)


@router.post("/{solicitud_id}/notas", response_model=NotaOut)
def agregar_nota(solicitud_id: int, body: NotaRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    repo = NotaRepository(db)
    from app.repositories.credito_repository import SolicitudCreditoRepository
    solicitud_repo = SolicitudCreditoRepository(db)
    solicitud = solicitud_repo.get_by_id(solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    nota = repo.create(solicitud_id=solicitud_id, empleado_id=empleado_id, contenido=body.contenido)
    db.commit()
    return nota
