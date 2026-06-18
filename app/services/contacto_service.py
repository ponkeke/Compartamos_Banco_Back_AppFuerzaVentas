from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.contacto_repository import ContactoRepository


class ContactoService:
    def __init__(self, db: Session):
        self.db = db
        self.contacto_repo = ContactoRepository(db)

    def listar(self, cliente_id: int):
        return self.contacto_repo.get_by_cliente_id(cliente_id)

    def crear(self, cliente_id: int, nombre: str, apellido: str, telefono: str):
        return self.contacto_repo.create(cliente_id, nombre, apellido, telefono)

    def eliminar(self, contacto_id: int, cliente_id: int):
        contacto = self.contacto_repo.get_by_id(contacto_id)
        if not contacto:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        if contacto.cliente_id != cliente_id:
            raise HTTPException(status_code=403, detail="No puedes eliminar este contacto")
        self.contacto_repo.delete(contacto)
        return {"mensaje": "Contacto eliminado"}
