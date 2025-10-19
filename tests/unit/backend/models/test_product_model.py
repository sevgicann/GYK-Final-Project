"""
Unit tests for Product and ProductRequirements models

Bu test dosyası Product ve ProductRequirements modelleri için birim testlerini içerir.
"""

import pytest
from datetime import datetime
from models.product import Product, ProductRequirements
from tests.fixtures.data.sample_data import SAMPLE_PRODUCTS


class TestProductModel:
    """Product model test sınıfı."""
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_creation(self, db_session):
        """Test product creation with valid data."""
        product_data = SAMPLE_PRODUCTS[0]
        product = Product(
            name=product_data['name'],
            category=product_data['category'],
            description=product_data['description']
        )
        
        db_session.add(product)
        db_session.commit()
        
        # Verify product was created
        assert product.id is not None
        assert product.name == product_data['name']
        assert product.category == product_data['category']
        assert product.description == product_data['description']
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_get_by_category(self, db_session):
        """Test getting products by category."""
        # Create test products
        product1 = Product(name="Wheat", category="Grain", description="Wheat grain")
        product2 = Product(name="Rice", category="Grain", description="Rice grain")
        product3 = Product(name="Tomato", category="Vegetable", description="Tomato vegetable")
        
        db_session.add_all([product1, product2, product3])
        db_session.commit()
        
        # Test getting products by category
        grain_products = Product.get_by_category("Grain")
        assert len(grain_products) == 2
        assert all(p.category == "Grain" for p in grain_products)
        
        vegetable_products = Product.get_by_category("Vegetable")
        assert len(vegetable_products) == 1
        assert vegetable_products[0].name == "Tomato"
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_search(self, db_session):
        """Test product search functionality."""
        # Create test products
        product1 = Product(name="Wheat", category="Grain", description="Basic grain crop")
        product2 = Product(name="Tomato", category="Vegetable", description="Red vegetable")
        product3 = Product(name="Corn", category="Grain", description="Yellow grain crop")
        
        db_session.add_all([product1, product2, product3])
        db_session.commit()
        
        # Test search by name
        results = Product.search_products("wheat")
        assert len(results) == 1
        assert results[0].name == "Wheat"
        
        # Test search by description
        results = Product.search_products("vegetable")
        assert len(results) == 1
        assert results[0].name == "Tomato"
        
        # Test search with no results
        results = Product.search_products("nonexistent")
        assert len(results) == 0
        
        # Test case insensitive search
        results = Product.search_products("WHEAT")
        assert len(results) == 1
        assert results[0].name == "Wheat"
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_get_all_categories(self, db_session):
        """Test getting all unique categories."""
        # Create test products
        product1 = Product(name="Wheat", category="Grain", description="Wheat grain")
        product2 = Product(name="Rice", category="Grain", description="Rice grain")
        product3 = Product(name="Tomato", category="Vegetable", description="Tomato vegetable")
        product4 = Product(name="Apple", category="Fruit", description="Apple fruit")
        
        db_session.add_all([product1, product2, product3, product4])
        db_session.commit()
        
        # Test getting all categories
        categories = Product.get_all_categories()
        assert len(categories) == 3
        assert "Grain" in categories
        assert "Vegetable" in categories
        assert "Fruit" in categories
    
    @pytest.mark.unit
    def test_product_to_dict(self):
        """Test converting product to dictionary."""
        product = Product(
            name="Test Product",
            category="Test Category",
            description="Test Description",
            image_url="http://example.com/image.jpg"
        )
        
        product_dict = product.to_dict()
        
        # Verify dictionary structure
        assert isinstance(product_dict, dict)
        assert product_dict['name'] == "Test Product"
        assert product_dict['category'] == "Test Category"
        assert product_dict['description'] == "Test Description"
        assert product_dict['image_url'] == "http://example.com/image.jpg"
        assert product_dict['is_active'] is True
        assert 'created_at' in product_dict
        assert 'updated_at' in product_dict
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_requirements_relationship(self, db_session):
        """Test product-requirements relationship."""
        # Create product
        product = Product(name="Test Product", category="Test Category")
        db_session.add(product)
        db_session.commit()
        
        # Create requirements
        requirements = ProductRequirements(
            product_id=product.id,
            ph_min=6.0,
            ph_max=7.0,
            nitrogen_min=100,
            nitrogen_max=150,
            temperature_min=20,
            temperature_max=25
        )
        db_session.add(requirements)
        db_session.commit()
        
        # Test relationship
        assert product.requirements is not None
        assert product.requirements.product_id == product.id
        assert product.requirements.ph_min == 6.0
        assert product.requirements.ph_max == 7.0
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_required_fields(self, db_session):
        """Test that required fields are enforced."""
        # Test missing name
        with pytest.raises(Exception):
            product = Product(category="Test Category")
            db_session.add(product)
            db_session.commit()
        
        # Test missing category
        with pytest.raises(Exception):
            product = Product(name="Test Product")
            db_session.add(product)
            db_session.commit()
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_default_values(self, db_session):
        """Test default values for product fields."""
        product = Product(name="Test Product", category="Test Category")
        
        db_session.add(product)
        db_session.commit()
        
        # Verify default values
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None


class TestProductRequirementsModel:
    """ProductRequirements model test sınıfı."""
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_requirements_creation(self, db_session):
        """Test product requirements creation."""
        # Create product first
        product = Product(name="Test Product", category="Test Category")
        db_session.add(product)
        db_session.commit()
        
        # Create requirements
        requirements = ProductRequirements(
            product_id=product.id,
            ph_min=6.0,
            ph_max=7.5,
            nitrogen_min=90,
            nitrogen_max=140,
            phosphorus_min=35,
            phosphorus_max=65,
            potassium_min=180,
            potassium_max=240,
            humidity_min=16,
            humidity_max=24,
            temperature_min=15,
            temperature_max=26,
            rainfall_min=400,
            rainfall_max=900,
            notes="Test requirements"
        )
        
        db_session.add(requirements)
        db_session.commit()
        
        # Verify requirements were created
        assert requirements.id is not None
        assert requirements.product_id == product.id
        assert requirements.ph_min == 6.0
        assert requirements.ph_max == 7.5
        assert requirements.nitrogen_min == 90
        assert requirements.nitrogen_max == 140
        assert requirements.notes == "Test requirements"
    
    @pytest.mark.unit
    def test_product_requirements_to_dict(self):
        """Test converting requirements to dictionary."""
        requirements = ProductRequirements(
            product_id="test-product-id",
            ph_min=6.0,
            ph_max=7.5,
            nitrogen_min=90,
            nitrogen_max=140,
            temperature_min=15,
            temperature_max=26,
            notes="Test notes"
        )
        
        req_dict = requirements.to_dict()
        
        # Verify dictionary structure
        assert isinstance(req_dict, dict)
        assert req_dict['product_id'] == "test-product-id"
        assert req_dict['ph']['min'] == 6.0
        assert req_dict['ph']['max'] == 7.5
        assert req_dict['nitrogen']['min'] == 90
        assert req_dict['nitrogen']['max'] == 140
        assert req_dict['temperature']['min'] == 15
        assert req_dict['temperature']['max'] == 26
        assert req_dict['notes'] == "Test notes"
        assert 'created_at' in req_dict
        assert 'updated_at' in req_dict
    
    @pytest.mark.unit
    def test_product_requirements_suitability_check(self):
        """Test product suitability check for environment."""
        requirements = ProductRequirements(
            ph_min=6.0,
            ph_max=7.0,
            temperature_min=20,
            temperature_max=25,
            humidity_min=60,
            humidity_max=80
        )
        
        # Mock environment data
        class MockEnvironmentData:
            def __init__(self, ph, temperature, humidity):
                self.ph = ph
                self.temperature = temperature
                self.humidity = humidity
        
        # Test suitable environment
        suitable_env = MockEnvironmentData(ph=6.5, temperature=22, humidity=70)
        is_suitable, issues = requirements.is_suitable_for_environment(suitable_env)
        assert is_suitable is True
        assert len(issues) == 0
        
        # Test unsuitable environment - pH too low
        unsuitable_env = MockEnvironmentData(ph=5.5, temperature=22, humidity=70)
        is_suitable, issues = requirements.is_suitable_for_environment(unsuitable_env)
        assert is_suitable is False
        assert len(issues) > 0
        assert "pH too low" in issues[0]
        
        # Test unsuitable environment - temperature too high
        unsuitable_env = MockEnvironmentData(ph=6.5, temperature=30, humidity=70)
        is_suitable, issues = requirements.is_suitable_for_environment(unsuitable_env)
        assert is_suitable is False
        assert len(issues) > 0
        assert "Temperature too high" in issues[0]
        
        # Test unsuitable environment - humidity too low
        unsuitable_env = MockEnvironmentData(ph=6.5, temperature=22, humidity=50)
        is_suitable, issues = requirements.is_suitable_for_environment(unsuitable_env)
        assert is_suitable is False
        assert len(issues) > 0
        assert "Humidity too low" in issues[0]
    
    @pytest.mark.unit
    def test_product_requirements_suitability_with_none_values(self):
        """Test suitability check when some requirements are None."""
        requirements = ProductRequirements(
            ph_min=6.0,
            ph_max=7.0,
            # temperature_min and temperature_max are None
            humidity_min=60,
            humidity_max=80
        )
        
        class MockEnvironmentData:
            def __init__(self, ph, temperature, humidity):
                self.ph = ph
                self.temperature = temperature
                self.humidity = humidity
        
        # Test with None temperature values (should not cause errors)
        env_data = MockEnvironmentData(ph=6.5, temperature=30, humidity=70)
        is_suitable, issues = requirements.is_suitable_for_environment(env_data)
        assert is_suitable is True  # Should be suitable since temperature limits are None
        assert len(issues) == 0
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_requirements_foreign_key_constraint(self, db_session):
        """Test foreign key constraint for product requirements."""
        # Try to create requirements without valid product_id
        with pytest.raises(Exception):
            requirements = ProductRequirements(
                product_id="non-existent-product-id",
                ph_min=6.0,
                ph_max=7.0
            )
            db_session.add(requirements)
            db_session.commit()
    
    @pytest.mark.unit
    @pytest.mark.database
    def test_product_cascade_delete(self, db_session):
        """Test cascade delete when product is deleted."""
        # Create product with requirements
        product = Product(name="Test Product", category="Test Category")
        db_session.add(product)
        db_session.commit()
        
        requirements = ProductRequirements(
            product_id=product.id,
            ph_min=6.0,
            ph_max=7.0
        )
        db_session.add(requirements)
        db_session.commit()
        
        # Delete product
        db_session.delete(product)
        db_session.commit()
        
        # Verify requirements are also deleted
        remaining_requirements = ProductRequirements.query.filter_by(product_id=product.id).first()
        assert remaining_requirements is None
