from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.repositories.cartera_repository import CarteraRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.credito_repository import SolicitudCreditoRepository
from app.schemas.cartera_schema import VisitaCarteraRequest, CarteraDetalleOut

router = APIRouter(prefix="/cartera", tags=["Cartera / Asignación"])


@router.get("", response_model=list[CarteraDetalleOut])
def listar_cartera(fecha: str | None = None, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    repo = CarteraRepository(db)
    items = repo.get_by_empleado_id(empleado_id)
    result = []
    for item in items:
        solicitud_repo = SolicitudCreditoRepository(db)
        solicitud = solicitud_repo.get_by_id(item.solicitud_id)
        cliente_nombre = None
        documento = None
        cliente_id = None
        if solicitud:
            cliente_repo = ClienteRepository(db)
            cliente = cliente_repo.get_by_id(solicitud.cliente_id)
            if cliente:
                cliente_nombre = f"{cliente.nombres} {cliente.apellidos}"
                documento = cliente.dni
                cliente_id = cliente.id
        result.append({
            "id": item.id,
            "solicitud_id": item.solicitud_id,
            "empleado_id": item.empleado_id,
            "estado_visita": item.estado_visita,
            "tipo_gestion": item.tipo_gestion,
            "prioridad": item.prioridad,
            "score_prioridad": item.score_prioridad,
            "monto_credito": item.monto_credito,
            "fecha_asignacion": item.fecha_asignacion,
            "cliente_nombre": cliente_nombre,
            "documento": documento,
            "cliente_id": cliente_id,
        })
    return result


@router.post("/{cartera_id}/visita")
def registrar_visita_cartera(cartera_id: int, body: VisitaCarteraRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    repo = CarteraRepository(db)
    item = repo.get_by_id(cartera_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item de cartera no encontrado")
    repo.registrar_visita(item, resultado=body.resultado, observacion=body.observacion, lat=body.lat, lng=body.lng)
    db.commit()
    return {"mensaje": "Visita registrada exitosamente"}
