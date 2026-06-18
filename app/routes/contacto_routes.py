from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_cliente_id
from app.schemas.contacto_schema import ContactoCreate, ContactoOut
from app.services.contacto_service import ContactoService

router = APIRouter(prefix="/contactos", tags=["Contactos"])


@router.get("", response_model=list[ContactoOut])
def listar_contactos(cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = ContactoService(db)
    return service.listar(cliente_id)


@router.post("", response_model=ContactoOut)
def crear_contacto(body: ContactoCreate, cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = ContactoService(db)
    contacto = service.crear(cliente_id, body.nombre, body.apellido, body.telefono)
    db.commit()
    return contacto


@router.delete("/{contacto_id}")
def eliminar_contacto(contacto_id: int, cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    service = ContactoService(db)
    result = service.eliminar(contacto_id, cliente_id)
    db.commit()
    return result
