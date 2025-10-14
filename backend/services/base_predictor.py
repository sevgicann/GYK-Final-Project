"""
Base Predictor Interface - Interface Segregation Principle (SOLID)
Defines contracts for bi-directional ML prediction services
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum


class PredictionDirection(Enum):
    """Prediction direction enumeration"""
    ENVIRONMENT_TO_CROP = "environment_to_crop"  # Given environment → predict crop
    CROP_TO_ENVIRONMENT = "crop_to_environment"  # Given crop → predict optimal environment


class BasePredictor(ABC):
    """
    Base interface for bi-directional ML predictors
    Following Interface Segregation Principle
    """
    
    @abstractmethod
    def predict_crop_from_environment(self, environment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict best crop given environmental conditions
        
        Args:
            environment_data: Dictionary containing environmental features
                - soil_ph, nitrogen, phosphorus, potassium, moisture
                - temperature_celsius, rainfall_mm
                - region, soil_type, fertilizer_type, irrigation_method, weather_condition
                
        Returns:
            Dictionary with prediction result:
            {
                'success': bool,
                'predicted_crop': str,
                'confidence': float,
                'top_3_predictions': List[Tuple[str, float]]
            }
        """
        pass
    
    @abstractmethod
    def predict_environment_from_crop(self, crop: str, region: str) -> Dict[str, Any]:
        """
        Predict optimal environmental conditions for a target crop
        
        Args:
            crop: Target crop name
            region: Target region name
            
        Returns:
            Dictionary with optimal conditions:
            {
                'success': bool,
                'crop': str,
                'region': str,
                'optimal_conditions': {
                    'soil_ph': float,
                    'nitrogen': float,
                    'phosphorus': float,
                    'potassium': float,
                    'moisture': float,
                    'temperature_celsius': float,
                    'rainfall_mm': float,
                    'soil_type': str,
                    'fertilizer_type': str,
                    'irrigation_method': str,
                    'weather_condition': str
                },
                'success_probability': float
            }
        """
        pass
    
    @abstractmethod
    def is_loaded(self) -> bool:
        """Check if model is loaded and ready"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get model metadata and information"""
        pass

