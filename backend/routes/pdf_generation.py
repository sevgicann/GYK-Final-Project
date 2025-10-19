from flask import Blueprint, request, jsonify, send_file
import os
import sys
import logging

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pdf_llm_service import generate_crop_recommendation_pdf, generate_environment_conditions_pdf
except ImportError as e:
    print(f"Warning: Could not import pdf_llm_service: {e}")
    # Create dummy functions for testing
    def generate_crop_recommendation_pdf(*args, **kwargs):
        return {'success': False, 'message': 'PDF service not available', 'error': 'Import error'}
    
    def generate_environment_conditions_pdf(*args, **kwargs):
        return {'success': False, 'message': 'PDF service not available', 'error': 'Import error'}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pdf_generation_bp = Blueprint('pdf_generation', __name__)

@pdf_generation_bp.route('/api/pdf/generate-crop-recommendation', methods=['POST'])
def generate_crop_recommendation():
    """
    Generate PDF report for crop recommendations using LLM
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'location', 'region', 'soil_type', 'sunlight', 
            'irrigation_method', 'fertilizer_type', 'ph', 
            'nitrogen', 'phosphorus', 'potassium', 'humidity', 
            'temperature', 'rainfall', 'recommendations'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Extract data
        location = data['location']
        region = data['region']
        soil_type = data['soil_type']
        sunlight = data['sunlight']
        irrigation_method = data['irrigation_method']
        fertilizer_type = data['fertilizer_type']
        ph = float(data['ph'])
        nitrogen = float(data['nitrogen'])
        phosphorus = float(data['phosphorus'])
        potassium = float(data['potassium'])
        humidity = float(data['humidity'])
        temperature = float(data['temperature'])
        rainfall = float(data['rainfall'])
        recommendations = data['recommendations']
        
        logger.info(f"Generating crop recommendation PDF for {location}, {region}")
        logger.info(f"Recommendations: {recommendations}")
        
        # Generate PDF
        result = generate_crop_recommendation_pdf(
            location=location,
            region=region,
            soil_type=soil_type,
            sunlight=sunlight,
            irrigation_method=irrigation_method,
            fertilizer_type=fertilizer_type,
            ph=ph,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            humidity=humidity,
            temperature=temperature,
            rainfall=rainfall,
            recommendations=recommendations
        )
        
        if result['success']:
            # Return the PDF file
            filename = result['filename']
            file_path = os.path.join(os.getcwd(), filename)
            
            if os.path.exists(file_path):
                return send_file(
                    file_path,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='application/pdf'
                )
            else:
                return jsonify({
                    'success': False,
                    'message': 'PDF dosyası oluşturulamadı'
                }), 500
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in generate_crop_recommendation: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'PDF oluşturulurken hata oluştu: {str(e)}'
        }), 500


@pdf_generation_bp.route('/api/pdf/generate-environment-conditions', methods=['POST'])
def generate_environment_conditions():
    """
    Generate PDF report for environment conditions using LLM
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'crop_name', 'region', 'soil_type', 
            'irrigation_method', 'fertilizer_type', 'sunlight'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Extract data
        crop_name = data['crop_name']
        region = data['region']
        soil_type = data['soil_type']
        irrigation_method = data['irrigation_method']
        fertilizer_type = data['fertilizer_type']
        sunlight = data['sunlight']
        
        logger.info(f"Generating environment conditions PDF for {crop_name}, {region}")
        
        # Generate PDF
        result = generate_environment_conditions_pdf(
            crop_name=crop_name,
            region=region,
            soil_type=soil_type,
            irrigation_method=irrigation_method,
            fertilizer_type=fertilizer_type,
            sunlight=sunlight
        )
        
        if result['success']:
            # Return the PDF file
            filename = result['filename']
            file_path = os.path.join(os.getcwd(), filename)
            
            if os.path.exists(file_path):
                return send_file(
                    file_path,
                    as_attachment=True,
                    download_name=filename,
                    mimetype='application/pdf'
                )
            else:
                return jsonify({
                    'success': False,
                    'message': 'PDF dosyası oluşturulamadı'
                }), 500
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in generate_environment_conditions: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'PDF oluşturulurken hata oluştu: {str(e)}'
        }), 500


@pdf_generation_bp.route('/api/pdf/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for PDF generation service
    """
    return jsonify({
        'success': True,
        'message': 'PDF generation service is running',
        'status': 'healthy'
    })


@pdf_generation_bp.route('/api/pdf/test', methods=['GET'])
def test_endpoint():
    """
    Test endpoint to verify PDF service is working
    """
    try:
        return jsonify({
            'success': True,
            'message': 'PDF test endpoint is working',
            'timestamp': str(os.path.getctime(__file__))
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Test endpoint error: {str(e)}'
        }), 500