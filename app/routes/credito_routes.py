from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_cliente_id
from app.schemas.credito_schema import SolicitudCreditoRequest, SolicitudCreditoOut
from app.services.credito_service import CreditoService

router = APIRouter(prefix="/creditos", tags=["Créditos"])


@router.post("/solicitar", response_model=SolicitudCreditoOut)
def solicitar_credito(body: SolicitudCreditoRequest, cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    solicitud = service.solicitar(
        cliente_id,
        body.tipo_credito,
        body.monto_solicitado,
        body.numero_cuotas,
        body.motivo,
        body.ingresos_mensuales,
        body.actividad_economica,
    )
    db.commit()
    return solicitud


@router.get("")
def listar_creditos(cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    return service.listar(cliente_id)
