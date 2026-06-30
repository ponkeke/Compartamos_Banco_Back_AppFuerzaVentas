from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.schemas.firma_schema import FirmaRequest, FirmaOut
from app.services.firma_service import FirmaService

router = APIRouter(prefix="/firmas", tags=["Firmas"])


@router.post("", response_model=FirmaOut)
def registrar_firma(body: FirmaRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = FirmaService(db)
    result = service.registrar_firma(
        solicitud_id=body.solicitud_id,
        firma_base64=body.firma_base64,
    )
    db.commit()
    return result
