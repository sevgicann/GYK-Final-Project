from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.environment import Environment
from models.recommendation import Recommendation
from flask import current_app

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch profile',
            'error': str(e)
        }), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile"""
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
                'message': 'Profile data is required'
            }), 400
        
        # Update allowed fields
        if 'name' in data:
            user.name = (data['name'] or '').strip()
        
        if 'language' in data:
            user.language = data['language']
        
        if 'city' in data:
            user.city = (data['city'] or '').strip()
        
        if 'district' in data:
            user.district = (data['district'] or '').strip()
        
        if 'latitude' in data:
            user.latitude = data['latitude']
        
        if 'longitude' in data:
            user.longitude = data['longitude']
        
        if 'is_gps_enabled' in data:
            user.is_gps_enabled = data['is_gps_enabled']
        
        if 'notifications_enabled' in data:
            user.notifications_enabled = data['notifications_enabled']
        
        if 'theme' in data:
            user.theme = data['theme']
        
        current_app.extensions['sqlalchemy'].db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'data': {
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        current_app.extensions['sqlalchemy'].db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update profile',
            'error': str(e)
        }), 500

@users_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Get user dashboard data"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Get user's environments
        environments = Environment.get_user_environments(user_id)
        
        # Get recent recommendations
        recent_recommendations = Recommendation.query.filter_by(
            user_id=user_id, 
            status='active'
        ).order_by(Recommendation.created_at.desc()).limit(5).all()
        
        # Get statistics
        total_environments = len(environments)
        total_recommendations = Recommendation.query.filter_by(user_id=user_id).count()
        active_recommendations = Recommendation.query.filter_by(
            user_id=user_id, 
            status='active'
        ).count()
        favorite_recommendations = Recommendation.query.filter_by(
            user_id=user_id, 
            is_favorite=True
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict_public(),
                'environments': [env.to_dict() for env in environments],
                'recent_recommendations': [rec.to_dict_summary() for rec in recent_recommendations],
                'statistics': {
                    'total_environments': total_environments,
                    'total_recommendations': total_recommendations,
                    'active_recommendations': active_recommendations,
                    'favorite_recommendations': favorite_recommendations
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch dashboard data',
            'error': str(e)
        }), 500

@users_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    """Get user settings"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'settings': {
                    'language': user.language,
                    'notifications_enabled': user.notifications_enabled,
                    'theme': user.theme,
                    'location': {
                        'city': user.city,
                        'district': user.district,
                        'latitude': user.latitude,
                        'longitude': user.longitude,
                        'is_gps_enabled': user.is_gps_enabled
                    }
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch settings',
            'error': str(e)
        }), 500

@users_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    """Update user settings"""
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
                'message': 'Settings data is required'
            }), 400
        
        # Update settings
        if 'language' in data:
            user.language = data['language']
        
        if 'notifications_enabled' in data:
            user.notifications_enabled = data['notifications_enabled']
        
        if 'theme' in data:
            user.theme = data['theme']
        
        if 'location' in data:
            location = data['location']
            if 'city' in location:
                user.city = (location['city'] or '').strip()
            if 'district' in location:
                user.district = (location['district'] or '').strip()
            if 'latitude' in location:
                user.latitude = location['latitude']
            if 'longitude' in location:
                user.longitude = location['longitude']
            if 'is_gps_enabled' in location:
                user.is_gps_enabled = location['is_gps_enabled']
        
        current_app.extensions['sqlalchemy'].db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Settings updated successfully',
            'data': {
                'settings': {
                    'language': user.language,
                    'notifications_enabled': user.notifications_enabled,
                    'theme': user.theme,
                    'location': {
                        'city': user.city,
                        'district': user.district,
                        'latitude': user.latitude,
                        'longitude': user.longitude,
                        'is_gps_enabled': user.is_gps_enabled
                    }
                }
            }
        }), 200
        
    except Exception as e:
        current_app.extensions['sqlalchemy'].db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to update settings',
            'error': str(e)
        }), 500

@users_bp.route('/deactivate', methods=['POST'])
@jwt_required()
def deactivate_account():
    """Deactivate user account"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Deactivate account
        user.is_active = False
        current_app.extensions['sqlalchemy'].db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Account deactivated successfully'
        }), 200
        
    except Exception as e:
        current_app.extensions['sqlalchemy'].db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to deactivate account',
            'error': str(e)
        }), 500
