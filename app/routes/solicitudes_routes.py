from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.schemas.credito_schema import (
    SolicitudCreditoOut,
    SolicitudCreditoDetailOut,
    EvaluarSolicitudRequest,
    DesembolsarResponse,
)
from app.services.credito_service import CreditoService

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes (Fuerza de Ventas)"])


@router.get("", response_model=list[SolicitudCreditoOut])
def listar_solicitudes_pendientes(empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    return service.listar_pendientes()


@router.get("/{solicitud_id}", response_model=SolicitudCreditoDetailOut)
def obtener_detalle_solicitud(solicitud_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    return service.obtener_detalle(solicitud_id)


@router.put("/{solicitud_id}/evaluar", response_model=SolicitudCreditoOut)
def evaluar_solicitud(solicitud_id: int, body: EvaluarSolicitudRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    solicitud = service.evaluar(solicitud_id, empleado_id, body.estado, body.observacion)
    db.commit()
    return solicitud


@router.put("/{solicitud_id}/desembolsar", response_model=DesembolsarResponse)
def desembolsar_solicitud(solicitud_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    result = service.desembolsar(solicitud_id, empleado_id)
    db.commit()
    return result
