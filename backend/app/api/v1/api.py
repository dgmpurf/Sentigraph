from fastapi import APIRouter

from app.api.v1.routes import (
    alerts,
    analysis,
    benchmarks,
    cases,
    crawl,
    health,
    keywords,
    llm,
    notifications,
    platforms,
    propagation,
    public_parsers,
    recommendation,
    scheduler,
    simulation,
    sources,
    summary,
    visualization,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(keywords.router, prefix="/keywords", tags=["keywords"])
api_router.include_router(platforms.router, prefix="/platforms", tags=["platforms"])
api_router.include_router(public_parsers.router, prefix="/public-parsers", tags=["public-parsers"])
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(benchmarks.router, prefix="/benchmarks", tags=["benchmarks"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(cases.router, prefix="/cases", tags=["cases"])
api_router.include_router(crawl.router, prefix="/crawl", tags=["crawl"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(visualization.router, prefix="/visualization", tags=["visualization"])
api_router.include_router(summary.router, prefix="/summary", tags=["summary"])
api_router.include_router(recommendation.router, prefix="/recommendation", tags=["recommendation"])
api_router.include_router(propagation.router, prefix="/propagation", tags=["propagation"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(scheduler.router, prefix="/scheduler", tags=["scheduler"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
