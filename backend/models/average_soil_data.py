from app import db
from datetime import datetime
import uuid
from utils.logger import log_database_operation, log_function_call, get_logger

class AverageSoilData(db.Model):
    """Master table for average soil data based on environmental conditions"""
    __tablename__ = 'average_soil_data'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Environmental conditions (grouping keys)
    soil_type = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    fertilizer_type = db.Column(db.String(50), nullable=False)
    irrigation_method = db.Column(db.String(50), nullable=False)
    weather_condition = db.Column(db.String(50), nullable=False)
    
    # Average soil parameters
    avg_soil_ph = db.Column(db.Numeric(5, 2), nullable=False)
    avg_nitrogen = db.Column(db.Numeric(8, 2), nullable=False)
    avg_phosphorus = db.Column(db.Numeric(8, 2), nullable=False)
    avg_potassium = db.Column(db.Numeric(8, 2), nullable=False)
    avg_moisture = db.Column(db.Numeric(5, 2), nullable=False)
    avg_temperature_celsius = db.Column(db.Numeric(5, 2), nullable=False)
    avg_rainfall_mm = db.Column(db.Numeric(8, 2), nullable=False)
    
    # Metadata
    data_count = db.Column(db.Integer, default=1)  # Number of records used for average
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicates
    __table_args__ = (
        db.UniqueConstraint('soil_type', 'region', 'fertilizer_type', 'irrigation_method', 'weather_condition', 
                          name='unique_environmental_conditions'),
    )
    
    def __repr__(self):
        return f'<AverageSoilData {self.region}-{self.soil_type}>'
    
    def to_dict(self):
        """Convert average soil data to dictionary"""
        return {
            'id': self.id,
            'environmental_conditions': {
                'soil_type': self.soil_type,
                'region': self.region,
                'fertilizer_type': self.fertilizer_type,
                'irrigation_method': self.irrigation_method,
                'weather_condition': self.weather_condition
            },
            'average_values': {
                'ph': float(self.avg_soil_ph),
                'nitrogen': float(self.avg_nitrogen),
                'phosphorus': float(self.avg_phosphorus),
                'potassium': float(self.avg_potassium),
                'moisture': float(self.avg_moisture),
                'temperature_celsius': float(self.avg_temperature_celsius),
                'rainfall_mm': float(self.avg_rainfall_mm)
            },
            'metadata': {
                'data_count': self.data_count,
                'last_updated': self.last_updated.isoformat(),
                'created_at': self.created_at.isoformat()
            }
        }
    
    @staticmethod
    @log_database_operation
    def get_average_data(soil_type=None, region=None, fertilizer_type=None, 
                        irrigation_method=None, weather_condition=None):
        """Get average soil data based on environmental conditions"""
        logger = get_logger('models.average_soil_data')
        
        try:
            query = AverageSoilData.query
            
            # Apply filters if provided
            if soil_type:
                query = query.filter(AverageSoilData.soil_type == soil_type)
            if region:
                query = query.filter(AverageSoilData.region == region)
            if fertilizer_type:
                query = query.filter(AverageSoilData.fertilizer_type == fertilizer_type)
            if irrigation_method:
                query = query.filter(AverageSoilData.irrigation_method == irrigation_method)
            if weather_condition:
                query = query.filter(AverageSoilData.weather_condition == weather_condition)
            
            results = query.all()
            
            logger.info(f"Found {len(results)} average soil data records")
            return results
            
        except Exception as e:
            logger.error(f"Error getting average soil data: {e}")
            return []
    
    @staticmethod
    @log_database_operation
    def get_best_match(soil_type=None, region=None, fertilizer_type=None, 
                      irrigation_method=None, weather_condition=None):
        """Get the best matching average soil data with fallback logic"""
        logger = get_logger('models.average_soil_data')
        
        try:
            # Try exact match first
            exact_match = AverageSoilData.query.filter(
                AverageSoilData.soil_type == soil_type,
                AverageSoilData.region == region,
                AverageSoilData.fertilizer_type == fertilizer_type,
                AverageSoilData.irrigation_method == irrigation_method,
                AverageSoilData.weather_condition == weather_condition
            ).first()
            
            if exact_match:
                logger.info("Found exact match for average soil data")
                return exact_match
            
            # Try partial matches with priority order
            fallback_queries = [
                # Match by region and soil type
                AverageSoilData.query.filter(
                    AverageSoilData.region == region,
                    AverageSoilData.soil_type == soil_type
                ),
                # Match by region only
                AverageSoilData.query.filter(
                    AverageSoilData.region == region
                ),
                # Match by soil type only
                AverageSoilData.query.filter(
                    AverageSoilData.soil_type == soil_type
                ),
                # Get any record as last resort
                AverageSoilData.query
            ]
            
            for query in fallback_queries:
                result = query.first()
                if result:
                    logger.info(f"Found fallback match for average soil data: {result.region}-{result.soil_type}")
                    return result
            
            logger.warning("No average soil data found, even with fallback")
            return None
            
        except Exception as e:
            logger.error(f"Error getting best match for average soil data: {e}")
            return None
    
    @staticmethod
    @log_database_operation
    def get_default_averages():
        """Get default average values when no specific match is found"""
        logger = get_logger('models.average_soil_data')
        
        try:
            # Get any record to use as default
            default_record = AverageSoilData.query.first()
            
            if default_record:
                logger.info("Using existing record as default average")
                return default_record
            
            # If no records exist, return hardcoded defaults
            logger.warning("No average soil data records found, using hardcoded defaults")
            return {
                'ph': 6.5,
                'nitrogen': 120.0,
                'phosphorus': 60.0,
                'potassium': 225.0,
                'moisture': 26.0,
                'temperature_celsius': 23.0,
                'rainfall_mm': 850.0
            }
            
        except Exception as e:
            logger.error(f"Error getting default averages: {e}")
            return {
                'ph': 6.5,
                'nitrogen': 120.0,
                'phosphorus': 60.0,
                'potassium': 225.0,
                'moisture': 26.0,
                'temperature_celsius': 23.0,
                'rainfall_mm': 850.0
            }
    
    @staticmethod
    @log_database_operation
    def bulk_insert_from_sql_result(sql_results):
        """Bulk insert average soil data from SQL query results"""
        logger = get_logger('models.average_soil_data')
        
        try:
            records_to_insert = []
            
            for row in sql_results:
                record = AverageSoilData(
                    soil_type=row['soil_type'],
                    region=row['region'],
                    fertilizer_type=row['fertilizer_type'],
                    irrigation_method=row['irrigation_method'],
                    weather_condition=row['weather_condition'],
                    avg_soil_ph=row['avg_soil_ph'],
                    avg_nitrogen=row['avg_nitrogen'],
                    avg_phosphorus=row['avg_phosphorus'],
                    avg_potassium=row['avg_potassium'],
                    avg_moisture=row['avg_moisture'],
                    avg_temperature_celsius=row['avg_temperature_celsius'],
                    avg_rainfall_mm=row['avg_rainfall_mm']
                )
                records_to_insert.append(record)
            
            # Clear existing data first
            AverageSoilData.query.delete()
            db.session.commit()
            
            # Insert new data
            db.session.bulk_save_objects(records_to_insert)
            db.session.commit()
            
            logger.info(f"Successfully inserted {len(records_to_insert)} average soil data records")
            return True
            
        except Exception as e:
            logger.error(f"Error bulk inserting average soil data: {e}")
            db.session.rollback()
            return False
