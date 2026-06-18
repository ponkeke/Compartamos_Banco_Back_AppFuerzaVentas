from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_cliente_id
from app.schemas.notificacion_schema import NotificacionOut
from app.repositories.notificacion_repository import NotificacionRepository

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])


@router.get("", response_model=list[NotificacionOut])
def listar_notificaciones(cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    repo = NotificacionRepository(db)
    return repo.get_by_cliente_id(cliente_id)


@router.put("/{notificacion_id}/leer", response_model=NotificacionOut)
def marcar_leida(notificacion_id: int, cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    repo = NotificacionRepository(db)
    notif = repo.get_by_id(notificacion_id)
    if not notif:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    if notif.cliente_id != cliente_id:
        raise HTTPException(status_code=403, detail="No puedes modificar esta notificación")
    repo.marcar_leida(notif)
    db.commit()
    return notif
