"""Core package."""

from .config import Settings, get_settings
from .lifespan import get_ml_service, lifespan

__all__ = ["Settings", "get_settings", "lifespan", "get_ml_service"]
