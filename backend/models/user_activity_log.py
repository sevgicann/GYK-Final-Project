from app import db
from datetime import datetime
import uuid
import json
from utils.logger import log_database_operation, log_function_call, get_logger

class UserActivityLog(db.Model):
    """User activity log transaction table for tracking user actions"""
    __tablename__ = 'user_activity_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Activity information
    activity_type = db.Column(db.String(50), nullable=False)  # 'login', 'logout', 'recommendation_request', 'product_view', etc.
    activity_category = db.Column(db.String(30), nullable=False)  # 'authentication', 'recommendation', 'product', 'environment', 'system'
    
    # Activity details
    description = db.Column(db.String(255), nullable=False)
    details = db.Column(db.JSON)  # Additional activity-specific data
    
    # Request/Response information
    request_method = db.Column(db.String(10))  # GET, POST, PUT, DELETE
    endpoint = db.Column(db.String(255))  # API endpoint accessed
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.Text)
    
    # Status and result
    status = db.Column(db.String(20), default='success')  # 'success', 'error', 'warning'
    status_code = db.Column(db.Integer)  # HTTP status code
    error_message = db.Column(db.Text)
    
    # Performance metrics
    response_time_ms = db.Column(db.Float)  # Response time in milliseconds
    memory_usage_mb = db.Column(db.Float)  # Memory usage in MB
    
    # Session information
    session_id = db.Column(db.String(100))
    device_type = db.Column(db.String(20))  # 'mobile', 'desktop', 'tablet'
    platform = db.Column(db.String(50))  # 'android', 'ios', 'web', 'flutter'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='activity_logs')
    
    def __repr__(self):
        return f'<UserActivityLog {self.activity_type} - {self.user_id}>'
    
    def to_dict(self):
        """Convert activity log to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'activity_category': self.activity_category,
            'description': self.description,
            'details': self.details,
            'request_method': self.request_method,
            'endpoint': self.endpoint,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'status': self.status,
            'status_code': self.status_code,
            'error_message': self.error_message,
            'response_time_ms': self.response_time_ms,
            'memory_usage_mb': self.memory_usage_mb,
            'session_id': self.session_id,
            'device_type': self.device_type,
            'platform': self.platform,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    @log_database_operation
    def log_activity(user_id, activity_type, activity_category, description, 
                    details=None, request_method=None, endpoint=None, 
                    ip_address=None, user_agent=None, status='success', 
                    status_code=None, error_message=None, response_time_ms=None,
                    memory_usage_mb=None, session_id=None, device_type=None, platform=None):
        """Log a user activity"""
        logger = get_logger('models.user_activity_log')
        logger.info(f"Logging activity for user {user_id}: {activity_type}")
        
        try:
            activity = UserActivityLog(
                user_id=user_id,
                activity_type=activity_type,
                activity_category=activity_category,
                description=description,
                details=details,
                request_method=request_method,
                endpoint=endpoint,
                ip_address=ip_address,
                user_agent=user_agent,
                status=status,
                status_code=status_code,
                error_message=error_message,
                response_time_ms=response_time_ms,
                memory_usage_mb=memory_usage_mb,
                session_id=session_id,
                device_type=device_type,
                platform=platform
            )
            
            db.session.add(activity)
            db.session.commit()
            
            logger.success(f"Activity logged successfully: {activity.id}")
            return activity
            
        except Exception as e:
            logger.error(f"Failed to log activity: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    @log_database_operation
    def get_user_activities(user_id, activity_type=None, limit=100, days=30):
        """Get user activities"""
        logger = get_logger('models.user_activity_log')
        logger.info(f"Getting activities for user {user_id}")
        
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = UserActivityLog.query.filter(
            UserActivityLog.user_id == user_id,
            UserActivityLog.created_at >= cutoff_date
        )
        
        if activity_type:
            query = query.filter_by(activity_type=activity_type)
        
        activities = query.order_by(UserActivityLog.created_at.desc()).limit(limit).all()
        
        logger.success(f"Found {len(activities)} activities for user {user_id}")
        return activities
    
    @staticmethod
    @log_database_operation
    def get_activity_statistics(user_id=None, days=30):
        """Get activity statistics"""
        logger = get_logger('models.user_activity_log')
        logger.info(f"Getting activity statistics for last {days} days")
        
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = UserActivityLog.query.filter(UserActivityLog.created_at >= cutoff_date)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        activities = query.all()
        
        stats = {
            'total_activities': len(activities),
            'activities_by_type': {},
            'activities_by_category': {},
            'success_rate': 0,
            'avg_response_time': 0,
            'daily_activities': {},
            'device_breakdown': {},
            'platform_breakdown': {}
        }
        
        success_count = 0
        total_response_time = 0
        response_count = 0
        
        for activity in activities:
            # Count by type
            stats['activities_by_type'][activity.activity_type] = \
                stats['activities_by_type'].get(activity.activity_type, 0) + 1
            
            # Count by category
            stats['activities_by_category'][activity.activity_category] = \
                stats['activities_by_category'].get(activity.activity_category, 0) + 1
            
            # Count by day
            day = activity.created_at.strftime('%Y-%m-%d')
            stats['daily_activities'][day] = stats['daily_activities'].get(day, 0) + 1
            
            # Device breakdown
            if activity.device_type:
                stats['device_breakdown'][activity.device_type] = \
                    stats['device_breakdown'].get(activity.device_type, 0) + 1
            
            # Platform breakdown
            if activity.platform:
                stats['platform_breakdown'][activity.platform] = \
                    stats['platform_breakdown'].get(activity.platform, 0) + 1
            
            # Success rate
            if activity.status == 'success':
                success_count += 1
            
            # Response time
            if activity.response_time_ms:
                total_response_time += activity.response_time_ms
                response_count += 1
        
        # Calculate rates
        if activities:
            stats['success_rate'] = (success_count / len(activities)) * 100
        
        if response_count > 0:
            stats['avg_response_time'] = total_response_time / response_count
        
        logger.success(f"Activity statistics calculated: {stats['total_activities']} total activities")
        return stats
    
    @staticmethod
    @log_database_operation
    def get_recommendation_requests(user_id=None, days=30):
        """Get recommendation request activities"""
        logger = get_logger('models.user_activity_log')
        logger.info(f"Getting recommendation requests for last {days} days")
        
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = UserActivityLog.query.filter(
            UserActivityLog.activity_type.in_(['recommendation_request', 'crop_recommendation', 'environment_recommendation']),
            UserActivityLog.created_at >= cutoff_date
        )
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        requests = query.order_by(UserActivityLog.created_at.desc()).all()
        
        logger.success(f"Found {len(requests)} recommendation requests")
        return requests
    
    @staticmethod
    @log_database_operation
    def cleanup_old_logs(days_to_keep=90):
        """Clean up old activity logs"""
        logger = get_logger('models.user_activity_log')
        logger.info(f"Cleaning up activity logs older than {days_to_keep} days")
        
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        old_logs = UserActivityLog.query.filter(UserActivityLog.created_at < cutoff_date).all()
        count = len(old_logs)
        
        for log in old_logs:
            db.session.delete(log)
        
        db.session.commit()
        
        logger.success(f"Cleaned up {count} old activity logs")
        return count
