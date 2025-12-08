"""
Configuration module for the Tourism Recommendation Engine API.

This module uses Pydantic Settings for type-safe configuration management
with automatic environment variable loading and validation.
"""

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables with the same name.
    Uses .env file for local development.
    """
    
    # Application Metadata
    app_name: str = Field(default="Tourism Recommendation Engine", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    environment: str = Field(default="development", description="Environment (development/production)")
    
    # API Configuration
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 route prefix")
    debug: bool = Field(default=True, description="Debug mode")
    
    # Model Configuration
    xgboost_model_path: Path = Field(default=Path("models/enjoyment_model.json"), description="Path to XGBoost model")
    locations_data_path: Path = Field(default=Path("data/locations_metadata.csv"), description="Path to locations CSV")
    
    # Recommendation Settings
    max_distance_km: float = Field(default=50.0, ge=1.0, le=500.0, description="Maximum search radius in kilometers")
    top_n_recommendations: int = Field(default=5, ge=1, le=20, description="Number of recommendations to return")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, ge=1024, le=65535, description="Server port")
    
    # CORS Configuration
    allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        description="Allowed CORS origins (comma-separated)"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        protected_namespaces=('settings_',)  # Avoid model_ namespace conflict
    )
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]
    
    @field_validator("xgboost_model_path", "locations_data_path", mode="before")
    @classmethod
    def validate_paths(cls, v):
        """Ensure paths are Path objects."""
        if isinstance(v, str):
            return Path(v)
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"
    
    @property
    def absolute_model_path(self) -> Path:
        """Get absolute path to the model file."""
        if self.xgboost_model_path.is_absolute():
            return self.xgboost_model_path
        return Path(__file__).parent.parent.parent / self.xgboost_model_path
    
    @property
    def absolute_locations_path(self) -> Path:
        """Get absolute path to the locations data file."""
        if self.locations_data_path.is_absolute():
            return self.locations_data_path
        return Path(__file__).parent.parent.parent / self.locations_data_path


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses LRU cache to ensure settings are loaded only once and reused
    across the application lifetime.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


# Convenience export
settings = get_settings()
