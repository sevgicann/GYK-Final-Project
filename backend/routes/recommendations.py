from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.recommendation import Recommendation
from models.user import User
from models.product import Product
from models.environment import Environment
from app import db
from datetime import datetime
from utils.logger import log_api_call, get_logger, log_info, log_success

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/test-get', methods=['GET'])
def test_endpoint():
    """Test endpoint"""
    return jsonify({'message': 'Test endpoint works!'}), 200

@recommendations_bp.route('/test-post', methods=['POST'])
def generate_recommendation():
    """Generate recommendation based on user input"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
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
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Öneri oluşturulurken hata oluştu',
            'error': str(e)
        }), 500

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
