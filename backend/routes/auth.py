from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re
from utils.logger import log_api_call, get_logger, log_info, log_error, log_success

# Import User from app
def get_user_class():
    from app import User
    return User

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"

@auth_bp.route('/register', methods=['POST'])
@log_api_call
def register():
    """Register a new user"""
    logger = get_logger('routes.auth')
    log_info("Starting user registration process")
    
    try:
        data = request.get_json()
        logger.debug(f"Registration request data: {data}")
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        name = (data.get('name') or '').strip()
        email = (data.get('email') or '').strip().lower()
        password = data.get('password', '')
        language = data.get('language', 'tr')
        
        # Extract additional user information
        phone = data.get('phone', '')
        city = data.get('city', '')
        district = data.get('district', '')
        latitude = data.get('latitude', '')
        longitude = data.get('longitude', '')
        is_gps_enabled = data.get('is_gps_enabled', False)
        notifications_enabled = data.get('notifications_enabled', True)
        theme = data.get('theme', 'light')
        
        # Detailed logging of user registration data
        logger.info("=" * 60)
        logger.info("NEW USER REGISTRATION ATTEMPT:")
        logger.info(f"  Personal Information:")
        logger.info(f"    - Name: {name}")
        logger.info(f"    - Email: {email}")
        logger.info(f"    - Phone: {phone if phone else 'Not provided'}")
        logger.info(f"    - Language: {language}")
        logger.info(f"  Location Information:")
        logger.info(f"    - City: {city if city else 'Not provided'}")
        logger.info(f"    - District: {district if district else 'Not provided'}")
        logger.info(f"    - Latitude: {latitude if latitude else 'Not provided'}")
        logger.info(f"    - Longitude: {longitude if longitude else 'Not provided'}")
        logger.info(f"    - GPS Enabled: {is_gps_enabled}")
        logger.info(f"  Preferences:")
        logger.info(f"    - Notifications Enabled: {notifications_enabled}")
        logger.info(f"    - Theme: {theme}")
        logger.info(f"  Security:")
        logger.info(f"    - Password Length: {len(password) if password else 0} characters")
        logger.info(f"    - Password Hash: {'*' * 20} (hidden for security)")
        logger.info("=" * 60)
        
        # Validation
        if not name:
            return jsonify({
                'success': False,
                'message': 'Name is required'
            }), 400
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        if not password:
            return jsonify({
                'success': False,
                'message': 'Password is required'
            }), 400
        
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Check if user already exists
        User = get_user_class()
        if User.find_by_email(email):
            return jsonify({
                'success': False,
                'message': 'User with this email already exists'
            }), 409
        
        # Create new user
        user = User(
            name=name,
            email=email,
            language=language
        )
        user.set_password(password)
        
        db = current_app.extensions['sqlalchemy'].db
        db.session.add(user)
        current_app.extensions['sqlalchemy'].db.session.commit()
        
        # Generate token
        token = user.generate_token()
        
        # Log successful registration
        logger.info("=" * 60)
        logger.info("✅ USER REGISTRATION SUCCESSFUL:")
        logger.info(f"  User ID: {user.id}")
        logger.info(f"  Name: {user.name}")
        logger.info(f"  Email: {user.email}")
        logger.info(f"  Language: {user.language}")
        logger.info(f"  Registration Time: {user.created_at}")
        logger.info(f"  Token Generated: {'Yes' if token else 'No'}")
        logger.info("=" * 60)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 201
        
    except Exception as e:
        current_app.extensions['sqlalchemy'].db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Registration failed',
            'error': str(e)
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        email = (data.get('email') or '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        
        if not password:
            return jsonify({
                'success': False,
                'message': 'Password is required'
            }), 400
        
        # Find user
        User = get_user_class()
        user = User.find_by_email(email)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Check password
        if not user.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Account is deactivated'
            }), 401
        
        # Update last login
        user.update_last_login()
        
        # Generate token
        token = user.generate_token()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Login failed',
            'error': str(e)
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        user_id = get_jwt_identity()
        User = get_user_class()
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
            'message': 'Failed to get user information',
            'error': str(e)
        }), 500

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        User = get_user_class()
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

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        User = get_user_class()
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
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        # Validation
        if not current_password:
            return jsonify({
                'success': False,
                'message': 'Current password is required'
            }), 400
        
        if not new_password:
            return jsonify({
                'success': False,
                'message': 'New password is required'
            }), 400
        
        # Check current password
        if not user.check_password(current_password):
            return jsonify({
                'success': False,
                'message': 'Current password is incorrect'
            }), 401
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Update password
        user.set_password(new_password)
        current_app.extensions['sqlalchemy'].db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        current_app.extensions['sqlalchemy'].db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to change password',
            'error': str(e)
        }), 500
