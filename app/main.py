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

# Determine default port and base URL (defaulting to port 8000 if not in .env)
HOST = getattr(settings, "HOST", "http://localhost:8000")

print("-" * 60)
print(f"Server Title:    {settings.PROJECT_NAME}")
print(f"Environment:     {settings.ENVIRONMENT}")
print(f"Health Check:    {HOST}/health")
print(f"Interactive Docs:{HOST}{settings.API_V1_STR}/docs")
print(f"Campaign API:    {HOST}{settings.API_V1_STR}/campaign/orchestrate")
print(f"Allowed Origins: {settings.ALLOWED_ORIGINS}")
print(f"Gemini Key Set:  {'Yes' if settings.GEMINI_API_KEY else 'No (Using Template Fallback)'}")
print("-" * 60)