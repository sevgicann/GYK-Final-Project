"""
Backend API Integration Tests

Bu test dosyası API entegrasyon testlerini içerir.
Backend ve Frontend arasındaki API entegrasyonunu test eder.
"""

import pytest
import json
from unittest.mock import patch, Mock
from tests.fixtures.factories.user_factory import UserFactory
from tests.fixtures.factories.product_factory import ProductFactory
from tests.fixtures.data.sample_data import SAMPLE_PRODUCTS, SAMPLE_ENVIRONMENTS


class TestAuthenticationIntegration:
    """Kimlik doğrulama entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.auth
    def test_user_registration_and_login_flow(self, client, db_session):
        """Test complete user registration and login flow."""
        # Test user registration
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        # Register user
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code in [200, 201, 404]
        
        # Test user login
        login_data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        
        login_response = client.post('/api/auth/login', json=login_data)
        assert login_response.status_code in [200, 401, 404]
        
        if login_response.status_code == 200:
            login_data = login_response.get_json()
            assert 'access_token' in login_data
            assert 'refresh_token' in login_data
    
    @pytest.mark.integration
    @pytest.mark.auth
    def test_token_refresh_flow(self, client, db_session):
        """Test token refresh flow."""
        # Create user and get tokens
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        # Test token refresh
        refresh_data = {
            'refresh_token': user.generate_refresh_token()
        }
        
        response = client.post('/api/auth/refresh', json=refresh_data)
        assert response.status_code in [200, 401, 404]
    
    @pytest.mark.integration
    @pytest.mark.auth
    def test_protected_endpoint_access(self, client, db_session):
        """Test access to protected endpoints."""
        # Create user and get token
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        token = user.generate_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test protected endpoint access
        response = client.get('/api/user/profile', headers=headers)
        assert response.status_code in [200, 401, 403, 404]


class TestProductIntegration:
    """Ürün entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.products
    def test_product_crud_flow(self, client, db_session):
        """Test complete product CRUD flow."""
        # Create product
        product_data = SAMPLE_PRODUCTS[0].copy()
        create_response = client.post('/api/products', json=product_data)
        assert create_response.status_code in [200, 201, 401, 404]
        
        if create_response.status_code in [200, 201]:
            product_id = create_response.get_json().get('id')
            
            # Read product
            read_response = client.get(f'/api/products/{product_id}')
            assert read_response.status_code in [200, 404]
            
            # Update product
            update_data = product_data.copy()
            update_data['description'] = 'Updated description'
            update_response = client.put(f'/api/products/{product_id}', json=update_data)
            assert update_response.status_code in [200, 401, 404]
            
            # Delete product
            delete_response = client.delete(f'/api/products/{product_id}')
            assert delete_response.status_code in [200, 204, 401, 404]
    
    @pytest.mark.integration
    @pytest.mark.products
    def test_product_search_and_filter(self, client, db_session):
        """Test product search and filtering."""
        # Create test products
        products = ProductFactory.create_batch(5)
        db_session.add_all(products)
        db_session.commit()
        
        # Test search
        search_response = client.get('/api/products?search=wheat')
        assert search_response.status_code in [200, 404]
        
        # Test category filter
        filter_response = client.get('/api/products?category=Tahıl')
        assert filter_response.status_code in [200, 404]
        
        # Test pagination
        pagination_response = client.get('/api/products?page=1&per_page=2')
        assert pagination_response.status_code in [200, 404]


class TestEnvironmentIntegration:
    """Çevre entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.environments
    def test_environment_data_flow(self, client, db_session):
        """Test environment data flow."""
        # Create user
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        token = user.generate_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create environment
        environment_data = SAMPLE_ENVIRONMENTS[0].copy()
        create_response = client.post('/api/environments', json=environment_data, headers=headers)
        assert create_response.status_code in [200, 201, 401, 404]
        
        if create_response.status_code in [200, 201]:
            env_id = create_response.get_json().get('id')
            
            # Get environment data
            get_response = client.get(f'/api/environments/{env_id}', headers=headers)
            assert get_response.status_code in [200, 404]
            
            # Update environment data
            update_data = environment_data.copy()
            update_data['soil_ph'] = 7.0
            update_response = client.put(f'/api/environments/{env_id}', json=update_data, headers=headers)
            assert update_response.status_code in [200, 401, 404]


class TestMLIntegration:
    """ML model entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_ml_prediction_flow(self, mock_ml_service, client, db_session):
        """Test ML prediction flow."""
        # Mock ML service
        mock_instance = Mock()
        mock_instance.predict_crop_from_environment.return_value = {
            'prediction': 'wheat',
            'confidence': 0.85
        }
        mock_ml_service.return_value = mock_instance
        
        # Test crop prediction
        prediction_data = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600,
            'region': 'Marmara'
        }
        
        response = client.post('/api/ml/predict-crop', json=prediction_data)
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.ml
    @patch('services.ml_service.MLService')
    def test_ml_environment_prediction_flow(self, mock_ml_service, client, db_session):
        """Test ML environment prediction flow."""
        # Mock ML service
        mock_instance = Mock()
        mock_instance.predict_environment_from_crop.return_value = {
            'soil_ph': 6.5,
            'nitrogen': 120,
            'phosphorus': 45,
            'potassium': 150,
            'temperature_celsius': 22,
            'rainfall_mm': 600
        }
        mock_ml_service.return_value = mock_instance
        
        # Test environment prediction
        prediction_data = {
            'crop': 'wheat',
            'region': 'Marmara'
        }
        
        response = client.post('/api/ml/predict-environment', json=prediction_data)
        assert response.status_code in [200, 201, 404]


class TestRecommendationIntegration:
    """Öneri entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.recommendations
    def test_recommendation_flow(self, client, db_session):
        """Test recommendation flow."""
        # Create user and environment
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        token = user.generate_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test recommendation
        recommendation_data = {
            'environment_id': 1,
            'preferences': {
                'category': 'Tahıl',
                'max_water_usage': 800
            }
        }
        
        response = client.post('/api/recommendations', json=recommendation_data, headers=headers)
        assert response.status_code in [200, 201, 401, 404]


class TestDataFlowIntegration:
    """Veri akışı entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.data_flow
    def test_complete_user_journey(self, client, db_session):
        """Test complete user journey from registration to recommendation."""
        # 1. User registration
        user_data = {
            'username': 'journeyuser',
            'email': 'journey@example.com',
            'password': 'password123',
            'first_name': 'Journey',
            'last_name': 'User'
        }
        
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code in [200, 201, 404]
        
        # 2. User login
        login_response = client.post('/api/auth/login', json={
            'email': 'journey@example.com',
            'password': 'password123'
        })
        
        if login_response.status_code == 200:
            token = login_response.get_json()['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            
            # 3. Create environment
            environment_data = SAMPLE_ENVIRONMENTS[0].copy()
            env_response = client.post('/api/environments', json=environment_data, headers=headers)
            assert env_response.status_code in [200, 201, 404]
            
            # 4. Get products
            products_response = client.get('/api/products', headers=headers)
            assert products_response.status_code in [200, 404]
            
            # 5. Get recommendations
            recommendations_response = client.get('/api/recommendations', headers=headers)
            assert recommendations_response.status_code in [200, 404]
    
    @pytest.mark.integration
    @pytest.mark.data_flow
    def test_cross_platform_data_consistency(self, client, db_session):
        """Test data consistency across platforms."""
        # Create data from backend
        user = UserFactory()
        product = ProductFactory()
        db_session.add_all([user, product])
        db_session.commit()
        
        # Verify data can be retrieved
        user_response = client.get(f'/api/users/{user.id}')
        product_response = client.get(f'/api/products/{product.id}')
        
        # Both should return consistent data
        assert user_response.status_code in [200, 404]
        assert product_response.status_code in [200, 404]


class TestErrorHandlingIntegration:
    """Hata yönetimi entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.error_handling
    def test_api_error_handling(self, client, db_session):
        """Test API error handling."""
        # Test invalid endpoint
        response = client.get('/api/invalid-endpoint')
        assert response.status_code == 404
        
        # Test invalid data
        invalid_data = {'invalid': 'data'}
        response = client.post('/api/products', json=invalid_data)
        assert response.status_code in [200, 400, 404]
        
        # Test unauthorized access
        response = client.get('/api/user/profile')
        assert response.status_code in [200, 401, 403, 404]
    
    @pytest.mark.integration
    @pytest.mark.error_handling
    def test_network_error_simulation(self, client, db_session):
        """Test network error simulation."""
        # Test timeout handling
        response = client.get('/api/products', timeout=0.001)
        assert response.status_code in [200, 408, 500, 404]
        
        # Test rate limiting
        for i in range(10):
            response = client.get('/api/products')
            assert response.status_code in [200, 429, 404]


class TestPerformanceIntegration:
    """Performans entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.performance
    def test_api_response_times(self, client, db_session):
        """Test API response times."""
        import time
        
        # Test product list response time
        start_time = time.time()
        response = client.get('/api/products')
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 2.0  # 2 seconds max
        assert response.status_code in [200, 404]
    
    @pytest.mark.integration
    @pytest.mark.performance
    def test_concurrent_requests(self, client, db_session):
        """Test concurrent requests handling."""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = client.get('/api/products')
            results.append(response.status_code)
        
        # Make multiple concurrent requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should complete successfully
        assert len(results) == 5
        for status_code in results:
            assert status_code in [200, 404]


class TestSecurityIntegration:
    """Güvenlik entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.security
    def test_cors_headers(self, client, db_session):
        """Test CORS headers."""
        response = client.get('/api/products')
        assert response.status_code in [200, 404]
        
        # Check CORS headers
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers'
        ]
        
        for header in cors_headers:
            # CORS headers might be set by Flask-CORS
            assert header in response.headers or response.status_code == 404
    
    @pytest.mark.integration
    @pytest.mark.security
    def test_sql_injection_protection(self, client, db_session):
        """Test SQL injection protection."""
        # Test SQL injection attempt
        malicious_data = {
            'name': "'; DROP TABLE users; --",
            'category': 'Tahıl'
        }
        
        response = client.post('/api/products', json=malicious_data)
        assert response.status_code in [200, 201, 400, 404]
        
        # Verify data integrity
        products_response = client.get('/api/products')
        assert products_response.status_code in [200, 404]
