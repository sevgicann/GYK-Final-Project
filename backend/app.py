from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta
import os
from dotenv import load_dotenv
from utils.logger import get_logger, log_info, log_error, log_success

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize logger
logger = get_logger('app')
log_info("Initializing Terramind Flask application")

# ML Service (will be initialized after app setup)
ml_service = None

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:pass.123@localhost:5432/terramind_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
log_info("Initializing database connection")
db = SQLAlchemy(app)

log_info("Initializing database migrations")
migrate = Migrate(app, db)

log_info("Initializing JWT authentication")
jwt = JWTManager(app)

log_info("Initializing CORS")
CORS(app, origins=['*'], supports_credentials=True)  # Tüm origin'lere izin ver

# Rate limiting
log_info("Initializing rate limiting")
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Models will be imported after app context is set

# Import routes
log_info("Importing API routes")
from routes.auth import auth_bp
from routes.users import users_bp
from routes.products import products_bp
from routes.public import public_bp
from routes.environments import environments_bp
from routes.recommendations import recommendations_bp
from routes.ml_endpoints import ml_bp
from routes.product_selection import product_selection_bp

# Register blueprints
log_info("Registering API routes")
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(public_bp, url_prefix='/api/public')
app.register_blueprint(environments_bp, url_prefix='/api/environments')
app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
app.register_blueprint(ml_bp, url_prefix='/api/ml')
app.register_blueprint(product_selection_bp, url_prefix='/api/product-selection')

# Request logging middleware
@app.before_request
def log_request():
    """Log all incoming requests with user data"""
    request_logger = get_logger('requests')
    
    # Log basic request info
    request_logger.info(f"[REQUEST] {request.method} {request.path} from {request.remote_addr}")
    request_logger.debug(f"[HEADERS] {dict(request.headers)}")
    
    # Log request body (excluding sensitive data)
    if request.is_json:
        try:
            body = request.get_json()
            if body:
                # Create safe copy without sensitive data
                safe_body = {}
                sensitive_keys = {'password', 'token', 'secret', 'key', 'auth'}
                
                for key, value in body.items():
                    if any(sensitive in key.lower() for sensitive in sensitive_keys):
                        safe_body[key] = "***"
                    else:
                        safe_body[key] = value
                
                request_logger.info(f"[REQUEST_DATA] {safe_body}")
        except Exception as e:
            request_logger.warning(f"[REQUEST_BODY_ERROR] Could not parse JSON: {e}")
    
    # Log query parameters
    if request.args:
        request_logger.debug(f"[QUERY_PARAMS] {dict(request.args)}")

@app.after_request
def log_response(response):
    """Log all outgoing responses"""
    response_logger = get_logger('requests')
    response_logger.info(f"[RESPONSE] {response.status_code} for {request.method} {request.path}")
    
    # Log response body for errors
    if response.status_code >= 400:
        try:
            response_data = response.get_json()
            if response_data:
                response_logger.warning(f"[ERROR_RESPONSE] {response_data}")
        except Exception:
            pass
    
    return response

# Blueprints are already registered above

# Initialize ML Service
def init_ml_service():
    """Initialize ML service with models"""
    global ml_service
    try:
        from services.ml_service import get_ml_service
        log_info("Initializing ML Service...")
        ml_service = get_ml_service()
        ml_service.initialize_models()
        log_success("ML Service initialized successfully")
    except Exception as e:
        log_error(f"ML Service initialization failed: {str(e)}")
        log_error("Application will continue without ML capabilities")

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    log_info("Health check requested")
    
    health_data = {
        'status': 'OK',
        'message': 'Terramind API is running',
        'version': '1.0.0',
        'environment': os.getenv('FLASK_ENV', 'development')
    }
    
    # Add ML service status if available
    if ml_service:
        try:
            ml_health = ml_service.health_check()
            health_data['ml_service'] = ml_health
        except Exception as e:
            health_data['ml_service'] = {
                'status': 'error',
                'error': str(e)
            }
    
    return jsonify(health_data), 200

# Test endpoint
@app.route('/test-recommendation', methods=['POST'])
def test_recommendation():
    """Test recommendation endpoint"""
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

# Test login endpoint (without database)
@app.route('/test-login', methods=['POST'])
def test_login():
    """Test login endpoint without database"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        email = (data.get('email') or '').strip().lower()
        password = data.get('password', '')
        
        # Simple validation
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
        
        # Mock login (accept any email/password for testing)
        if email and password:
            # Create mock user data
            mock_user = {
                'id': 'test-user-123',
                'name': 'Test User',
                'email': email,
                'phone': None,
                'created_at': '2025-01-01T00:00:00Z',
                'updated_at': '2025-01-01T00:00:00Z',
                'language': 'tr',
                'is_active': True
            }
            
            # Create mock token
            mock_token = 'test-token-' + email.replace('@', '-').replace('.', '-')
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'data': {
                    'user': mock_user,
                    'token': mock_token
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Login failed',
            'error': str(e)
        }), 500

# Test register endpoint (without database)
@app.route('/test-register', methods=['POST'])
def test_register():
    """Test register endpoint without database"""
    logger = get_logger('test.register')
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request data is required'
            }), 400
        
        # Extract user information (only basic fields)
        name = (data.get('name') or '').strip()
        email = (data.get('email') or '').strip().lower()
        password = data.get('password', '')
        
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
        
        if not password:
            return jsonify({
                'success': False,
                'message': 'Password is required'
            }), 400
        
        # Detailed logging of user registration data
        logger.info("=" * 60)
        logger.info("NEW USER REGISTRATION ATTEMPT:")
        logger.info(f"  Personal Information:")
        logger.info(f"    - Name: {name}")
        logger.info(f"    - Email: {email}")
        logger.info(f"  Security:")
        logger.info(f"    - Password Length: {len(password) if password else 0} characters")
        logger.info(f"    - Password Hash: {'*' * 20} (hidden for security)")
        logger.info("=" * 60)
        
        # Mock successful registration
        mock_user = {
            'id': f'test-user-{hash(email) % 10000}',
            'name': name,
            'email': email,
            'phone': None,
            'created_at': '2025-01-01T00:00:00Z',
            'updated_at': '2025-01-01T00:00:00Z',
            'language': 'tr',
            'is_active': True
        }
        
        # Create mock token
        mock_token = 'test-token-' + email.replace('@', '-').replace('.', '-')
        
        # Log successful registration
        logger.info("=" * 60)
        logger.info("✅ USER REGISTRATION SUCCESSFUL:")
        logger.info(f"  User ID: {mock_user['id']}")
        logger.info(f"  Name: {mock_user['name']}")
        logger.info(f"  Email: {mock_user['email']}")
        logger.info(f"  Language: {mock_user['language']}")
        logger.info(f"  Registration Time: {mock_user['created_at']}")
        logger.info(f"  Token Generated: Yes")
        logger.info("=" * 60)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': mock_user,
                'token': mock_token
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Registration failed',
            'error': str(e)
        }), 500

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Welcome to Terramind API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'auth': '/api/auth',
            'users': '/api/users',
            'products': '/api/products',
            'environments': '/api/environments',
            'recommendations': '/api/recommendations'
        }
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'API endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'success': False,
        'message': 'Rate limit exceeded. Please try again later.'
    }), 429

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'success': False,
        'message': 'Token has expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'success': False,
        'message': 'Invalid token'
    }), 401

# JWT unauthorized loader removed - authentication handled per endpoint

# Initialize database and ML service when app starts
with app.app_context():
    try:
        # Import models after app context is set
        log_info("Importing database models")
        from models.user import User
        from models.product import Product, ProductRequirements
        from models.environment import Environment, EnvironmentData
        from models.recommendation import Recommendation
        from models.model_results import ModelResult
        from models.user_activity_log import UserActivityLog
        
        db.create_all()
        # Initialize ML service - temporarily disabled
        # init_ml_service()
        
        
        log_success("Database, ML service and routes initialized successfully")
    except Exception as e:
        log_error(f"Failed to initialize database or ML service: {str(e)}")

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=5000)
