"""
ML Prediction Endpoints - Bi-directional Crop Recommendations
Provides API endpoints for:
1. Environment → Crop predictions
2. Crop → Environment optimization
"""
from flask import Blueprint, request, jsonify
from utils.logger import get_logger
from utils.i18n import adapt_request, adapt_response, detect_language

logger = get_logger(__name__)

# Create ML blueprint
ml_bp = Blueprint('ml', __name__)


# ML Service lazy import
def get_ml_service():
    """Lazy import ML service to avoid circular dependencies"""
    try:
        from services.ml_service import get_ml_service as _get_service
        return _get_service()
    except Exception as e:
        logger.error(f"Failed to import ML service: {str(e)}")
        return None


@ml_bp.route('/health', methods=['GET'])
def ml_health_check():
    """
    Check ML service health and available models
    
    GET /api/ml/health
    
    Response:
    {
        "success": true,
        "data": {
            "status": "healthy",
            "models": {"xgboost": true, "lightgbm": true},
            "default_model": "lightgbm",
            "capabilities": {...}
        }
    }
    """
    try:
        ml_service = get_ml_service()
        
        if not ml_service:
            return jsonify({
                'success': False,
                'status': 'unavailable',
                'message': 'ML service not initialized'
            }), 503
        
        health_status = ml_service.health_check()
        
        return jsonify({
            'success': True,
            'data': health_status
        }), 200
        
    except Exception as e:
        logger.error(f"ML health check error: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e)
        }), 500


@ml_bp.route('/predict-crop', methods=['POST'])
def predict_crop_from_environment():
    """
    Predict best crop from environmental conditions
    Direction: Environment → Crop
    
    POST /api/ml/predict-crop
    
    Request body (Turkish or English):
    {
        "region": "Marmara",
        "soil_type": "Killi Toprak",
        "soil_ph": 6.5,
        "nitrogen": 90,
        "phosphorus": 42,
        "potassium": 43,
        "moisture": 65,
        "temperature_celsius": 25,
        "rainfall_mm": 600,
        "fertilizer_type": "Amonyum Sülfat",
        "irrigation_method": "Damla Sulama",
        "weather_condition": "Güneşli",
        "model_type": "lightgbm",  // Optional: "xgboost" or "lightgbm"
        "language": "tr"  // Optional: for response translation
    }
    
    Response:
    {
        "success": true,
        "data": {
            "predicted_crop": "corn",
            "confidence": 0.85,
            "top_3_predictions": [
                ["corn", 0.85],
                ["wheat", 0.10],
                ["rice", 0.05]
            ],
            "model_used": "lightgbm",
            "direction": "environment_to_crop"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Extract preferences
        target_lang = data.pop('language', 'tr')
        model_type = data.pop('model_type', None)
        
        # Detect source language and adapt to canonical English
        source_lang = detect_language(data)
        canonical_data = adapt_request(data, source_lang)
        
        logger.info("=" * 80)
        logger.info("🌾 ML CROP PREDICTION REQUEST (Environment → Crop)")
        logger.info(f"  Source Language: {source_lang}")
        logger.info(f"  Model: {model_type or 'default (lightgbm)'}")
        logger.info("  Input Features:")
        for key, value in canonical_data.items():
            logger.info(f"    {key}: {value}")
        logger.info("=" * 80)
        
        # Get ML service
        ml_service = get_ml_service()
        if not ml_service:
            return jsonify({
                'success': False,
                'message': 'ML service not available'
            }), 503
        
        # Make prediction
        prediction_result = ml_service.predict_crop_from_environment(
            canonical_data,
            model_type=model_type
        )
        
        if not prediction_result.get('success'):
            logger.error(f"Prediction failed: {prediction_result.get('error')}")
            return jsonify(prediction_result), 500
        
        # Log result
        predicted_crop = prediction_result.get('predicted_crop')
        confidence = prediction_result.get('confidence')
        
        logger.info("✅ PREDICTION RESULT:")
        logger.info(f"  Predicted Crop: {predicted_crop}")
        logger.info(f"  Confidence: {confidence:.2%}")
        logger.info(f"  Model Used: {prediction_result.get('model_used')}")
        logger.info("=" * 80)
        
        # Adapt response to target language
        response_data = adapt_response(prediction_result, target_lang)
        
        return jsonify({
            'success': True,
            'data': response_data
        }), 200
        
    except Exception as e:
        logger.error(f"Crop prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Crop prediction failed',
            'error': str(e)
        }), 500


@ml_bp.route('/optimize-environment', methods=['POST'])
def predict_environment_from_crop():
    """
    Predict optimal environmental conditions for a target crop
    Direction: Crop → Environment
    
    POST /api/ml/optimize-environment
    
    Request body (Turkish or English):
    {
        "crop": "buğday",  // or "wheat"
        "region": "Marmara",
        "model_type": "lightgbm",  // Optional: "xgboost" or "lightgbm"
        "language": "tr"  // Optional: for response translation
    }
    
    Response:
    {
        "success": true,
        "data": {
            "crop": "wheat",
            "region": "Marmara",
            "optimal_conditions": {
                "soil_ph": 6.8,
                "nitrogen": 120,
                "phosphorus": 45,
                "potassium": 50,
                "moisture": 65,
                "temperature_celsius": 22,
                "rainfall_mm": 800,
                "soil_type": "Loamy",
                "fertilizer_type": "Nitrogenous",
                "irrigation_method": "Drip Irrigation",
                "weather_condition": "Sunny"
            },
            "success_probability": 92.5,
            "model_used": "lightgbm",
            "direction": "crop_to_environment"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Extract preferences
        target_lang = data.pop('language', 'tr')
        model_type = data.pop('model_type', None)
        
        # Detect source language and adapt
        source_lang = detect_language(data)
        canonical_data = adapt_request(data, source_lang)
        
        crop = canonical_data.get('crop')
        region = canonical_data.get('region')
        
        if not crop or not region:
            return jsonify({
                'success': False,
                'message': 'Both crop and region are required'
            }), 400
        
        logger.info("=" * 80)
        logger.info("🔍 ML ENVIRONMENT OPTIMIZATION REQUEST (Crop → Environment)")
        logger.info(f"  Target Crop: {crop}")
        logger.info(f"  Target Region: {region}")
        logger.info(f"  Model: {model_type or 'default (lightgbm)'}")
        logger.info("=" * 80)
        
        # Get ML service
        ml_service = get_ml_service()
        if not ml_service:
            return jsonify({
                'success': False,
                'message': 'ML service not available'
            }), 503
        
        # Run optimization
        optimization_result = ml_service.predict_environment_from_crop(
            crop,
            region,
            model_type=model_type
        )
        
        if not optimization_result.get('success'):
            logger.error(f"Optimization failed: {optimization_result.get('error')}")
            return jsonify(optimization_result), 500
        
        # Log result
        optimal_conditions = optimization_result.get('optimal_conditions', {})
        probability = optimization_result.get('success_probability', 0)
        
        logger.info("✅ OPTIMIZATION RESULT:")
        logger.info(f"  Success Probability: {probability:.2f}%")
        logger.info(f"  Model Used: {optimization_result.get('model_used')}")
        logger.info("  Optimal Conditions:")
        for param, value in optimal_conditions.items():
            logger.info(f"    {param}: {value}")
        logger.info("=" * 80)
        
        # Adapt response to target language
        response_data = adapt_response(optimization_result, target_lang)
        
        return jsonify({
            'success': True,
            'data': response_data
        }), 200
        
    except Exception as e:
        logger.error(f"Environment optimization error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Environment optimization failed',
            'error': str(e)
        }), 500


@ml_bp.route('/model-info', methods=['GET'])
def get_model_info():
    """
    Get information about available ML models
    
    GET /api/ml/model-info?model_type=lightgbm
    
    Query params:
    - model_type: Optional, 'xgboost' or 'lightgbm'
    
    Response:
    {
        "success": true,
        "data": {
            "status": "loaded",
            "model_type": "LightGBM",
            "algorithm": "Gradient Boosting Decision Tree",
            "features": {...},
            "crops": [...],
            "capabilities": [...]
        }
    }
    """
    try:
        model_type = request.args.get('model_type')
        
        ml_service = get_ml_service()
        if not ml_service:
            return jsonify({
                'success': False,
                'message': 'ML service not available'
            }), 503
        
        model_info = ml_service.get_model_info(model_type)
        
        return jsonify({
            'success': True,
            'data': model_info
        }), 200
        
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

