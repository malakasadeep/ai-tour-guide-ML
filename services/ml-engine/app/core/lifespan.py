"""
Application lifespan management.

Handles startup and shutdown events for the FastAPI application.
Uses the modern lifespan context manager pattern (FastAPI 0.93+).
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.config import get_settings
from app.services.ml_services import MLService

logger = logging.getLogger(__name__)


# Global ML service instance (shared across requests)
ml_service: MLService | None = None


def get_ml_service() -> MLService:
    """
    Dependency injection function to get the ML service instance.
    
    This is used as a FastAPI dependency to inject the ML service
    into route handlers.
    
    Returns:
        MLService: The initialized ML service instance
    
    Raises:
        RuntimeError: If service is not initialized
    """
    if ml_service is None:
        raise RuntimeError("ML Service not initialized. This should not happen.")
    return ml_service


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.
    
    Handles initialization and cleanup of resources:
    - Startup: Load ML model and location data
    - Shutdown: Clean up resources (if needed)
    
    Args:
        app: FastAPI application instance
    
    Yields:
        None: Application runs while context is active
    """
    # ========== STARTUP ==========
    logger.info("=" * 60)
    logger.info("🚀 STARTING TOURISM RECOMMENDATION ENGINE")
    logger.info("=" * 60)
    
    try:
        # Get settings
        settings = get_settings()
        logger.info(f"📋 Environment: {settings.environment}")
        logger.info(f"📋 Debug Mode: {settings.debug}")
        
        # Initialize ML Service
        global ml_service
        ml_service = MLService(settings)
        ml_service.initialize()
        
        # Store in app state for easy access
        app.state.ml_service = ml_service
        app.state.settings = settings
        
        stats = ml_service.get_stats()
        logger.info(f"📊 Model Loaded: {stats['model_loaded']}")
        logger.info(f"📊 Locations Loaded: {stats['locations_loaded']}")
        
        logger.info("=" * 60)
        logger.info("✅ APPLICATION READY")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ STARTUP FAILED: {e}", exc_info=True)
        raise
    
    # Application runs here
    yield
    
    # ========== SHUTDOWN ==========
    logger.info("=" * 60)
    logger.info("🛑 SHUTTING DOWN TOURISM RECOMMENDATION ENGINE")
    logger.info("=" * 60)
    
    # Clean up resources if needed
    # (XGBoost and pandas cleanup is automatic)
    
    logger.info("✅ SHUTDOWN COMPLETE")
