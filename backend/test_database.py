#!/usr/bin/env python3
"""
Database test script for Terramind
This script tests the database functionality and new models
"""

import os
import sys
from datetime import datetime
from flask import Flask
from app import app, db
from models.user import User
from models.product import Product, ProductRequirements
from models.environment import Environment, EnvironmentData
from models.recommendation import Recommendation
from models.model_results import ModelResult
from models.user_activity_log import UserActivityLog
from utils.logger import get_logger, log_info, log_error, log_success

# Initialize logger
logger = get_logger('test_database')

def test_database_connection():
    """Test database connection"""
    try:
        log_info("Testing database connection...")
        with app.app_context():
            db.engine.execute('SELECT 1')
        log_success("Database connection successful")
        return True
    except Exception as e:
        log_error(f"Database connection failed: {str(e)}")
        return False

def test_user_operations():
    """Test user operations"""
    try:
        log_info("Testing user operations...")
        with app.app_context():
            # Create test user
            test_user = User(
                name="Test User",
                email="test@example.com",
                language="tr",
                city="Ankara",
                district="Çankaya",
                latitude=39.9334,
                longitude=32.8597
            )
            test_user.set_password("testpassword123")
            
            db.session.add(test_user)
            db.session.commit()
            
            # Test password check
            assert test_user.check_password("testpassword123")
            assert not test_user.check_password("wrongpassword")
            
            # Test token generation
            token = test_user.generate_token()
            assert token is not None
            
            # Test user lookup
            found_user = User.find_by_email("test@example.com")
            assert found_user is not None
            assert found_user.email == "test@example.com"
            
            # Clean up
            db.session.delete(test_user)
            db.session.commit()
            
        log_success("User operations test passed")
        return True
    except Exception as e:
        log_error(f"User operations test failed: {str(e)}")
        return False

def test_product_operations():
    """Test product operations"""
    try:
        log_info("Testing product operations...")
        with app.app_context():
            # Create test product
            test_product = Product(
                name="Test Wheat",
                category="Cereals",
                description="Test wheat variety",
                image_url="https://example.com/wheat.jpg"
            )
            
            db.session.add(test_product)
            db.session.commit()
            
            # Create product requirements
            requirements = ProductRequirements(
                product_id=test_product.id,
                ph_min=6.0,
                ph_max=7.5,
                temperature_min=15.0,
                temperature_max=25.0,
                humidity_min=40.0,
                humidity_max=70.0
            )
            
            db.session.add(requirements)
            db.session.commit()
            
            # Test product lookup
            found_product = Product.query.filter_by(name="Test Wheat").first()
            assert found_product is not None
            assert found_product.requirements is not None
            
            # Test category search
            cereals = Product.get_by_category("Cereals")
            assert len(cereals) > 0
            
            # Clean up
            db.session.delete(requirements)
            db.session.delete(test_product)
            db.session.commit()
            
        log_success("Product operations test passed")
        return True
    except Exception as e:
        log_error(f"Product operations test failed: {str(e)}")
        return False

def test_model_result_operations():
    """Test model result operations"""
    try:
        log_info("Testing model result operations...")
        with app.app_context():
            # Create test user first
            test_user = User(
                name="Test User",
                email="test@example.com",
                language="tr"
            )
            test_user.set_password("testpassword123")
            db.session.add(test_user)
            db.session.commit()
            
            # Create test model result
            input_data = {
                "ph": 6.5,
                "temperature": 20.0,
                "humidity": 60.0,
                "nitrogen": 50.0
            }
            
            predictions = {
                "wheat": 0.85,
                "barley": 0.72,
                "corn": 0.68
            }
            
            model_result = ModelResult.create_result(
                user_id=test_user.id,
                model_type="crop_recommendation",
                model_version="v1.0",
                algorithm="lightgbm",
                input_data=input_data,
                predictions=predictions,
                confidence_scores={"wheat": 0.9, "barley": 0.8, "corn": 0.7},
                processing_time_ms=150.5
            )
            
            # Test model result lookup
            user_results = ModelResult.get_user_results(test_user.id)
            assert len(user_results) > 0
            
            # Test statistics
            stats = ModelResult.get_model_statistics()
            assert stats['total_requests'] > 0
            
            # Clean up
            db.session.delete(model_result)
            db.session.delete(test_user)
            db.session.commit()
            
        log_success("Model result operations test passed")
        return True
    except Exception as e:
        log_error(f"Model result operations test failed: {str(e)}")
        return False

def test_activity_log_operations():
    """Test activity log operations"""
    try:
        log_info("Testing activity log operations...")
        with app.app_context():
            # Create test user first
            test_user = User(
                name="Test User",
                email="test@example.com",
                language="tr"
            )
            test_user.set_password("testpassword123")
            db.session.add(test_user)
            db.session.commit()
            
            # Create test activity log
            activity = UserActivityLog.log_activity(
                user_id=test_user.id,
                activity_type="login",
                activity_category="authentication",
                description="User logged in",
                ip_address="192.168.1.1",
                user_agent="Mozilla/5.0...",
                device_type="desktop",
                platform="web"
            )
            
            # Test activity lookup
            user_activities = UserActivityLog.get_user_activities(test_user.id)
            assert len(user_activities) > 0
            
            # Test statistics
            stats = UserActivityLog.get_activity_statistics(test_user.id)
            assert stats['total_activities'] > 0
            
            # Clean up
            db.session.delete(activity)
            db.session.delete(test_user)
            db.session.commit()
            
        log_success("Activity log operations test passed")
        return True
    except Exception as e:
        log_error(f"Activity log operations test failed: {str(e)}")
        return False

def test_recommendation_operations():
    """Test recommendation operations"""
    try:
        log_info("Testing recommendation operations...")
        with app.app_context():
            # Create test user
            test_user = User(
                name="Test User",
                email="test@example.com",
                language="tr"
            )
            test_user.set_password("testpassword123")
            db.session.add(test_user)
            
            # Create test product
            test_product = Product(
                name="Test Wheat",
                category="Cereals",
                description="Test wheat variety"
            )
            db.session.add(test_product)
            
            # Create test environment
            test_environment = Environment(
                user_id=test_user.id,
                name="Test Field",
                city="Ankara",
                district="Çankaya"
            )
            db.session.add(test_environment)
            
            db.session.commit()
            
            # Create test recommendation
            recommendation = Recommendation(
                user_id=test_user.id,
                product_id=test_product.id,
                environment_id=test_environment.id,
                recommendation_type="product_to_environment",
                confidence_score=0.85,
                suitability_score=0.80,
                model_type="crop_recommendation",
                model_version="v1.0",
                algorithm="lightgbm",
                title="Wheat Recommendation",
                description="Wheat is suitable for this environment",
                benefits="High yield potential",
                challenges="Requires regular watering"
            )
            
            db.session.add(recommendation)
            db.session.commit()
            
            # Test recommendation lookup
            user_recommendations = Recommendation.get_user_recommendations(test_user.id)
            assert len(user_recommendations) > 0
            
            # Test view count increment
            recommendation.increment_view_count()
            assert recommendation.view_count == 1
            
            # Test statistics
            stats = Recommendation.get_recommendation_statistics(test_user.id)
            assert stats['total_recommendations'] > 0
            
            # Clean up
            db.session.delete(recommendation)
            db.session.delete(test_environment)
            db.session.delete(test_product)
            db.session.delete(test_user)
            db.session.commit()
            
        log_success("Recommendation operations test passed")
        return True
    except Exception as e:
        log_error(f"Recommendation operations test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    log_info("Starting database tests...")
    
    tests = [
        ("Database Connection", test_database_connection),
        ("User Operations", test_user_operations),
        ("Product Operations", test_product_operations),
        ("Model Result Operations", test_model_result_operations),
        ("Activity Log Operations", test_activity_log_operations),
        ("Recommendation Operations", test_recommendation_operations)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        log_info(f"Running test: {test_name}")
        try:
            if test_func():
                passed += 1
                log_success(f"✅ {test_name} PASSED")
            else:
                failed += 1
                log_error(f"❌ {test_name} FAILED")
        except Exception as e:
            failed += 1
            log_error(f"❌ {test_name} FAILED with exception: {str(e)}")
    
    log_info(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        log_success("All tests passed! 🎉")
        return True
    else:
        log_error(f"{failed} tests failed! ❌")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        success = run_all_tests()
        sys.exit(0 if success else 1)
    else:
        print("Usage: python test_database.py test")
        print("This will run all database tests")

if __name__ == "__main__":
    main()
