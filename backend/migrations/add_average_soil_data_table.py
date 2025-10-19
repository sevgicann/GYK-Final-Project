#!/usr/bin/env python3
"""
Migration script to add average_soil_data table
Run this script to create the average_soil_data table and populate it with data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.average_soil_data import AverageSoilData
from utils.logger import get_logger

def create_average_soil_data_table():
    """Create the average_soil_data table"""
    logger = get_logger('migration.average_soil_data')
    
    try:
        with app.app_context():
            # Create the table
            db.create_all()
            logger.info("average_soil_data table created successfully")
            return True
    except Exception as e:
        logger.error(f"Error creating average_soil_data table: {e}")
        return False

def populate_average_soil_data():
    """Populate the average_soil_data table with data from crop_dataset"""
    logger = get_logger('migration.average_soil_data')
    
    try:
        with app.app_context():
            # Execute the SQL query to get average data
            sql_query = """
            SELECT
                soil_type,
                region,
                fertilizer_type,
                irrigation_method,
                weather_condition,
                AVG("soil_ph"::numeric) AS avg_soil_ph,
                AVG("nitrogen"::numeric) AS avg_nitrogen,
                AVG("phosphorus"::numeric) AS avg_phosphorus,
                AVG("potassium"::numeric) AS avg_potassium,
                AVG("moisture"::numeric) AS avg_moisture,
                AVG("temperature_celsius"::numeric) AS avg_temperature_celsius,
                AVG("rainfall_mm"::numeric) AS avg_rainfall_mm
            FROM
                crop_dataset
            GROUP BY
                soil_type,
                region,
                fertilizer_type,
                irrigation_method,
                weather_condition
            ORDER BY
                region ASC,
                soil_type ASC,
                fertilizer_type ASC,
                irrigation_method ASC,
                weather_condition ASC
            """
            
            from sqlalchemy import text
            result = db.session.execute(text(sql_query))
            sql_results = [row._asdict() for row in result]
            
            logger.info(f"SQL query returned {len(sql_results)} records")
            
            # Bulk insert the results
            success = AverageSoilData.bulk_insert_from_sql_result(sql_results)
            
            if success:
                logger.info(f"Successfully populated average_soil_data table with {len(sql_results)} records")
                return True
            else:
                logger.error("Failed to populate average_soil_data table")
                return False
                
    except Exception as e:
        logger.error(f"Error populating average_soil_data table: {e}")
        return False

def main():
    """Main migration function"""
    logger = get_logger('migration.average_soil_data')
    
    logger.info("Starting average_soil_data table migration...")
    
    # Step 1: Create table
    logger.info("Step 1: Creating average_soil_data table...")
    if not create_average_soil_data_table():
        logger.error("Migration failed at table creation step")
        return False
    
    # Step 2: Populate table
    logger.info("Step 2: Populating average_soil_data table...")
    if not populate_average_soil_data():
        logger.error("Migration failed at data population step")
        return False
    
    logger.info("Migration completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
