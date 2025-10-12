from app import db
from datetime import datetime
import uuid

class Recommendation(db.Model):
    """Recommendation model for storing AI-generated recommendations"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    environment_id = db.Column(db.String(36), db.ForeignKey('environments.id'), nullable=False)
    
    # Recommendation details
    recommendation_type = db.Column(db.String(20), nullable=False)  # 'product_to_environment' or 'environment_to_product'
    confidence_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    suitability_score = db.Column(db.Float, default=0.0)  # 0.0 to 1.0
    
    # Recommendation content
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text)
    challenges = db.Column(db.Text)
    suggestions = db.Column(db.Text)
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, dismissed, implemented
    is_favorite = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Recommendation {self.title}>'
    
    def to_dict(self):
        """Convert recommendation to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'environment_id': self.environment_id,
            'recommendation_type': self.recommendation_type,
            'confidence_score': self.confidence_score,
            'suitability_score': self.suitability_score,
            'title': self.title,
            'description': self.description,
            'benefits': self.benefits,
            'challenges': self.challenges,
            'suggestions': self.suggestions,
            'status': self.status,
            'is_favorite': self.is_favorite,
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
