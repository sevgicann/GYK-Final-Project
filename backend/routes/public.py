from flask import Blueprint, request, jsonify
from models.average_soil_data import AverageSoilData
from datetime import datetime
from utils.logger import log_api_call, get_logger

public_bp = Blueprint('public', __name__)

@public_bp.route('/average-soil-data', methods=['GET'])
@log_api_call
def get_average_soil_data():
    """Get average soil data based on environmental conditions"""
    logger = get_logger('routes.public')
    
    try:
        # Get query parameters
        soil_type = request.args.get('soil_type')
        region = request.args.get('region')
        fertilizer_type = request.args.get('fertilizer_type')
        irrigation_method = request.args.get('irrigation_method')
        weather_condition = request.args.get('weather_condition')
        
        logger.info("=" * 60)
        logger.info("🌱 AVERAGE SOIL DATA REQUEST:")
        logger.info(f"  Soil Type: {soil_type}")
        logger.info(f"  Region: {region}")
        logger.info(f"  Fertilizer Type: {fertilizer_type}")
        logger.info(f"  Irrigation Method: {irrigation_method}")
        logger.info(f"  Weather Condition: {weather_condition}")
        logger.info(f"  Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # Get average soil data with fallback logic
        average_data = AverageSoilData.get_best_match(
            soil_type=soil_type,
            region=region,
            fertilizer_type=fertilizer_type,
            irrigation_method=irrigation_method,
            weather_condition=weather_condition
        )
        
        if average_data:
            logger.info(f"Found average soil data: {average_data.region}-{average_data.soil_type}")
            
            return jsonify({
                'success': True,
                'data': average_data.to_dict(),
                'message': 'Average soil data retrieved successfully'
            }), 200
        else:
            # Return default values if no match found
            logger.warning("No matching average soil data found, returning defaults")
            default_values = AverageSoilData.get_default_averages()
            
            return jsonify({
                'success': True,
                'data': {
                    'environmental_conditions': {
                        'soil_type': soil_type,
                        'region': region,
                        'fertilizer_type': fertilizer_type,
                        'irrigation_method': irrigation_method,
                        'weather_condition': weather_condition
                    },
                    'average_values': default_values,
                    'metadata': {
                        'data_count': 0,
                        'is_default': True,
                        'last_updated': datetime.utcnow().isoformat()
                    }
                },
                'message': 'Using default average values (no specific match found)'
            }), 200
            
    except Exception as e:
        logger.error(f"Error getting average soil data: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve average soil data',
            'error': str(e)
        }), 500

@public_bp.route('/average-soil-data/all', methods=['GET'])
@log_api_call
def get_all_average_soil_data():
    """Get all available average soil data combinations"""
    logger = get_logger('routes.public')
    
    try:
        # Get all average soil data
        all_data = AverageSoilData.query.all()
        
        logger.info(f"Retrieved {len(all_data)} average soil data records")
        
        return jsonify({
            'success': True,
            'data': [record.to_dict() for record in all_data],
            'count': len(all_data),
            'message': 'All average soil data retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting all average soil data: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to retrieve all average soil data',
            'error': str(e)
        }), 500

@public_bp.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint without authentication"""
    return jsonify({
        'success': True,
        'message': 'Test endpoint working'
    }), 200
