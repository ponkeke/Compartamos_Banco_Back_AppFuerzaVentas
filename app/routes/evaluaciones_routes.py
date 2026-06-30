import random
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.schemas.evaluacion_schema import EvaluacionPreRequest, EvaluacionBuroRequest, EvaluacionOut
from app.services.evaluacion_service import EvaluacionService
from app.repositories.credito_repository import SolicitudCreditoRepository
from app.repositories.evaluacion_repository import EvaluacionRepository
from app.repositories.empleado_repository import EmpleadoRepository

router = APIRouter(prefix="/evaluaciones", tags=["Evaluaciones"])


@router.post("/pre", response_model=EvaluacionOut)
def pre_evaluar(body: EvaluacionPreRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = EvaluacionService(db)
    result = service.pre_evaluar(
        solicitud_id=body.solicitud_id,
        empleado_id=empleado_id,
        resultado=body.resultado,
        capacidad_pago=body.capacidad_pago,
        observaciones=body.observaciones,
    )
    db.commit()
    return result


@router.post("/buro", response_model=EvaluacionOut)
def evaluar_buro(body: EvaluacionBuroRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = EvaluacionService(db)
    result = service.evaluar_buro(
        solicitud_id=body.solicitud_id,
        empleado_id=empleado_id,
        resultado=body.resultado,
        observaciones=body.observaciones,
    )
    db.commit()
    return result
