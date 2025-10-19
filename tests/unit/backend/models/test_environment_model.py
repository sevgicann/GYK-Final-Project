"""
Unit tests for Environment and EnvironmentData models

Bu test dosyası Environment ve EnvironmentData modelleri için birim testlerini içerir.
"""

import pytest
from datetime import datetime, timedelta
from models.environment import Environment, EnvironmentData
from models.user import User
from tests.fixtures.data.sample_data import SAMPLE_ENVIRONMENTS


class TestEnvironmentModel:
    """Environment model test sınıfı."""
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_creation(self, db_session):
        """Test environment creation with valid data."""
        # Create user first
        user = User(name="Test User", email="test@example.com")
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        # Create environment
        environment_data = SAMPLE_ENVIRONMENTS[0]
        environment = Environment(
            user_id=user.id,
            name="My Garden",
            location_type="manual",
            city=environment_data['region'],
            latitude=41.0082,
            longitude=29.0156
        )
        
        db_session.add(environment)
        db_session.commit()
        
        # Verify environment was created
        assert environment.id is not None
        assert environment.user_id == user.id
        assert environment.name == "My Garden"
        assert environment.location_type == "manual"
        assert environment.city == environment_data['region']
        assert environment.latitude == 41.0082
        assert environment.longitude == 29.0156
        assert environment.is_active is True
        assert environment.created_at is not None
        assert environment.updated_at is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_get_user_environments(self, db_session):
        """Test getting environments for a specific user."""
        # Create users
        user1 = User(name="User 1", email="user1@example.com")
        user1.set_password("password123")
        user2 = User(name="User 2", email="user2@example.com")
        user2.set_password("password123")
        db_session.add_all([user1, user2])
        db_session.commit()
        
        # Create environments for user1
        env1 = Environment(user_id=user1.id, name="Garden 1", location_type="manual")
        env2 = Environment(user_id=user1.id, name="Garden 2", location_type="gps")
        env3 = Environment(user_id=user1.id, name="Garden 3", location_type="manual", is_active=False)
        
        # Create environment for user2
        env4 = Environment(user_id=user2.id, name="Field 1", location_type="manual")
        
        db_session.add_all([env1, env2, env3, env4])
        db_session.commit()
        
        # Test getting user1's active environments
        user1_environments = Environment.get_user_environments(user1.id)
        assert len(user1_environments) == 2  # Only active environments
        assert all(env.user_id == user1.id for env in user1_environments)
        assert all(env.is_active for env in user1_environments)
        
        # Test getting user2's environments
        user2_environments = Environment.get_user_environments(user2.id)
        assert len(user2_environments) == 1
        assert user2_environments[0].name == "Field 1"
    
    @pytest.mark.unit
    def test_environment_to_dict(self):
        """Test converting environment to dictionary."""
        environment = Environment(
            user_id="test-user-id",
            name="Test Environment",
            location_type="gps",
            city="Istanbul",
            district="Kadıköy",
            latitude=41.0082,
            longitude=29.0156,
            is_active=True
        )
        
        env_dict = environment.to_dict()
        
        # Verify dictionary structure
        assert isinstance(env_dict, dict)
        assert env_dict['user_id'] == "test-user-id"
        assert env_dict['name'] == "Test Environment"
        assert env_dict['location_type'] == "gps"
        assert env_dict['is_active'] is True
        
        # Verify location data
        assert 'location' in env_dict
        assert env_dict['location']['city'] == "Istanbul"
        assert env_dict['location']['district'] == "Kadıköy"
        assert env_dict['location']['latitude'] == 41.0082
        assert env_dict['location']['longitude'] == 29.0156
        
        # Verify timestamps
        assert 'created_at' in env_dict
        assert 'updated_at' in env_dict
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_default_values(self, db_session):
        """Test default values for environment fields."""
        # Create user
        user = User(name="Test User", email="test@example.com")
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        # Create environment with minimal data
        environment = Environment(
            user_id=user.id,
            name="Test Environment"
        )
        
        db_session.add(environment)
        db_session.commit()
        
        # Verify default values
        assert environment.location_type == "manual"  # Default location type
        assert environment.is_active is True  # Default active status
        assert environment.created_at is not None
        assert environment.updated_at is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_relationships(self, db_session):
        """Test environment relationships."""
        # Create user and environment
        user = User(name="Test User", email="test@example.com")
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        environment = Environment(user_id=user.id, name="Test Environment")
        db_session.add(environment)
        db_session.commit()
        
        # Test relationship with user
        assert environment.user is not None
        assert environment.user.id == user.id
        
        # Test relationship with environment_data
        assert hasattr(environment, 'environment_data')
        assert len(environment.environment_data) == 0  # Initially empty
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_required_fields(self, db_session):
        """Test that required fields are enforced."""
        # Create user
        user = User(name="Test User", email="test@example.com")
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        # Test missing user_id
        with pytest.raises(Exception):
            environment = Environment(name="Test Environment")
            db_session.add(environment)
            db_session.commit()
        
        # Test missing name
        with pytest.raises(Exception):
            environment = Environment(user_id=user.id)
            db_session.add(environment)
            db_session.commit()


class TestEnvironmentDataModel:
    """EnvironmentData model test sınıfı."""
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_data_creation(self, db_session):
        """Test environment data creation."""
        # Create user and environment
        user = User(name="Test User", email="test@example.com")
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        environment = Environment(user_id=user.id, name="Test Environment")
        db_session.add(environment)
        db_session.commit()
        
        # Create environment data
        env_data = SAMPLE_ENVIRONMENTS[0]
        environment_data = EnvironmentData(
            environment_id=environment.id,
            ph=env_data['soil_ph'],
            nitrogen=env_data['nitrogen'],
            phosphorus=env_data['phosphorus'],
            potassium=env_data['potassium'],
            soil_type=env_data['soil_type'],
            temperature=env_data['temperature_celsius'],
            humidity=env_data['moisture'],
            rainfall=env_data['rainfall_mm'],
            data_source="manual"
        )
        
        db_session.add(environment_data)
        db_session.commit()
        
        # Verify environment data was created
        assert environment_data.id is not None
        assert environment_data.environment_id == environment.id
        assert environment_data.ph == env_data['soil_ph']
        assert environment_data.nitrogen == env_data['nitrogen']
        assert environment_data.phosphorus == env_data['phosphorus']
        assert environment_data.potassium == env_data['potassium']
        assert environment_data.soil_type == env_data['soil_type']
        assert environment_data.temperature == env_data['temperature_celsius']
        assert environment_data.humidity == env_data['moisture']
        assert environment_data.rainfall == env_data['rainfall_mm']
        assert environment_data.data_source == "manual"
        assert environment_data.measured_at is not None
        assert environment_data.created_at is not None
    
    @pytest.mark.unit
    def test_environment_data_to_dict(self):
        """Test converting environment data to dictionary."""
        environment_data = EnvironmentData(
            environment_id="test-env-id",
            ph=6.5,
            nitrogen=90,
            phosphorus=42,
            potassium=43,
            organic_matter=2.5,
            soil_type="Killi Toprak",
            temperature=25,
            humidity=65,
            rainfall=600,
            sunlight_hours=8,
            wind_speed=10,
            altitude=100,
            slope=5,
            drainage="good",
            data_source="sensor"
        )
        
        data_dict = environment_data.to_dict()
        
        # Verify dictionary structure
        assert isinstance(data_dict, dict)
        assert data_dict['environment_id'] == "test-env-id"
        assert data_dict['data_source'] == "sensor"
        assert 'measured_at' in data_dict
        assert 'created_at' in data_dict
        
        # Verify soil data
        assert 'soil' in data_dict
        assert data_dict['soil']['ph'] == 6.5
        assert data_dict['soil']['nitrogen'] == 90
        assert data_dict['soil']['phosphorus'] == 42
        assert data_dict['soil']['potassium'] == 43
        assert data_dict['soil']['organic_matter'] == 2.5
        assert data_dict['soil']['soil_type'] == "Killi Toprak"
        
        # Verify weather data
        assert 'weather' in data_dict
        assert data_dict['weather']['temperature'] == 25
        assert data_dict['weather']['humidity'] == 65
        assert data_dict['weather']['rainfall'] == 600
        assert data_dict['weather']['sunlight_hours'] == 8
        assert data_dict['weather']['wind_speed'] == 10
        
        # Verify terrain data
        assert 'terrain' in data_dict
        assert data_dict['terrain']['altitude'] == 100
        assert data_dict['terrain']['slope'] == 5
        assert data_dict['terrain']['drainage'] == "good"
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_data_get_latest_data(self, db_session):
        """Test getting latest environment data."""
        # Create user and environment
        user = User(name="Test User", email="test@example.com")
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        environment = Environment(user_id=user.id, name="Test Environment")
        db_session.add(environment)
        db_session.commit()
        
        # Create multiple environment data records with different timestamps
        now = datetime.utcnow()
        old_data = EnvironmentData(
            environment_id=environment.id,
            ph=6.0,
            measured_at=now - timedelta(hours=2)
        )
        new_data = EnvironmentData(
            environment_id=environment.id,
            ph=7.0,
            measured_at=now - timedelta(hours=1)
        )
        
        db_session.add_all([old_data, new_data])
        db_session.commit()
        
        # Test getting latest data
        latest_data = EnvironmentData.get_latest_data(environment.id)
        assert latest_data is not None
        assert latest_data.ph == 7.0  # Should be the newer record
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_data_get_historical_data(self, db_session):
        """Test getting historical environment data."""
        # Create user and environment
        user = User(name="Test User", email="test@example.com")
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        environment = Environment(user_id=user.id, name="Test Environment")
        db_session.add(environment)
        db_session.commit()
        
        # Create environment data with different timestamps
        now = datetime.utcnow()
        old_data1 = EnvironmentData(
            environment_id=environment.id,
            ph=6.0,
            measured_at=now - timedelta(days=40)
        )
        old_data2 = EnvironmentData(
            environment_id=environment.id,
            ph=6.5,
            measured_at=now - timedelta(days=20)
        )
        recent_data = EnvironmentData(
            environment_id=environment.id,
            ph=7.0,
            measured_at=now - timedelta(days=5)
        )
        
        db_session.add_all([old_data1, old_data2, recent_data])
        db_session.commit()
        
        # Test getting historical data (last 30 days)
        historical_data = EnvironmentData.get_historical_data(environment.id, days=30)
        assert len(historical_data) == 2  # Only data within last 30 days
        assert historical_data[0].ph == 7.0  # Should be ordered by date desc
        assert historical_data[1].ph == 6.5
        
        # Test getting historical data (last 10 days)
        recent_historical = EnvironmentData.get_historical_data(environment.id, days=10)
        assert len(recent_historical) == 1
        assert recent_historical[0].ph == 7.0
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_data_default_values(self, db_session):
        """Test default values for environment data fields."""
        # Create user and environment
        user = User(name="Test User", email="test@example.com")
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        environment = Environment(user_id=user.id, name="Test Environment")
        db_session.add(environment)
        db_session.commit()
        
        # Create environment data with minimal data
        environment_data = EnvironmentData(environment_id=environment.id)
        
        db_session.add(environment_data)
        db_session.commit()
        
        # Verify default values
        assert environment_data.data_source == "manual"  # Default data source
        assert environment_data.measured_at is not None  # Should be set automatically
        assert environment_data.created_at is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_data_foreign_key_constraint(self, db_session):
        """Test foreign key constraint for environment data."""
        # Try to create environment data without valid environment_id
        with pytest.raises(Exception):
            environment_data = EnvironmentData(
                environment_id="non-existent-environment-id",
                ph=6.5
            )
            db_session.add(environment_data)
            db_session.commit()
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_environment_cascade_delete(self, db_session):
        """Test cascade delete when environment is deleted."""
        # Create user and environment
        user = User(name="Test User", email="test@example.com")
        user.set_password("password123")
        db_session.add(user)
        db_session.commit()
        
        environment = Environment(user_id=user.id, name="Test Environment")
        db_session.add(environment)
        db_session.commit()
        
        # Create environment data
        environment_data = EnvironmentData(
            environment_id=environment.id,
            ph=6.5,
            nitrogen=90
        )
        db_session.add(environment_data)
        db_session.commit()
        
        # Delete environment
        db_session.delete(environment)
        db_session.commit()
        
        # Verify environment data is also deleted
        remaining_data = EnvironmentData.query.filter_by(environment_id=environment.id).first()
        assert remaining_data is None
