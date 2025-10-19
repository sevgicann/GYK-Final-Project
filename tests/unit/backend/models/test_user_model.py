"""
Unit tests for User model

Bu test dosyası User modeli için birim testlerini içerir.
"""

import pytest
from datetime import datetime
from werkzeug.security import check_password_hash
from models.user import User
from tests.fixtures.data.sample_data import SAMPLE_USERS


class TestUserModel:
    """User model test sınıfı."""
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_creation(self, db_session):
        """Test user creation with valid data."""
        user_data = SAMPLE_USERS[0]
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            language=user_data['language']
        )
        user.set_password(user_data['password'])
        
        db_session.add(user)
        db_session.commit()
        
        # Verify user was created
        assert user.id is not None
        assert user.name == user_data['name']
        assert user.email == user_data['email']
        assert user.language == user_data['language']
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_password_hashing(self, db_session):
        """Test password hashing and verification."""
        user_data = SAMPLE_USERS[0]
        user = User(
            name=user_data['name'],
            email=user_data['email']
        )
        
        # Test password setting
        user.set_password(user_data['password'])
        assert user.password_hash is not None
        assert user.password_hash != user_data['password']  # Should be hashed
        
        # Test password verification
        assert user.check_password(user_data['password']) is True
        assert user.check_password('wrong_password') is False
    
    @pytest.mark.unit
    def test_user_password_check_with_empty_password(self):
        """Test password check with empty password."""
        user = User(name="Test", email="test@example.com")
        user.set_password("password123")
        
        # Empty password should return False
        assert user.check_password("") is False
        assert user.check_password(None) is False
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_email_uniqueness(self, db_session):
        """Test that email must be unique."""
        user_data = SAMPLE_USERS[0]
        
        # Create first user
        user1 = User(
            name=user_data['name'],
            email=user_data['email']
        )
        user1.set_password(user_data['password'])
        db_session.add(user1)
        db_session.commit()
        
        # Try to create second user with same email
        user2 = User(
            name="Another User",
            email=user_data['email']  # Same email
        )
        user2.set_password("another_password")
        db_session.add(user2)
        
        # Should raise IntegrityError
        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            db_session.commit()
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_find_by_email(self, db_session):
        """Test finding user by email."""
        user_data = SAMPLE_USERS[0]
        user = User(
            name=user_data['name'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        
        db_session.add(user)
        db_session.commit()
        
        # Test finding by email
        found_user = User.find_by_email(user_data['email'])
        assert found_user is not None
        assert found_user.email == user_data['email']
        
        # Test finding non-existent email
        not_found = User.find_by_email('nonexistent@example.com')
        assert not_found is None
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_find_by_id(self, db_session):
        """Test finding user by ID."""
        user_data = SAMPLE_USERS[0]
        user = User(
            name=user_data['name'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        
        db_session.add(user)
        db_session.commit()
        
        # Test finding by ID
        found_user = User.find_by_id(user.id)
        assert found_user is not None
        assert found_user.id == user.id
        
        # Test finding non-existent ID
        not_found = User.find_by_id('non-existent-id')
        assert not_found is None
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_generate_token(self, db_session):
        """Test JWT token generation."""
        user_data = SAMPLE_USERS[0]
        user = User(
            name=user_data['name'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        
        db_session.add(user)
        db_session.commit()
        
        # Test token generation
        token = user.generate_token()
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_update_last_login(self, db_session):
        """Test updating last login timestamp."""
        user_data = SAMPLE_USERS[0]
        user = User(
            name=user_data['name'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        
        db_session.add(user)
        db_session.commit()
        
        # Initial last_login should be None
        assert user.last_login is None
        
        # Update last login
        user.update_last_login()
        
        # Verify last_login was updated
        assert user.last_login is not None
        assert isinstance(user.last_login, datetime)
        
        # Verify it's recent (within last minute)
        now = datetime.utcnow()
        time_diff = (now - user.last_login).total_seconds()
        assert time_diff < 60  # Less than 1 minute
    
    @pytest.mark.unit
    def test_user_to_dict(self):
        """Test converting user to dictionary."""
        user = User(
            name="Test User",
            email="test@example.com",
            language="tr",
            city="Istanbul",
            district="Kadıköy",
            latitude=41.0082,
            longitude=29.0156,
            is_gps_enabled=True,
            notifications_enabled=True,
            theme="dark"
        )
        user.set_password("password123")
        
        user_dict = user.to_dict()
        
        # Verify dictionary structure
        assert isinstance(user_dict, dict)
        assert user_dict['name'] == "Test User"
        assert user_dict['email'] == "test@example.com"
        assert user_dict['language'] == "tr"
        assert user_dict['is_active'] is True
        assert 'created_at' in user_dict
        assert 'updated_at' in user_dict
        
        # Verify location data
        assert 'location' in user_dict
        assert user_dict['location']['city'] == "Istanbul"
        assert user_dict['location']['district'] == "Kadıköy"
        assert user_dict['location']['latitude'] == 41.0082
        assert user_dict['location']['longitude'] == 29.0156
        assert user_dict['location']['is_gps_enabled'] is True
        
        # Verify preferences
        assert 'preferences' in user_dict
        assert user_dict['preferences']['notifications_enabled'] is True
        assert user_dict['preferences']['theme'] == "dark"
        
        # Verify password is not included
        assert 'password' not in user_dict
        assert 'password_hash' not in user_dict
    
    @pytest.mark.unit
    def test_user_to_dict_public(self):
        """Test converting user to public dictionary."""
        user = User(
            name="Test User",
            email="test@example.com",
            language="tr",
            city="Istanbul",
            district="Kadıköy",
            is_gps_enabled=True
        )
        user.set_password("password123")
        
        public_dict = user.to_dict_public()
        
        # Verify public dictionary structure
        assert isinstance(public_dict, dict)
        assert public_dict['name'] == "Test User"
        assert public_dict['language'] == "tr"
        
        # Verify location data
        assert 'location' in public_dict
        assert public_dict['location']['city'] == "Istanbul"
        assert public_dict['location']['district'] == "Kadıköy"
        assert public_dict['location']['is_gps_enabled'] is True
        
        # Verify sensitive data is not included
        assert 'email' not in public_dict
        assert 'password' not in public_dict
        assert 'password_hash' not in public_dict
        assert 'preferences' not in public_dict
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_repr(self, db_session):
        """Test user string representation."""
        user_data = SAMPLE_USERS[0]
        user = User(
            name=user_data['name'],
            email=user_data['email']
        )
        
        repr_string = repr(user)
        assert isinstance(repr_string, str)
        assert user_data['email'] in repr_string
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_required_fields(self, db_session):
        """Test that required fields are enforced."""
        # Test missing name
        with pytest.raises(Exception):
            user = User(email="test@example.com")
            db_session.add(user)
            db_session.commit()
        
        # Test missing email
        with pytest.raises(Exception):
            user = User(name="Test User")
            db_session.add(user)
            db_session.commit()
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_default_values(self, db_session):
        """Test default values for user fields."""
        user = User(
            name="Test User",
            email="test@example.com"
        )
        user.set_password("password123")
        
        db_session.add(user)
        db_session.commit()
        
        # Verify default values
        assert user.language == 'tr'  # Default language
        assert user.is_active is True  # Default active status
        assert user.is_gps_enabled is False  # Default GPS disabled
        assert user.notifications_enabled is True  # Default notifications enabled
        assert user.theme == 'light'  # Default theme
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_user_relationships(self, db_session):
        """Test user relationships with other models."""
        user_data = SAMPLE_USERS[0]
        user = User(
            name=user_data['name'],
            email=user_data['email']
        )
        user.set_password(user_data['password'])
        
        db_session.add(user)
        db_session.commit()
        
        # Test relationships exist
        assert hasattr(user, 'environments')
        assert hasattr(user, 'recommendations')
        
        # Test relationships are empty initially
        assert len(user.environments) == 0
        assert len(user.recommendations) == 0
