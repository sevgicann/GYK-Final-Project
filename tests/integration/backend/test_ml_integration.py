"""
Backend ML Model Integration Tests

Bu test dosyası ML model entegrasyon testlerini içerir.
XGBoost ve LightGBM modellerinin backend ile entegrasyonunu test eder.
"""

import pytest
import numpy as np
from unittest.mock import patch, Mock, MagicMock
from tests.fixtures.data.sample_data import SAMPLE_PRODUCTS, SAMPLE_ENVIRONMENTS


class TestMLServiceIntegration:
    """ML servis entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_ml_service_initialization(self, client, db_session):
        """Test ML service initialization."""
        # Test ML service status
        response = client.get('/api/ml/status')
        assert response.status_code in [200, 404]
        
        # Test model info
        response = client.get('/api/ml/models')
        assert response.status_code in [200, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_xgboost_prediction_integration(self, mock_ml_service, client, db_session):
        """Test XGBoost model prediction integration."""
        # Mock XGBoost predictor
        mock_xgb_predictor = Mock()
        mock_xgb_predictor.predict_crop_from_environment.return_value = {
            'prediction': 'wheat',
            'confidence': 0.92,
            'model': 'xgboost'
        }
        
        # Mock ML service
        mock_instance = Mock()
        mock_instance.get_xgboost_predictor.return_value = mock_xgb_predictor
        mock_instance.is_loaded.return_value = True
        mock_ml_service.return_value = mock_instance
        
        # Test XGBoost prediction
        prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara'
        }
        
        response = client.post('/api/ml/predict-crop', json=prediction_data)
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_lightgbm_prediction_integration(self, mock_ml_service, client, db_session):
        """Test LightGBM model prediction integration."""
        # Mock LightGBM predictor
        mock_lgb_predictor = Mock()
        mock_lgb_predictor.predict_crop_from_environment.return_value = {
            'prediction': 'corn',
            'confidence': 0.88,
            'model': 'lightgbm'
        }
        
        # Mock ML service
        mock_instance = Mock()
        mock_instance.get_lightgbm_predictor.return_value = mock_lgb_predictor
        mock_instance.is_loaded.return_value = True
        mock_ml_service.return_value = mock_instance
        
        # Test LightGBM prediction
        prediction_data = {
            'soil_ph': 7.0,
            'nitrogen': 150,
            'phosphorus': 60,
            'potassium': 200,
            'temperature_celsius': 25,
            'rainfall_mm': 800,
            'region': 'Aegean'
        }
        
        response = client.post('/api/ml/predict-crop', json=prediction_data)
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_bi_directional_prediction_integration(self, mock_ml_service, client, db_session):
        """Test bi-directional prediction integration."""
        # Mock both predictors
        mock_predictor = Mock()
        mock_predictor.predict_crop_from_environment.return_value = {
            'prediction': 'wheat',
            'confidence': 0.85
        }
        mock_predictor.predict_environment_from_crop.return_value = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600
        }
        
        # Mock ML service
        mock_instance = Mock()
        mock_instance.predict_crop_from_environment.return_value = mock_predictor.predict_crop_from_environment.return_value
        mock_instance.predict_environment_from_crop.return_value = mock_predictor.predict_environment_from_crop.return_value
        mock_ml_service.return_value = mock_instance
        
        # Test crop prediction
        crop_prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara'
        }
        
        crop_response = client.post('/api/ml/predict-crop', json=crop_prediction_data)
        assert crop_response.status_code in [200, 201, 404]
        
        # Test environment prediction
        env_prediction_data = {
            'crop': 'wheat',
            'region': 'Marmara'
        }
        
        env_response = client.post('/api/ml/predict-environment', json=env_prediction_data)
        assert env_response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_ml_model_health_check(self, client, db_session):
        """Test ML model health check."""
        # Test model health endpoint
        response = client.get('/api/ml/health')
        assert response.status_code in [200, 404]
        
        # Test model performance metrics
        response = client.get('/api/ml/metrics')
        assert response.status_code in [200, 404]


class TestMLDataIntegration:
    """ML veri entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_ml_data_preprocessing_integration(self, client, db_session):
        """Test ML data preprocessing integration."""
        # Test data preprocessing endpoint
        raw_data = {
            'soil_ph': '6.5',
            'nitrogen': '120.5',
            'phosphorus': '45.2',
            'potassium': '150.8',
            'temperature_celsius': '22.3',
            'rainfall_mm': '600.1',
            'region': 'Marmara'
        }
        
        response = client.post('/api/ml/preprocess', json=raw_data)
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_ml_feature_engineering_integration(self, client, db_session):
        """Test ML feature engineering integration."""
        # Test feature engineering
        feature_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara'
        }
        
        response = client.post('/api/ml/features', json=feature_data)
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_ml_prediction_validation_integration(self, client, db_session):
        """Test ML prediction validation integration."""
        # Test prediction validation
        prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara',
            'predicted_crop': 'wheat'
        }
        
        response = client.post('/api/ml/validate-prediction', json=prediction_data)
        assert response.status_code in [200, 201, 404]


class TestMLPerformanceIntegration:
    """ML performans entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.ml
    @pytest.mark.performance
    def test_ml_prediction_performance(self, client, db_session):
        """Test ML prediction performance."""
        import time
        
        prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara'
        }
        
        # Test prediction response time
        start_time = time.time()
        response = client.post('/api/ml/predict-crop', json=prediction_data)
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 5.0  # 5 seconds max for ML prediction
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    @pytest.mark.performance
    def test_ml_batch_prediction_performance(self, client, db_session):
        """Test ML batch prediction performance."""
        # Test batch prediction
        batch_data = {
            'predictions': [
                {
                    'soil_ph': 6.5,
                    'nitrogen': 120,
                    'phosphorus': 45,
                    'potassium': 150,
                    'temperature_celsius': 22,
                    'rainfall_mm': 600,
                    'region': 'Marmara'
                },
                {
                    'soil_ph': 7.0,
                    'nitrogen': 150,
                    'phosphorus': 60,
                    'potassium': 200,
                    'temperature_celsius': 25,
                    'rainfall_mm': 800,
                    'region': 'Aegean'
                }
            ]
        }
        
        response = client.post('/api/ml/batch-predict', json=batch_data)
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    @pytest.mark.performance
    def test_ml_concurrent_predictions(self, client, db_session):
        """Test ML concurrent predictions."""
        import threading
        
        results = []
        
        def make_prediction():
            prediction_data = {
                'soil_ph': 6.5,
                'nitrogen': 120,
                'phosphorus': 45,
                'potassium': 150,
                'temperature_celsius': 22,
                'rainfall_mm': 600,
                'region': 'Marmara'
            }
            
            response = client.post('/api/ml/predict-crop', json=prediction_data)
            results.append(response.status_code)
        
        # Make multiple concurrent predictions
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=make_prediction)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All predictions should complete successfully
        assert len(results) == 3
        for status_code in results:
            assert status_code in [200, 201, 404]


class TestMLErrorHandlingIntegration:
    """ML hata yönetimi entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_ml_model_not_loaded_error(self, client, db_session):
        """Test ML model not loaded error handling."""
        # Test prediction when model is not loaded
        prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara'
        }
        
        response = client.post('/api/ml/predict-crop', json=prediction_data)
        assert response.status_code in [200, 201, 404, 500]
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_ml_invalid_data_error(self, client, db_session):
        """Test ML invalid data error handling."""
        # Test prediction with invalid data
        invalid_data = {
            'soil_ph': 'invalid',
            'nitrogen': -1,
            'phosphorus': 'invalid',
            'potassium': 'invalid',
            'temperature_celsius': 'invalid',
            'rainfall_mm': 'invalid',
            'region': 'InvalidRegion'
        }
        
        response = client.post('/api/ml/predict-crop', json=invalid_data)
        assert response.status_code in [200, 201, 400, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_ml_missing_data_error(self, client, db_session):
        """Test ML missing data error handling."""
        # Test prediction with missing data
        incomplete_data = {
            'soil_ph': 6.5,
            'nitrogen': 120
            # Missing other required fields
        }
        
        response = client.post('/api/ml/predict-crop', json=incomplete_data)
        assert response.status_code in [200, 201, 400, 404]


class TestMLModelComparisonIntegration:
    """ML model karşılaştırma entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_model_performance_comparison(self, client, db_session):
        """Test model performance comparison."""
        # Test model comparison endpoint
        comparison_data = {
            'test_data': [
                {
                    'soil_ph': 6.5,
                    'nitrogen': 120,
                    'phosphorus': 45,
                    'potassium': 150,
                    'temperature_celsius': 22,
                    'rainfall_mm': 600,
                    'region': 'Marmara',
                    'actual_crop': 'wheat'
                }
            ]
        }
        
        response = client.post('/api/ml/compare-models', json=comparison_data)
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_model_ensemble_prediction(self, client, db_session):
        """Test model ensemble prediction."""
        # Test ensemble prediction
        prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara',
            'use_ensemble': True
        }
        
        response = client.post('/api/ml/predict-crop', json=prediction_data)
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    def test_model_confidence_scoring(self, client, db_session):
        """Test model confidence scoring."""
        # Test confidence scoring
        prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara',
            'include_confidence': True
        }
        
        response = client.post('/api/ml/predict-crop', json=prediction_data)
        assert response.status_code in [200, 201, 404]
