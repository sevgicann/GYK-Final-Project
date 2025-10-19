"""
User Factory for creating test users

Bu modül test kullanıcıları oluşturmak için factory fonksiyonları içerir.
"""

import factory
from factory.fuzzy import FuzzyText, FuzzyChoice
from models.user import User
from tests.fixtures.data.sample_data import SAMPLE_USERS


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating User instances."""
    
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"
    
    # Required fields
    name = factory.Faker('name')
    email = factory.LazyAttribute(lambda obj: f"{obj.name.lower().replace(' ', '.')}@example.com")
    language = factory.Faker('random_element', elements=['tr', 'en'])
    
    # Location fields
    city = factory.Faker('city')
    district = factory.Faker('city_suffix')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    is_gps_enabled = factory.Faker('boolean')
    
    # Preference fields
    notifications_enabled = factory.Faker('boolean')
    theme = factory.Faker('random_element', elements=['light', 'dark'])
    
    # Status fields
    is_active = True
    
    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        """Set password after user creation."""
        if extracted:
            obj.set_password(extracted)
        else:
            obj.set_password('testpassword123')


class TurkishUserFactory(UserFactory):
    """Factory for creating Turkish users."""
    
    name = factory.Faker('name', locale='tr_TR')
    email = factory.LazyAttribute(lambda obj: f"{obj.name.lower().replace(' ', '.')}@example.com")
    language = 'tr'
    city = factory.Faker('random_element', elements=[
        'Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya', 'Adana',
        'Konya', 'Gaziantep', 'Mersin', 'Diyarbakır'
    ])


class EnglishUserFactory(UserFactory):
    """Factory for creating English users."""
    
    name = factory.Faker('name', locale='en_US')
    email = factory.LazyAttribute(lambda obj: f"{obj.name.lower().replace(' ', '.')}@example.com")
    language = 'en'
    city = factory.Faker('city', locale='en_US')


class AdminUserFactory(UserFactory):
    """Factory for creating admin users."""
    
    name = "Admin User"
    email = "admin@example.com"
    language = 'tr'
    is_active = True


class InactiveUserFactory(UserFactory):
    """Factory for creating inactive users."""
    
    is_active = False


class GPSEnabledUserFactory(UserFactory):
    """Factory for creating GPS-enabled users."""
    
    is_gps_enabled = True
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')


class GPSDisabledUserFactory(UserFactory):
    """Factory for creating GPS-disabled users."""
    
    is_gps_enabled = False
    latitude = None
    longitude = None


def create_sample_user(user_data=None):
    """Create a user with sample data."""
    if user_data is None:
        user_data = SAMPLE_USERS[0]
    
    return UserFactory(
        name=user_data['name'],
        email=user_data['email'],
        language=user_data['language'],
        phone=user_data.get('phone'),
    )


def create_multiple_users(count=5):
    """Create multiple users."""
    return UserFactory.create_batch(count)


def create_users_with_locations():
    """Create users with different location settings."""
    users = []
    
    # GPS enabled user
    users.append(GPSEnabledUserFactory())
    
    # GPS disabled user
    users.append(GPSDisabledUserFactory())
    
    # Turkish user
    users.append(TurkishUserFactory())
    
    # English user
    users.append(EnglishUserFactory())
    
    return users


def create_test_user_for_auth():
    """Create a test user for authentication tests."""
    return UserFactory(
        name="Test User",
        email="test@example.com",
        language="tr"
    )


def create_users_with_preferences():
    """Create users with different preferences."""
    users = []
    
    # Light theme user
    users.append(UserFactory(theme='light'))
    
    # Dark theme user
    users.append(UserFactory(theme='dark'))
    
    # Notifications enabled user
    users.append(UserFactory(notifications_enabled=True))
    
    # Notifications disabled user
    users.append(UserFactory(notifications_enabled=False))
    
    return users
