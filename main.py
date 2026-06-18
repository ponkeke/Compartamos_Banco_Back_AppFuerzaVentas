import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from app.core.cfg_database import engine, Base
from app.routes import auth_routes, cliente_routes, contacto_routes, operacion_routes, credito_routes, notificacion_routes, solicitudes_routes

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
app.include_router(contacto_routes.router)
app.include_router(operacion_routes.router)
app.include_router(credito_routes.router)
app.include_router(notificacion_routes.router)
app.include_router(solicitudes_routes.router)


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
