# db will be imported from app when needed
from datetime import datetime
import uuid
from utils.logger import log_database_operation, log_function_call, get_logger

class Recommendation(db.Model):
    """Recommendation transaction model for storing AI-generated recommendations"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    environment_id = db.Column(db.String(36), db.ForeignKey('environments.id'), nullable=False)
    model_result_id = db.Column(db.String(36), db.ForeignKey('model_results.id'), nullable=True)  # Link to model result
    
    # Recommendation details
    recommendation_type = db.Column(db.String(20), nullable=False)  # 'product_to_environment' or 'environment_to_product'
    confidence_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    suitability_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    
    # Model information
    model_type = db.Column(db.String(50), nullable=False)  # 'crop_recommendation', 'environment_recommendation'
    model_version = db.Column(db.String(20), nullable=False)  # 'v1.0', 'v2.0', etc.
    algorithm = db.Column(db.String(30), nullable=False)  # 'lightgbm', 'xgboost', 'random_forest'
    
    # Recommendation content
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text)
    challenges = db.Column(db.Text)
    suggestions = db.Column(db.Text)
    
    # Input data that generated this recommendation
    input_parameters = db.Column(db.JSON)  # Store the input parameters used
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, dismissed, implemented
    is_favorite = db.Column(db.Boolean, default=False)
    
    # User interaction tracking
    view_count = db.Column(db.Integer, default=0)
    last_viewed_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    model_result = db.relationship('ModelResult', backref='recommendations')
    
    def __repr__(self):
        return f'<Recommendation {self.title}>'
    
    def to_dict(self):
        """Convert recommendation to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'environment_id': self.environment_id,
            'model_result_id': self.model_result_id,
            'recommendation_type': self.recommendation_type,
            'confidence_score': self.confidence_score,
            'suitability_score': self.suitability_score,
            'model_type': self.model_type,
            'model_version': self.model_version,
            'algorithm': self.algorithm,
            'title': self.title,
            'description': self.description,
            'benefits': self.benefits,
            'challenges': self.challenges,
            'suggestions': self.suggestions,
            'input_parameters': self.input_parameters,
            'status': self.status,
            'is_favorite': self.is_favorite,
            'view_count': self.view_count,
            'last_viewed_at': self.last_viewed_at.isoformat() if self.last_viewed_at else None,
            'product': self.product.to_dict() if self.product else None,
            'environment': self.environment.to_dict() if self.environment else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def to_dict_summary(self):
        """Convert recommendation to summary dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'confidence_score': self.confidence_score,
            'suitability_score': self.suitability_score,
            'status': self.status,
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def get_user_recommendations(user_id, status='active'):
        """Get recommendations for a user"""
        return Recommendation.query.filter_by(user_id=user_id, status=status).order_by(Recommendation.created_at.desc()).all()
    
    @staticmethod
    def get_favorite_recommendations(user_id):
        """Get favorite recommendations for a user"""
        return Recommendation.query.filter_by(user_id=user_id, is_favorite=True).order_by(Recommendation.created_at.desc()).all()
    
    @staticmethod
    def get_recommendations_by_type(user_id, recommendation_type):
        """Get recommendations by type"""
        return Recommendation.query.filter_by(
            user_id=user_id, 
            recommendation_type=recommendation_type,
            status='active'
        ).order_by(Recommendation.confidence_score.desc()).all()
    
    def mark_as_favorite(self):
        """Mark recommendation as favorite"""
        self.is_favorite = True
        db.session.commit()
    
    def unmark_as_favorite(self):
        """Unmark recommendation as favorite"""
        self.is_favorite = False
        db.session.commit()
    
    def dismiss(self):
        """Dismiss recommendation"""
        self.status = 'dismissed'
        db.session.commit()
    
    def implement(self):
        """Mark recommendation as implemented"""
        self.status = 'implemented'
        db.session.commit()
    
    @log_function_call
    def increment_view_count(self):
        """Increment view count and update last viewed timestamp"""
        logger = get_logger('models.recommendation')
        logger.info(f"Incrementing view count for recommendation {self.id}")
        
        self.view_count += 1
        self.last_viewed_at = datetime.utcnow()
        db.session.commit()
        
        logger.success(f"View count incremented to {self.view_count} for recommendation {self.id}")
    
    @staticmethod
    @log_database_operation
    def create_from_model_result(model_result, product_id, environment_id, 
                                recommendation_data, input_parameters=None):
        """Create recommendation from model result"""
        logger = get_logger('models.recommendation')
        logger.info(f"Creating recommendation from model result {model_result.id}")
        
        try:
            recommendation = Recommendation(
                user_id=model_result.user_id,
                product_id=product_id,
                environment_id=environment_id,
                model_result_id=model_result.id,
                recommendation_type=recommendation_data.get('recommendation_type'),
                confidence_score=recommendation_data.get('confidence_score', 0.0),
                suitability_score=recommendation_data.get('suitability_score', 0.0),
                model_type=model_result.model_type,
                model_version=model_result.model_version,
                algorithm=model_result.algorithm,
                title=recommendation_data.get('title'),
                description=recommendation_data.get('description'),
                benefits=recommendation_data.get('benefits'),
                challenges=recommendation_data.get('challenges'),
                suggestions=recommendation_data.get('suggestions'),
                input_parameters=input_parameters
            )
            
            db.session.add(recommendation)
            db.session.commit()
            
            logger.success(f"Recommendation created successfully: {recommendation.id}")
            return recommendation
            
        except Exception as e:
            logger.error(f"Failed to create recommendation: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    @log_database_operation
    def get_recommendation_statistics(user_id=None, days=30):
        """Get recommendation statistics"""
        logger = get_logger('models.recommendation')
        logger.info(f"Getting recommendation statistics for last {days} days")
        
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = Recommendation.query.filter(Recommendation.created_at >= cutoff_date)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        recommendations = query.all()
        
        stats = {
            'total_recommendations': len(recommendations),
            'by_type': {},
            'by_model': {},
            'by_algorithm': {},
            'avg_confidence': 0,
            'avg_suitability': 0,
            'status_breakdown': {},
            'favorite_count': 0,
            'total_views': 0
        }
        
        total_confidence = 0
        total_suitability = 0
        confidence_count = 0
        suitability_count = 0
        
        for rec in recommendations:
            # Count by type
            stats['by_type'][rec.recommendation_type] = \
                stats['by_type'].get(rec.recommendation_type, 0) + 1
            
            # Count by model
            stats['by_model'][rec.model_type] = \
                stats['by_model'].get(rec.model_type, 0) + 1
            
            # Count by algorithm
            stats['by_algorithm'][rec.algorithm] = \
                stats['by_algorithm'].get(rec.algorithm, 0) + 1
            
            # Count by status
            stats['status_breakdown'][rec.status] = \
                stats['status_breakdown'].get(rec.status, 0) + 1
            
            # Count favorites
            if rec.is_favorite:
                stats['favorite_count'] += 1
            
            # Sum views
            stats['total_views'] += rec.view_count
            
            # Calculate averages
            if rec.confidence_score:
                total_confidence += rec.confidence_score
                confidence_count += 1
            
            if rec.suitability_score:
                total_suitability += rec.suitability_score
                suitability_count += 1
        
        # Calculate averages
        if confidence_count > 0:
            stats['avg_confidence'] = total_confidence / confidence_count
        
        if suitability_count > 0:
            stats['avg_suitability'] = total_suitability / suitability_count
        
        logger.success(f"Recommendation statistics calculated: {stats['total_recommendations']} total recommendations")
        return stats
