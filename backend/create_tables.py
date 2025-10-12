#!/usr/bin/env python3
"""
Database table creation script for Terramind application
This script creates all necessary tables in the PostgreSQL database
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_database_tables():
    """Create all database tables"""
    
    # Database connection settings
    # Update these according to your PostgreSQL setup
    DB_HOST = os.getenv('DB_HOST', 'db')  # Docker service name
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'terramind_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'pass.123')
    
    # Create database URL
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    print(f"🔗 Connecting to database: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    print(f"👤 Using user: {DB_USER}")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")
        
        # Import Flask app to get models
        from app import app, db
        
        with app.app_context():
            print("📋 Creating database tables...")
            
            # Create all tables
            db.create_all()
            
            print("✅ All tables created successfully!")
            
            # List created tables
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """))
                tables = [row[0] for row in result.fetchall()]
                
                print(f"📊 Created {len(tables)} tables:")
                for table in tables:
                    print(f"   - {table}")
            
            # Insert sample data
            insert_sample_data()
            
    except SQLAlchemyError as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def insert_sample_data():
    """Insert sample data for testing"""
    print("\n🌱 Inserting sample data...")
    
    try:
        from app import db
        from models.user import User
        from models.product import Product, ProductRequirements
        from models.environment import Environment, EnvironmentData
        from models.recommendation import Recommendation
        
        # Create sample user
        user = User(
            name="Test User",
            email="test@example.com",
            language="tr",
            city="İstanbul",
            district="Kadıköy",
            latitude=41.0082,
            longitude=28.9784,
            is_gps_enabled=True
        )
        user.set_password("123456")
        
        # Create sample products
        products = [
            Product(
                name="Domates",
                category="Sebze",
                description="Sera domates yetiştiriciliği için uygun",
                image_url="/images/tomato.jpg"
            ),
            Product(
                name="Biber",
                category="Sebze", 
                description="Dolmalık biber yetiştiriciliği",
                image_url="/images/pepper.jpg"
            ),
            Product(
                name="Çilek",
                category="Meyve",
                description="Sera çilek yetiştiriciliği",
                image_url="/images/strawberry.jpg"
            ),
            Product(
                name="Salatalık",
                category="Sebze",
                description="Sera salatalık yetiştiriciliği",
                image_url="/images/cucumber.jpg"
            )
        ]
        
        # Create product requirements
        requirements_data = [
            # Domates
            {
                'ph_min': 6.0, 'ph_max': 6.8,
                'temperature_min': 18.0, 'temperature_max': 25.0,
                'humidity_min': 60.0, 'humidity_max': 80.0,
                'nitrogen_min': 120.0, 'nitrogen_max': 180.0,
                'phosphorus_min': 60.0, 'phosphorus_max': 90.0,
                'potassium_min': 200.0, 'potassium_max': 300.0
            },
            # Biber
            {
                'ph_min': 6.0, 'ph_max': 6.5,
                'temperature_min': 20.0, 'temperature_max': 28.0,
                'humidity_min': 50.0, 'humidity_max': 70.0,
                'nitrogen_min': 100.0, 'nitrogen_max': 150.0,
                'phosphorus_min': 50.0, 'phosphorus_max': 80.0,
                'potassium_min': 150.0, 'potassium_max': 250.0
            },
            # Çilek
            {
                'ph_min': 5.5, 'ph_max': 6.5,
                'temperature_min': 15.0, 'temperature_max': 22.0,
                'humidity_min': 70.0, 'humidity_max': 85.0,
                'nitrogen_min': 80.0, 'nitrogen_max': 120.0,
                'phosphorus_min': 40.0, 'phosphorus_max': 70.0,
                'potassium_min': 120.0, 'potassium_max': 200.0
            },
            # Salatalık
            {
                'ph_min': 6.0, 'ph_max': 7.0,
                'temperature_min': 20.0, 'temperature_max': 30.0,
                'humidity_min': 60.0, 'humidity_max': 80.0,
                'nitrogen_min': 100.0, 'nitrogen_max': 160.0,
                'phosphorus_min': 50.0, 'phosphorus_max': 80.0,
                'potassium_min': 150.0, 'potassium_max': 250.0
            }
        ]
        
        # Create sample environment
        environment = Environment(
            user_id=None,  # Will be set after user is saved
            name="Test Bahçe",
            location_type="manual",
            city="İstanbul",
            district="Kadıköy",
            latitude=41.0082,
            longitude=28.9784
        )
        
        # Create environment data
        environment_data = EnvironmentData(
            environment_id=None,  # Will be set after environment is saved
            ph=6.5,
            nitrogen=140.0,
            phosphorus=65.0,
            potassium=220.0,
            organic_matter=3.5,
            soil_type="Tınlı",
            temperature=23.0,
            humidity=70.0,
            rainfall=850.0,
            sunlight_hours=8.5,
            wind_speed=2.5,
            altitude=50.0,
            slope=5.0,
            drainage="good",
            data_source="manual"
        )
        
        # Add to database
        db.session.add(user)
        db.session.flush()  # Get user ID
        
        # Update environment with user_id
        environment.user_id = user.id
        
        # Add products and requirements
        for i, product in enumerate(products):
            db.session.add(product)
            db.session.flush()  # Get product ID
            
            # Create requirements for this product
            req_data = requirements_data[i]
            requirements = ProductRequirements(
                product_id=product.id,
                **req_data,
                notes=f"{product.name} için ideal yetiştirme koşulları"
            )
            db.session.add(requirements)
        
        # Add environment and data
        db.session.add(environment)
        db.session.flush()  # Get environment ID
        
        environment_data.environment_id = environment.id
        db.session.add(environment_data)
        
        # Commit all changes
        db.session.commit()
        
        print("✅ Sample data inserted successfully!")
        print(f"   - 1 user: {user.email}")
        print(f"   - {len(products)} products with requirements")
        print(f"   - 1 environment with data")
        
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        db.session.rollback()

if __name__ == "__main__":
    print("🚀 Terramind Database Setup")
    print("=" * 50)
    
    success = create_database_tables()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("\n📝 Next steps:")
        print("   1. Update your .env file with correct database credentials")
        print("   2. Start your Flask application")
        print("   3. Test the API endpoints")
    else:
        print("\n💥 Database setup failed!")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if PostgreSQL is running")
        print("   2. Verify database credentials")
        print("   3. Ensure database 'terramind_db' exists")
        print("   4. Check network connectivity")
        sys.exit(1)
