"""
Unit tests for ML Service

Bu test dosyası ML Service sınıfı için birim testlerini içerir.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from services.ml_service import MLService, get_ml_service
from services.base_predictor import PredictionDirection
from tests.fixtures.data.sample_data import SAMPLE_ML_PREDICTIONS


class TestMLService:
    """ML Service test sınıfı."""
    
    @pytest.mark.unit
    def test_singleton_pattern(self):
        """Test that MLService follows singleton pattern."""
        # Reset singleton instance
        MLService._instance = None
        
        # Create two instances
        service1 = MLService()
        service2 = MLService()
        
        # They should be the same instance
        assert service1 is service2
        assert id(service1) == id(service2)
    
    @pytest.mark.unit
    def test_singleton_initialization_flag(self):
        """Test that singleton initialization flag works correctly."""
        # Reset singleton instance
        MLService._instance = None
        
        service = MLService()
        assert service._initialized is True
        
        # Create another instance - should not reinitialize
        service2 = MLService()
        assert service2._initialized is True
        assert service is service2
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_initialize_models_success(self, mock_lightgbm, mock_xgboost):
        """Test successful model initialization."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictors
        mock_xgboost_instance = Mock()
        mock_lightgbm_instance = Mock()
        mock_xgboost.return_value = mock_xgboost_instance
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        
        # Initialize models
        service.initialize_models()
        
        # Verify predictors were created
        mock_xgboost.assert_called_once_with("models/crop_model.pkl")
        mock_lightgbm.assert_called_once_with("models/sentetik_crop_model.pkl")
        
        # Verify predictors are assigned
        assert service.xgboost_predictor is mock_xgboost_instance
        assert service.lightgbm_predictor is mock_lightgbm_instance
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_initialize_models_xgboost_failure(self, mock_lightgbm, mock_xgboost):
        """Test model initialization with XGBoost failure."""
        # Reset singleton
        MLService._instance = None
        
        # Mock XGBoost to fail, LightGBM to succeed
        mock_xgboost.side_effect = Exception("XGBoost model not found")
        mock_lightgbm_instance = Mock()
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        
        # Initialize models - should not raise exception
        service.initialize_models()
        
        # Verify XGBoost failed but LightGBM succeeded
        assert service.xgboost_predictor is None
        assert service.lightgbm_predictor is mock_lightgbm_instance
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_initialize_models_all_fail(self, mock_lightgbm, mock_xgboost):
        """Test model initialization when all models fail."""
        # Reset singleton
        MLService._instance = None
        
        # Mock both to fail
        mock_xgboost.side_effect = Exception("XGBoost model not found")
        mock_lightgbm.side_effect = Exception("LightGBM model not found")
        
        service = MLService()
        
        # Should raise RuntimeError
        with pytest.raises(RuntimeError, match="No ML models could be initialized"):
            service.initialize_models()
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_get_predictor_default(self, mock_lightgbm, mock_xgboost):
        """Test getting default predictor."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictors
        mock_xgboost_instance = Mock()
        mock_lightgbm_instance = Mock()
        mock_xgboost.return_value = mock_xgboost_instance
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test default predictor (should be lightgbm)
        predictor = service._get_predictor()
        assert predictor is mock_lightgbm_instance
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_get_predictor_specific(self, mock_lightgbm, mock_xgboost):
        """Test getting specific predictor."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictors
        mock_xgboost_instance = Mock()
        mock_lightgbm_instance = Mock()
        mock_xgboost.return_value = mock_xgboost_instance
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test specific predictors
        xgb_predictor = service._get_predictor('xgboost')
        lgb_predictor = service._get_predictor('lightgbm')
        
        assert xgb_predictor is mock_xgboost_instance
        assert lgb_predictor is mock_lightgbm_instance
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_get_predictor_unknown_type(self, mock_lightgbm, mock_xgboost):
        """Test getting predictor with unknown type."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictors
        mock_xgboost_instance = Mock()
        mock_lightgbm_instance = Mock()
        mock_xgboost.return_value = mock_xgboost_instance
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test unknown type - should return default
        predictor = service._get_predictor('unknown')
        assert predictor is mock_lightgbm_instance  # Should return default (lightgbm)
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_predict_crop_from_environment_success(self, mock_lightgbm, mock_xgboost):
        """Test successful crop prediction from environment."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictor
        mock_lightgbm_instance = Mock()
        mock_lightgbm_instance.is_loaded.return_value = True
        mock_lightgbm_instance.predict_crop_from_environment.return_value = {
            'success': True,
            'predicted_crop': 'wheat',
            'confidence': 0.85,
            'top_3_predictions': [('wheat', 0.85), ('corn', 0.72), ('rice', 0.68)]
        }
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test prediction
        environment_data = SAMPLE_ML_PREDICTIONS['environment_to_crop']['input']
        result = service.predict_crop_from_environment(environment_data)
        
        # Verify result
        assert result['success'] is True
        assert result['predicted_crop'] == 'wheat'
        assert result['confidence'] == 0.85
        assert result['model_used'] == 'lightgbm'
        assert result['direction'] == PredictionDirection.ENVIRONMENT_TO_CROP.value
        
        # Verify predictor was called
        mock_lightgbm_instance.predict_crop_from_environment.assert_called_once_with(environment_data)
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_predict_crop_from_environment_no_predictor(self, mock_lightgbm, mock_xgboost):
        """Test crop prediction when no predictor is available."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictor as not loaded
        mock_lightgbm_instance = Mock()
        mock_lightgbm_instance.is_loaded.return_value = False
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test prediction
        environment_data = SAMPLE_ML_PREDICTIONS['environment_to_crop']['input']
        result = service.predict_crop_from_environment(environment_data)
        
        # Verify error result
        assert result['success'] is False
        assert 'error' in result
        assert result['error'] == 'No predictor available'
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_predict_crop_from_environment_exception(self, mock_lightgbm, mock_xgboost):
        """Test crop prediction when predictor raises exception."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictor to raise exception
        mock_lightgbm_instance = Mock()
        mock_lightgbm_instance.is_loaded.return_value = True
        mock_lightgbm_instance.predict_crop_from_environment.side_effect = Exception("Prediction failed")
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test prediction
        environment_data = SAMPLE_ML_PREDICTIONS['environment_to_crop']['input']
        result = service.predict_crop_from_environment(environment_data)
        
        # Verify error result
        assert result['success'] is False
        assert 'error' in result
        assert result['error'] == 'Prediction failed'
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_predict_environment_from_crop_success(self, mock_lightgbm, mock_xgboost):
        """Test successful environment prediction from crop."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictor
        mock_lightgbm_instance = Mock()
        mock_lightgbm_instance.is_loaded.return_value = True
        mock_lightgbm_instance.predict_environment_from_crop.return_value = {
            'success': True,
            'crop': 'tomato',
            'region': 'Marmara',
            'optimal_conditions': {
                'soil_ph': 6.5,
                'nitrogen': 150,
                'phosphorus': 60,
                'potassium': 250,
                'temperature_celsius': 24,
                'humidity': 70,
                'rainfall_mm': 800
            },
            'success_probability': 0.85
        }
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test prediction
        result = service.predict_environment_from_crop('tomato', 'Marmara')
        
        # Verify result
        assert result['success'] is True
        assert result['crop'] == 'tomato'
        assert result['region'] == 'Marmara'
        assert result['model_used'] == 'lightgbm'
        assert result['direction'] == PredictionDirection.CROP_TO_ENVIRONMENT.value
        assert 'optimal_conditions' in result
        
        # Verify predictor was called
        mock_lightgbm_instance.predict_environment_from_crop.assert_called_once_with('tomato', 'Marmara')
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_get_available_models(self, mock_lightgbm, mock_xgboost):
        """Test getting available models status."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictors with different statuses
        mock_xgboost_instance = Mock()
        mock_xgboost_instance.is_loaded.return_value = True
        mock_lightgbm_instance = Mock()
        mock_lightgbm_instance.is_loaded.return_value = False
        
        mock_xgboost.return_value = mock_xgboost_instance
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test getting available models
        models_status = service.get_available_models()
        
        # Verify status
        assert models_status['xgboost'] is True
        assert models_status['lightgbm'] is False
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_get_model_info(self, mock_lightgbm, mock_xgboost):
        """Test getting model information."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictor
        mock_lightgbm_instance = Mock()
        mock_lightgbm_instance.get_model_info.return_value = {
            'status': 'loaded',
            'model_type': 'LightGBM',
            'features': ['soil_ph', 'nitrogen', 'phosphorus']
        }
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test getting model info
        info = service.get_model_info('lightgbm')
        
        # Verify info
        assert info['status'] == 'loaded'
        assert info['model_type'] == 'LightGBM'
        assert 'features' in info
        
        # Verify predictor was called
        mock_lightgbm_instance.get_model_info.assert_called_once()
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_get_model_info_unavailable(self, mock_lightgbm, mock_xgboost):
        """Test getting model info when predictor is unavailable."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictors as None
        mock_xgboost.return_value = None
        mock_lightgbm.return_value = None
        
        service = MLService()
        service.initialize_models()
        
        # Test getting model info
        info = service.get_model_info()
        
        # Verify unavailable status
        assert info['status'] == 'unavailable'
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_health_check(self, mock_lightgbm, mock_xgboost):
        """Test health check functionality."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictors
        mock_xgboost_instance = Mock()
        mock_xgboost_instance.is_loaded.return_value = True
        mock_xgboost_instance.get_model_info.return_value = {
            'status': 'loaded',
            'model_type': 'XGBoost'
        }
        
        mock_lightgbm_instance = Mock()
        mock_lightgbm_instance.is_loaded.return_value = False
        mock_lightgbm_instance.get_model_info.return_value = {
            'status': 'unloaded',
            'model_type': 'LightGBM'
        }
        
        mock_xgboost.return_value = mock_xgboost_instance
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test health check
        health = service.health_check()
        
        # Verify health status
        assert health['status'] == 'healthy'  # At least one model is available
        assert health['models']['xgboost'] is True
        assert health['models']['lightgbm'] is False
        assert health['default_model'] == 'lightgbm'
        assert health['initialized'] is True
        assert health['capabilities']['environment_to_crop'] is True
        assert health['capabilities']['crop_to_environment'] is True
        assert 'model_details' in health
        assert 'xgboost' in health['model_details']
        assert 'lightgbm' in health['model_details']
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_health_check_unhealthy(self, mock_lightgbm, mock_xgboost):
        """Test health check when no models are available."""
        # Reset singleton
        MLService._instance = None
        
        # Mock predictors as not loaded
        mock_xgboost_instance = Mock()
        mock_xgboost_instance.is_loaded.return_value = False
        mock_lightgbm_instance = Mock()
        mock_lightgbm_instance.is_loaded.return_value = False
        
        mock_xgboost.return_value = mock_xgboost_instance
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test health check
        health = service.health_check()
        
        # Verify unhealthy status
        assert health['status'] == 'unhealthy'
        assert health['models']['xgboost'] is False
        assert health['models']['lightgbm'] is False
        assert health['capabilities']['environment_to_crop'] is False
        assert health['capabilities']['crop_to_environment'] is False
    
    @pytest.mark.unit
    def test_get_ml_service_function(self):
        """Test the global get_ml_service function."""
        # Reset singleton
        MLService._instance = None
        
        # Test function
        service1 = get_ml_service()
        service2 = get_ml_service()
        
        # Should return the same singleton instance
        assert service1 is service2
        assert isinstance(service1, MLService)
    
    @pytest.mark.unit
    @patch('services.ml_service.XGBoostCropPredictor')
    @patch('services.ml_service.LightGBMCropPredictor')
    def test_predict_with_specific_model_type(self, mock_lightgbm, mock_xgboost):
        """Test prediction with specific model type."""
        # Reset singleton
        MLService._instance = None
        
        # Mock both predictors
        mock_xgboost_instance = Mock()
        mock_xgboost_instance.is_loaded.return_value = True
        mock_xgboost_instance.predict_crop_from_environment.return_value = {
            'success': True,
            'predicted_crop': 'wheat',
            'confidence': 0.80
        }
        
        mock_lightgbm_instance = Mock()
        mock_lightgbm_instance.is_loaded.return_value = True
        mock_lightgbm_instance.predict_crop_from_environment.return_value = {
            'success': True,
            'predicted_crop': 'corn',
            'confidence': 0.85
        }
        
        mock_xgboost.return_value = mock_xgboost_instance
        mock_lightgbm.return_value = mock_lightgbm_instance
        
        service = MLService()
        service.initialize_models()
        
        # Test prediction with XGBoost
        environment_data = SAMPLE_ML_PREDICTIONS['environment_to_crop']['input']
        result = service.predict_crop_from_environment(environment_data, model_type='xgboost')
        
        # Verify XGBoost was used
        assert result['predicted_crop'] == 'wheat'
        assert result['model_used'] == 'xgboost'
        mock_xgboost_instance.predict_crop_from_environment.assert_called_once()
        
        # Test prediction with LightGBM
        result = service.predict_crop_from_environment(environment_data, model_type='lightgbm')
        
        # Verify LightGBM was used
        assert result['predicted_crop'] == 'corn'
        assert result['model_used'] == 'lightgbm'
        mock_lightgbm_instance.predict_crop_from_environment.assert_called_once()
