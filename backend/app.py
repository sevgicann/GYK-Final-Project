from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta, datetime
import os
import uuid
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
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
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///terramind.db')
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
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "supports_credentials": True
    }
})

# Rate limiting
log_info("Initializing rate limiting")
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Models will be imported after app context is set

# Define User model after db is initialized
class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(5), default='tr')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, email, password, language='tr'):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.language = language
        self.is_active = True
    
    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """Generate JWT token for the user"""
        return create_access_token(identity=self.id)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'language': self.language,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID"""
        return cls.query.filter_by(id=user_id).first()

# Define Environment model after db is initialized
class Environment(db.Model):
    """Environment model for storing user's environmental data"""
    __tablename__ = 'environments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    soil_type = db.Column(db.String(100), nullable=False)
    fertilizer = db.Column(db.String(100), nullable=False)
    irrigation = db.Column(db.String(100), nullable=False)
    sunlight = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert environment to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'region': self.region,
            'soil_type': self.soil_type,
            'fertilizer': self.fertilizer,
            'irrigation': self.irrigation,
            'sunlight': self.sunlight,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Environment {self.region} - {self.soil_type}>'
    
    @classmethod
    def get_user_environments(cls, user_id):
        """Get all environments for a user"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()

# Define Recommendation model after db is initialized
class Recommendation(db.Model):
    """Recommendation model for storing ML recommendations"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    model_used = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert recommendation to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_name': self.product_name,
            'confidence': self.confidence,
            'model_used': self.model_used,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Recommendation {self.product_name} - {self.confidence}>'

# Define ProductRequirements model after db is initialized
class ProductRequirements(db.Model):
    """Product requirements model for storing environmental requirements"""
    __tablename__ = 'product_requirements'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    
    # pH requirements
    ph_min = db.Column(db.Float)
    ph_max = db.Column(db.Float)
    
    # Nutrient requirements
    nitrogen_min = db.Column(db.Float)
    nitrogen_max = db.Column(db.Float)
    phosphorus_min = db.Column(db.Float)
    phosphorus_max = db.Column(db.Float)
    potassium_min = db.Column(db.Float)
    potassium_max = db.Column(db.Float)
    
    # Environmental requirements
    humidity_min = db.Column(db.Float)
    humidity_max = db.Column(db.Float)
    temperature_min = db.Column(db.Float)
    temperature_max = db.Column(db.Float)
    rainfall_min = db.Column(db.Float)
    rainfall_max = db.Column(db.Float)
    
    # Additional notes
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProductRequirements {self.product_id}>'
    
    def to_dict(self):
        """Convert requirements to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'ph': {'min': self.ph_min, 'max': self.ph_max},
            'nitrogen': {'min': self.nitrogen_min, 'max': self.nitrogen_max},
            'phosphorus': {'min': self.phosphorus_min, 'max': self.phosphorus_max},
            'potassium': {'min': self.potassium_min, 'max': self.potassium_max},
            'humidity': {'min': self.humidity_min, 'max': self.humidity_max},
            'temperature': {'min': self.temperature_min, 'max': self.temperature_max},
            'rainfall': {'min': self.rainfall_min, 'max': self.rainfall_max},
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Define Product model after db is initialized
class Product(db.Model):
    """Product model for agricultural products"""
    __tablename__ = 'products'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requirements = db.relationship('ProductRequirements', backref='product', uselist=False, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'requirements': self.requirements.to_dict() if self.requirements else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_by_category(category):
        """Get products by category"""
        return Product.query.filter_by(category=category, is_active=True).all()
    
    @staticmethod
    def get_all_categories():
        """Get all unique categories"""
        categories = db.session.query(Product.category).filter_by(is_active=True).distinct().all()
        return [cat[0] for cat in categories]
    
    @staticmethod
    def search_products(query):
        """Search products by name or description"""
        return Product.query.filter(
            db.or_(
                Product.name.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%')
            ),
            Product.is_active == True
        ).all()

# Define AverageSoilData model after db is initialized
class AverageSoilData(db.Model):
    """Average soil data model for storing regional soil averages"""
    __tablename__ = 'average_soil_data'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    soil_type = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    fertilizer_type = db.Column(db.String(100), nullable=False)
    irrigation_method = db.Column(db.String(100), nullable=False)
    weather_condition = db.Column(db.String(100), nullable=False)
    
    # Soil properties
    ph = db.Column(db.Float, nullable=False)
    nitrogen = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AverageSoilData {self.region} - {self.soil_type}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'soil_type': self.soil_type,
            'region': self.region,
            'fertilizer_type': self.fertilizer_type,
            'irrigation_method': self.irrigation_method,
            'weather_condition': self.weather_condition,
            'ph': self.ph,
            'nitrogen': self.nitrogen,
            'phosphorus': self.phosphorus,
            'potassium': self.potassium,
            'humidity': self.humidity,
            'temperature': self.temperature,
            'rainfall': self.rainfall,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_best_match(cls, soil_type, region, fertilizer_type, irrigation_method, weather_condition):
        """Get best matching average soil data"""
        # Try exact match first
        exact_match = cls.query.filter_by(
            soil_type=soil_type,
            region=region,
            fertilizer_type=fertilizer_type,
            irrigation_method=irrigation_method,
            weather_condition=weather_condition
        ).first()
        
        if exact_match:
            return exact_match
        
        # Try partial matches
        partial_match = cls.query.filter_by(
            soil_type=soil_type,
            region=region
        ).first()
        
        if partial_match:
            return partial_match
        
        # Try region only
        region_match = cls.query.filter_by(region=region).first()
        if region_match:
            return region_match
        
        return None
    
    @classmethod
    def get_default_averages(cls):
        """Get default average values"""
        return {
            'ph': 6.5,
            'nitrogen': 100,
            'phosphorus': 50,
            'potassium': 200,
            'humidity': 25,
            'temperature': 20,
            'rainfall': 500
        }

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
# from routes.pdf_generation import pdf_generation_bp  # Temporarily disabled

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
# app.register_blueprint(pdf_generation_bp, url_prefix='/api/pdf')  # Temporarily disabled

# PDF endpoints - Simple implementation without external dependencies
@app.route('/api/pdf/test', methods=['GET'])
def pdf_test():
    """Test PDF endpoint"""
    try:
        return jsonify({
            'success': True,
            'message': 'PDF test endpoint is working',
            'timestamp': str(datetime.now()),
            'status': 'healthy'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'PDF test endpoint error: {str(e)}'
        }), 500

@app.route('/api/pdf/health', methods=['GET'])
def pdf_health():
    """PDF service health check"""
    try:
        return jsonify({
            'success': True,
            'message': 'PDF generation service is running',
            'status': 'healthy',
            'timestamp': str(datetime.now())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'PDF health check error: {str(e)}'
        }), 500

@app.route('/api/pdf/generate-crop-recommendation', methods=['POST'])
def generate_crop_pdf():
    """Generate crop recommendation PDF using Google Gemini AI and FPDF"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Extract data
        location = data.get('location', 'Bilinmeyen')
        region = data.get('region', 'Bilinmeyen')
        soil_type = data.get('soil_type', 'Bilinmeyen')
        sunlight = data.get('sunlight', 'Bilinmeyen')
        irrigation_method = data.get('irrigation_method', 'Bilinmeyen')
        fertilizer = data.get('fertilizer_type', 'Bilinmeyen')
        ph = data.get('ph', 6.5)
        nitrogen = data.get('nitrogen', 100)
        phosphorus = data.get('phosphorus', 50)
        potassium = data.get('potassium', 200)
        humidity = data.get('humidity', 25)
        temperature = data.get('temperature', 20)
        rainfall = data.get('rainfall', 500)
        recommendations = data.get('recommendations', [])
        
        # Try to use the real PDF generation service
        try:
            from pdf_llm_service import generate_crop_recommendation_pdf
            
            # Prepare data for the PDF service
            pdf_data = {
                'location': location,
                'region': region,
                'soil_type': soil_type,
                'sunlight': sunlight,
                'irrigation_method': irrigation_method,
                'fertilizer': fertilizer,
                'ph': ph,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'humidity': humidity,
                'temperature': temperature,
                'rainfall': rainfall,
                'recommendations': recommendations
            }
            
            # Generate PDF using the real service
            pdf_path = generate_crop_recommendation_pdf(pdf_data)
            
            if pdf_path and os.path.exists(pdf_path):
                # Read the generated PDF file
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                
                # Convert to base64 for JSON response
                import base64
                pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                
                # Clean up the temporary file
                os.remove(pdf_path)
                
                return jsonify({
                    'success': True,
                    'message': 'PDF raporu başarıyla oluşturuldu',
                    'pdf_content': pdf_base64,
                    'filename': f'crop_recommendation_{location}_{int(datetime.now().timestamp())}.pdf',
                    'content_type': 'application/pdf'
                })
            else:
                raise Exception("PDF dosyası oluşturulamadı")
                
        except ImportError:
            # Fallback to simple text if pdf_llm_service is not available
            log_info("PDF service not available, using fallback text generation")
            
            response_text = f"""
TARIM ÜRÜN ÖNERİ RAPORU
========================

Konum: {location}
Bölge: {region}
Toprak Tipi: {soil_type}
Güneş Işığı: {sunlight}
Sulama: {irrigation_method}
Gübre: {fertilizer}
pH: {ph}
Azot: {nitrogen}
Fosfor: {phosphorus}
Potasyum: {potassium}
Nem: {humidity}%
Sıcaklık: {temperature}°C
Yağış: {rainfall}mm
Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M')}

ÖNERİLEN ÜRÜNLER:
"""
            
            for i, rec in enumerate(recommendations, 1):
                product_name = rec.get('product_name', f'Ürün {i}')
                confidence = rec.get('confidence', 0.0)
                confidence_percent = int(confidence * 100)
                response_text += f"{i}. {product_name} - Uygunluk: %{confidence_percent}\n"
            
            response_text += f"""
NOT: Bu basit bir test raporudur. 
Gerçek PDF generation özelliği için gerekli kütüphaneler yüklenmemiş.

Rapor oluşturulma zamanı: {datetime.now()}
"""
            
            return jsonify({
                'success': True,
                'message': 'PDF raporu başarıyla oluşturuldu (Fallback modu)',
                'content': response_text,
                'filename': f'crop_recommendation_{location}_{int(datetime.now().timestamp())}.txt'
            })
        
    except Exception as e:
        log_error(f"PDF generation error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'PDF oluşturulurken hata oluştu: {str(e)}'
        }), 500

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
