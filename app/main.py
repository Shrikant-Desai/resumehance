from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
from app.middleware.logging import log_requests


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        docs_url="/docs" if settings.DEBUG else None,  # hide docs in production
        redoc_url="/redoc" if settings.DEBUG else None,  # hide redoc in production
    )

    register_middleware(app)
    register_routes(app)

    return app


def register_middleware(app: FastAPI):
    # CORS — controls which domains can call your API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.DEBUG else ["https://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # logging middleware
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)


def register_routes(app: FastAPI):
    from app.api.v1.routes import health, job, resume, analysis

    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(job.router, prefix="/api/v1", tags=["Jobs"])
    app.include_router(resume.router, prefix="/api/v1", tags=["Resumes"])
    app.include_router(analysis.router, prefix="/api/v1", tags=["Analysis"])


app = create_app()
