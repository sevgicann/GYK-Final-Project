from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.recommendation import Recommendation
from models.user import User
from models.product import Product
from models.environment import Environment
from app import db
from datetime import datetime
from utils.logger import log_api_call, get_logger, log_info, log_success
from utils.i18n import adapt_request, adapt_response, get_field_options, detect_language

recommendations_bp = Blueprint('recommendations', __name__)

# ML Service lazy import to avoid circular dependencies
def get_ml_service():
    """Lazy import ML service"""
    try:
        from services.ml_service import get_ml_service as _get_service
        return _get_service()
    except Exception as e:
        logger = get_logger('routes.recommendations')
        logger.error(f"Failed to import ML service: {str(e)}")
        return None

@recommendations_bp.route('/field-options', methods=['GET'])
def get_field_options_endpoint():
    """
    Get available options for categorical fields
    Query params: field (crop, region, soil_type, etc.), language (tr/en, default: tr)
    """
    try:
        field_name = request.args.get('field', 'crop')
        language = request.args.get('language', 'tr')
        
        options = get_field_options(field_name, language)
        
        return jsonify({
            'success': True,
            'data': {
                'field': field_name,
                'options': options,
                'language': language
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting field options: {str(e)}'
        }), 500

@recommendations_bp.route('/test-get', methods=['GET'])
def test_endpoint():
    """Test endpoint"""
    return jsonify({'message': 'Test endpoint works!'}), 200

@recommendations_bp.route('/test-post-simple', methods=['POST'])
def test_post_endpoint():
    """Test POST endpoint"""
    data = request.get_json()
    return jsonify({'message': 'Test POST endpoint works!', 'data': data}), 200

@recommendations_bp.route('/simple-location', methods=['POST'])
def simple_location():
    """Simple location endpoint"""
    data = request.get_json()
    return jsonify({'message': 'Simple location works!', 'data': data}), 200

@recommendations_bp.route('/location-data', methods=['POST'])
def save_location_data():
    """Save location data from user selection"""
    logger = get_logger('routes.recommendations')
    
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("No data received in location data request")
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Detailed logging of location data
        logger.info("=" * 80)
        logger.info("📍 LOCATION DATA RECEIVED:")
        logger.info(f"  Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 80)
        
        # Extract and log location information
        location_type = (data.get('location_type') or '').strip()
        city = (data.get('city') or '').strip()
        region = (data.get('region') or '').strip()
        district = (data.get('district') or '').strip()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        logger.info("🗺️ LOCATION INFORMATION:")
        logger.info(f"  Location Type: {location_type}")
        logger.info(f"  City: {city}")
        logger.info(f"  Region: {region}")
        logger.info(f"  District: {district if district else 'Not provided'}")
        if latitude and longitude:
            logger.info(f"  Coordinates: {latitude}, {longitude}")
        else:
            logger.info(f"  Coordinates: Not provided")
        
        logger.info("=" * 80)
        logger.info("✅ LOCATION DATA SAVED SUCCESSFULLY")
        logger.info("=" * 80)
        
        return jsonify({
            'success': True,
            'message': 'Konum bilgileri başarıyla kaydedildi',
            'data': {
                'location_type': location_type,
                'city': city,
                'region': region,
                'district': district,
                'latitude': latitude,
                'longitude': longitude,
                'saved_at': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error saving location data: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Konum bilgileri kaydedilirken hata oluştu',
            'error': str(e)
        }), 500

@recommendations_bp.route('/environment-data', methods=['POST'])
def save_environment_data():
    """Save environment data from user selection with i18n support"""
    logger = get_logger('routes.recommendations')
    
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("No data received in environment data request")
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Get target language for response
        target_lang = data.pop('language', 'tr')
        
        # Detect source language and adapt to canonical English
        source_lang = detect_language(data)
        canonical_data = adapt_request(data, source_lang)
        
        logger.info("=" * 80)
        logger.info("🌍 ENVIRONMENT DATA RECEIVED:")
        logger.info(f"  Source Language: {source_lang}")
        logger.info(f"  Target Language: {target_lang}")
        logger.info(f"  Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 80)
        
        # Log canonical (English) data
        logger.info("🌱 CANONICAL ENVIRONMENT DATA (EN):")
        logger.info(f"  Region: {canonical_data.get('region')}")
        logger.info(f"  Soil Type: {canonical_data.get('soil_type')}")
        logger.info(f"  Fertilizer: {canonical_data.get('fertilizer_type')}")
        logger.info(f"  Irrigation: {canonical_data.get('irrigation_method')}")
        logger.info(f"  Weather: {canonical_data.get('weather_condition')}")
        
        logger.info("=" * 80)
        logger.info("✅ ENVIRONMENT DATA PROCESSED")
        logger.info("=" * 80)
        
        # Adapt response back to target language
        response_data = adapt_response(canonical_data, target_lang)
        
        return jsonify({
            'success': True,
            'message': 'Çevre bilgileri başarıyla kaydedildi' if target_lang == 'tr' else 'Environment data saved successfully',
            'data': {
                **response_data,
                'saved_at': datetime.now().isoformat(),
                'canonical_format': canonical_data  # For debugging
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error saving environment data: {str(e)}")
        # Try to get target_lang if it exists, otherwise default to 'tr'
        target_lang = data.get('language', 'tr') if 'data' in locals() else 'tr'
        return jsonify({
            'success': False,
            'message': 'Çevre bilgileri kaydedilirken hata oluştu' if target_lang == 'tr' else 'Error saving environment data',
            'error': str(e)
        }), 500

@recommendations_bp.route('/soil-data', methods=['POST'])
def save_soil_data():
    """Save soil data from user input"""
    logger = get_logger('routes.recommendations')
    
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("No data received in soil data request")
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Detailed logging of soil data
        logger.info("=" * 80)
        logger.info("🌿 SOIL DATA RECEIVED:")
        logger.info(f"  Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 80)
        
        # Extract and log soil parameters
        ph = (data.get('ph') or '').strip()
        nitrogen = (data.get('nitrogen') or '').strip()
        phosphorus = (data.get('phosphorus') or '').strip()
        potassium = (data.get('potassium') or '').strip()
        humidity = (data.get('humidity') or '').strip()
        temperature = (data.get('temperature') or '').strip()
        rainfall = (data.get('rainfall') or '').strip()
        is_manual_entry = data.get('is_manual_entry', False)
        
        logger.info("🔧 SOIL PARAMETERS:")
        logger.info(f"  Input Method: {'Manuel Giriş' if is_manual_entry else 'Ortalama Değerler'}")
        logger.info(f"  pH: {ph}")
        logger.info(f"  Nitrogen (ppm): {nitrogen}")
        logger.info(f"  Phosphorus (ppm): {phosphorus}")
        logger.info(f"  Potassium (ppm): {potassium}")
        logger.info(f"  Humidity (%): {humidity}")
        logger.info(f"  Temperature (°C): {temperature}")
        logger.info(f"  Rainfall (mm): {rainfall}")
        
        logger.info("=" * 80)
        logger.info("✅ SOIL DATA SAVED SUCCESSFULLY")
        logger.info("=" * 80)
        
        return jsonify({
            'success': True,
            'message': 'Toprak verileri başarıyla kaydedildi',
            'data': {
                'ph': ph,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'humidity': humidity,
                'temperature': temperature,
                'rainfall': rainfall,
                'is_manual_entry': is_manual_entry,
                'saved_at': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error saving soil data: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Toprak verileri kaydedilirken hata oluştu',
            'error': str(e)
        }), 500

@recommendations_bp.route('/test-post', methods=['POST'])
def generate_recommendation():
    """Handle different types of data (location, environment, soil, recommendation)"""
    print("🎯 ROUTE FUNCTION CALLED!")
    logger = get_logger('routes.recommendations')
    logger.info("🎯 ROUTE FUNCTION CALLED!")
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Check data type
        data_type = data.get('data_type', 'recommendation')
        print(f"🔍 Processing data type: {data_type}")
        logger.info(f"🔍 Processing data type: {data_type}")
        print(f"📦 Received data: {data}")
        logger.info(f"📦 Received data: {data}")
        
        # Return debug information
        return jsonify({
            'success': True,
            'message': f'Debug: data_type={data_type}',
            'data': {
                'data_type': data_type,
                'received_data': data,
                'timestamp': datetime.now().isoformat()
            }
        }), 200
            
    except Exception as e:
        logger.error(f"Error in generate_recommendation: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'İşlem sırasında hata oluştu',
            'error': str(e)
        }), 500

def _handle_location_data(data, logger):
    """Handle location data"""
    logger.info("=" * 80)
    logger.info("📍 LOCATION DATA RECEIVED:")
    logger.info(f"  Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 80)
    
    # Extract and log location information
    location_type = (data.get('location_type') or '').strip()
    city = (data.get('city') or '').strip()
    region = (data.get('region') or '').strip()
    district = (data.get('district') or '').strip()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    logger.info("🗺️ LOCATION INFORMATION:")
    logger.info(f"  Location Type: {location_type}")
    logger.info(f"  City: {city}")
    logger.info(f"  Region: {region}")
    logger.info(f"  District: {district if district else 'Not provided'}")
    if latitude and longitude:
        logger.info(f"  Coordinates: {latitude}, {longitude}")
    else:
        logger.info(f"  Coordinates: Not provided")
    
    logger.info("=" * 80)
    logger.info("✅ LOCATION DATA SAVED SUCCESSFULLY")
    logger.info("=" * 80)
    
    return jsonify({
        'success': True,
        'message': 'Konum bilgileri başarıyla kaydedildi',
        'data': {
            'location_type': location_type,
            'city': city,
            'region': region,
            'district': district,
            'latitude': latitude,
            'longitude': longitude,
            'saved_at': datetime.now().isoformat()
        }
    }), 200

def _handle_environment_data(data, logger):
    """Handle environment data"""
    print("🚀 ENTERING _handle_environment_data function")
    logger.info("🚀 ENTERING _handle_environment_data function")
    print("=" * 80)
    logger.info("=" * 80)
    print("🌍 ENVIRONMENT DATA RECEIVED:")
    logger.info("🌍 ENVIRONMENT DATA RECEIVED:")
    print(f"  Timestamp: {datetime.now().isoformat()}")
    logger.info(f"  Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)
    logger.info("=" * 80)
    
    # Extract and log environment information
    region = (data.get('region') or '').strip()
    soil_type = (data.get('soil_type') or '').strip()
    fertilizer = (data.get('fertilizer') or '').strip()
    irrigation = (data.get('irrigation') or '').strip()
    sunlight = (data.get('sunlight') or '').strip()
    
    logger.info("🌱 ENVIRONMENT INFORMATION:")
    logger.info(f"  📍 Region: {region if region else 'NOT SELECTED'}")
    logger.info(f"  🌿 Soil Type: {soil_type if soil_type else 'NOT SELECTED'}")
    logger.info(f"  🧪 Fertilizer: {fertilizer if fertilizer else 'NOT SELECTED'}")
    logger.info(f"  💧 Irrigation Method: {irrigation if irrigation else 'NOT SELECTED'}")
    logger.info(f"  ☀️ Sunlight: {sunlight if sunlight else 'NOT SELECTED'}")
    
    # Log which specific field was changed
    changed_fields = []
    if region: changed_fields.append(f"Region → {region}")
    if soil_type: changed_fields.append(f"Soil Type → {soil_type}")
    if fertilizer: changed_fields.append(f"Fertilizer → {fertilizer}")
    if irrigation: changed_fields.append(f"Irrigation → {irrigation}")
    if sunlight: changed_fields.append(f"Sunlight → {sunlight}")
    
    if changed_fields:
        logger.info("🔄 CHANGED FIELDS:")
        for field in changed_fields:
            logger.info(f"  ✅ {field}")
    else:
        logger.info("⚠️ NO FIELDS CHANGED")
    
    logger.info("=" * 80)
    logger.info("✅ ENVIRONMENT DATA SAVED SUCCESSFULLY")
    logger.info("=" * 80)
    
    return jsonify({
        'success': True,
        'message': 'Çevre bilgileri başarıyla kaydedildi',
        'data': {
            'region': region,
            'soil_type': soil_type,
            'fertilizer': fertilizer,
            'irrigation': irrigation,
            'sunlight': sunlight,
            'saved_at': datetime.now().isoformat()
        }
    }), 200

def _handle_soil_data(data, logger):
    """Handle soil data"""
    print("🚀 ENTERING _handle_soil_data function")
    logger.info("🚀 ENTERING _handle_soil_data function")
    print("=" * 80)
    logger.info("=" * 80)
    print("🌿 SOIL DATA RECEIVED:")
    logger.info("🌿 SOIL DATA RECEIVED:")
    print(f"  Timestamp: {datetime.now().isoformat()}")
    logger.info(f"  Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)
    logger.info("=" * 80)
    
    # Extract and log soil parameters
    ph = (data.get('ph') or '').strip()
    nitrogen = (data.get('nitrogen') or '').strip()
    phosphorus = (data.get('phosphorus') or '').strip()
    potassium = (data.get('potassium') or '').strip()
    humidity = (data.get('humidity') or '').strip()
    temperature = (data.get('temperature') or '').strip()
    rainfall = (data.get('rainfall') or '').strip()
    is_manual_entry = data.get('is_manual_entry', False)
    
    logger.info("🔧 SOIL PARAMETERS:")
    logger.info(f"  📝 Input Method: {'Manuel Giriş' if is_manual_entry else 'Ortalama Değerler'}")
    logger.info(f"  🧪 pH: {ph if ph else 'NOT ENTERED'}")
    logger.info(f"  🟢 Nitrogen (ppm): {nitrogen if nitrogen else 'NOT ENTERED'}")
    logger.info(f"  🟡 Phosphorus (ppm): {phosphorus if phosphorus else 'NOT ENTERED'}")
    logger.info(f"  🟠 Potassium (ppm): {potassium if potassium else 'NOT ENTERED'}")
    logger.info(f"  💧 Humidity (%): {humidity if humidity else 'NOT ENTERED'}")
    logger.info(f"  🌡️ Temperature (°C): {temperature if temperature else 'NOT ENTERED'}")
    logger.info(f"  🌧️ Rainfall (mm): {rainfall if rainfall else 'NOT ENTERED'}")
    
    # Log which specific field was changed
    changed_fields = []
    if ph: changed_fields.append(f"pH → {ph}")
    if nitrogen: changed_fields.append(f"Nitrogen → {nitrogen}")
    if phosphorus: changed_fields.append(f"Phosphorus → {phosphorus}")
    if potassium: changed_fields.append(f"Potassium → {potassium}")
    if humidity: changed_fields.append(f"Humidity → {humidity}")
    if temperature: changed_fields.append(f"Temperature → {temperature}")
    if rainfall: changed_fields.append(f"Rainfall → {rainfall}")
    
    if changed_fields:
        logger.info("🔄 CHANGED FIELDS:")
        for field in changed_fields:
            logger.info(f"  ✅ {field}")
    else:
        logger.info("⚠️ NO FIELDS CHANGED")
    
    logger.info("=" * 80)
    logger.info("✅ SOIL DATA SAVED SUCCESSFULLY")
    logger.info("=" * 80)
    
    return jsonify({
        'success': True,
        'message': 'Toprak verileri başarıyla kaydedildi',
        'data': {
            'ph': ph,
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'humidity': humidity,
            'temperature': temperature,
            'rainfall': rainfall,
            'is_manual_entry': is_manual_entry,
            'saved_at': datetime.now().isoformat()
        }
    }), 200

def _handle_recommendation_data(data, logger):
    """Handle recommendation data (default)"""
    # Extract user input
    soil_type = data.get('soil_type', '')
    climate = data.get('climate', '')
    region = data.get('region', '')
    
    # Simple response
    return jsonify({
        'success': True,
        'message': 'Backend tarafından öneri gönderildi',
        'data': {
            'soil_type': soil_type,
            'climate': climate,
            'region': region
        }
    }), 200

@recommendations_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_recommendations():
    """Get all recommendations for the current user"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Query parameters
        status = request.args.get('status', 'active')
        recommendation_type = request.args.get('type')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = Recommendation.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if recommendation_type:
            query = query.filter_by(recommendation_type=recommendation_type)
        
        # Pagination
        recommendations = query.order_by(Recommendation.created_at.desc()).paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': [rec.to_dict() for rec in recommendations.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': recommendations.total,
                    'pages': recommendations.pages,
                    'has_next': recommendations.has_next,
                    'has_prev': recommendations.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch recommendations',
            'error': str(e)
        }), 500

@recommendations_bp.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorite_recommendations():
    """Get favorite recommendations for the current user"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        recommendations = Recommendation.get_favorite_recommendations(user_id)
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': [rec.to_dict() for rec in recommendations]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch favorite recommendations',
            'error': str(e)
        }), 500

@recommendations_bp.route('/<recommendation_id>', methods=['GET'])
@jwt_required()
def get_recommendation(recommendation_id):
    """Get a specific recommendation"""
    try:
        user_id = get_jwt_identity()
        recommendation = Recommendation.query.filter_by(
            id=recommendation_id, 
            user_id=user_id
        ).first()
        
        if not recommendation:
            return jsonify({
                'success': False,
                'message': 'Recommendation not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'recommendation': recommendation.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch recommendation',
            'error': str(e)
        }), 500

@recommendations_bp.route('/<recommendation_id>/favorite', methods=['POST'])
@jwt_required()
def toggle_favorite(recommendation_id):
    """Toggle favorite status of a recommendation"""
    try:
        user_id = get_jwt_identity()
        recommendation = Recommendation.query.filter_by(
            id=recommendation_id, 
            user_id=user_id
        ).first()
        
        if not recommendation:
            return jsonify({
                'success': False,
                'message': 'Recommendation not found'
            }), 404
        
        # Toggle favorite status
        if recommendation.is_favorite:
            recommendation.unmark_as_favorite()
            message = 'Removed from favorites'
        else:
            recommendation.mark_as_favorite()
            message = 'Added to favorites'
        
        return jsonify({
            'success': True,
            'message': message,
            'data': {
                'recommendation': recommendation.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to toggle favorite status',
            'error': str(e)
        }), 500

@recommendations_bp.route('/<recommendation_id>/dismiss', methods=['POST'])
@jwt_required()
def dismiss_recommendation(recommendation_id):
    """Dismiss a recommendation"""
    try:
        user_id = get_jwt_identity()
        recommendation = Recommendation.query.filter_by(
            id=recommendation_id, 
            user_id=user_id
        ).first()
        
        if not recommendation:
            return jsonify({
                'success': False,
                'message': 'Recommendation not found'
            }), 404
        
        recommendation.dismiss()
        
        return jsonify({
            'success': True,
            'message': 'Recommendation dismissed',
            'data': {
                'recommendation': recommendation.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to dismiss recommendation',
            'error': str(e)
        }), 500

@recommendations_bp.route('/<recommendation_id>/implement', methods=['POST'])
@jwt_required()
def implement_recommendation(recommendation_id):
    """Mark a recommendation as implemented"""
    try:
        user_id = get_jwt_identity()
        recommendation = Recommendation.query.filter_by(
            id=recommendation_id, 
            user_id=user_id
        ).first()
        
        if not recommendation:
            return jsonify({
                'success': False,
                'message': 'Recommendation not found'
            }), 404
        
        recommendation.implement()
        
        return jsonify({
            'success': True,
            'message': 'Recommendation marked as implemented',
            'data': {
                'recommendation': recommendation.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to implement recommendation',
            'error': str(e)
        }), 500

@recommendations_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_recommendations():
    """Generate new recommendations based on user's environment and preferences"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        recommendation_type = data.get('type', 'product_to_environment')  # or 'environment_to_product'
        environment_id = data.get('environment_id')
        product_id = data.get('product_id')
        
        if recommendation_type == 'product_to_environment' and not product_id:
            return jsonify({
                'success': False,
                'message': 'Product ID is required for product-to-environment recommendations'
            }), 400
        
        if recommendation_type == 'environment_to_product' and not environment_id:
            return jsonify({
                'success': False,
                'message': 'Environment ID is required for environment-to-product recommendations'
            }), 400
        
        generated_recommendations = []
        
        if recommendation_type == 'product_to_environment':
            # Generate recommendations for where to grow a specific product
            product = Product.query.get(product_id)
            if not product:
                return jsonify({
                    'success': False,
                    'message': 'Product not found'
                }), 404
            
            # Get user's environments
            environments = Environment.get_user_environments(user_id)
            
            for environment in environments:
                latest_data = EnvironmentData.get_latest_data(environment.id)
                if latest_data and product.requirements:
                    suitable, issues = product.requirements.is_suitable_for_environment(latest_data)
                    
                    # Calculate scores
                    suitability_score = 1.0 if suitable else 0.5
                    confidence_score = 0.8 if suitable else 0.3
                    
                    # Create recommendation
                    recommendation = Recommendation(
                        user_id=user_id,
                        product_id=product_id,
                        environment_id=environment.id,
                        recommendation_type=recommendation_type,
                        confidence_score=confidence_score,
                        suitability_score=suitability_score,
                        title=f"Grow {product.name} in {environment.name}",
                        description=f"Based on your environment data, {product.name} is {'suitable' if suitable else 'partially suitable'} for growing in {environment.name}.",
                        benefits=f"Growing {product.name} in this environment can provide good yields with proper care.",
                        challenges=", ".join(issues) if issues else "No major challenges identified.",
                        suggestions=f"Ensure proper soil preparation and follow recommended growing practices for {product.name}."
                    )
                    
                    db.session.add(recommendation)
                    generated_recommendations.append(recommendation)
        
        elif recommendation_type == 'environment_to_product':
            # Generate recommendations for what to grow in a specific environment
            environment = Environment.query.filter_by(
                id=environment_id, 
                user_id=user_id, 
                is_active=True
            ).first()
            
            if not environment:
                return jsonify({
                    'success': False,
                    'message': 'Environment not found'
                }), 404
            
            latest_data = EnvironmentData.get_latest_data(environment_id)
            if not latest_data:
                return jsonify({
                    'success': False,
                    'message': 'No environment data found for this environment'
                }), 400
            
            # Get all products
            products = Product.query.filter_by(is_active=True).all()
            
            for product in products:
                if product.requirements:
                    suitable, issues = product.requirements.is_suitable_for_environment(latest_data)
                    
                    # Calculate scores
                    suitability_score = 1.0 if suitable else 0.5
                    confidence_score = 0.8 if suitable else 0.3
                    
                    # Create recommendation
                    recommendation = Recommendation(
                        user_id=user_id,
                        product_id=product.id,
                        environment_id=environment_id,
                        recommendation_type=recommendation_type,
                        confidence_score=confidence_score,
                        suitability_score=suitability_score,
                        title=f"Grow {product.name} in {environment.name}",
                        description=f"Based on your environment data, {product.name} is {'highly suitable' if suitable else 'moderately suitable'} for growing in {environment.name}.",
                        benefits=f"Growing {product.name} can be beneficial in this environment with proper care and attention.",
                        challenges=", ".join(issues) if issues else "No major challenges identified.",
                        suggestions=f"Follow recommended growing practices for {product.name} and monitor environmental conditions regularly."
                    )
                    
                    db.session.add(recommendation)
                    generated_recommendations.append(recommendation)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Generated {len(generated_recommendations)} recommendations',
            'data': {
                'recommendations': [rec.to_dict() for rec in generated_recommendations]
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to generate recommendations',
            'error': str(e)
        }), 500

@recommendations_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_recommendation_stats():
    """Get recommendation statistics for the current user"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Get statistics
        total_recommendations = Recommendation.query.filter_by(user_id=user_id).count()
        active_recommendations = Recommendation.query.filter_by(user_id=user_id, status='active').count()
        favorite_recommendations = Recommendation.query.filter_by(user_id=user_id, is_favorite=True).count()
        implemented_recommendations = Recommendation.query.filter_by(user_id=user_id, status='implemented').count()
        dismissed_recommendations = Recommendation.query.filter_by(user_id=user_id, status='dismissed').count()
        
        # Get recommendations by type
        product_to_env = Recommendation.query.filter_by(
            user_id=user_id, 
            recommendation_type='product_to_environment'
        ).count()
        
        env_to_product = Recommendation.query.filter_by(
            user_id=user_id, 
            recommendation_type='environment_to_product'
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_recommendations': total_recommendations,
                'active_recommendations': active_recommendations,
                'favorite_recommendations': favorite_recommendations,
                'implemented_recommendations': implemented_recommendations,
                'dismissed_recommendations': dismissed_recommendations,
                'by_type': {
                    'product_to_environment': product_to_env,
                    'environment_to_product': env_to_product
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch recommendation statistics',
            'error': str(e)
        }), 500
    """
    Predict best crop for given environmental conditions
    
    Request body (Turkish or English):
    {
        "region": "Marmara" / "Marmara",
        "soil_type": "Killi Toprak" / "Clay",
        "soil_ph": 6.5,
        "nitrogen": 90,
        "phosphorus": 42,
        "potassium": 43,
        "moisture": 65,
        "temperature_celsius": 25,
        "rainfall_mm": 600,
        "fertilizer_type": "Amonyum Sülfat" / "Ammonium Sulphate",
        "irrigation_method": "Damla Sulama" / "Drip Irrigation",
        "weather_condition": "Güneşli" / "sunny",
        "use_synthetic": true,  // Optional, default: true
        "language": "tr"  // Optional, for response language
    }
    """
    logger = get_logger('routes.recommendations')
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Extract preferences
        target_lang = data.pop('language', 'tr')
        use_synthetic = data.pop('use_synthetic', True)
        
        # Detect source language and adapt to canonical English
        source_lang = detect_language(data)
        canonical_data = adapt_request(data, source_lang)
        
        logger.info("=" * 80)
        logger.info("🤖 ML CROP PREDICTION REQUEST:")
        logger.info(f"  Source Language: {source_lang}")
        logger.info(f"  Model Type: {'Synthetic (LightGBM)' if use_synthetic else 'XGBoost'}")
        logger.info("=" * 80)
        logger.info("🌱 CANONICAL INPUT DATA (EN):")
        for key, value in canonical_data.items():
            logger.info(f"  {key}: {value}")
        logger.info("=" * 80)
        
        # Get ML service
        ml_service = get_ml_service()
        if not ml_service:
            return jsonify({
                'success': False,
                'message': 'ML service not available'
            }), 503
        
        # Make prediction
        prediction_result = ml_service.predict_crop(canonical_data, use_synthetic=use_synthetic)
        
        if not prediction_result.get('success'):
            logger.error(f"Prediction failed: {prediction_result.get('error')}")
            return jsonify(prediction_result), 500
        
        # Log result
        predicted_crop = prediction_result.get('crop')
        confidence = prediction_result.get('confidence')
        
        logger.info("✅ PREDICTION RESULT:")
        logger.info(f"  Predicted Crop: {predicted_crop}")
        if confidence:
            logger.info(f"  Confidence: {confidence:.2%}")
        logger.info("=" * 80)
        
        # Adapt response to target language
        response_data = adapt_response(prediction_result, target_lang)
        
        return jsonify({
            'success': True,
            'data': response_data,
            'metadata': {
                'model_type': 'synthetic' if use_synthetic else 'xgboost',
                'language': target_lang
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Crop prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Crop prediction failed',
            'error': str(e)
        }), 500


@recommendations_bp.route('/predict-crop-probabilities', methods=['POST'])
def predict_crop_probabilities():
    """
    Get prediction probabilities for all crops
    Same input format as /predict-crop
    Returns top 3 crops with probabilities
    """
    logger = get_logger('routes.recommendations')
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Extract preferences
        target_lang = data.pop('language', 'tr')
        use_synthetic = data.pop('use_synthetic', True)
        
        # Detect source language and adapt to canonical English
        source_lang = detect_language(data)
        canonical_data = adapt_request(data, source_lang)
        
        logger.info("🤖 ML PROBABILITY PREDICTION REQUEST")
        
        # Get ML service
        ml_service = get_ml_service()
        if not ml_service:
            return jsonify({
                'success': False,
                'message': 'ML service not available'
            }), 503
        
        # Get probabilities
        prob_result = ml_service.get_crop_probabilities(canonical_data, use_synthetic=use_synthetic)
        
        if not prob_result.get('success'):
            logger.error(f"Probability prediction failed: {prob_result.get('error')}")
            return jsonify(prob_result), 500
        
        # Log top 3
        top_3 = prob_result.get('top_3', [])
        logger.info("✅ TOP 3 PREDICTIONS:")
        for i, (crop, prob) in enumerate(top_3, 1):
            logger.info(f"  {i}. {crop}: {prob:.2%}")
        
        # Adapt response to target language
        response_data = adapt_response(prob_result, target_lang)
        
        return jsonify({
            'success': True,
            'data': response_data,
            'metadata': {
                'model_type': 'synthetic' if use_synthetic else 'xgboost',
                'language': target_lang
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Probability prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Probability prediction failed',
            'error': str(e)
        }), 500


@recommendations_bp.route('/optimize-conditions', methods=['POST'])
def optimize_conditions():
    """
    Find optimal environmental conditions for a target crop
    
    Request body (Turkish or English):
    {
        "crop": "buğday" / "wheat",
        "region": "Marmara" / "Marmara",
        "language": "tr"  // Optional
    }
    
    Returns optimal values for all environmental parameters
    """
    logger = get_logger('routes.recommendations')
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Extract parameters
        target_lang = data.pop('language', 'tr')
        
        # Detect source language and adapt
        source_lang = detect_language(data)
        canonical_data = adapt_request(data, source_lang)
        
        target_crop = canonical_data.get('crop')
        target_region = canonical_data.get('region')
        
        if not target_crop or not target_region:
            return jsonify({
                'success': False,
                'message': 'Both crop and region are required'
            }), 400
        
        logger.info("=" * 80)
        logger.info("🔍 ML OPTIMIZATION REQUEST:")
        logger.info(f"  Target Crop: {target_crop}")
        logger.info(f"  Target Region: {target_region}")
        logger.info("=" * 80)
        
        # Get ML service
        ml_service = get_ml_service()
        if not ml_service:
            return jsonify({
                'success': False,
                'message': 'ML service not available'
            }), 503
        
        # Run optimization
        optimization_result = ml_service.optimize_for_crop(target_crop, target_region)
        
        if not optimization_result.get('success'):
            logger.error(f"Optimization failed: {optimization_result.get('error')}")
            return jsonify(optimization_result), 500
        
        # Log result
        optimal_conditions = optimization_result.get('optimal_conditions', {})
        probability = optimization_result.get('probability', 0)
        
        logger.info("✅ OPTIMAL CONDITIONS FOUND:")
        logger.info(f"  Success Probability: {probability}%")
        logger.info("  Recommended Parameters:")
        for param, value in optimal_conditions.items():
            logger.info(f"    {param}: {value}")
        logger.info("=" * 80)
        
        # Adapt response to target language
        response_data = adapt_response(optimization_result, target_lang)
        
        return jsonify({
            'success': True,
            'data': response_data,
            'metadata': {
                'language': target_lang
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Optimization error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Optimization failed',
            'error': str(e)
        }), 500


@recommendations_bp.route('/ml-health', methods=['GET'])
def ml_health_check():
    """Check ML service health and available models"""
    logger = get_logger('routes.recommendations')
    
    try:
        ml_service = get_ml_service()
        
        if not ml_service:
            return jsonify({
                'success': False,
                'status': 'unavailable',
                'message': 'ML service not initialized'
            }), 503
        
        health_status = ml_service.health_check()
        
        logger.info(f"ML Service Health Check: {health_status}")
        
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
