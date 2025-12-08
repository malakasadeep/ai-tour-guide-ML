"""Pydantic schemas package for request/response validation."""

from .requests import UserProfile, PredictRequest, RecommendRequest
from .responses import PredictionResponse, RecommendationItem, RecommendationsResponse, HealthResponse

__all__ = [
    "UserProfile",
    "PredictRequest",
    "RecommendRequest",
    "PredictionResponse",
    "RecommendationItem",
    "RecommendationsResponse",
    "HealthResponse",
]
