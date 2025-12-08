"""
Tourism Recommendation Engine - FastAPI Application

A production-grade ML-powered API for personalized tourist location recommendations
in Sri Lanka using XGBoost predictions and geospatial filtering.

Author: Senior Backend Engineer & MLOps Architect
Version: 1.0.0
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import router as v1_router
from app.core import get_settings, lifespan

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Get application settings
settings = get_settings()


def create_application() -> FastAPI:
    """
    Application factory for creating FastAPI instance.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="""
        ## Tourism Recommendation Engine API
        
        A machine learning powered API for personalized tourist location recommendations in Sri Lanka.
        
        ### Features
        - 🎯 **Predict Enjoyment Score**: Get predicted enjoyment score for any location
        - 🗺️ **Smart Recommendations**: Get top N nearby locations ranked by predicted enjoyment
        - 🧠 **ML-Powered**: Uses XGBoost regression model trained on tourist interaction data
        - 📍 **Geospatial Filtering**: Haversine distance calculation for location proximity
        - 🔄 **Hybrid Filtering**: Combines distance-based candidate generation with ML ranking
        
        ### Technology Stack
        - **Framework**: FastAPI 0.109+
        - **ML Model**: XGBoost Regressor
        - **Data Processing**: Pandas, NumPy
        - **Validation**: Pydantic v2
        
        ### Endpoints
        - `GET /api/v1/health` - Health check
        - `POST /api/v1/predict` - Predict score for specific location
        - `POST /api/v1/recommend` - Get personalized recommendations
        """,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
        debug=settings.debug
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(
        v1_router,
        prefix=settings.api_v1_prefix,
        tags=["API v1"]
    )
    
    # Root endpoint
    @app.get("/", include_in_schema=False)
    async def root():
        """Root endpoint redirect to docs."""
        return JSONResponse({
            "message": "Tourism Recommendation Engine API",
            "version": settings.app_version,
            "docs": "/docs",
            "health": f"{settings.api_v1_prefix}/health"
        })
    
    return app


# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    # Run with uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
