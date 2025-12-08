"""
ML Service for Tourism Recommendation Engine.

This module implements the core machine learning logic including:
- XGBoost model loading and inference
- Haversine distance calculation
- Hybrid filtering (distance + ML ranking)
"""

import logging
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import xgboost as xgb

from app.core.config import Settings

logger = logging.getLogger(__name__)


class MLService:
    """
    Machine Learning service for tourist enjoyment prediction.
    
    This service handles:
    1. Loading the XGBoost model and location data
    2. Predicting enjoyment scores based on user profiles
    3. Finding nearby locations using Haversine distance
    4. Ranking locations by predicted enjoyment (hybrid filtering)
    
    The service is initialized once at startup and reused across requests.
    """
    
    # Feature columns expected by the model
    FEATURE_COLUMNS = [
        'u_hist', 'u_adv', 'u_nat', 'u_rel',
        'l_hist', 'l_adv', 'l_nat', 'l_rel', 
        'l_outdoor', 'l_lat', 'l_lng', 'c_raining'
    ]
    
    # Location attribute columns from CSV
    LOCATION_ATTRIBUTES = [
        'l_hist', 'l_adv', 'l_nat', 'l_rel', 
        'l_outdoor', 'l_lat', 'l_lng'
    ]
    
    def __init__(self, settings: Settings):
        """
        Initialize the ML service.
        
        Args:
            settings: Application settings instance
        """
        self.settings = settings
        self.model: Optional[xgb.XGBRegressor] = None
        self.locations_df: Optional[pd.DataFrame] = None
        self._is_ready = False
    
    def load_model(self) -> None:
        """
        Load the XGBoost model from disk.
        
        Raises:
            FileNotFoundError: If model file doesn't exist
            Exception: If model loading fails
        """
        model_path = self.settings.absolute_model_path
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        try:
            self.model = xgb.XGBRegressor()
            self.model.load_model(str(model_path))
            logger.info(f"✅ Model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise
    
    def load_locations(self) -> None:
        """
        Load location metadata from CSV.
        
        Expected columns: Location_Name, l_hist, l_adv, l_nat, l_rel, 
                         l_outdoor, l_lat, l_lng
        
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If required columns are missing
        """
        data_path = self.settings.absolute_locations_path
        
        if not data_path.exists():
            raise FileNotFoundError(f"Locations data file not found: {data_path}")
        
        try:
            self.locations_df = pd.read_csv(data_path)
            
            # Validate required columns
            required_cols = ['Location_Name'] + self.LOCATION_ATTRIBUTES
            missing_cols = set(required_cols) - set(self.locations_df.columns)
            
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Create a clean index on location names (case-insensitive)
            self.locations_df['Location_Name_Lower'] = self.locations_df['Location_Name'].str.lower().str.strip()
            
            logger.info(f"✅ Loaded {len(self.locations_df)} locations from {data_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load locations data: {e}")
            raise
    
    def initialize(self) -> None:
        """
        Initialize the service by loading model and data.
        
        This should be called once during application startup.
        """
        logger.info("🚀 Initializing ML Service...")
        self.load_model()
        self.load_locations()
        self._is_ready = True
        logger.info("✅ ML Service initialized successfully")
    
    @property
    def is_ready(self) -> bool:
        """Check if service is ready to handle requests."""
        return self._is_ready and self.model is not None and self.locations_df is not None
    
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points on Earth.
        
        Uses the Haversine formula to compute distance in kilometers.
        
        Args:
            lat1: Latitude of point 1 (degrees)
            lon1: Longitude of point 1 (degrees)
            lat2: Latitude of point 2 (degrees)
            lon2: Longitude of point 2 (degrees)
        
        Returns:
            Distance in kilometers
        
        References:
            https://en.wikipedia.org/wiki/Haversine_formula
        """
        # Earth's radius in kilometers
        R = 6371.0
        
        # Convert to radians
        lat1_rad, lon1_rad = radians(lat1), radians(lon1)
        lat2_rad, lon2_rad = radians(lat2), radians(lon2)
        
        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        
        distance = R * c
        return distance
    
    def get_location_by_name(self, location_name: str) -> Optional[pd.Series]:
        """
        Find a location by name (case-insensitive).
        
        Args:
            location_name: Name of the location to find
        
        Returns:
            Location data as pandas Series, or None if not found
        """
        if self.locations_df is None:
            return None
        
        search_name = location_name.lower().strip()
        matches = self.locations_df[self.locations_df['Location_Name_Lower'] == search_name]
        
        if len(matches) > 0:
            return matches.iloc[0]
        
        return None
    
    def predict_score(
        self,
        user_profile: Dict[str, float],
        location_data: pd.Series,
        is_raining: bool = False
    ) -> float:
        """
        Predict enjoyment score for a user-location pair.
        
        Args:
            user_profile: User preferences (u_hist, u_adv, u_nat, u_rel)
            location_data: Location attributes from DataFrame
            is_raining: Current weather condition (default: False)
        
        Returns:
            Predicted enjoyment score (1-10)
        """
        if not self.is_ready:
            raise RuntimeError("ML Service not initialized")
        
        # Combine user profile, location attributes, and context
        features = {
            **user_profile,
            'l_hist': location_data['l_hist'],
            'l_adv': location_data['l_adv'],
            'l_nat': location_data['l_nat'],
            'l_rel': location_data['l_rel'],
            'l_outdoor': location_data['l_outdoor'],
            'l_lat': location_data['l_lat'],
            'l_lng': location_data['l_lng'],
            'c_raining': 1.0 if is_raining else 0.0
        }
        
        # Create DataFrame with correct feature order
        input_df = pd.DataFrame([features])[self.FEATURE_COLUMNS]
        
        # Predict
        prediction = self.model.predict(input_df)[0]
        
        # Clip to valid range [1, 10]
        return float(np.clip(prediction, 1.0, 10.0))
    
    @staticmethod
    def get_recommendation_level(score: float) -> str:
        """
        Determine recommendation level based on predicted score.
        
        Args:
            score: Predicted enjoyment score (1-10)
        
        Returns:
            Recommendation level string
        """
        if score >= 7.5:
            return "HIGHLY RECOMMENDED"
        elif score >= 6.0:
            return "RECOMMENDED"
        elif score >= 4.0:
            return "MIGHT ENJOY"
        else:
            return "NOT RECOMMENDED"
    
    def find_nearby_locations(
        self,
        origin_lat: float,
        origin_lng: float,
        max_distance_km: float
    ) -> pd.DataFrame:
        """
        Find all locations within a specified radius.
        
        Args:
            origin_lat: Origin latitude
            origin_lng: Origin longitude
            max_distance_km: Maximum search radius in kilometers
        
        Returns:
            DataFrame of nearby locations with distances
        """
        if self.locations_df is None:
            return pd.DataFrame()
        
        # Calculate distances to all locations
        distances = self.locations_df.apply(
            lambda row: self.haversine_distance(
                origin_lat, origin_lng,
                row['l_lat'], row['l_lng']
            ),
            axis=1
        )
        
        # Filter by max distance
        nearby_mask = distances <= max_distance_km
        nearby_locations = self.locations_df[nearby_mask].copy()
        nearby_locations['distance_km'] = distances[nearby_mask]
        
        return nearby_locations
    
    def recommend_locations(
        self,
        user_profile: Dict[str, float],
        origin_lat: float,
        origin_lng: float,
        max_distance_km: float,
        top_n: int,
        is_raining: bool = False
    ) -> List[Tuple[pd.Series, float, float]]:
        """
        Recommend top N locations using hybrid filtering.
        
        Algorithm:
        1. Candidate Generation: Find locations within max_distance_km
        2. Scoring: Predict enjoyment score for each candidate
        3. Ranking: Sort by score and return top N
        
        Args:
            user_profile: User preferences
            origin_lat: Search origin latitude
            origin_lng: Search origin longitude
            max_distance_km: Maximum search radius
            top_n: Number of recommendations to return
            is_raining: Current weather condition
        
        Returns:
            List of (location_data, predicted_score, distance_km) tuples
        """
        if not self.is_ready:
            raise RuntimeError("ML Service not initialized")
        
        # Step 1: Candidate Generation (Distance Filter)
        candidates = self.find_nearby_locations(origin_lat, origin_lng, max_distance_km)
        
        if len(candidates) == 0:
            return []
        
        # Step 2: Scoring (ML Ranking)
        predictions = []
        for _, location in candidates.iterrows():
            score = self.predict_score(user_profile, location, is_raining)
            predictions.append((location, score, location['distance_km']))
        
        # Step 3: Ranking
        # Sort by score (descending), then by distance (ascending) as tiebreaker
        predictions.sort(key=lambda x: (-x[1], x[2]))
        
        # Return top N
        return predictions[:top_n]
    
    def get_stats(self) -> Dict:
        """
        Get service statistics for health checks.
        
        Returns:
            Dictionary with service stats
        """
        return {
            "model_loaded": self.model is not None,
            "locations_loaded": len(self.locations_df) if self.locations_df is not None else 0,
            "is_ready": self.is_ready
        }
