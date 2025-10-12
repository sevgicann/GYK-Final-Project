from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.logger import log_api_call, get_logger, log_info, log_success
from datetime import datetime

product_selection_bp = Blueprint('product_selection', __name__)

@product_selection_bp.route('/select-product', methods=['POST'])
@jwt_required()
@log_api_call
def select_product():
    """Handle product selection from frontend"""
    logger = get_logger('routes.product_selection')
    
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("No data received in product selection request")
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Extract product information
        product_name = (data.get('product_name') or '').strip()
        product_id = data.get('product_id', '') or ''
        product_category = data.get('product_category', '') or ''
        product_description = data.get('product_description', '') or ''
        
        # Detailed logging of product selection
        logger.info("=" * 60)
        logger.info("🌱 PRODUCT SELECTION REQUEST:")
        logger.info(f"  Product Information:")
        logger.info(f"    - Name: {product_name}")
        logger.info(f"    - ID: {product_id}")
        logger.info(f"    - Category: {product_category}")
        logger.info(f"    - Description: {product_description}")
        logger.info(f"  Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # Validation
        if not product_name:
            logger.warning("Product name is empty")
            return jsonify({
                'success': False,
                'message': 'Product name is required'
            }), 400
        
        # Here you can add business logic for product selection
        # For example, store in database, analyze requirements, etc.
        
        # Mock response for now
        response_data = {
            'selected_product': {
                'name': product_name,
                'id': product_id,
                'category': product_category,
                'description': product_description,
                'selected_at': datetime.now().isoformat()
            },
            'recommendations': {
                'suitable_regions': ['Ege', 'Akdeniz', 'Marmara'],
                'suitable_climate': 'Sıcak ve nemli iklim',
                'soil_requirements': 'pH 6.0-7.0, iyi drenaj',
                'season': 'İlkbahar-Yaz'
            }
        }
        
        # Log successful product selection
        logger.info("=" * 60)
        logger.info("✅ PRODUCT SELECTION SUCCESSFUL:")
        logger.info(f"  Selected Product: {product_name}")
        logger.info(f"  Category: {product_category}")
        logger.info(f"  Selection Time: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        return jsonify({
            'success': True,
            'message': 'Product selected successfully',
            'data': response_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error in product selection: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Product selection failed',
            'error': str(e)
        }), 500

@product_selection_bp.route('/select-location', methods=['POST'])
@jwt_required()
@log_api_call
def select_location():
    """Handle location selection from frontend (GPS or Manual)"""
    logger = get_logger('routes.product_selection')
    
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("No data received in location selection request")
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Extract location information with proper null handling
        logger.info(f"DEBUG: Raw data received: {data}")
        
        location_type = data.get('location_type', '').strip() if data.get('location_type') else ''
        logger.info(f"DEBUG: location_type = {location_type}")
        
        # Extract city and region (required for both GPS and manual)
        city = data.get('city', '').strip() if data.get('city') else ''
        region = data.get('region', '').strip() if data.get('region') else ''
        climate_zone = data.get('climate_zone', '').strip() if data.get('climate_zone') else ''
        
        # Extract coordinates (only for GPS)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Extract district (optional for both)
        district = data.get('district', '').strip() if data.get('district') else ''
        
        logger.info(f"DEBUG: Processed values - city: {city}, region: {region}, district: {district}")
        logger.info(f"DEBUG: GPS coordinates - lat: {latitude}, lon: {longitude}")
        logger.info(f"DEBUG: Location type: {location_type}")
        
        # Detailed logging of location selection
        logger.info("=" * 60)
        logger.info("📍 LOCATION SELECTION REQUEST:")
        logger.info(f"  Location Type: {location_type.upper() if location_type else 'UNKNOWN'}")
        logger.info(f"  City: {city}")
        logger.info(f"  Region: {region}")
        logger.info(f"  District: {district if district else 'Not provided'}")
        logger.info(f"  Climate Zone: {climate_zone if climate_zone else 'Not provided'}")
        if latitude and longitude:
            logger.info(f"  Coordinates: {latitude}, {longitude}")
        else:
            logger.info(f"  Coordinates: Not provided")
        logger.info(f"  Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # Validation based on location type
        if not location_type or location_type not in ['gps', 'manual']:
            logger.warning("Invalid location type provided")
            return jsonify({
                'success': False,
                'message': 'Location type must be either "gps" or "manual"'
            }), 400
        
        # Basic validation - city and region are required for both types
        if not city or not region:
            logger.warning("City or region is missing")
            return jsonify({
                'success': False,
                'message': 'City and region are required'
            }), 400
        
        # GPS-specific validation
        if location_type == 'gps':
            if latitude is None or longitude is None:
                logger.warning("GPS coordinates are missing")
                return jsonify({
                    'success': False,
                    'message': 'GPS coordinates (latitude and longitude) are required for GPS location type'
                }), 400
            logger.info(f"GPS location validated: {city}, {region} at ({latitude}, {longitude})")
        else:
            # Manual location - coordinates should be null
            if latitude is not None or longitude is not None:
                logger.warning("Manual location should not have GPS coordinates")
                # Don't fail, just log warning and clear coordinates
                latitude = None
                longitude = None
            logger.info(f"Manual location validated: {city}, {region}")
        
        # Here you can add business logic for location selection
        # For example, validate coordinates, check climate data, etc.
        
        # Create response based on location type
        response_data = {
            'selected_location': {
                'type': location_type,
                'city': city,
                'region': region,
                'district': district if district else None,
                'climate_zone': climate_zone if climate_zone else None,
                'selected_at': datetime.now().isoformat()
            },
            'location_analysis': {
                'climate_type': f'{region} iklimi',
                'growing_season': 'Mart-Ekim',
                'average_temperature': '18-25°C',
                'humidity_level': 'Orta-Yüksek',
                'soil_types': ['Tınlı', 'Kumlu-Tınlı']
            }
        }
        
        # Add coordinates only for GPS location type
        if location_type == 'gps':
            response_data['selected_location']['coordinates'] = {
                'latitude': latitude,
                'longitude': longitude
            }
            response_data['location_analysis']['gps_precision'] = 'Yüksek hassasiyet'
        else:
            response_data['location_analysis']['location_method'] = 'Manuel seçim'
        
        # Log successful location selection
        logger.info("=" * 60)
        logger.info("✅ LOCATION SELECTION SUCCESSFUL:")
        logger.info(f"  Location Type: {location_type.upper()}")
        logger.info(f"  Selected City: {city}")
        logger.info(f"  Selected Region: {region}")
        logger.info(f"  Selection Time: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        return jsonify({
            'success': True,
            'message': 'Location selected successfully',
            'data': response_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error in location selection: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Location selection failed',
            'error': str(e)
        }), 500

@product_selection_bp.route('/get-environment-recommendations', methods=['POST'])
@jwt_required()
@log_api_call
def get_environment_recommendations():
    """Get environment recommendations based on selected product and location"""
    logger = get_logger('routes.product_selection')
    
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("No data received in environment recommendations request")
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Extract product and location data
        product_name = (data.get('product_name') or '').strip()
        city = (data.get('city') or '').strip()
        region = (data.get('region') or '').strip()
        location_type = data.get('location_type', 'manual') or 'manual'
        
        # Detailed logging of recommendation request
        logger.info("=" * 60)
        logger.info("🌍 ENVIRONMENT RECOMMENDATIONS REQUEST:")
        logger.info(f"  Product: {product_name}")
        logger.info(f"  Location: {city}, {region}")
        logger.info(f"  Location Type: {location_type}")
        logger.info(f"  Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # Validation
        if not product_name or not city or not region:
            logger.warning("Missing required data for recommendations")
            return jsonify({
                'success': False,
                'message': 'Product name, city, and region are required'
            }), 400
        
        # Here you can add your recommendation algorithm
        # For now, return mock recommendations based on product and location
        
        recommendations = {
            'soil_recommendations': {
                'ph_level': '6.0-7.0',
                'soil_type': 'Tınlı toprak',
                'drainage': 'İyi drenaj gerekli',
                'organic_matter': 'Yüksek organik madde'
            },
            'environmental_conditions': {
                'temperature': '18-25°C',
                'humidity': '60-80%',
                'sunlight': 'Günde 6-8 saat',
                'rainfall': 'Aylık 100-150mm'
            },
            'farming_practices': {
                'irrigation': 'Damla sulama önerilir',
                'fertilizer': 'Organik gübre kullanın',
                'planting_season': 'İlkbahar (Mart-Nisan)',
                'harvest_time': 'Yaz sonu (Ağustos-Eylül)'
            },
            'regional_adaptations': {
                'climate_considerations': f'{region} bölgesi için özel öneriler',
                'local_pests': 'Bölgesel zararlı kontrolü gerekli',
                'weather_protection': 'Geç don riski için koruma önlemleri'
            }
        }
        
        # Log successful recommendations generation
        logger.info("=" * 60)
        logger.info("✅ ENVIRONMENT RECOMMENDATIONS GENERATED:")
        logger.info(f"  Product: {product_name}")
        logger.info(f"  Location: {city}, {region}")
        logger.info(f"  Recommendations Generated: {len(recommendations)} categories")
        logger.info(f"  Generation Time: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        return jsonify({
            'success': True,
            'message': 'Environment recommendations generated successfully',
            'data': {
                'product': product_name,
                'location': f"{city}, {region}",
                'recommendations': recommendations,
                'generated_at': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating environment recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to generate environment recommendations',
            'error': str(e)
        }), 500
