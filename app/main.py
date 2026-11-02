from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import campaign

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs"
)

# CORS configuration for mobile and web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register routes
app.include_router(campaign.router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}
