"""
Request schemas for API endpoints.

Defines Pydantic models for validating incoming API requests.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserProfile(BaseModel):
    """
    User preference profile for personalized recommendations.
    
    All preference values should be normalized between 0.0 and 1.0:
    - 0.0 = No interest
    - 1.0 = Maximum interest
    """
    
    u_hist: float = Field(..., ge=0.0, le=1.0, description="Interest in historical sites")
    u_adv: float = Field(..., ge=0.0, le=1.0, description="Interest in adventure activities")
    u_nat: float = Field(..., ge=0.0, le=1.0, description="Interest in nature/natural beauty")
    u_rel: float = Field(..., ge=0.0, le=1.0, description="Interest in religious sites")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "u_hist": 0.9,
                    "u_adv": 0.4,
                    "u_nat": 0.6,
                    "u_rel": 0.2
                }
            ]
        }
    }


class PredictRequest(BaseModel):
    """
    Request schema for single location score prediction.
    
    Combines user profile with a specific destination to predict enjoyment score.
    """
    
    user_profile: UserProfile = Field(..., description="User preference profile")
    location_name: str = Field(..., min_length=1, max_length=200, description="Name of the destination")
    
    @field_validator("location_name")
    @classmethod
    def validate_location_name(cls, v: str) -> str:
        """Normalize location name (strip whitespace)."""
        return v.strip()
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_profile": {
                        "u_hist": 0.9,
                        "u_adv": 0.4,
                        "u_nat": 0.6,
                        "u_rel": 0.2
                    },
                    "location_name": "Sigiriya Rock Fortress"
                }
            ]
        }
    }


class RecommendRequest(BaseModel):
    """
    Request schema for nearby location recommendations.
    
    Requires either target_location OR current GPS coordinates.
    Returns top N locations ranked by predicted enjoyment score within max distance.
    """
    
    user_profile: UserProfile = Field(..., description="User preference profile")
    
    # Option 1: Search around a target location
    target_location: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Target destination name to search nearby"
    )
    
    # Option 2: Search around current GPS position
    current_lat: Optional[float] = Field(
        default=None,
        ge=-90.0,
        le=90.0,
        description="Current latitude (if not using target_location)"
    )
    current_lng: Optional[float] = Field(
        default=None,
        ge=-180.0,
        le=180.0,
        description="Current longitude (if not using target_location)"
    )
    
    # Optional filters
    max_distance_km: Optional[float] = Field(
        default=None,
        ge=1.0,
        le=500.0,
        description="Maximum search radius in kilometers (overrides config default)"
    )
    top_n: Optional[int] = Field(
        default=None,
        ge=1,
        le=20,
        description="Number of recommendations to return (overrides config default)"
    )
    
    @field_validator("target_location")
    @classmethod
    def validate_target_location(cls, v: Optional[str]) -> Optional[str]:
        """Normalize target location name."""
        return v.strip() if v else None
    
    def model_post_init(self, __context) -> None:
        """Validate that either target_location or GPS coordinates are provided."""
        has_target = self.target_location is not None
        has_gps = self.current_lat is not None and self.current_lng is not None
        
        if not has_target and not has_gps:
            raise ValueError(
                "Either 'target_location' or both 'current_lat' and 'current_lng' must be provided"
            )
        
        if has_gps and (self.current_lat is None or self.current_lng is None):
            raise ValueError(
                "Both 'current_lat' and 'current_lng' must be provided together"
            )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_profile": {
                        "u_hist": 0.9,
                        "u_adv": 0.4,
                        "u_nat": 0.6,
                        "u_rel": 0.2
                    },
                    "target_location": "Colombo",
                    "max_distance_km": 50.0,
                    "top_n": 5
                },
                {
                    "user_profile": {
                        "u_hist": 0.9,
                        "u_adv": 0.4,
                        "u_nat": 0.6,
                        "u_rel": 0.2
                    },
                    "current_lat": 6.9271,
                    "current_lng": 79.8612,
                    "max_distance_km": 30.0,
                    "top_n": 5
                }
            ]
        }
    }
