from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.schemas.auth_schema import (
    RegisterRequest,
    LoginClienteIn,
    LoginClienteResponse,
    LoginEmpleadoIn,
    LoginEmpleadoResponse,
)
from app.services.auth_service import AuthService
from app.schemas.cliente_schema import ClienteOut

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=ClienteOut)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    cliente = service.register(body.dni, body.nombres, body.apellidos, body.password)
    db.commit()
    return cliente


@router.post("/login-cliente", response_model=LoginClienteResponse)
def login_cliente(body: LoginClienteIn, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_cliente(body.numero_documento, body.password)


@router.post("/login-empleado", response_model=LoginEmpleadoResponse)
def login_empleado(body: LoginEmpleadoIn, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_empleado(body.codigo_empleado, body.password)


# Alias temporal: /auth/login → login-empleado (frontend React actual)
@router.post("/login", response_model=LoginEmpleadoResponse)
def login_alias(body: LoginEmpleadoIn, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login_empleado(body.codigo_empleado, body.password)
