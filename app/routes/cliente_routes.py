from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_cliente_id, get_current_empleado_id
from app.services.cliente_service import ClienteService
from app.repositories.cliente_repository import ClienteRepository

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("")
def listar_clientes(empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.listar_clientes()


@router.get("/pendientes")
def listar_pendientes(empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.listar_pendientes()


@router.get("/{cliente_id}")
def obtener_cliente(cliente_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.obtener_cliente(cliente_id)


@router.put("/{cliente_id}/aprobar")
def aprobar_cliente(cliente_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = ClienteService(db)
    result = service.aprobar_cliente(cliente_id)
    db.commit()
    return result


@router.put("/{cliente_id}/rechazar")
def rechazar_cliente(cliente_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = ClienteService(db)
    result = service.rechazar_cliente(cliente_id)
    db.commit()
    return result


@router.get("/{cliente_id}/ficha")
def ficha_cliente(cliente_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.obtener_cliente(cliente_id)


@router.post("/{cliente_id}/ubicacion")
def actualizar_ubicacion(cliente_id: int, body: dict, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    return {"mensaje": "Ubicación actualizada", "cliente_id": cliente_id, "lat": body.get("lat"), "lng": body.get("lng")}
