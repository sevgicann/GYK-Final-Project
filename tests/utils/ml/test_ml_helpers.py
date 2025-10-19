"""
ML Test Helpers

Bu modül ML model testleri için yardımcı fonksiyonları içerir.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from unittest.mock import Mock, MagicMock
from tests.fixtures.data.sample_data import SAMPLE_ML_PREDICTIONS


class MLTestHelpers:
    """ML test helper functions."""
    
    @staticmethod
    def create_mock_environment_data(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create mock environment data for testing.
        
        Args:
            overrides: Dictionary to override default values
            
        Returns:
            Mock environment data
        """
        default_data = {
            'region': 'Marmara',
            'soil_type': 'Killi Toprak',
            'soil_ph': 6.5,
            'nitrogen': 90,
            'phosphorus': 42,
            'potassium': 43,
            'moisture': 65,
            'temperature_celsius': 25,
            'rainfall_mm': 600,
            'fertilizer_type': 'Amonyum Sülfat',
            'irrigation_method': 'Damla Sulama',
            'weather_condition': 'Güneşli',
            'language': 'tr'
        }
        
        if overrides:
            default_data.update(overrides)
        
        return default_data
    
    @staticmethod
    def create_mock_crop_data(crop: str = 'tomato', region: str = 'Marmara') -> Dict[str, Any]:
        """
        Create mock crop data for testing.
        
        Args:
            crop: Crop name
            region: Region name
            
        Returns:
            Mock crop data
        """
        return {
            'crop': crop,
            'region': region,
            'language': 'tr'
        }
    
    @staticmethod
    def create_mock_prediction_result(success: bool = True, 
                                    predicted_crop: str = 'wheat',
                                    confidence: float = 0.85) -> Dict[str, Any]:
        """
        Create mock prediction result.
        
        Args:
            success: Whether prediction was successful
            predicted_crop: Predicted crop name
            confidence: Confidence score
            
        Returns:
            Mock prediction result
        """
        if success:
            return {
                'success': True,
                'predicted_crop': predicted_crop,
                'confidence': confidence,
                'top_3_predictions': [
                    (predicted_crop, confidence),
                    ('corn', 0.72),
                    ('rice', 0.68)
                ],
                'model_used': 'lightgbm',
                'direction': 'environment_to_crop'
            }
        else:
            return {
                'success': False,
                'error': 'Prediction failed'
            }
    
    @staticmethod
    def create_mock_environment_optimization_result(success: bool = True,
                                                   crop: str = 'tomato',
                                                   region: str = 'Marmara') -> Dict[str, Any]:
        """
        Create mock environment optimization result.
        
        Args:
            success: Whether optimization was successful
            crop: Crop name
            region: Region name
            
        Returns:
            Mock optimization result
        """
        if success:
            return {
                'success': True,
                'crop': crop,
                'region': region,
                'optimal_conditions': {
                    'soil_ph': 6.5,
                    'nitrogen': 150,
                    'phosphorus': 60,
                    'potassium': 250,
                    'moisture': 70,
                    'temperature_celsius': 24,
                    'rainfall_mm': 800,
                    'soil_type': 'Killi Toprak',
                    'fertilizer_type': 'Organik Gübre',
                    'irrigation_method': 'Damla Sulama',
                    'weather_condition': 'Güneşli'
                },
                'success_probability': 0.85,
                'model_used': 'lightgbm',
                'direction': 'crop_to_environment'
            }
        else:
            return {
                'success': False,
                'error': 'Environment optimization failed'
            }
    
    @staticmethod
    def create_mock_model_info(model_type: str = 'lightgbm',
                              status: str = 'loaded',
                              features: List[str] = None) -> Dict[str, Any]:
        """
        Create mock model info.
        
        Args:
            model_type: Model type (xgboost, lightgbm)
            status: Model status (loaded, unloaded)
            features: List of model features
            
        Returns:
            Mock model info
        """
        if features is None:
            features = ['soil_ph', 'nitrogen', 'phosphorus', 'potassium', 'moisture', 'temperature_celsius']
        
        return {
            'status': status,
            'model_type': model_type.title(),
            'algorithm': 'Gradient Boosting Decision Tree' if model_type == 'lightgbm' else 'Extreme Gradient Boosting',
            'features': {
                'numeric': features,
                'categorical': ['region', 'soil_type', 'fertilizer_type'],
                'engineered': True
            },
            'crops': ['wheat', 'rice', 'corn', 'tomato', 'potato', 'onion'],
            'capabilities': ['environment_to_crop', 'crop_to_environment']
        }
    
    @staticmethod
    def create_mock_health_check(models_status: Dict[str, bool] = None) -> Dict[str, Any]:
        """
        Create mock health check result.
        
        Args:
            models_status: Status of models
            
        Returns:
            Mock health check result
        """
        if models_status is None:
            models_status = {'xgboost': True, 'lightgbm': True}
        
        return {
            'status': 'healthy' if any(models_status.values()) else 'unhealthy',
            'models': models_status,
            'default_model': 'lightgbm',
            'initialized': True,
            'capabilities': {
                'environment_to_crop': any(models_status.values()),
                'crop_to_environment': any(models_status.values())
            },
            'model_details': {
                'xgboost': MLTestHelpers.create_mock_model_info('xgboost', 'loaded' if models_status.get('xgboost') else 'unloaded'),
                'lightgbm': MLTestHelpers.create_mock_model_info('lightgbm', 'loaded' if models_status.get('lightgbm') else 'unloaded')
            }
        }
    
    @staticmethod
    def create_mock_predictor(model_type: str = 'lightgbm',
                            is_loaded: bool = True,
                            prediction_result: Dict[str, Any] = None,
                            optimization_result: Dict[str, Any] = None) -> Mock:
        """
        Create mock predictor instance.
        
        Args:
            model_type: Model type
            is_loaded: Whether model is loaded
            prediction_result: Mock prediction result
            optimization_result: Mock optimization result
            
        Returns:
            Mock predictor instance
        """
        mock_predictor = Mock()
        mock_predictor.is_loaded.return_value = is_loaded
        mock_predictor.get_model_info.return_value = MLTestHelpers.create_mock_model_info(model_type)
        
        if prediction_result is None:
            prediction_result = MLTestHelpers.create_mock_prediction_result()
        if optimization_result is None:
            optimization_result = MLTestHelpers.create_mock_environment_optimization_result()
        
        mock_predictor.predict_crop_from_environment.return_value = prediction_result
        mock_predictor.predict_environment_from_crop.return_value = optimization_result
        
        return mock_predictor
    
    @staticmethod
    def create_test_dataframe(rows: int = 100) -> pd.DataFrame:
        """
        Create test DataFrame with mock agricultural data.
        
        Args:
            rows: Number of rows to create
            
        Returns:
            Test DataFrame
        """
        np.random.seed(42)  # For reproducible results
        
        data = {
            'soil_ph': np.random.uniform(4.0, 8.0, rows),
            'nitrogen': np.random.uniform(50, 200, rows),
            'phosphorus': np.random.uniform(20, 100, rows),
            'potassium': np.random.uniform(100, 300, rows),
            'moisture': np.random.uniform(30, 90, rows),
            'temperature_celsius': np.random.uniform(10, 35, rows),
            'rainfall_mm': np.random.uniform(200, 2000, rows),
            'region': np.random.choice(['Marmara', 'Akdeniz', 'Karadeniz', 'İç Anadolu'], rows),
            'soil_type': np.random.choice(['Killi Toprak', 'Kumlu Toprak', 'Asitli Toprak'], rows),
            'crop': np.random.choice(['wheat', 'rice', 'corn', 'tomato', 'potato'], rows)
        }
        
        return pd.DataFrame(data)
    
    @staticmethod
    def assert_prediction_result(result: Dict[str, Any], 
                               expected_success: bool = True,
                               expected_crop: str = None,
                               min_confidence: float = 0.0) -> None:
        """
        Assert prediction result structure and values.
        
        Args:
            result: Prediction result to validate
            expected_success: Expected success status
            expected_crop: Expected crop name
            min_confidence: Minimum confidence score
        """
        assert 'success' in result, "Result should contain 'success' field"
        assert result['success'] == expected_success, f"Expected success={expected_success}, got {result['success']}"
        
        if expected_success:
            assert 'predicted_crop' in result, "Result should contain 'predicted_crop' field"
            assert 'confidence' in result, "Result should contain 'confidence' field"
            assert result['confidence'] >= min_confidence, f"Confidence {result['confidence']} should be >= {min_confidence}"
            
            if expected_crop:
                assert result['predicted_crop'] == expected_crop, f"Expected crop '{expected_crop}', got '{result['predicted_crop']}'"
            
            assert 'top_3_predictions' in result, "Result should contain 'top_3_predictions' field"
            assert isinstance(result['top_3_predictions'], list), "top_3_predictions should be a list"
            assert len(result['top_3_predictions']) <= 3, "top_3_predictions should have at most 3 items"
        else:
            assert 'error' in result, "Error result should contain 'error' field"
    
    @staticmethod
    def assert_optimization_result(result: Dict[str, Any],
                                 expected_success: bool = True,
                                 expected_crop: str = None,
                                 min_probability: float = 0.0) -> None:
        """
        Assert environment optimization result structure and values.
        
        Args:
            result: Optimization result to validate
            expected_success: Expected success status
            expected_crop: Expected crop name
            min_probability: Minimum success probability
        """
        assert 'success' in result, "Result should contain 'success' field"
        assert result['success'] == expected_success, f"Expected success={expected_success}, got {result['success']}"
        
        if expected_success:
            assert 'crop' in result, "Result should contain 'crop' field"
            assert 'region' in result, "Result should contain 'region' field"
            assert 'optimal_conditions' in result, "Result should contain 'optimal_conditions' field"
            assert 'success_probability' in result, "Result should contain 'success_probability' field"
            
            assert result['success_probability'] >= min_probability, f"Probability {result['success_probability']} should be >= {min_probability}"
            
            if expected_crop:
                assert result['crop'] == expected_crop, f"Expected crop '{expected_crop}', got '{result['crop']}'"
            
            optimal_conditions = result['optimal_conditions']
            required_fields = ['soil_ph', 'nitrogen', 'phosphorus', 'potassium', 'moisture', 'temperature_celsius']
            for field in required_fields:
                assert field in optimal_conditions, f"optimal_conditions should contain '{field}'"
                assert isinstance(optimal_conditions[field], (int, float)), f"{field} should be numeric"
        else:
            assert 'error' in result, "Error result should contain 'error' field"
    
    @staticmethod
    def assert_model_info(info: Dict[str, Any], expected_status: str = 'loaded') -> None:
        """
        Assert model info structure and values.
        
        Args:
            info: Model info to validate
            expected_status: Expected model status
        """
        assert 'status' in info, "Model info should contain 'status' field"
        assert 'model_type' in info, "Model info should contain 'model_type' field"
        assert 'algorithm' in info, "Model info should contain 'algorithm' field"
        assert 'features' in info, "Model info should contain 'features' field"
        assert 'crops' in info, "Model info should contain 'crops' field"
        assert 'capabilities' in info, "Model info should contain 'capabilities' field"
        
        assert info['status'] == expected_status, f"Expected status '{expected_status}', got '{info['status']}'"
        assert isinstance(info['features'], dict), "Features should be a dictionary"
        assert isinstance(info['crops'], list), "Crops should be a list"
        assert isinstance(info['capabilities'], list), "Capabilities should be a list"
        
        assert 'numeric' in info['features'], "Features should contain 'numeric' field"
        assert 'categorical' in info['features'], "Features should contain 'categorical' field"
    
    @staticmethod
    def assert_health_check(health: Dict[str, Any], expected_status: str = 'healthy') -> None:
        """
        Assert health check result structure and values.
        
        Args:
            health: Health check result to validate
            expected_status: Expected health status
        """
        assert 'status' in health, "Health check should contain 'status' field"
        assert 'models' in health, "Health check should contain 'models' field"
        assert 'default_model' in health, "Health check should contain 'default_model' field"
        assert 'initialized' in health, "Health check should contain 'initialized' field"
        assert 'capabilities' in health, "Health check should contain 'capabilities' field"
        assert 'model_details' in health, "Health check should contain 'model_details' field"
        
        assert health['status'] == expected_status, f"Expected status '{expected_status}', got '{health['status']}'"
        assert isinstance(health['models'], dict), "Models should be a dictionary"
        assert isinstance(health['capabilities'], dict), "Capabilities should be a dictionary"
        assert isinstance(health['model_details'], dict), "Model details should be a dictionary"
        
        assert 'environment_to_crop' in health['capabilities'], "Capabilities should contain 'environment_to_crop'"
        assert 'crop_to_environment' in health['capabilities'], "Capabilities should contain 'crop_to_environment'"
