# db will be imported from app when needed
from datetime import datetime
import uuid

class Environment(db.Model):
    """Environment model for storing user's environmental data"""
    __tablename__ = 'environments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # e.g., "My Garden", "Field 1"
    location_type = db.Column(db.String(20), default='manual')  # 'gps' or 'manual'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Location information
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Relationships
    environment_data = db.relationship('EnvironmentData', backref='environment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Environment {self.name}>'
    
    def to_dict(self):
        """Convert environment to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'location_type': self.location_type,
            'is_active': self.is_active,
            'location': {
                'city': self.city,
                'district': self.district,
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def get_user_environments(user_id):
        """Get all environments for a user"""
        return Environment.query.filter_by(user_id=user_id, is_active=True).all()

class EnvironmentData(db.Model):
    """Environment data model for storing soil and weather conditions"""
    __tablename__ = 'environment_data'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    environment_id = db.Column(db.String(36), db.ForeignKey('environments.id'), nullable=False)
    
    # Soil data
    ph = db.Column(db.Float)
    nitrogen = db.Column(db.Float)
    phosphorus = db.Column(db.Float)
    potassium = db.Column(db.Float)
    organic_matter = db.Column(db.Float)
    soil_type = db.Column(db.String(50))  # clay, sand, loam, etc.
    
    # Weather data
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    sunlight_hours = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    
    # Additional data
    altitude = db.Column(db.Float)
    slope = db.Column(db.Float)
    drainage = db.Column(db.String(20))  # good, moderate, poor
    
    # Data source and timestamp
    data_source = db.Column(db.String(20), default='manual')  # manual, sensor, api
    measured_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EnvironmentData {self.environment_id}>'
    
    def to_dict(self):
        """Convert environment data to dictionary"""
        return {
            'id': self.id,
            'environment_id': self.environment_id,
            'soil': {
                'ph': self.ph,
                'nitrogen': self.nitrogen,
                'phosphorus': self.phosphorus,
                'potassium': self.potassium,
                'organic_matter': self.organic_matter,
                'soil_type': self.soil_type
            },
            'weather': {
                'temperature': self.temperature,
                'humidity': self.humidity,
                'rainfall': self.rainfall,
                'sunlight_hours': self.sunlight_hours,
                'wind_speed': self.wind_speed
            },
            'terrain': {
                'altitude': self.altitude,
                'slope': self.slope,
                'drainage': self.drainage
            },
            'data_source': self.data_source,
            'measured_at': self.measured_at.isoformat(),
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def get_latest_data(environment_id):
        """Get latest environment data for an environment"""
        return EnvironmentData.query.filter_by(environment_id=environment_id).order_by(EnvironmentData.measured_at.desc()).first()
    
    @staticmethod
    def get_historical_data(environment_id, days=30):
        """Get historical environment data for an environment"""
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return EnvironmentData.query.filter(
            EnvironmentData.environment_id == environment_id,
            EnvironmentData.measured_at >= cutoff_date
        ).order_by(EnvironmentData.measured_at.desc()).all()
