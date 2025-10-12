from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.environment import Environment, EnvironmentData
from models.user import User
from app import db
from datetime import datetime

environments_bp = Blueprint('environments', __name__)

@environments_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_environments():
    """Get all environments for the current user"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        environments = Environment.get_user_environments(user_id)
        
        return jsonify({
            'success': True,
            'data': {
                'environments': [env.to_dict() for env in environments]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch environments',
            'error': str(e)
        }), 500

@environments_bp.route('/', methods=['POST'])
@jwt_required()
def create_environment():
    """Create a new environment"""
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
                'message': 'Environment data is required'
            }), 400
        
        # Validate required fields
        name = data.get('name', '').strip()
        if not name:
            return jsonify({
                'success': False,
                'message': 'Environment name is required'
            }), 400
        
        # Create environment
        environment = Environment(
            user_id=user_id,
            name=name,
            location_type=data.get('location_type', 'manual'),
            city=data.get('city', '').strip(),
            district=data.get('district', '').strip(),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        
        db.session.add(environment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Environment created successfully',
            'data': {
                'environment': environment.to_dict()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to create environment',
            'error': str(e)
        }), 500

@environments_bp.route('/<environment_id>', methods=['GET'])
@jwt_required()
def get_environment(environment_id):
    """Get a specific environment"""
    try:
        user_id = get_jwt_identity()
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
        
        return jsonify({
            'success': True,
            'data': {
                'environment': environment.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch environment',
            'error': str(e)
        }), 500

@environments_bp.route('/<environment_id>', methods=['PUT'])
@jwt_required()
def update_environment(environment_id):
    """Update an environment"""
    try:
        user_id = get_jwt_identity()
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
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Environment data is required'
            }), 400
        
        # Update fields
        if 'name' in data:
            environment.name = data['name'].strip()
        
        if 'location_type' in data:
            environment.location_type = data['location_type']
        
        if 'city' in data:
            environment.city = data['city'].strip()
        
        if 'district' in data:
            environment.district = data['district'].strip()
        
        if 'latitude' in data:
            environment.latitude = data['latitude']
        
        if 'longitude' in data:
            environment.longitude = data['longitude']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Environment updated successfully',
            'data': {
                'environment': environment.to_dict()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update environment',
            'error': str(e)
        }), 500

@environments_bp.route('/<environment_id>', methods=['DELETE'])
@jwt_required()
def delete_environment(environment_id):
    """Delete an environment"""
    try:
        user_id = get_jwt_identity()
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
        
        # Soft delete
        environment.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Environment deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to delete environment',
            'error': str(e)
        }), 500

@environments_bp.route('/<environment_id>/data', methods=['POST'])
@jwt_required()
def add_environment_data(environment_id):
    """Add environment data to an environment"""
    try:
        user_id = get_jwt_identity()
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
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Environment data is required'
            }), 400
        
        # Create environment data
        env_data = EnvironmentData(
            environment_id=environment_id,
            ph=data.get('ph'),
            nitrogen=data.get('nitrogen'),
            phosphorus=data.get('phosphorus'),
            potassium=data.get('potassium'),
            organic_matter=data.get('organic_matter'),
            soil_type=data.get('soil_type'),
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            rainfall=data.get('rainfall'),
            sunlight_hours=data.get('sunlight_hours'),
            wind_speed=data.get('wind_speed'),
            altitude=data.get('altitude'),
            slope=data.get('slope'),
            drainage=data.get('drainage'),
            data_source=data.get('data_source', 'manual'),
            measured_at=datetime.fromisoformat(data.get('measured_at', datetime.utcnow().isoformat()))
        )
        
        db.session.add(env_data)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Environment data added successfully',
            'data': {
                'environment_data': env_data.to_dict()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to add environment data',
            'error': str(e)
        }), 500

@environments_bp.route('/<environment_id>/data', methods=['GET'])
@jwt_required()
def get_environment_data(environment_id):
    """Get environment data for an environment"""
    try:
        user_id = get_jwt_identity()
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
        
        # Get latest data
        latest_data = EnvironmentData.get_latest_data(environment_id)
        
        # Get historical data (last 30 days by default)
        days = int(request.args.get('days', 30))
        historical_data = EnvironmentData.get_historical_data(environment_id, days)
        
        return jsonify({
            'success': True,
            'data': {
                'environment': environment.to_dict(),
                'latest_data': latest_data.to_dict() if latest_data else None,
                'historical_data': [data.to_dict() for data in historical_data]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch environment data',
            'error': str(e)
        }), 500

@environments_bp.route('/<environment_id>/recommend', methods=['POST'])
@jwt_required()
def recommend_for_environment(environment_id):
    """Get product recommendations for an environment"""
    try:
        user_id = get_jwt_identity()
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
        
        # Get latest environment data
        latest_data = EnvironmentData.get_latest_data(environment_id)
        
        if not latest_data:
            return jsonify({
                'success': False,
                'message': 'No environment data found. Please add environment data first.'
            }), 400
        
        # Import here to avoid circular imports
        from models.product import Product
        
        # Get all products
        products = Product.query.filter_by(is_active=True).all()
        recommendations = []
        
        for product in products:
            if product.requirements:
                # Check suitability
                suitable, issues = product.requirements.is_suitable_for_environment(latest_data)
                
                # Calculate suitability score
                score = 0.0
                if suitable:
                    score = 1.0
                else:
                    # Calculate partial score
                    total_checks = 0
                    passed_checks = 0
                    
                    if product.requirements.ph_min is not None or product.requirements.ph_max is not None:
                        total_checks += 1
                        if latest_data.ph and product.requirements.ph_min <= latest_data.ph <= product.requirements.ph_max:
                            passed_checks += 1
                    
                    if product.requirements.temperature_min is not None or product.requirements.temperature_max is not None:
                        total_checks += 1
                        if latest_data.temperature and product.requirements.temperature_min <= latest_data.temperature <= product.requirements.temperature_max:
                            passed_checks += 1
                    
                    if product.requirements.humidity_min is not None or product.requirements.humidity_max is not None:
                        total_checks += 1
                        if latest_data.humidity and product.requirements.humidity_min <= latest_data.humidity <= product.requirements.humidity_max:
                            passed_checks += 1
                    
                    if total_checks > 0:
                        score = passed_checks / total_checks
                
                recommendations.append({
                    'product': product.to_dict(),
                    'suitability_score': score,
                    'suitable': suitable,
                    'issues': issues
                })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': {
                'environment': environment.to_dict(),
                'environment_data': latest_data.to_dict(),
                'recommendations': recommendations
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to generate recommendations',
            'error': str(e)
        }), 500
