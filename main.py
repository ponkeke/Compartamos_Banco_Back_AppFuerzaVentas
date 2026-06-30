import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from app.core.cfg_database import engine, Base
from app.routes import (
    auth_routes,
    cliente_routes,
    credito_routes,
    notificacion_routes,
    solicitudes_routes,
    evaluaciones_routes,
    visitas_routes,
    documentos_routes,
    firmas_routes,
    movimientos_routes,
    cronograma_routes,
    cartera_routes,
    cobranza_routes,
    reportes_routes,
    aliases_routes,
)

import app.models.nota_solicitud
import app.models.cartera_asignacion

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[DB] Not creating tables (may already exist): {e}")

app = FastAPI(
    title="Compartamos Banco - Core Mobile API",
    description="Backend API para la aplicación móvil de Compartamos Banco",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(cliente_routes.router)
app.include_router(credito_routes.router)
app.include_router(notificacion_routes.router)
app.include_router(solicitudes_routes.router)
app.include_router(evaluaciones_routes.router)
app.include_router(visitas_routes.router)
app.include_router(documentos_routes.router)
app.include_router(firmas_routes.router)
app.include_router(movimientos_routes.router)
app.include_router(cronograma_routes.router)
app.include_router(cartera_routes.router)
app.include_router(cobranza_routes.router)
app.include_router(reportes_routes.router)
app.include_router(aliases_routes.router)


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Compartamos Banco - Core Mobile API",
        swagger_favicon_url="/static/favicon.png",
    )


@app.get("/")
def root():
    return {"message": "Compartamos Banco - Core Mobile API", "status": "running"}
