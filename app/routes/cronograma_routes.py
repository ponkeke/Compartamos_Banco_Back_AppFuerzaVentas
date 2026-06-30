from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.schemas.cronograma_schema import CronogramaCuotaOut
from app.services.credito_service import CreditoService

router = APIRouter(prefix="/cronograma", tags=["Cronograma"])


@router.get("/{credito_id}", response_model=list[CronogramaCuotaOut])
def obtener_cronograma(credito_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    return service.get_cronograma(credito_id)
