from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.models.solicitud_credito import SolicitudCredito
from app.models.empleado import Empleado

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/productividad")
def productividad(empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    total_solicitudes = db.query(func.count(SolicitudCredito.id)).scalar() or 0
    aprobadas = db.query(func.count(SolicitudCredito.id)).filter(SolicitudCredito.estado == "APROBADO").scalar() or 0
    desembolsadas = db.query(func.count(SolicitudCredito.id)).filter(SolicitudCredito.estado == "DESEMBOLSADO").scalar() or 0
    empleados_activos = db.query(func.count(Empleado.id)).filter(Empleado.estado == "ACTIVO").scalar() or 0
    empleados = db.query(Empleado).filter(Empleado.estado == "ACTIVO").all()
    detalle = []
    for emp in empleados:
        emp_sols = db.query(func.count(SolicitudCredito.id)).filter(SolicitudCredito.cliente_id.isnot(None)).scalar() or 0
        detalle.append({
            "asesor": f"{emp.nombres} {emp.apellidos}",
            "enviadas": emp_sols,
            "aprobadas": 0,
            "desembolsadas": 0,
            "monto": 0,
            "porcentaje_aprob": 0,
        })
    from decimal import Decimal
    return {
        "total_enviadas": total_solicitudes,
        "total_aprobadas": aprobadas,
        "total_desembolsadas": desembolsadas,
        "asesores_activos": empleados_activos,
        "detalle": detalle,
        "grafico": [{"asesor": d["asesor"], "enviadas": d["enviadas"]} for d in detalle],
    }
