# db will be imported from app when needed
from datetime import datetime
import uuid
from utils.logger import log_database_operation, log_function_call, get_logger

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
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    @log_database_operation
    def get_by_category(category):
        """Get products by category"""
        logger = get_logger('models.product')
        logger.info(f"Getting products by category: {category}")
        products = Product.query.filter_by(category=category, is_active=True).all()
        logger.success(f"Found {len(products)} products in category '{category}'")
        return products
    
    @staticmethod
    @log_database_operation
    def search_products(query):
        """Search products by name or description"""
        logger = get_logger('models.product')
        logger.info(f"Searching products with query: '{query}'")
        products = Product.query.filter(
            db.or_(
                Product.name.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%')
            ),
            Product.is_active == True
        ).all()
        logger.success(f"Found {len(products)} products matching '{query}'")
        return products
    
    @staticmethod
    @log_database_operation
    def get_all_categories():
        """Get all unique categories"""
        logger = get_logger('models.product')
        logger.info("Getting all product categories")
        categories = db.session.query(Product.category).filter_by(is_active=True).distinct().all()
        category_list = [category[0] for category in categories]
        logger.success(f"Found {len(category_list)} categories: {category_list}")
        return category_list

class ProductRequirements(db.Model):
    """Product requirements model for growing conditions"""
    __tablename__ = 'product_requirements'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    
    # Soil requirements
    ph_min = db.Column(db.Float)
    ph_max = db.Column(db.Float)
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
            'ph': {
                'min': self.ph_min,
                'max': self.ph_max
            },
            'nitrogen': {
                'min': self.nitrogen_min,
                'max': self.nitrogen_max
            },
            'phosphorus': {
                'min': self.phosphorus_min,
                'max': self.phosphorus_max
            },
            'potassium': {
                'min': self.potassium_min,
                'max': self.potassium_max
            },
            'humidity': {
                'min': self.humidity_min,
                'max': self.humidity_max
            },
            'temperature': {
                'min': self.temperature_min,
                'max': self.temperature_max
            },
            'rainfall': {
                'min': self.rainfall_min,
                'max': self.rainfall_max
            },
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @log_function_call
    def is_suitable_for_environment(self, environment_data):
        """Check if product is suitable for given environment"""
        logger = get_logger('models.product')
        logger.info(f"Checking suitability for product {self.product_id}")
        
        suitable = True
        issues = []
        
        # Check pH
        if self.ph_min and environment_data.ph < self.ph_min:
            suitable = False
            issues.append(f"pH too low: {environment_data.ph} < {self.ph_min}")
        if self.ph_max and environment_data.ph > self.ph_max:
            suitable = False
            issues.append(f"pH too high: {environment_data.ph} > {self.ph_max}")
        
        # Check temperature
        if self.temperature_min and environment_data.temperature < self.temperature_min:
            suitable = False
            issues.append(f"Temperature too low: {environment_data.temperature} < {self.temperature_min}")
        if self.temperature_max and environment_data.temperature > self.temperature_max:
            suitable = False
            issues.append(f"Temperature too high: {environment_data.temperature} > {self.temperature_max}")
        
        # Check humidity
        if self.humidity_min and environment_data.humidity < self.humidity_min:
            suitable = False
            issues.append(f"Humidity too low: {environment_data.humidity} < {self.humidity_min}")
        if self.humidity_max and environment_data.humidity > self.humidity_max:
            suitable = False
            issues.append(f"Humidity too high: {environment_data.humidity} > {self.humidity_max}")
        
        if suitable:
            logger.success(f"Product {self.product_id} is suitable for environment")
        else:
            logger.warning(f"Product {self.product_id} is not suitable: {issues}")
        
        return suitable, issues
