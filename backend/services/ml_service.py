"""
ML Service Manager - Singleton Pattern & Dependency Injection
Central service for managing bi-directional ML predictions
"""
from typing import Optional, Dict, Any
from .base_predictor import BasePredictor, PredictionDirection
from .xgboost_predictor import XGBoostCropPredictor
from .lightgbm_predictor import LightGBMCropPredictor
from utils.logger import get_logger

logger = get_logger(__name__)


class MLService:
    """
    Singleton service for managing ML predictors
    Provides unified interface for bi-directional predictions
    """
    
    _instance: Optional['MLService'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.xgboost_predictor: Optional[XGBoostCropPredictor] = None
        self.lightgbm_predictor: Optional[LightGBMCropPredictor] = None
        self.default_predictor: str = 'lightgbm'  # Default to LightGBM (more advanced)
        
        logger.info("🤖 MLService singleton created")
    
    def initialize_models(self,
                         xgboost_model_path: str = "models/crop_model.pkl",
                         lightgbm_model_path: str = "models/sentetik_crop_model.pkl"):
        """
        Initialize all ML predictors
        
        Args:
            xgboost_model_path: Path to XGBoost model
            lightgbm_model_path: Path to LightGBM model
        """
        try:
            logger.info("🚀 Initializing ML predictors...")
            
            # Initialize XGBoost predictor
            try:
                self.xgboost_predictor = XGBoostCropPredictor(xgboost_model_path)
                logger.info("✅ XGBoost predictor initialized")
            except Exception as e:
                logger.warning(f"⚠️  XGBoost predictor failed to initialize: {e}")
            
            # Initialize LightGBM predictor
            try:
                self.lightgbm_predictor = LightGBMCropPredictor(lightgbm_model_path)
                logger.info("✅ LightGBM predictor initialized")
            except Exception as e:
                logger.warning(f"⚠️  LightGBM predictor failed to initialize: {e}")
            
            # Check if at least one model loaded
            if not self.xgboost_predictor and not self.lightgbm_predictor:
                raise RuntimeError("No ML models could be initialized")
            
            logger.info("🎉 ML Service initialization complete")
            
        except Exception as e:
            logger.error(f"❌ ML Service initialization failed: {str(e)}")
            raise
    
    def _get_predictor(self, model_type: Optional[str] = None) -> Optional[BasePredictor]:
        """
        Get predictor instance
        
        Args:
            model_type: 'xgboost' or 'lightgbm', defaults to self.default_predictor
            
        Returns:
            Predictor instance or None
        """
        if model_type is None:
            model_type = self.default_predictor
        
        if model_type == 'xgboost':
            return self.xgboost_predictor
        elif model_type == 'lightgbm':
            return self.lightgbm_predictor
        else:
            logger.warning(f"Unknown model type: {model_type}, using default")
            return self.lightgbm_predictor or self.xgboost_predictor
    
    def predict_crop_from_environment(self,
                                     environment_data: Dict[str, Any],
                                     model_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Predict best crop given environmental conditions
        Direction: Environment → Crop
        
        Args:
            environment_data: Environmental features
            model_type: 'xgboost' or 'lightgbm' (optional)
            
        Returns:
            Prediction result dictionary
        """
        try:
            predictor = self._get_predictor(model_type)
            
            if not predictor or not predictor.is_loaded():
                return {
                    'success': False,
                    'error': 'No predictor available'
                }
            
            logger.info(f"🌾 Predicting crop from environment using {model_type or self.default_predictor}")
            result = predictor.predict_crop_from_environment(environment_data)
            
            # Add metadata
            if result.get('success'):
                result['model_used'] = model_type or self.default_predictor
                result['direction'] = PredictionDirection.ENVIRONMENT_TO_CROP.value
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Crop prediction error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_environment_from_crop(self,
                                     crop: str,
                                     region: str,
                                     model_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Predict optimal environmental conditions for a target crop
        Direction: Crop → Environment
        
        Args:
            crop: Target crop name
            region: Target region
            model_type: 'xgboost' or 'lightgbm' (optional)
            
        Returns:
            Optimization result dictionary
        """
        try:
            predictor = self._get_predictor(model_type)
            
            if not predictor or not predictor.is_loaded():
                return {
                    'success': False,
                    'error': 'No predictor available'
                }
            
            logger.info(f"🔍 Optimizing environment for crop '{crop}' using {model_type or self.default_predictor}")
            result = predictor.predict_environment_from_crop(crop, region)
            
            # Add metadata
            if result.get('success'):
                result['model_used'] = model_type or self.default_predictor
                result['direction'] = PredictionDirection.CROP_TO_ENVIRONMENT.value
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Environment optimization error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_available_models(self) -> Dict[str, bool]:
        """Get status of all models"""
        return {
            'xgboost': self.xgboost_predictor.is_loaded() if self.xgboost_predictor else False,
            'lightgbm': self.lightgbm_predictor.is_loaded() if self.lightgbm_predictor else False,
        }
    
    def get_model_info(self, model_type: Optional[str] = None) -> Dict[str, Any]:
        """Get information about a specific model"""
        predictor = self._get_predictor(model_type)
        
        if not predictor:
            return {'status': 'unavailable'}
        
        return predictor.get_model_info()
    
    def health_check(self) -> Dict[str, Any]:
        """Health check for ML service"""
        models_status = self.get_available_models()
        
        xgboost_info = self.xgboost_predictor.get_model_info() if self.xgboost_predictor else {}
        lightgbm_info = self.lightgbm_predictor.get_model_info() if self.lightgbm_predictor else {}
        
        return {
            'status': 'healthy' if any(models_status.values()) else 'unhealthy',
            'models': models_status,
            'default_model': self.default_predictor,
            'initialized': self._initialized,
            'capabilities': {
                'environment_to_crop': any(models_status.values()),
                'crop_to_environment': any(models_status.values())
            },
            'model_details': {
                'xgboost': xgboost_info,
                'lightgbm': lightgbm_info
            }
        }


# Global instance getter
def get_ml_service() -> MLService:
    """Get ML service singleton instance"""
    return MLService()

