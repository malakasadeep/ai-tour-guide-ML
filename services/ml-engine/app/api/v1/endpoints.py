"""
API v1 endpoints for Tourism Recommendation Engine.

Implements two main endpoints:
1. POST /predict - Predict enjoyment score for a specific location
2. POST /recommend - Get top N location recommendations
3. GET /health - Health check
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.lifespan import get_ml_service
from app.schemas import (
    HealthResponse,
    PredictRequest,
    PredictionResponse,
    RecommendationsResponse,
    RecommendRequest,
    RecommendationItem,
)
from app.services.ml_services import MLService

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API and ML service are running properly",
    tags=["System"]
)
async def health_check(
    ml_service: Annotated[MLService, Depends(get_ml_service)]
) -> HealthResponse:
    """
    Health check endpoint.
    
    Returns service status and model loading information.
    """
    stats = ml_service.get_stats()
    
    return HealthResponse(
        status="healthy" if stats["is_ready"] else "degraded",
        version="1.0.0",
        model_loaded=stats["model_loaded"],
        locations_loaded=stats["locations_loaded"]
    )


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Enjoyment Score",
    description="Predict enjoyment score for a specific location based on user profile",
    tags=["Predictions"]
)
async def predict_score(
    request: PredictRequest,
    ml_service: Annotated[MLService, Depends(get_ml_service)]
) -> PredictionResponse:
    """
    Predict enjoyment score for a user-location pair.
    
    Args:
        request: Prediction request with user profile and location name
        ml_service: Injected ML service dependency
    
    Returns:
        PredictionResponse with predicted score and location details
    
    Raises:
        HTTPException 404: If location not found
        HTTPException 500: If prediction fails
    """
    try:
        # Find the location
        location = ml_service.get_location_by_name(request.location_name)
        
        if location is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location '{request.location_name}' not found in database"
            )
        
        # Convert user profile to dict
        user_profile = request.user_profile.model_dump()
        
        # Predict score
        predicted_score = ml_service.predict_score(
            user_profile=user_profile,
            location_data=location,
            is_raining=False  # Could be enhanced to accept weather as input
        )
        
        # Prepare location attributes for response
        location_attrs = {
            "l_hist": float(location["l_hist"]),
            "l_adv": float(location["l_adv"]),
            "l_nat": float(location["l_nat"]),
            "l_rel": float(location["l_rel"]),
            "l_outdoor": float(location["l_outdoor"]),
            "l_lat": float(location["l_lat"]),
            "l_lng": float(location["l_lng"])
        }
        
        return PredictionResponse(
            location_name=location["Location_Name"],
            predicted_score=predicted_score,
            recommendation_level=ml_service.get_recommendation_level(predicted_score),
            location_attributes=location_attrs
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post(
    "/recommend",
    response_model=RecommendationsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Location Recommendations",
    description="Get top N location recommendations based on user profile and search origin",
    tags=["Recommendations"]
)
async def get_recommendations(
    request: RecommendRequest,
    ml_service: Annotated[MLService, Depends(get_ml_service)]
) -> RecommendationsResponse:
    """
    Get personalized location recommendations.
    
    Uses hybrid filtering:
    1. Candidate Generation: Find locations within max_distance_km
    2. Ranking: Score each candidate with ML model
    3. Return top N sorted by predicted enjoyment
    
    Args:
        request: Recommendation request with user profile and origin
        ml_service: Injected ML service dependency
    
    Returns:
        RecommendationsResponse with ranked recommendations
    
    Raises:
        HTTPException 404: If target location not found
        HTTPException 500: If recommendation fails
    """
    try:
        # Determine search origin
        origin_lat: float
        origin_lng: float
        origin_info: dict
        
        if request.target_location:
            # Option 1: Search around a target location
            target = ml_service.get_location_by_name(request.target_location)
            
            if target is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Target location '{request.target_location}' not found"
                )
            
            origin_lat = float(target["l_lat"])
            origin_lng = float(target["l_lng"])
            origin_info = {
                "type": "location",
                "name": target["Location_Name"],
                "lat": origin_lat,
                "lng": origin_lng
            }
        else:
            # Option 2: Search around GPS coordinates
            origin_lat = request.current_lat
            origin_lng = request.current_lng
            origin_info = {
                "type": "gps",
                "lat": origin_lat,
                "lng": origin_lng
            }
        
        # Get search parameters (use defaults from config if not provided)
        max_distance = request.max_distance_km or ml_service.settings.max_distance_km
        top_n = request.top_n or ml_service.settings.top_n_recommendations
        
        # Convert user profile to dict
        user_profile = request.user_profile.model_dump()
        
        # Get recommendations using hybrid filtering
        recommendations = ml_service.recommend_locations(
            user_profile=user_profile,
            origin_lat=origin_lat,
            origin_lng=origin_lng,
            max_distance_km=max_distance,
            top_n=top_n,
            is_raining=False  # Could be enhanced
        )
        
        # Build response
        recommendation_items = []
        for rank, (location, score, distance) in enumerate(recommendations, start=1):
            item = RecommendationItem(
                rank=rank,
                location_name=location["Location_Name"],
                predicted_score=score,
                recommendation_level=ml_service.get_recommendation_level(score),
                distance_km=distance,
                latitude=float(location["l_lat"]),
                longitude=float(location["l_lng"]),
                highlights={
                    "historical": float(location["l_hist"]),
                    "adventure": float(location["l_adv"]),
                    "nature": float(location["l_nat"]),
                    "religious": float(location["l_rel"]),
                    "outdoor": float(location["l_outdoor"])
                }
            )
            recommendation_items.append(item)
        
        # Count total candidates (for transparency)
        all_nearby = ml_service.find_nearby_locations(origin_lat, origin_lng, max_distance)
        
        return RecommendationsResponse(
            search_origin=origin_info,
            total_candidates=len(all_nearby),
            recommendations=recommendation_items,
            max_distance_km=max_distance,
            user_profile=user_profile
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Recommendation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recommendation failed: {str(e)}"
        )
