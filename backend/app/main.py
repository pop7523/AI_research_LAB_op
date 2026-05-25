from fastapi import FastAPI

from app.api.routes_articles import router as articles_router
from app.api.routes_entities import router as entities_router
from app.api.routes_sources import router as sources_router
from app.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "app": settings.app_name}

    app.include_router(sources_router)
    app.include_router(articles_router)
    app.include_router(entities_router)
    return app


app = create_app()

