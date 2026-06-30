from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.cfg_database import get_db
from app.core.security import get_current_empleado_id
from app.schemas.documento_schema import DocumentoRequest, DocumentoOut
from app.services.documento_service import DocumentoService

router = APIRouter(prefix="/documentos", tags=["Documentos"])


@router.post("", response_model=DocumentoOut)
def subir_documento(body: DocumentoRequest, empleado_id: int = Depends(get_current_empleado_id), db: Session = Depends(get_db)):
    service = DocumentoService(db)
    result = service.subir_documento(
        solicitud_id=body.solicitud_id,
        tipo_documento=body.tipo_documento,
        archivo_url=body.archivo_url,
    )
    db.commit()
    return result
