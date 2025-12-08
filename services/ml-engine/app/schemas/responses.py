"""
Response schemas for API endpoints.

Defines Pydantic models for API responses.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """
    Response schema for single location prediction.
    
    Returns the predicted enjoyment score for a specific location.
    """
    
    location_name: str = Field(..., description="Name of the destination")
    predicted_score: float = Field(..., ge=0.0, le=10.0, description="Predicted enjoyment score (0-10)")
    recommendation_level: str = Field(..., description="Recommendation category: HIGHLY RECOMMENDED, RECOMMENDED, MIGHT ENJOY, NOT RECOMMENDED")
    
    # Location attributes (for transparency)
    location_attributes: dict = Field(..., description="Location feature values used in prediction")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location_name": "Sigiriya Rock Fortress",
                    "predicted_score": 8.75,
                    "recommendation_level": "HIGHLY RECOMMENDED",
                    "location_attributes": {
                        "l_hist": 0.95,
                        "l_adv": 0.7,
                        "l_nat": 0.8,
                        "l_rel": 0.1,
                        "l_outdoor": 0.9,
                        "l_lat": 7.957,
                        "l_lng": 80.7603
                    }
                }
            ]
        }
    }


class RecommendationItem(BaseModel):
    """
    Single recommendation item with score and distance information.
    """
    
    rank: int = Field(..., ge=1, description="Recommendation rank (1 = best)")
    location_name: str = Field(..., description="Name of the destination")
    predicted_score: float = Field(..., ge=0.0, le=10.0, description="Predicted enjoyment score (0-10)")
    recommendation_level: str = Field(..., description="Recommendation category: HIGHLY RECOMMENDED, RECOMMENDED, MIGHT ENJOY, NOT RECOMMENDED")
    distance_km: float = Field(..., ge=0.0, description="Distance from search origin in kilometers")
    
    # Location coordinates
    latitude: float = Field(..., description="Location latitude")
    longitude: float = Field(..., description="Location longitude")
    
    # Key attributes (for UI display)
    highlights: dict = Field(..., description="Key location attributes")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "rank": 1,
                    "location_name": "Sigiriya Rock Fortress",
                    "predicted_score": 8.75,
                    "recommendation_level": "HIGHLY RECOMMENDED",
                    "distance_km": 12.5,
                    "latitude": 7.957,
                    "longitude": 80.7603,
                    "highlights": {
                        "historical": 0.95,
                        "adventure": 0.7,
                        "nature": 0.8,
                        "religious": 0.1,
                        "outdoor": 0.9
                    }
                }
            ]
        }
    }


class RecommendationsResponse(BaseModel):
    """
    Response schema for location recommendations.
    
    Returns top N locations ranked by predicted enjoyment score.
    """
    
    search_origin: dict = Field(..., description="Search origin information")
    total_candidates: int = Field(..., ge=0, description="Total locations found within search radius")
    recommendations: List[RecommendationItem] = Field(..., description="Ranked recommendations")
    
    # Metadata
    max_distance_km: float = Field(..., description="Search radius used")
    user_profile: dict = Field(..., description="User profile used for predictions")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "search_origin": {
                        "type": "location",
                        "name": "Colombo",
                        "lat": 6.9271,
                        "lng": 79.8612
                    },
                    "total_candidates": 15,
                    "recommendations": [
                        {
                            "rank": 1,
                            "location_name": "Galle Fort",
                            "predicted_score": 8.75,
                            "recommendation_level": "HIGHLY RECOMMENDED",
                            "distance_km": 12.5,
                            "latitude": 6.0329,
                            "longitude": 80.2168,
                            "highlights": {
                                "historical": 0.9,
                                "adventure": 0.2,
                                "nature": 0.6,
                                "religious": 0.3,
                                "outdoor": 0.5
                            }
                        }
                    ],
                    "max_distance_km": 50.0,
                    "user_profile": {
                        "u_hist": 0.9,
                        "u_adv": 0.4,
                        "u_nat": 0.6,
                        "u_rel": 0.2
                    }
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """
    Response schema for health check endpoint.
    """
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    locations_loaded: int = Field(..., ge=0, description="Number of locations loaded")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "version": "1.0.0",
                    "model_loaded": True,
                    "locations_loaded": 50
                }
            ]
        }
    }
