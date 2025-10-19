from app import db
from datetime import datetime
import uuid
import json
from utils.logger import log_database_operation, log_function_call, get_logger

class ModelResult(db.Model):
    """Model results transaction table for storing AI model predictions"""
    __tablename__ = 'model_results'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Model information
    model_type = db.Column(db.String(50), nullable=False)  # 'crop_recommendation', 'environment_recommendation'
    model_version = db.Column(db.String(20), nullable=False)  # 'v1.0', 'v2.0', etc.
    algorithm = db.Column(db.String(30), nullable=False)  # 'lightgbm', 'xgboost', 'random_forest'
    
    # Input data (JSON format for flexibility)
    input_data = db.Column(db.JSON, nullable=False)
    
    # Model predictions
    predictions = db.Column(db.JSON, nullable=False)  # Raw model output
    confidence_scores = db.Column(db.JSON)  # Confidence scores for each prediction
    processing_time_ms = db.Column(db.Float)  # Model processing time in milliseconds
    
    # Results interpretation
    top_recommendations = db.Column(db.JSON)  # Top 5 recommendations with details
    recommendation_type = db.Column(db.String(30))  # 'product_to_environment', 'environment_to_product'
    
    # Status and metadata
    status = db.Column(db.String(20), default='completed')  # 'processing', 'completed', 'failed'
    error_message = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='model_results')
    
    def __repr__(self):
        return f'<ModelResult {self.model_type} - {self.user_id}>'
    
    def to_dict(self):
        """Convert model result to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'model_type': self.model_type,
            'model_version': self.model_version,
            'algorithm': self.algorithm,
            'input_data': self.input_data,
            'predictions': self.predictions,
            'confidence_scores': self.confidence_scores,
            'processing_time_ms': self.processing_time_ms,
            'top_recommendations': self.top_recommendations,
            'recommendation_type': self.recommendation_type,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @staticmethod
    @log_database_operation
    def create_result(user_id, model_type, model_version, algorithm, input_data, 
                     predictions, confidence_scores=None, processing_time_ms=None):
        """Create a new model result record"""
        logger = get_logger('models.model_results')
        logger.info(f"Creating model result for user {user_id}, model: {model_type}")
        
        try:
            result = ModelResult(
                user_id=user_id,
                model_type=model_type,
                model_version=model_version,
                algorithm=algorithm,
                input_data=input_data,
                predictions=predictions,
                confidence_scores=confidence_scores,
                processing_time_ms=processing_time_ms,
                status='completed',
                completed_at=datetime.utcnow()
            )
            
            db.session.add(result)
            db.session.commit()
            
            logger.success(f"Model result created successfully: {result.id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to create model result: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    @log_database_operation
    def get_user_results(user_id, model_type=None, limit=50):
        """Get model results for a user"""
        logger = get_logger('models.model_results')
        logger.info(f"Getting model results for user {user_id}")
        
        query = ModelResult.query.filter_by(user_id=user_id, status='completed')
        
        if model_type:
            query = query.filter_by(model_type=model_type)
        
        results = query.order_by(ModelResult.created_at.desc()).limit(limit).all()
        
        logger.success(f"Found {len(results)} model results for user {user_id}")
        return results
    
    @staticmethod
    @log_database_operation
    def get_recent_results(hours=24, limit=100):
        """Get recent model results across all users"""
        logger = get_logger('models.model_results')
        logger.info(f"Getting recent model results from last {hours} hours")
        
        from datetime import timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        results = ModelResult.query.filter(
            ModelResult.created_at >= cutoff_time,
            ModelResult.status == 'completed'
        ).order_by(ModelResult.created_at.desc()).limit(limit).all()
        
        logger.success(f"Found {len(results)} recent model results")
        return results
    
    @log_function_call
    def update_top_recommendations(self, recommendations):
        """Update top recommendations based on model output"""
        logger = get_logger('models.model_results')
        logger.info(f"Updating top recommendations for result {self.id}")
        
        self.top_recommendations = recommendations
        db.session.commit()
        
        logger.success(f"Top recommendations updated for result {self.id}")
    
    @staticmethod
    @log_database_operation
    def get_model_statistics(model_type=None, days=30):
        """Get model usage statistics"""
        logger = get_logger('models.model_results')
        logger.info(f"Getting model statistics for last {days} days")
        
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = ModelResult.query.filter(
            ModelResult.created_at >= cutoff_date,
            ModelResult.status == 'completed'
        )
        
        if model_type:
            query = query.filter_by(model_type=model_type)
        
        results = query.all()
        
        stats = {
            'total_requests': len(results),
            'avg_processing_time': sum(r.processing_time_ms or 0 for r in results) / len(results) if results else 0,
            'model_types': {},
            'algorithms': {},
            'daily_requests': {}
        }
        
        for result in results:
            # Count by model type
            stats['model_types'][result.model_type] = stats['model_types'].get(result.model_type, 0) + 1
            
            # Count by algorithm
            stats['algorithms'][result.algorithm] = stats['algorithms'].get(result.algorithm, 0) + 1
            
            # Count by day
            day = result.created_at.strftime('%Y-%m-%d')
            stats['daily_requests'][day] = stats['daily_requests'].get(day, 0) + 1
        
        logger.success(f"Model statistics calculated: {stats['total_requests']} total requests")
        return stats
