from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_cliente_id
from app.schemas.transaccion_schema import YapeoRequest, DepositoRequest, TransaccionOut
from app.services.operacion_service import OperacionService

router = APIRouter(prefix="/operaciones", tags=["Operaciones"])


@router.post("/yapeo")
def yapeo(body: YapeoRequest, cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = OperacionService(db)
    result = service.yapeo(cliente_id, body.numero_destino, body.monto)
    db.commit()
    return result


@router.post("/deposito")
def deposito(body: DepositoRequest, cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = OperacionService(db)
    result = service.deposito(cliente_id, body.monto, body.descripcion)
    db.commit()
    return result


@router.get("/movimientos", response_model=list[TransaccionOut])
def movimientos(cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = OperacionService(db)
    return service.movimientos(cliente_id)
