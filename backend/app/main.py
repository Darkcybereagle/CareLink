from fastapi import FastAPI

from app.api.routes.ai import router as ai_router
from app.api.routes.care import router as care_router
from app.api.routes.providers import router as providers_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router

app = FastAPI(
    title="CareLink AI API",
    description="Secure healthcare access and care coordination API.",
    version="0.6.0",
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(care_router, prefix="/api/v1")
app.include_router(providers_router, prefix="/api/v1")


@app.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "carelink-api"}
