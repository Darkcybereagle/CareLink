from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes.ai import router as ai_router
from app.api.routes.auth import router as auth_router
from app.api.routes.care import router as care_router
from app.api.routes.providers import router as providers_router
from app.api.routes.quality import router as quality_router
from app.api.routes.nursing import router as nursing_router
from app.api.routes.users import router as users_router
from app.db.database import engine

app = FastAPI(title="CareLink AI API", description="Secure healthcare access and care coordination API.", version="2.0.0")

for router in (auth_router, users_router, ai_router, care_router, providers_router, quality_router, nursing_router):
    app.include_router(router, prefix="/api/v1")


@app.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "carelink-api"}


@app.get("/ready", tags=["System"])
def readiness_check() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ready", "database": "ok"}
