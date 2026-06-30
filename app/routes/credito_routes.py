from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_cliente_id, get_current_empleado_id
from app.schemas.credito_schema import (
    SolicitudCreditoRequest,
    SolicitudCreditoOut,
    CreditoOut,
    CreditoDetailOut,
)
from app.services.credito_service import CreditoService
import traceback

router = APIRouter(prefix="/creditos", tags=["Créditos"])


@router.post("/solicitar", response_model=SolicitudCreditoOut)
def solicitar_credito(body: SolicitudCreditoRequest, cliente_id: int = Depends(get_current_cliente_id), db: Session = Depends(get_db)):
    print("===================================")
    print(">>> SOLICITUD RECIBIDA")
    print(f"cliente_id={cliente_id}")
    print(f"body={body.model_dump()}")
    print("===================================")
    try:
        print(">>> DB SESSION OK")
        service = CreditoService(db)
        print(">>> CREANDO MODELO")
        solicitud = service.solicitar(
            cliente_id=cliente_id,
            tipo_credito=body.tipo_credito,
            monto_solicitado=body.monto_solicitado,
            numero_cuotas=body.numero_cuotas,
            motivo=body.motivo,
            ingreso_mensual=body.ingreso_mensual or body.ingresos_mensuales,
            gasto_mensual=body.gasto_mensual,
            actividad_economica=body.actividad_economica,
            garantia=body.garantia,
            destino=body.destino or body.destino_credito,
            plazo=body.plazo,
        )
        print(">>> ANTES DE COMMIT")
        db.commit()
        print(">>> COMMIT OK")
        print(">>> ANTES DE REFRESH")
        db.refresh(solicitud)
        print(">>> REFRESH OK")
        print(">>> ANTES DE RESPONDER")
        return solicitud
    except Exception as e:
        print("===================================")
        print(">>> ERROR DETECTADO")
        print(f"type={type(e)}")
        print(f"str={e}")
        traceback.print_exc()
        print("===================================")
        raise


@router.get("", response_model=list[CreditoOut])
def listar_creditos(empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    return service.listar_creditos()


@router.get("/{credito_id}", response_model=CreditoDetailOut)
def obtener_credito(credito_id: int, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = CreditoService(db)
    return service.obtener_credito(credito_id)
