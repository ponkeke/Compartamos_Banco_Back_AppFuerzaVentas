from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_cliente_id, get_current_empleado_id
from app.schemas.transaccion_schema import TransaccionOut, MovimientoRequest
from app.services.operacion_service import OperacionService

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])


@router.get("", response_model=list[TransaccionOut])
def listar_movimientos(cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = OperacionService(db)
    return service.listar_movimientos(cliente_id)


@router.post("", response_model=TransaccionOut)
def registrar_movimiento(body: MovimientoRequest, cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = OperacionService(db)
    result = service.registrar_movimiento(
        cuenta_id=body.cuenta_id,
        tipo=body.tipo,
        descripcion=body.descripcion,
        monto=body.monto,
    )
    db.commit()
    return result
