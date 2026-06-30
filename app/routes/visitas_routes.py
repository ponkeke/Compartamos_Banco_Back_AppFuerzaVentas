from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.schemas.visita_schema import VisitaCampoRequest, VisitaCampoOut
from app.services.visita_service import VisitaService

router = APIRouter(prefix="/visitas-campo", tags=["Visitas de Campo"])


@router.post("", response_model=VisitaCampoOut)
def registrar_visita(body: VisitaCampoRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = VisitaService(db)
    result = service.registrar_visita(
        solicitud_id=body.solicitud_id,
        empleado_id=empleado_id,
        estado_visita=body.estado_visita,
        observacion=body.observacion,
        latitud=body.latitud,
        longitud=body.longitud,
    )
    db.commit()
    return result
