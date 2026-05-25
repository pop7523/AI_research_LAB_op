from fastapi import FastAPI

from app.api.routes_articles import router as articles_router
from app.api.routes_claims import router as claims_router
from app.api.routes_entities import router as entities_router
from app.api.routes_events import router as events_router
from app.api.routes_facts import router as facts_router
from app.api.routes_issues import router as issues_router
from app.api.routes_reports import router as reports_router
from app.api.routes_review import router as review_router
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
    app.include_router(facts_router)
    app.include_router(claims_router)
    app.include_router(events_router)
    app.include_router(issues_router)
    app.include_router(reports_router)
    app.include_router(review_router)
    return app


app = create_app()
