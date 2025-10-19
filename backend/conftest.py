"""
Pytest configuration and fixtures for TerraMind Backend Tests

Bu dosya tüm testler için ortak konfigürasyon ve fixture'ları içerir.
"""

import os
import pytest
import tempfile
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from unittest.mock import patch, MagicMock

# Test environment setup
os.environ['TESTING'] = 'True'
os.environ['FLASK_ENV'] = 'testing'

from app import app, db, jwt


@pytest.fixture(scope='session')
def test_app():
    """Create and configure a test Flask application."""
    # Create a temporary file to serve as the database
    db_fd, db_path = tempfile.mkstemp()
    
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-jwt-secret-key',
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(test_app):
    """Create a test client for the Flask application."""
    return test_app.test_client()


@pytest.fixture
def app_context(test_app):
    """Create an application context for testing."""
    with test_app.app_context():
        yield test_app


@pytest.fixture
def db_session(app_context):
    """Create a database session for testing."""
    yield db.session
    db.session.rollback()


@pytest.fixture
def auth_headers():
    """Create authentication headers for API testing."""
    def _create_headers(token='test-token'):
        return {'Authorization': f'Bearer {token}'}
    return _create_headers


@pytest.fixture
def mock_ml_service():
    """Mock ML service for testing."""
    with patch('services.ml_service.MLService') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        
        # Mock prediction methods
        mock_instance.predict_crop.return_value = {
            'success': True,
            'data': {
                'recommendations': [
                    {'crop': 'wheat', 'confidence': 0.85},
                    {'crop': 'corn', 'confidence': 0.72}
                ]
            }
        }
        
        mock_instance.predict_environment.return_value = {
            'success': True,
            'data': {
                'optimal_conditions': {
                    'temperature': 25,
                    'humidity': 70,
                    'ph': 6.5
                }
            }
        }
        
        yield mock_instance


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'phone': '+905551234567',
        'language': 'tr'
    }


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        'name': 'Test Product',
        'category': 'Test Category',
        'description': 'Test Description',
        'requirements': {
            'ph': '6.0-7.0',
            'nitrogen': '100-150',
            'phosphorus': '40-60',
            'potassium': '120-200',
            'humidity': '60-80',
            'temperature': '20-25',
            'rainfall': '500-800',
            'notes': 'Test notes'
        }
    }


@pytest.fixture
def sample_environment_data():
    """Sample environment data for testing."""
    return {
        'region': 'Marmara',
        'soil_type': 'Killi Toprak',
        'soil_ph': 6.5,
        'nitrogen': 90,
        'phosphorus': 42,
        'potassium': 43,
        'moisture': 65,
        'temperature_celsius': 25,
        'rainfall_mm': 600,
        'fertilizer_type': 'Amonyum Sülfat',
        'irrigation_method': 'Damla Sulama',
        'weather_condition': 'Güneşli'
    }


@pytest.fixture(autouse=True)
def reset_database(db_session):
    """Reset database before each test."""
    # Clean up all tables
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    yield
    # Clean up after test
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()


# Custom markers for test categorization
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "security: mark test as a security test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "ml: mark test as machine learning test")
    config.addinivalue_line("markers", "auth: mark test as authentication test")
    config.addinivalue_line("markers", "api: mark test as API test")
    config.addinivalue_line("markers", "database: mark test as database test")
