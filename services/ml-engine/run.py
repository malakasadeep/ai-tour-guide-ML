"""
Run script for the Tourism Recommendation Engine.

This script provides a convenient way to run the application
with proper configuration.
"""

import uvicorn

from app.core.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.is_production else "warning",
        access_log=True
    )
