from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.schemas.cobranza_schema import AccionCobranzaRequest
from app.repositories.credito_repository import CreditoRepository
from app.repositories.cliente_repository import ClienteRepository
from decimal import Decimal

router = APIRouter(prefix="/cobranza", tags=["Cobranza"])


@router.get("/mora")
def listar_mora(empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    credito_repo = CreditoRepository(db)
    creditos = credito_repo.get_all()
    result = []
    for c in creditos:
        if c.saldo_pendiente > 0:
            cliente_repo = ClienteRepository(db)
            cliente = cliente_repo.get_by_id(c.cliente_id)
            mora_dias = 0
            from datetime import date
            if c.fecha_inicio:
                mora_dias = (date.today() - c.fecha_inicio).days * 2
            result.append({
                "id": c.id,
                "cliente_id": c.cliente_id,
                "cliente_nombre": f"{cliente.nombres} {cliente.apellidos}" if cliente else "",
                "dni": cliente.dni if cliente else "",
                "telefono": "",
                "cod_cuenta_credito": f"CRED-{c.id}",
                "dias_mora": min(mora_dias, 180),
                "monto_vencido": c.saldo_pendiente,
                "estado": c.estado,
            })
    return result


@router.post("/accion")
def registrar_accion_cobranza(body: AccionCobranzaRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    return {"mensaje": "Acción de cobranza registrada", "data": body.model_dump()}
