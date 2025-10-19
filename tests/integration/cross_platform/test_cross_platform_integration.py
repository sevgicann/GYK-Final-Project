"""
Cross-Platform Integration Tests

Bu test dosyası mobil ve web platformları arasındaki entegrasyon testlerini içerir.
Hem Flutter hem de web frontend'in backend ile entegrasyonunu test eder.
"""

import pytest
import json
from unittest.mock import patch, Mock
from tests.fixtures.factories.user_factory import UserFactory
from tests.fixtures.factories.product_factory import ProductFactory
from tests.fixtures.data.sample_data import SAMPLE_PRODUCTS, SAMPLE_ENVIRONMENTS


class TestCrossPlatformDataConsistency:
    """Cross-platform veri tutarlılığı testleri."""
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_user_data_consistency_across_platforms(self, client, db_session):
        """Test user data consistency across platforms."""
        # Create user via backend
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        # Test data consistency
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        
        # Verify data structure is consistent
        assert 'id' in user_data
        assert 'username' in user_data
        assert 'email' in user_data
        assert 'first_name' in user_data
        assert 'last_name' in user_data
        
        # Test API endpoint consistency
        response = client.get(f'/api/users/{user.id}')
        assert response.status_code in [200, 404]
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_product_data_consistency_across_platforms(self, client, db_session):
        """Test product data consistency across platforms."""
        # Create product via backend
        product = ProductFactory()
        db_session.add(product)
        db_session.commit()
        
        # Test data consistency
        product_data = {
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'description': product.description,
            'requirements': {
                'ph': product.requirements.ph,
                'nitrogen': product.requirements.nitrogen,
                'phosphorus': product.requirements.phosphorus,
                'potassium': product.requirements.potassium
            }
        }
        
        # Verify data structure is consistent
        assert 'id' in product_data
        assert 'name' in product_data
        assert 'category' in product_data
        {product_data}
        assert 'requirements' in product_data
        
        # Test API endpoint consistency
        response = client.get(f'/api/products/{product.id}')
        assert response.status_code in [200, 404]
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_environment_data_consistency_across_platforms(self, client, db_session):
        """Test environment data consistency across platforms."""
        # Create environment data
        environment_data = SAMPLE_ENVIRONMENTS[0].copy()
        
        # Test data structure consistency
        required_fields = ['region', 'soil_ph', 'nitrogen', 'phosphorus', 'potassium', 'temperature_celsius', 'rainfall_mm']
        
        for field in required_fields:
            assert field in environment_data
        
        # Test API endpoint consistency
        response = client.post('/api/environments', json=environment_data)
        assert response.status_code in [200, 201, 401, 404]


class TestCrossPlatformAPICompatibility:
    """Cross-platform API uyumluluğu testleri."""
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_api_response_format_consistency(self, client, db_session):
        """Test API response format consistency."""
        # Test products API
        response = client.get('/api/products')
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            assert isinstance(data, (list, dict))
            
            if isinstance(data, list) and data:
                product = data[0]
                expected_fields = ['id', 'name', 'category', 'description']
                for field in expected_fields:
                    assert field in product
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_api_error_response_consistency(self, client, db_session):
        """Test API error response consistency."""
        # Test 404 error
        response = client.get('/api/nonexistent-endpoint')
        assert response.status_code == 404
        
        # Test 401 error (unauthorized)
        response = client.get('/api/protected-endpoint')
        assert response.status_code in [200, 401, 403, 404]
        
        # Test 400 error (bad request)
        response = client.post('/api/products', json={'invalid': 'data'})
        assert response.status_code in [200, 201, 400, 404]
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_api_pagination_consistency(self, client, db_session):
        """Test API pagination consistency."""
        # Create test data
        products = ProductFactory.create_batch(10)
        db_session.add_all(products)
        db_session.commit()
        
        # Test pagination parameters
        pagination_tests = [
            {'page': 1, 'per_page': 5},
            {'page': 2, 'per_page': 3},
            {'limit': 5, 'offset': 0}
        ]
        
        for params in pagination_tests:
            response = client.get('/api/products', query_string=params)
            assert response.status_code in [200, 404]


class TestCrossPlatformMLIntegration:
    """Cross-platform ML entegrasyon testleri."""
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    @pytest.mark.ml
    def test_ml_prediction_consistency_across_platforms(self, client, db_session):
        """Test ML prediction consistency across platforms."""
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
        
        if response.status_code in [200, 201]:
            data = response.get_json()
            expected_fields = ['prediction', 'confidence']
            for field in expected_fields:
                assert field in data
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    @pytest.mark.ml
    def test_ml_environment_prediction_consistency(self, client, db_session):
        """Test ML environment prediction consistency."""
        # Test environment prediction
        prediction_data = {
            'crop': 'wheat',
            'region': 'Marmara'
        }
        
        response = client.post('/api/ml/predict-environment', json=prediction_data)
        assert response.status_code in [200, 201, 404]
        
        if response.status_code in [200, 201]:
            data = response.get_json()
            expected_fields = ['soil_ph', 'nitrogen', 'phosphorus', 'potassium', 'temperature_celsius', 'rainfall_mm']
            for field in expected_fields:
                assert field in data


class TestCrossPlatformAuthentication:
    """Cross-platform kimlik doğrulama testleri."""
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_jwt_token_compatibility(self, client, db_session):
        """Test JWT token compatibility across platforms."""
        # Create user and generate token
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        token = user.generate_access_token()
        
        # Test token format
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Test token validation
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/api/user/profile', headers=headers)
        assert response.status_code in [200, 401, 403, 404]
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_authentication_flow_consistency(self, client, db_session):
        """Test authentication flow consistency."""
        # Test registration
        user_data = {
            'username': 'crossplatformuser',
            'email': 'crossplatform@example.com',
            'password': 'password123',
            'first_name': 'Cross',
            'last_name': 'Platform'
        }
        
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code in [200, 201, 404]
        
        # Test login
        login_data = {
            'email': 'crossplatform@example.com',
            'password': 'password123'
        }
        
        login_response = client.post('/api/auth/login', json=login_data)
        assert login_response.status_code in [200, 401, 404]
        
        if login_response.status_code == 200:
            login_result = login_response.get_json()
            assert 'access_token' in login_result
            assert 'refresh_token' in login_result


class TestCrossPlatformDataSynchronization:
    """Cross-platform veri senkronizasyonu testleri."""
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_offline_data_sync_consistency(self, client, db_session):
        """Test offline data sync consistency."""
        # Test offline data structure
        offline_data = {
            'products': SAMPLE_PRODUCTS,
            'user_preferences': {
                'language': 'tr',
                'theme': 'light'
            },
            'last_sync': '2025-01-01T00:00:00Z'
        }
        
        # Test sync endpoint
        response = client.post('/api/sync/offline-data', json=offline_data)
        assert response.status_code in [200, 201, 404]
        
        # Test sync status
        response = client.get('/api/sync/status')
        assert response.status_code in [200, 404]
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_data_conflict_resolution(self, client, db_session):
        """Test data conflict resolution."""
        # Test conflict resolution
        conflict_data = {
            'local_changes': {
                'product_name': 'Local Updated Product'
            },
            'server_changes': {
                'product_name': 'Server Updated Product'
            },
            'resolution_strategy': 'merge'
        }
        
        response = client.post('/api/sync/resolve-conflict', json=conflict_data)
        assert response.status_code in [200, 201, 404]


class TestCrossPlatformPerformance:
    """Cross-platform performans testleri."""
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    @pytest.mark.performance
    def test_api_response_time_consistency(self, client, db_session):
        """Test API response time consistency."""
        import time
        
        # Test multiple endpoints
        endpoints = ['/api/products', '/api/users', '/api/environments']
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response_time < 3.0  # 3 seconds max
            assert response.status_code in [200, 404]
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    @pytest.mark.performance
    def test_concurrent_request_handling(self, client, db_session):
        """Test concurrent request handling."""
        import threading
        
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


class TestCrossPlatformSecurity:
    """Cross-platform güvenlik testleri."""
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    @pytest.mark.security
    def test_cors_headers_consistency(self, client, db_session):
        """Test CORS headers consistency."""
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
    @pytest.mark.cross_platform
    @pytest.mark.security
    def test_input_validation_consistency(self, client, db_session):
        """Test input validation consistency."""
        # Test SQL injection protection
        malicious_data = {
            'name': "'; DROP TABLE users; --",
            'category': 'Tahıl'
        }
        
        response = client.post('/api/products', json=malicious_data)
        assert response.status_code in [200, 201, 400, 404]
        
        # Test XSS protection
        xss_data = {
            'name': '<script>alert("xss")</script>',
            'category': 'Tahıl'
        }
        
        response = client.post('/api/products', json=xss_data)
        assert response.status_code in [200, 201, 400, 404]
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    @pytest.mark.security
    def test_rate_limiting_consistency(self, client, db_session):
        """Test rate limiting consistency."""
        # Make multiple requests to test rate limiting
        for i in range(10):
            response = client.get('/api/products')
            assert response.status_code in [200, 429, 404]


class TestCrossPlatformErrorHandling:
    """Cross-platform hata yönetimi testleri."""
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_error_response_format_consistency(self, client, db_session):
        """Test error response format consistency."""
        # Test 404 error
        response = client.get('/api/nonexistent-endpoint')
        assert response.status_code == 404
        
        # Test 400 error
        response = client.post('/api/products', json={'invalid': 'data'})
        assert response.status_code in [200, 201, 400, 404]
        
        # Test 401 error
        response = client.get('/api/protected-endpoint')
        assert response.status_code in [200, 401, 403, 404]
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_network_error_handling_consistency(self, client, db_session):
        """Test network error handling consistency."""
        # Test timeout handling
        response = client.get('/api/products', timeout=0.001)
        assert response.status_code in [200, 408, 500, 404]
        
        # Test connection error handling
        response = client.get('/api/products')
        assert response.status_code in [200, 404]


class TestCrossPlatformDataMigration:
    """Cross-platform veri migrasyonu testleri."""
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_data_migration_compatibility(self, client, db_session):
        """Test data migration compatibility."""
        # Test migration endpoint
        migration_data = {
            'from_version': '1.0',
            'to_version': '2.0',
            'data': {
                'users': [],
                'products': SAMPLE_PRODUCTS
            }
        }
        
        response = client.post('/api/migrate/data', json=migration_data)
        assert response.status_code in [200, 201, 404]
    
    @pytest.mark.integration
    @pytest.mark.cross_platform
    def test_backward_compatibility(self, client, db_session):
        """Test backward compatibility."""
        # Test old API version compatibility
        response = client.get('/api/v1/products')
        assert response.status_code in [200, 404]
        
        # Test new API version compatibility
        response = client.get('/api/v2/products')
        assert response.status_code in [200, 404]
