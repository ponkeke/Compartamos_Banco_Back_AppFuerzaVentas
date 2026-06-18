from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_cliente_id
from app.services.cliente_service import ClienteService

router = APIRouter(prefix="/cliente", tags=["Cliente"])


@router.get("/home")
def home(cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = ClienteService(db)
    result = service.get_home(cliente_id)
    if result is None:
        return {"error": "Cliente no encontrado"}
    return result
