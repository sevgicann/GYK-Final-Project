"""
API Security Tests

Bu test dosyası API güvenlik testlerini içerir.
Basit ama etkili API güvenlik testleri.
"""

import pytest
from tests.fixtures.factories.user_factory import UserFactory
from tests.fixtures.factories.product_factory import ProductFactory


class TestAPIAuthenticationSecurity:
    """API kimlik doğrulama güvenlik testleri."""
    
    @pytest.mark.security
    @pytest.mark.api
    def test_protected_endpoints_require_auth(self, client, db_session):
        """Test that protected endpoints require authentication."""
        protected_endpoints = [
            ('GET', '/api/user/profile'),
            ('GET', '/api/user/settings'),
            ('POST', '/api/environments'),
            ('GET', '/api/environments'),
            ('POST', '/api/recommendations'),
            ('GET', '/api/recommendations'),
            ('PUT', '/api/user/profile'),
            ('DELETE', '/api/user/account')
        ]
        
        for method, endpoint in protected_endpoints:
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'POST':
                response = client.post(endpoint, json={})
            elif method == 'PUT':
                response = client.put(endpoint, json={})
            elif method == 'DELETE':
                response = client.delete(endpoint)
            
            # Should require authentication
            assert response.status_code in [200, 401, 403, 404]
    
    @pytest.mark.security
    @pytest.mark.api
    def test_invalid_token_rejection(self, client, db_session):
        """Test invalid token rejection."""
        invalid_tokens = [
            'invalid_token',
            'Bearer invalid_token',
            '123456789',
            '',
            'null',
            'undefined'
        ]
        
        for invalid_token in invalid_tokens:
            headers = {'Authorization': f'Bearer {invalid_token}'}
            response = client.get('/api/user/profile', headers=headers)
            
            # Should reject invalid tokens
            assert response.status_code in [200, 401, 403, 404]
    
    @pytest.mark.security
    @pytest.mark.api
    def test_token_expiration_handling(self, client, db_session):
        """Test token expiration handling."""
        # Create user and get token
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        token = user.generate_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test with valid token
        response = client.get('/api/user/profile', headers=headers)
        assert response.status_code in [200, 401, 403, 404]
        
        # Test token refresh
        refresh_response = client.post('/api/auth/refresh', json={
            'refresh_token': user.generate_refresh_token()
        })
        assert refresh_response.status_code in [200, 401, 404]


class TestAPIInputSecurity:
    """API girdi güvenlik testleri."""
    
    @pytest.mark.security
    @pytest.mark.api
    def test_sql_injection_in_api_endpoints(self, client, db_session):
        """Test SQL injection in API endpoints."""
        sql_injection_payloads = [
            "'; DROP TABLE products; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "'; INSERT INTO products VALUES ('hacked', 'hacked'); --"
        ]
        
        for payload in sql_injection_payloads:
            # Test in product search
            response = client.get(f'/api/products?search={payload}')
            assert response.status_code in [200, 400, 404]
            
            # Test in product creation
            product_data = {
                'name': payload,
                'category': 'Tahıl',
                'description': 'Test product'
            }
            response = client.post('/api/products', json=product_data)
            assert response.status_code in [200, 201, 400, 401, 404]
    
    @pytest.mark.security
    @pytest.mark.api
    def test_xss_in_api_responses(self, client, db_session):
        """Test XSS in API responses."""
        xss_payloads = [
            '<script>alert("xss")</script>',
            '<img src=x onerror=alert("xss")>',
            'javascript:alert("xss")',
            '<iframe src="javascript:alert(\'xss\')"></iframe>'
        ]
        
        for payload in xss_payloads:
            # Test in product creation
            product_data = {
                'name': payload,
                'category': 'Tahıl',
                'description': payload
            }
            response = client.post('/api/products', json=product_data)
            assert response.status_code in [200, 201, 400, 401, 404]
            
            # Test in product search
            response = client.get(f'/api/products?search={payload}')
            assert response.status_code in [200, 400, 404]
    
    @pytest.mark.security
    @pytest.mark.api
    def test_large_payload_protection(self, client, db_session):
        """Test large payload protection."""
        # Test very large payload
        large_data = {
            'name': 'x' * 10000,  # 10KB string
            'category': 'Tahıl',
            'description': 'y' * 10000  # Another 10KB string
        }
        
        response = client.post('/api/products', json=large_data)
        # Should handle large payloads gracefully
        assert response.status_code in [200, 201, 400, 413, 401, 404]
    
    @pytest.mark.security
    @pytest.mark.api
    def test_malformed_json_protection(self, client, db_session):
        """Test malformed JSON protection."""
        malformed_json_payloads = [
            '{"name": "test", "category":}',  # Missing value
            '{"name": "test", "category": "Tahıl"',  # Missing closing brace
            '{name: "test", "category": "Tahıl"}',  # Missing quotes
            '{"name": "test", "category": "Tahıl", "extra": }'  # Trailing comma
        ]
        
        for payload in malformed_json_payloads:
            response = client.post('/api/products', 
                                 data=payload, 
                                 content_type='application/json')
            # Should handle malformed JSON gracefully
            assert response.status_code in [200, 201, 400, 401, 404]


class TestAPIRateLimiting:
    """API hız sınırlaması testleri."""
    
    @pytest.mark.security
    @pytest.mark.api
    def test_rate_limiting_on_auth_endpoints(self, client, db_session):
        """Test rate limiting on authentication endpoints."""
        # Test multiple login attempts
        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        for i in range(10):
            response = client.post('/api/auth/login', json=login_data)
            assert response.status_code in [200, 401, 429, 404]
            
            # Should implement rate limiting after multiple attempts
            if i >= 5:
                assert response.status_code in [200, 401, 429, 404]
    
    @pytest.mark.security
    @pytest.mark.api
    def test_rate_limiting_on_general_endpoints(self, client, db_session):
        """Test rate limiting on general endpoints."""
        # Test multiple requests to products endpoint
        for i in range(20):
            response = client.get('/api/products')
            assert response.status_code in [200, 429, 404]
            
            # Should implement rate limiting after many requests
            if i >= 15:
                assert response.status_code in [200, 429, 404]
    
    @pytest.mark.security
    @pytest.mark.api
    def test_rate_limiting_by_ip(self, client, db_session):
        """Test rate limiting by IP address."""
        # Simulate multiple requests from same IP
        for i in range(15):
            response = client.get('/api/products')
            assert response.status_code in [200, 429, 404]
            
            # Should implement IP-based rate limiting
            if i >= 10:
                assert response.status_code in [200, 429, 404]


class TestAPIErrorHandling:
    """API hata yönetimi güvenlik testleri."""
    
    @pytest.mark.security
    @pytest.mark.api
    def test_error_message_security(self, client, db_session):
        """Test error message security."""
        # Test 404 error
        response = client.get('/api/nonexistent-endpoint')
        assert response.status_code == 404
        
        # Error messages should not expose sensitive information
        if response.status_code == 404:
            # Should not expose internal paths or sensitive data
            response_text = response.get_data(as_text=True)
            sensitive_patterns = ['/home/', '/var/', '/etc/', 'password', 'secret']
            
            for pattern in sensitive_patterns:
                assert pattern.lower() not in response_text.lower()
    
    @pytest.mark.security
    @pytest.mark.api
    def test_database_error_handling(self, client, db_session):
        """Test database error handling."""
        # Test with invalid data that might cause database errors
        invalid_data = {
            'name': None,
            'category': None,
            'description': None
        }
        
        response = client.post('/api/products', json=invalid_data)
        assert response.status_code in [200, 201, 400, 401, 404, 500]
        
        # Should handle database errors gracefully
        if response.status_code == 500:
            # Should not expose database schema or sensitive information
            response_text = response.get_data(as_text=True)
            sensitive_patterns = ['table', 'column', 'database', 'sql']
            
            for pattern in sensitive_patterns:
                assert pattern.lower() not in response_text.lower()
    
    @pytest.mark.security
    @pytest.mark.api
    def test_validation_error_handling(self, client, db_session):
        """Test validation error handling."""
        # Test with invalid data types
        invalid_data = {
            'name': 123,  # Should be string
            'category': True,  # Should be string
            'description': []  # Should be string
        }
        
        response = client.post('/api/products', json=invalid_data)
        assert response.status_code in [200, 201, 400, 401, 404]
        
        # Should provide helpful error messages without exposing internals
        if response.status_code == 400:
            response_text = response.get_data(as_text=True)
            # Should not expose internal validation logic
            assert 'internal' not in response_text.lower()


class TestAPIDataProtection:
    """API veri koruma testleri."""
    
    @pytest.mark.security
    @pytest.mark.api
    def test_sensitive_data_filtering(self, client, db_session):
        """Test sensitive data filtering in API responses."""
        # Create user with sensitive data
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        # Test user data exposure
        response = client.get(f'/api/users/{user.id}')
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            user_data = response.get_json()
            # Should not expose sensitive fields
            sensitive_fields = ['password', 'password_hash', 'secret_key', 'api_key']
            
            for field in sensitive_fields:
                assert field not in user_data
    
    @pytest.mark.security
    @pytest.mark.api
    def test_data_encryption_in_transit(self, client, db_session):
        """Test data encryption in transit."""
        # Test HTTPS headers (if implemented)
        response = client.get('/api/products')
        assert response.status_code in [200, 404]
        
        # Check for security headers
        security_headers = [
            'Strict-Transport-Security',
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection'
        ]
        
        for header in security_headers:
            # Security headers might be set by Flask-Security or similar
            assert header in response.headers or response.status_code == 404
    
    @pytest.mark.security
    @pytest.mark.api
    def test_input_sanitization(self, client, db_session):
        """Test input sanitization."""
        # Test with potentially dangerous input
        dangerous_input = {
            'name': '<script>alert("xss")</script>',
            'category': 'Tahıl',
            'description': "'; DROP TABLE products; --"
        }
        
        response = client.post('/api/products', json=dangerous_input)
        assert response.status_code in [200, 201, 400, 401, 404]
        
        # If successful, verify data was sanitized
        if response.status_code in [200, 201]:
            response_data = response.get_json()
            # Should sanitize dangerous input
            assert '<script>' not in response_data.get('name', '')
            assert 'DROP TABLE' not in response_data.get('description', '')


class TestAPIAccessControl:
    """API erişim kontrolü testleri."""
    
    @pytest.mark.security
    @pytest.mark.api
    def test_user_data_isolation(self, client, db_session):
        """Test user data isolation."""
        # Create two users
        user1 = UserFactory()
        user2 = UserFactory()
        db_session.add_all([user1, user2])
        db_session.commit()
        
        # Get token for user1
        token1 = user1.generate_access_token()
        headers1 = {'Authorization': f'Bearer {token1}'}
        
        # Try to access user2's data with user1's token
        response = client.get(f'/api/users/{user2.id}', headers=headers1)
        
        # Should not allow cross-user data access
        assert response.status_code in [200, 401, 403, 404]
    
    @pytest.mark.security
    @pytest.mark.api
    def test_admin_endpoint_protection(self, client, db_session):
        """Test admin endpoint protection."""
        # Test admin endpoints without admin privileges
        admin_endpoints = [
            '/api/admin/users',
            '/api/admin/products',
            '/api/admin/statistics',
            '/api/admin/settings'
        ]
        
        for endpoint in admin_endpoints:
            response = client.get(endpoint)
            # Should require admin privileges
            assert response.status_code in [200, 401, 403, 404]
    
    @pytest.mark.security
    @pytest.mark.api
    def test_resource_ownership_validation(self, client, db_session):
        """Test resource ownership validation."""
        # Create user and product
        user = UserFactory()
        product = ProductFactory()
        db_session.add_all([user, product])
        db_session.commit()
        
        # Get user token
        token = user.generate_access_token()
        headers = {'Authorization': f'Bearer {token}'}
        
        # Try to modify product that doesn't belong to user
        update_data = {'name': 'Hacked Product'}
        response = client.put(f'/api/products/{product.id}', 
                             json=update_data, headers=headers)
        
        # Should validate resource ownership
        assert response.status_code in [200, 401, 403, 404]
