"""
API Test Client Utilities

Bu modül API testleri için yardımcı fonksiyonları içerir.
"""

import json
from typing import Dict, Any, Optional
from flask import Flask
from flask.testing import FlaskClient
from tests.fixtures.data.sample_data import API_ENDPOINTS


class APITestClient:
    """API test client wrapper with helper methods."""
    
    def __init__(self, client: FlaskClient, app: Flask):
        self.client = client
        self.app = app
    
    def make_request(self, 
                    method: str, 
                    endpoint: str, 
                    data: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, str]] = None,
                    query_params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Make an API request and return parsed JSON response.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            headers: Request headers
            query_params: Query parameters
            
        Returns:
            Parsed JSON response
        """
        url = endpoint
        if query_params:
            url += '?' + '&'.join([f"{k}={v}" for k, v in query_params.items()])
        
        if method.upper() == 'GET':
            response = self.client.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = self.client.post(
                url, 
                data=json.dumps(data) if data else None,
                headers={**(headers or {}), 'Content-Type': 'application/json'}
            )
        elif method.upper() == 'PUT':
            response = self.client.put(
                url,
                data=json.dumps(data) if data else None,
                headers={**(headers or {}), 'Content-Type': 'application/json'}
            )
        elif method.upper() == 'DELETE':
            response = self.client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return {
            'status_code': response.status_code,
            'data': json.loads(response.data) if response.data else {},
            'headers': dict(response.headers)
        }
    
    def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None, 
            query_params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make GET request."""
        return self.make_request('GET', endpoint, headers=headers, query_params=query_params)
    
    def post(self, endpoint: str, data: Dict[str, Any], 
             headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make POST request."""
        return self.make_request('POST', endpoint, data=data, headers=headers)
    
    def put(self, endpoint: str, data: Dict[str, Any], 
            headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make PUT request."""
        return self.make_request('PUT', endpoint, data=data, headers=headers)
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make DELETE request."""
        return self.make_request('DELETE', endpoint, headers=headers)
    
    def authenticate(self, email: str, password: str) -> str:
        """
        Authenticate user and return JWT token.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            JWT token
        """
        response = self.post('/api/auth/login', {
            'email': email,
            'password': password
        })
        
        if response['status_code'] == 200 and response['data']['success']:
            return response['data']['data']['token']
        else:
            raise Exception(f"Authentication failed: {response['data']}")
    
    def get_auth_headers(self, token: str) -> Dict[str, str]:
        """Get authentication headers with token."""
        return {'Authorization': f'Bearer {token}'}
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        response = self.post('/api/auth/register', user_data)
        return response
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user."""
        response = self.post('/api/auth/login', {
            'email': email,
            'password': password
        })
        return response
    
    def create_product(self, product_data: Dict[str, Any], token: str) -> Dict[str, Any]:
        """Create a new product."""
        headers = self.get_auth_headers(token)
        response = self.post('/api/products', product_data, headers)
        return response
    
    def get_products(self, token: str, query_params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Get products."""
        headers = self.get_auth_headers(token)
        response = self.get('/api/products', headers, query_params)
        return response
    
    def get_product_by_id(self, product_id: str, token: str) -> Dict[str, Any]:
        """Get product by ID."""
        headers = self.get_auth_headers(token)
        response = self.get(f'/api/products/{product_id}', headers)
        return response
    
    def update_product(self, product_id: str, product_data: Dict[str, Any], token: str) -> Dict[str, Any]:
        """Update product."""
        headers = self.get_auth_headers(token)
        response = self.put(f'/api/products/{product_id}', product_data, headers)
        return response
    
    def delete_product(self, product_id: str, token: str) -> Dict[str, Any]:
        """Delete product."""
        headers = self.get_auth_headers(token)
        response = self.delete(f'/api/products/{product_id}', headers)
        return response
    
    def create_environment(self, environment_data: Dict[str, Any], token: str) -> Dict[str, Any]:
        """Create environment."""
        headers = self.get_auth_headers(token)
        response = self.post('/api/environments', environment_data, headers)
        return response
    
    def get_environments(self, token: str) -> Dict[str, Any]:
        """Get environments."""
        headers = self.get_auth_headers(token)
        response = self.get('/api/environments', headers)
        return response
    
    def predict_crop(self, environment_data: Dict[str, Any], token: str) -> Dict[str, Any]:
        """Predict crop from environment."""
        headers = self.get_auth_headers(token)
        response = self.post('/api/ml/predict-crop', environment_data, headers)
        return response
    
    def predict_environment(self, crop_data: Dict[str, Any], token: str) -> Dict[str, Any]:
        """Predict environment for crop."""
        headers = self.get_auth_headers(token)
        response = self.post('/api/ml/predict-environment', crop_data, headers)
        return response
    
    def get_ml_health(self, token: str) -> Dict[str, Any]:
        """Get ML service health."""
        headers = self.get_auth_headers(token)
        response = self.get('/api/ml/health', headers)
        return response


class APITestAssertions:
    """API test assertion helpers."""
    
    @staticmethod
    def assert_success_response(response: Dict[str, Any], expected_status: int = 200):
        """Assert successful API response."""
        assert response['status_code'] == expected_status, \
            f"Expected status {expected_status}, got {response['status_code']}"
        assert response['data']['success'] is True, \
            f"Expected success=True, got {response['data']}"
    
    @staticmethod
    def assert_error_response(response: Dict[str, Any], expected_status: int = 400):
        """Assert error API response."""
        assert response['status_code'] == expected_status, \
            f"Expected status {expected_status}, got {response['status_code']}"
        assert response['data']['success'] is False, \
            f"Expected success=False, got {response['data']}"
        assert 'message' in response['data'], \
            f"Expected error message, got {response['data']}"
    
    @staticmethod
    def assert_unauthorized_response(response: Dict[str, Any]):
        """Assert unauthorized API response."""
        APITestAssertions.assert_error_response(response, 401)
    
    @staticmethod
    def assert_not_found_response(response: Dict[str, Any]):
        """Assert not found API response."""
        APITestAssertions.assert_error_response(response, 404)
    
    @staticmethod
    def assert_validation_error(response: Dict[str, Any], field_name: str = None):
        """Assert validation error response."""
        APITestAssertions.assert_error_response(response, 400)
        
        if field_name:
            assert field_name.lower() in response['data']['message'].lower(), \
                f"Expected field '{field_name}' in error message: {response['data']['message']}"
    
    @staticmethod
    def assert_pagination_response(response: Dict[str, Any]):
        """Assert paginated response structure."""
        APITestAssertions.assert_success_response(response)
        
        data = response['data']['data']
        assert 'pagination' in data, "Expected pagination in response data"
        
        pagination = data['pagination']
        required_fields = ['page', 'per_page', 'total', 'pages', 'has_next', 'has_prev']
        for field in required_fields:
            assert field in pagination, f"Expected '{field}' in pagination data"
    
    @staticmethod
    def assert_list_response(response: Dict[str, Any], list_key: str = 'data'):
        """Assert list response structure."""
        APITestAssertions.assert_success_response(response)
        
        data = response['data']['data']
        assert list_key in data, f"Expected '{list_key}' in response data"
        assert isinstance(data[list_key], list), f"Expected '{list_key}' to be a list"


def create_api_client(client: FlaskClient, app: Flask) -> APITestClient:
    """Create API test client."""
    return APITestClient(client, app)


def make_authenticated_request(client: APITestClient, 
                             method: str, 
                             endpoint: str, 
                             email: str, 
                             password: str,
                             data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Make authenticated API request."""
    token = client.authenticate(email, password)
    headers = client.get_auth_headers(token)
    
    if method.upper() == 'GET':
        return client.get(endpoint, headers)
    elif method.upper() == 'POST':
        return client.post(endpoint, data or {}, headers)
    elif method.upper() == 'PUT':
        return client.put(endpoint, data or {}, headers)
    elif method.upper() == 'DELETE':
        return client.delete(endpoint, headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")


def test_api_endpoint(client: APITestClient, 
                     endpoint: str, 
                     method: str = 'GET',
                     expected_status: int = 200,
                     data: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Test API endpoint with basic assertions."""
    response = client.make_request(method, endpoint, data, headers)
    
    if expected_status == 200:
        APITestAssertions.assert_success_response(response)
    else:
        APITestAssertions.assert_error_response(response, expected_status)
    
    return response
