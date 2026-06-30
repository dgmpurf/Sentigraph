from fastapi import APIRouter

from app.api.v1.routes import (
    alerts,
    analysis,
    analysis_requests,
    benchmarks,
    cases,
    crawl,
    evidence,
    external_collector,
    health,
    internal_operator_review_only_staging,
    keywords,
    llm,
    notifications,
    opinion_ecosystem_dense_graph,
    opinion_ecosystem_generated_runs,
    platforms,
    propagation,
    public_parsers,
    recommendation,
    scheduler,
    search_discovery,
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
api_router.include_router(search_discovery.router, prefix="/search-discovery", tags=["search-discovery"])
api_router.include_router(external_collector.router, prefix="/external-collector", tags=["external-collector"])
api_router.include_router(
    internal_operator_review_only_staging.router,
    prefix="/internal/staging/review-only",
    tags=["internal-operator-review-only-staging"],
)
api_router.include_router(analysis_requests.router, prefix="/analysis-requests", tags=["analysis-requests"])
api_router.include_router(
    opinion_ecosystem_generated_runs.router,
    prefix="/opinion-ecosystem",
    tags=["opinion-ecosystem"],
)
api_router.include_router(
    opinion_ecosystem_dense_graph.router,
    prefix="/internal/opinion-ecosystem/dense-graph",
    tags=["internal-opinion-ecosystem-dense-graph"],
)
api_router.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
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
