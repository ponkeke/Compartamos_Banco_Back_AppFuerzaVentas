from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from typing import Optional

router = APIRouter(tags=["Alias / Compatibilidad"])


@router.post("/pre-evaluar")
def pre_evaluar_alias(body: dict, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    from app.services.evaluacion_service import EvaluacionService
    from app.repositories.credito_repository import SolicitudCreditoRepository
    service = EvaluacionService(db)
    solicitud_repo = SolicitudCreditoRepository(db)
    dni = body.get("numero_documento", "")
    nombre = body.get("nombres", "")
    ingresos = float(body.get("ingresos_estimados", 0))
    monto = float(body.get("monto_solicitado", 0))
    destino = body.get("destino_credito", "")
    tipo_negocio = body.get("tipo_negocio", "")

    puntaje = min(100, int(ingresos / 100) + int(monto > 500))
    if puntaje >= 70:
        calificacion = "APTO"
        motivo = "Cumple perfil de riesgo"
    elif puntaje >= 40:
        calificacion = "REVISAR"
        motivo = "Requiere evaluacion adicional"
    else:
        calificacion = "NO_PROCEDE"
        motivo = "No cumple criterios minimos"
    return {
        "calificacion": calificacion,
        "motivo": motivo,
        "puntaje": puntaje,
    }


@router.post("/buro/consulta")
def buro_consulta_alias(body: dict, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    dni = body.get("dni", "")
    import random
    niveles = ["NORMAL", "CPP", "DEFICIENTE", "DUDOSO", "PERDIDA"]
    return {
        "calificacion_sbs": random.choice(niveles),
        "entidades_con_deuda": random.randint(0, 8),
        "deuda_total": round(random.uniform(0, 50000), 2),
        "mayor_deuda": round(random.uniform(0, 20000), 2),
        "dias_mayor_mora": random.randint(0, 180),
        "en_lista_negra": False,
        "motivo_bloqueo": None,
        "interpretacion": "Sin observaciones significativas",
    }
