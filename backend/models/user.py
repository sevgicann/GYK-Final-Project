from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import uuid
from utils.logger import log_database_operation, log_function_call, get_logger

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
    
    # Location information
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_gps_enabled = db.Column(db.Boolean, default=False)
    
    # User preferences
    notifications_enabled = db.Column(db.Boolean, default=True)
    theme = db.Column(db.String(10), default='light')
    
    # Relationships
    environments = db.relationship('Environment', backref='user', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @log_function_call
    def set_password(self, password):
        """Hash and set password"""
        logger = get_logger('models.user')
        logger.info(f"Setting password for user {self.email}")
        self.password_hash = generate_password_hash(password)
        logger.debug("Password hashed successfully")
    
    @log_function_call
    def check_password(self, password):
        """Check if provided password matches hash"""
        logger = get_logger('models.user')
        logger.debug(f"Checking password for user {self.email}")
        result = check_password_hash(self.password_hash, password)
        logger.info(f"Password check result: {'✅ Valid' if result else '❌ Invalid'}")
        return result
    
    @log_function_call
    def generate_token(self):
        """Generate JWT token for user"""
        logger = get_logger('models.user')
        logger.info(f"Generating JWT token for user {self.email}")
        token = create_access_token(identity=self.id)
        logger.debug("JWT token generated successfully")
        return token
    
    @log_database_operation
    def update_last_login(self):
        """Update last login timestamp"""
        logger = get_logger('models.user')
        logger.info(f"Updating last login for user {self.email}")
        self.last_login = datetime.utcnow()
        db.session.commit()
        logger.success(f"Last login updated for user {self.email}")
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'language': self.language,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'location': {
                'city': self.city,
                'district': self.district,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'is_gps_enabled': self.is_gps_enabled
            },
            'preferences': {
                'notifications_enabled': self.notifications_enabled,
                'theme': self.theme
            }
        }
    
    def to_dict_public(self):
        """Convert user to public dictionary (without sensitive data)"""
        return {
            'id': self.id,
            'name': self.name,
            'language': self.language,
            'location': {
                'city': self.city,
                'district': self.district,
                'is_gps_enabled': self.is_gps_enabled
            }
        }
    
    @staticmethod
    @log_database_operation
    def find_by_email(email):
        """Find user by email"""
        logger = get_logger('models.user')
        logger.info(f"Searching for user with email: {email}")
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            logger.success(f"User found: {user.email}")
        else:
            logger.warning(f"User not found with email: {email}")
        return user
    
    @staticmethod
    @log_database_operation
    def find_by_id(user_id):
        """Find user by ID"""
        logger = get_logger('models.user')
        logger.info(f"Searching for user with ID: {user_id}")
        user = User.query.get(user_id)
        if user:
            logger.success(f"User found: {user.email}")
        else:
            logger.warning(f"User not found with ID: {user_id}")
        return user
