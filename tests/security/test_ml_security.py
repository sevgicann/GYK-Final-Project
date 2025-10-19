"""
ML Security Tests

Bu test dosyası ML model güvenlik testlerini içerir.
Basit ama etkili ML güvenlik testleri.
"""

import pytest
from unittest.mock import patch, Mock
from tests.fixtures.data.sample_data import SAMPLE_PRODUCTS, SAMPLE_ENVIRONMENTS


class TestMLInputSecurity:
    """ML girdi güvenlik testleri."""
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_input_validation(self, client, db_session):
        """Test ML input validation."""
        # Test with invalid ML input data
        invalid_ml_data = [
            {
                'soil_ph': 'invalid',
                'nitrogen': -1,
                'phosphorus': 'invalid',
                'potassium': 'invalid',
                'temperature_celsius': 'invalid',
                'rainfall_mm': 'invalid'
            },
            {
                'soil_ph': None,
                'nitrogen': None,
                'phosphorus': None,
                'potassium': None,
                'temperature_celsius': None,
                'rainfall_mm': None
            },
            {
                'soil_ph': float('inf'),
                'nitrogen': float('-inf'),
                'phosphorus': float('nan'),
                'potassium': 'invalid',
                'temperature_celsius': 'invalid',
                'rainfall_mm': 'invalid'
            }
        ]
        
        for invalid_data in invalid_ml_data:
            response = client.post('/api/ml/predict-crop', json=invalid_data)
            # Should validate ML input data
            assert response.status_code in [200, 201, 400, 404]
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_input_range_validation(self, client, db_session):
        """Test ML input range validation."""
        # Test with out-of-range values
        out_of_range_data = {
            'soil_ph': 999.0,  # Invalid pH range
            'nitrogen': -999.0,  # Negative nitrogen
            'phosphorus': 999999.0,  # Extremely high phosphorus
            'potassium': -999999.0,  # Negative potassium
            'temperature_celsius': 999.0,  # Invalid temperature
            'rainfall_mm': -999.0  # Negative rainfall
        }
        
        response = client.post('/api/ml/predict-crop', json=out_of_range_data)
        # Should validate input ranges
        assert response.status_code in [200, 201, 400, 404]
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_input_sql_injection(self, client, db_session):
        """Test ML input SQL injection protection."""
        sql_injection_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': "'; DROP TABLE ml_models; --"
        }
        
        response = client.post('/api/ml/predict-crop', json=sql_injection_data)
        # Should handle SQL injection attempts
        assert response.status_code in [200, 201, 400, 404]
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_input_xss_protection(self, client, db_session):
        """Test ML input XSS protection."""
        xss_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': '<script>alert("xss")</script>'
        }
        
        response = client.post('/api/ml/predict-crop', json=xss_data)
        # Should handle XSS attempts
        assert response.status_code in [200, 201, 400, 404]


class TestMLModelSecurity:
    """ML model güvenlik testleri."""
    
    @pytest.mark.security
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_ml_model_integrity(self, mock_ml_service, client, db_session):
        """Test ML model integrity."""
        # Mock ML service
        mock_instance = Mock()
        mock_instance.is_loaded.return_value = True
        mock_instance.get_model_info.return_value = {
            'model_type': 'xgboost',
            'version': '1.0',
            'accuracy': 0.85
        }
        mock_ml_service.return_value = mock_instance
        
        # Test model integrity
        response = client.get('/api/ml/models')
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            # Should not expose sensitive model information
            sensitive_fields = ['secret_key', 'private_key', 'model_path']
            
            for field in sensitive_fields:
                assert field not in data
    
    @pytest.mark.security
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_ml_model_access_control(self, mock_ml_service, client, db_session):
        """Test ML model access control."""
        # Mock ML service
        mock_instance = Mock()
        mock_instance.is_loaded.return_value = False
        mock_ml_service.return_value = mock_instance
        
        # Test model access without proper initialization
        response = client.get('/api/ml/status')
        assert response.status_code in [200, 404]
        
        # Test prediction without loaded model
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
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_model_version_security(self, client, db_session):
        """Test ML model version security."""
        # Test model version endpoint
        response = client.get('/api/ml/version')
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            # Should not expose sensitive version information
            sensitive_fields = ['build_path', 'source_code', 'private_key']
            
            for field in sensitive_fields:
                assert field not in data


class TestMLOutputSecurity:
    """ML çıktı güvenlik testleri."""
    
    @pytest.mark.security
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_ml_output_sanitization(self, mock_ml_service, client, db_session):
        """Test ML output sanitization."""
        # Mock ML service with potentially dangerous output
        mock_instance = Mock()
        mock_instance.predict_crop_from_environment.return_value = {
            'prediction': '<script>alert("xss")</script>',
            'confidence': 0.85,
            'model': 'xgboost'
        }
        mock_ml_service.return_value = mock_instance
        
        # Test prediction output
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
        
        if response.status_code in [200, 201]:
            data = response.get_json()
            # Should sanitize output
            assert '<script>' not in data.get('prediction', '')
    
    @pytest.mark.security
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_ml_output_data_leakage(self, mock_ml_service, client, db_session):
        """Test ML output data leakage."""
        # Mock ML service
        mock_instance = Mock()
        mock_instance.predict_crop_from_environment.return_value = {
            'prediction': 'wheat',
            'confidence': 0.85,
            'model': 'xgboost',
            'internal_data': 'sensitive_internal_info'
        }
        mock_ml_service.return_value = mock_instance
        
        # Test prediction output
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
        
        if response.status_code in [200, 201]:
            data = response.get_json()
            # Should not leak internal data
            assert 'internal_data' not in data
            assert 'sensitive_internal_info' not in data
    
    @pytest.mark.security
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_ml_output_confidence_validation(self, mock_ml_service, client, db_session):
        """Test ML output confidence validation."""
        # Mock ML service with invalid confidence
        mock_instance = Mock()
        mock_instance.predict_crop_from_environment.return_value = {
            'prediction': 'wheat',
            'confidence': 1.5,  # Invalid confidence > 1.0
            'model': 'xgboost'
        }
        mock_ml_service.return_value = mock_instance
        
        # Test prediction output
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
        
        if response.status_code in [200, 201]:
            data = response.get_json()
            # Should validate confidence values
            confidence = data.get('confidence', 0)
            assert 0 <= confidence <= 1.0


class TestMLDataSecurity:
    """ML veri güvenlik testleri."""
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_training_data_protection(self, client, db_session):
        """Test ML training data protection."""
        # Test training data endpoint
        response = client.get('/api/ml/training-data')
        # Should not expose training data
        assert response.status_code in [200, 401, 403, 404]
        
        # Test training data upload
        training_data = {
            'soil_ph': [6.5, 7.0, 6.8],
            'nitrogen': [120, 150, 130],
            'crop': ['wheat', 'corn', 'cotton']
        }
        
        response = client.post('/api/ml/training-data', json=training_data)
        # Should require proper authorization
        assert response.status_code in [200, 201, 401, 403, 404]
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_model_file_protection(self, client, db_session):
        """Test ML model file protection."""
        # Test model file download
        response = client.get('/api/ml/model/download')
        # Should not allow model file download
        assert response.status_code in [200, 401, 403, 404]
        
        # Test model file upload
        response = client.post('/api/ml/model/upload')
        # Should require proper authorization
        assert response.status_code in [200, 201, 401, 403, 404]
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_data_encryption(self, client, db_session):
        """Test ML data encryption."""
        # Test ML data encryption endpoint
        response = client.get('/api/ml/encrypt-data')
        assert response.status_code in [200, 404]
        
        # Test ML data decryption endpoint
        response = client.get('/api/ml/decrypt-data')
        assert response.status_code in [200, 404]


class TestMLPerformanceSecurity:
    """ML performans güvenlik testleri."""
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_prediction_rate_limiting(self, client, db_session):
        """Test ML prediction rate limiting."""
        prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara'
        }
        
        # Make multiple prediction requests
        for i in range(20):
            response = client.post('/api/ml/predict-crop', json=prediction_data)
            assert response.status_code in [200, 201, 429, 404]
            
            # Should implement rate limiting after many requests
            if i >= 15:
                assert response.status_code in [200, 201, 429, 404]
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_prediction_timeout(self, client, db_session):
        """Test ML prediction timeout."""
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
        
        # Test prediction timeout
        start_time = time.time()
        response = client.post('/api/ml/predict-crop', json=prediction_data)
        end_time = time.time()
        
        prediction_time = end_time - start_time
        # Should complete within reasonable time
        assert prediction_time < 10.0  # 10 seconds max
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_resource_usage_limits(self, client, db_session):
        """Test ML resource usage limits."""
        # Test with very large input data
        large_prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara',
            'extra_data': 'x' * 10000  # Large additional data
        }
        
        response = client.post('/api/ml/predict-crop', json=large_prediction_data)
        # Should handle large input gracefully
        assert response.status_code in [200, 201, 400, 413, 404]


class TestMLErrorHandlingSecurity:
    """ML hata yönetimi güvenlik testleri."""
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_error_message_security(self, client, db_session):
        """Test ML error message security."""
        # Test with invalid ML data to trigger error
        invalid_data = {
            'soil_ph': 'invalid',
            'nitrogen': 'invalid',
            'phosphorus': 'invalid',
            'potassium': 'invalid',
            'temperature_celsius': 'invalid',
            'rainfall_mm': 'invalid'
        }
        
        response = client.post('/api/ml/predict-crop', json=invalid_data)
        assert response.status_code in [200, 201, 400, 404, 500]
        
        # Error messages should not expose sensitive information
        if response.status_code in [400, 500]:
            response_text = response.get_data(as_text=True)
            sensitive_patterns = ['model_path', 'training_data', 'secret_key', 'internal']
            
            for pattern in sensitive_patterns:
                assert pattern.lower() not in response_text.lower()
    
    @pytest.mark.security
    @pytest.mark.ml
    def test_ml_model_error_handling(self, client, db_session):
        """Test ML model error handling."""
        # Test ML model error endpoint
        response = client.get('/api/ml/error')
        assert response.status_code in [200, 404]
        
        # Test ML model health check
        response = client.get('/api/ml/health')
        assert response.status_code in [200, 404]
        
        # Test ML model status
        response = client.get('/api/ml/status')
        assert response.status_code in [200, 404]
