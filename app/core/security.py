from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.cfg_config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print(f"[JWT] Token creado: payload={data} exp={expire.isoformat()}")
    return token


def decode_token(token: str) -> dict:
    try:
        print(f"[JWT] Intentando decodificar token: {token[:40]}...")
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True},
        )
        exp = payload.get("exp")
        now = datetime.now(timezone.utc)
        print(f"[JWT] Token decodificado OK")
        print(f"[JWT]   Payload: {payload}")
        if exp:
            exp_dt = datetime.fromtimestamp(exp, tz=timezone.utc)
            print(f"[JWT]   Expira: {exp_dt.isoformat()}")
            print(f"[JWT]   Ahora:  {now.isoformat()}")
            print(f"[JWT]   Valido: {now < exp_dt}")
        return payload
    except ExpiredSignatureError:
        print("[JWT] ERROR: Token expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
        )
    except JWTClaimsError as e:
        print(f"[JWT] ERROR: Claims inválidos: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {e}",
        )
    except JWTError as e:
        print(f"[JWT] ERROR: Firma inválida / JWTError: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firma inválida",
        )


def _validar_token(credentials: HTTPAuthorizationCredentials | None) -> str:
    print(f"[AUTH] HTTPBearer auto_error=False -> credentials={credentials}")
    if credentials is None:
        print("[AUTH] ERROR: No se recibió Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no recibido",
        )
    token = credentials.credentials
    print(f"[AUTH] Authorization header: Bearer {token[:40]}...")
    print(f"[AUTH] Token completo length: {len(token)}")
    payload = decode_token(token)
    return payload


def get_current_cliente_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    payload = _validar_token(credentials)
    cliente_id = payload.get("cliente_id")
    print(f"[AUTH] Payload busca cliente_id: {cliente_id}")
    print(f"[AUTH] Payload completo: {payload}")
    if cliente_id is None:
        print("[AUTH] ERROR: cliente_id no encontrado en payload")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no contiene cliente_id")
    print(f"[AUTH] Usuario identificado: cliente_id={cliente_id}")
    return cliente_id


def get_current_empleado_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    payload = _validar_token(credentials)
    empleado_id = payload.get("empleado_id")
    print(f"[AUTH] Payload busca empleado_id: {empleado_id}")
    print(f"[AUTH] Payload completo: {payload}")
    if empleado_id is None:
        print("[AUTH] ERROR: empleado_id no encontrado en payload")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no contiene empleado_id")
    print(f"[AUTH] Usuario identificado: empleado_id={empleado_id}")
    return empleado_id
