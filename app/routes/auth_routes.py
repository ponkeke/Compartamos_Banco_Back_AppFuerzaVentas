from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.schemas.auth_schema import (
    LoginClienteIn,
    LoginClienteResponse,
    LoginEmpleadoIn,
    LoginEmpleadoResponse,
)
from app.schemas.registro_schema import (
    SolicitudRegistroRequest,
    SolicitudRegistroOut,
    RechazarRequest,
)
from app.services.auth_service import AuthService
from app.services.registro_service import RegistroService
import traceback

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login-cliente", response_model=LoginClienteResponse)
def login_cliente(body: LoginClienteIn, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_cliente(body.numero_documento, body.password)


@router.post("/login-empleado", response_model=LoginEmpleadoResponse)
def login_empleado(body: LoginEmpleadoIn, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_empleado(body.codigo_empleado, body.password)


# ── Solicitudes de Registro (Flujo Cliente → Admin) ──


@router.post("/solicitud-registro", response_model=SolicitudRegistroOut)
def solicitar_registro(body: SolicitudRegistroRequest, db: Session = Depends(get_db)):
    print("========== SOLICITUD REGISTRO ==========")
    print("REQUEST BODY:")
    print(body.model_dump())
    print("========================================")
    try:
        service = RegistroService(db)
        solicitud = service.solicitar(
            body.dni, body.nombres, body.apellidos,
            body.celular, body.correo, body.password,
        )
        db.commit()
        return solicitud
    except Exception as e:
        print("========== ERROR ==========")
        print(f"ERROR: {e}")
        traceback.print_exc()
        print("===========================")
        raise


@router.get("/solicitud-registro/{solicitud_id}", response_model=SolicitudRegistroOut)
def obtener_solicitud_registro(
    solicitud_id: int,
    empleado_id: int = Depends(get_current_empleado_id),
    db: Session = Depends(get_db),
):
    service = RegistroService(db)
    return service.obtener(solicitud_id)


@router.get("/solicitudes-registro", response_model=list[SolicitudRegistroOut])
def listar_solicitudes_registro(
    empleado_id: int = Depends(get_current_empleado_id),
    db: Session = Depends(get_db),
):
    service = RegistroService(db)
    return service.listar()


@router.post("/solicitudes-registro/{solicitud_id}/aprobar", response_model=SolicitudRegistroOut)
def aprobar_solicitud_registro(
    solicitud_id: int,
    empleado_id: int = Depends(get_current_empleado_id),
    db: Session = Depends(get_db),
):
    service = RegistroService(db)
    result = service.aprobar(solicitud_id)
    db.commit()
    return result


@router.post("/solicitudes-registro/{solicitud_id}/rechazar", response_model=SolicitudRegistroOut)
def rechazar_solicitud_registro(
    solicitud_id: int,
    body: RechazarRequest,
    empleado_id: int = Depends(get_current_empleado_id),
    db: Session = Depends(get_db),
):
    service = RegistroService(db)
    result = service.rechazar(solicitud_id, body.observacion)
    db.commit()
    return result

