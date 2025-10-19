"""
Unit tests for Products routes

Bu test dosyası products routes için birim testlerini içerir.
"""

import pytest
from unittest.mock import patch, MagicMock
from tests.fixtures.data.sample_data import SAMPLE_PRODUCTS, SAMPLE_USERS


class TestProductsRoutes:
    """Products routes test sınıfı."""
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_products_success(self, client, db_session):
        """Test successful products retrieval."""
        # Create test products
        product1 = {
            'name': 'Wheat',
            'category': 'Grain',
            'description': 'Basic grain crop'
        }
        product2 = {
            'name': 'Tomato',
            'category': 'Vegetable',
            'description': 'Red vegetable'
        }
        
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code == 201
        
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create products
        response1 = client.post('/api/products', json=product1, headers=headers)
        response2 = client.post('/api/products', json=product2, headers=headers)
        
        # Get products
        response = client.get('/api/products', headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'products' in data['data']
        assert len(data['data']['products']) == 2
        
        # Verify pagination
        assert 'pagination' in data['data']
        pagination = data['data']['pagination']
        assert pagination['total'] == 2
        assert pagination['page'] == 1
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_products_with_category_filter(self, client, db_session):
        """Test products retrieval with category filter."""
        # Create test products
        grain_product = {
            'name': 'Wheat',
            'category': 'Grain',
            'description': 'Basic grain crop'
        }
        vegetable_product = {
            'name': 'Tomato',
            'category': 'Vegetable',
            'description': 'Red vegetable'
        }
        
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create products
        client.post('/api/products', json=grain_product, headers=headers)
        client.post('/api/products', json=vegetable_product, headers=headers)
        
        # Get products with category filter
        response = client.get('/api/products?category=Grain', headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['data']['products']) == 1
        assert data['data']['products'][0]['category'] == 'Grain'
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_products_with_search(self, client, db_session):
        """Test products retrieval with search query."""
        # Create test products
        product1 = {
            'name': 'Wheat',
            'category': 'Grain',
            'description': 'Basic grain crop'
        }
        product2 = {
            'name': 'Tomato',
            'category': 'Vegetable',
            'description': 'Red vegetable fruit'
        }
        
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create products
        client.post('/api/products', json=product1, headers=headers)
        client.post('/api/products', json=product2, headers=headers)
        
        # Search products
        response = client.get('/api/products?search=vegetable', headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['data']['products']) == 1
        assert 'vegetable' in data['data']['products'][0]['description'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_products_pagination(self, client, db_session):
        """Test products retrieval with pagination."""
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create multiple products
        for i in range(5):
            product = {
                'name': f'Product {i}',
                'category': 'Test',
                'description': f'Test product {i}'
            }
            client.post('/api/products', json=product, headers=headers)
        
        # Get first page
        response = client.get('/api/products?page=1&per_page=2', headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['data']['products']) == 2
        
        # Verify pagination info
        pagination = data['data']['pagination']
        assert pagination['total'] == 5
        assert pagination['page'] == 1
        assert pagination['per_page'] == 2
        assert pagination['pages'] == 3
        assert pagination['has_next'] is True
        assert pagination['has_prev'] is False
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_create_product_success(self, client, db_session):
        """Test successful product creation."""
        product_data = SAMPLE_PRODUCTS[0]
        
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create product
        response = client.post('/api/products', json=product_data, headers=headers)
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'product' in data['data']
        
        # Verify product data
        product = data['data']['product']
        assert product['name'] == product_data['name']
        assert product['category'] == product_data['category']
        assert product['description'] == product_data['description']
        assert 'id' in product
        assert 'created_at' in product
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_create_product_with_requirements(self, client, db_session):
        """Test product creation with requirements."""
        product_data = SAMPLE_PRODUCTS[0].copy()
        product_data['requirements'] = {
            'ph_min': 6.0,
            'ph_max': 7.5,
            'nitrogen_min': 90,
            'nitrogen_max': 140,
            'temperature_min': 15,
            'temperature_max': 26,
            'notes': 'Test requirements'
        }
        
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create product
        response = client.post('/api/products', json=product_data, headers=headers)
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        
        # Verify requirements were created
        product = data['data']['product']
        assert 'requirements' in product
        requirements = product['requirements']
        assert requirements['ph']['min'] == 6.0
        assert requirements['ph']['max'] == 7.5
        assert requirements['nitrogen']['min'] == 90
        assert requirements['nitrogen']['max'] == 140
        assert requirements['notes'] == 'Test requirements'
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_create_product_missing_data(self, client, db_session):
        """Test product creation with missing data."""
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Try to create product without required fields
        response = client.post('/api/products', json={}, headers=headers)
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'required' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_create_product_unauthorized(self, client):
        """Test product creation without authentication."""
        product_data = SAMPLE_PRODUCTS[0]
        
        response = client.post('/api/products', json=product_data)
        
        # Verify error response
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_product_by_id_success(self, client, db_session):
        """Test successful product retrieval by ID."""
        product_data = SAMPLE_PRODUCTS[0]
        
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create product
        create_response = client.post('/api/products', json=product_data, headers=headers)
        product_id = create_response.get_json()['data']['product']['id']
        
        # Get product by ID
        response = client.get(f'/api/products/{product_id}', headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'product' in data['data']
        
        # Verify product data
        product = data['data']['product']
        assert product['id'] == product_id
        assert product['name'] == product_data['name']
        assert product['category'] == product_data['category']
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_product_by_id_not_found(self, client, db_session):
        """Test product retrieval with non-existent ID."""
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Try to get non-existent product
        response = client.get('/api/products/non-existent-id', headers=headers)
        
        # Verify error response
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False
        assert 'not found' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_update_product_success(self, client, db_session):
        """Test successful product update."""
        product_data = SAMPLE_PRODUCTS[0]
        
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create product
        create_response = client.post('/api/products', json=product_data, headers=headers)
        product_id = create_response.get_json()['data']['product']['id']
        
        # Update product
        update_data = {
            'name': 'Updated Product Name',
            'category': 'Updated Category',
            'description': 'Updated description'
        }
        response = client.put(f'/api/products/{product_id}', json=update_data, headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        
        # Verify updated data
        product = data['data']['product']
        assert product['name'] == update_data['name']
        assert product['category'] == update_data['category']
        assert product['description'] == update_data['description']
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_delete_product_success(self, client, db_session):
        """Test successful product deletion."""
        product_data = SAMPLE_PRODUCTS[0]
        
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create product
        create_response = client.post('/api/products', json=product_data, headers=headers)
        product_id = create_response.get_json()['data']['product']['id']
        
        # Delete product
        response = client.delete(f'/api/products/{product_id}', headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'message' in data
        
        # Verify product is deleted
        get_response = client.get(f'/api/products/{product_id}', headers=headers)
        assert get_response.status_code == 404
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_delete_product_not_found(self, client, db_session):
        """Test product deletion with non-existent ID."""
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Try to delete non-existent product
        response = client.delete('/api/products/non-existent-id', headers=headers)
        
        # Verify error response
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False
        assert 'not found' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_get_products_categories(self, client, db_session):
        """Test getting product categories."""
        # Register user and login
        user_data = SAMPLE_USERS[0]
        register_response = client.post('/api/auth/register', json=user_data)
        login_response = client.post('/api/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        token = login_response.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create products with different categories
        categories = ['Grain', 'Vegetable', 'Fruit']
        for category in categories:
            product = {
                'name': f'Product {category}',
                'category': category,
                'description': f'Test {category} product'
            }
            client.post('/api/products', json=product, headers=headers)
        
        # Get categories
        response = client.get('/api/products/categories', headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'categories' in data['data']
        
        # Verify categories
        returned_categories = data['data']['categories']
        assert len(returned_categories) == 3
        for category in categories:
            assert category in returned_categories
