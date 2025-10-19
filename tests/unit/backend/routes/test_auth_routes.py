"""
Unit tests for Authentication routes

Bu test dosyası auth routes için birim testlerini içerir.
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import create_access_token
from tests.fixtures.data.sample_data import SAMPLE_USERS, INVALID_DATA


class TestAuthRoutes:
    """Authentication routes test sınıfı."""
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_register_success(self, client, db_session):
        """Test successful user registration."""
        user_data = SAMPLE_USERS[0]
        
        response = client.post('/api/auth/register', json=user_data)
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert 'message' in data
        assert 'data' in data
        assert 'user' in data['data']
        assert 'token' in data['data']
        
        # Verify user data
        user = data['data']['user']
        assert user['name'] == user_data['name']
        assert user['email'] == user_data['email']
        assert user['language'] == user_data['language']
        assert 'id' in user
        assert 'created_at' in user
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_register_missing_data(self, client):
        """Test registration with missing data."""
        response = client.post('/api/auth/register', json={})
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'message' in data
        assert 'Request data is required' in data['message']
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_register_missing_name(self, client):
        """Test registration with missing name."""
        user_data = SAMPLE_USERS[0].copy()
        user_data['name'] = ''
        
        response = client.post('/api/auth/register', json=user_data)
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'name' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        user_data = SAMPLE_USERS[0].copy()
        user_data['email'] = 'invalid-email'
        
        response = client.post('/api/auth/register', json=user_data)
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'email' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        user_data = SAMPLE_USERS[0].copy()
        user_data['password'] = '123'  # Too short
        
        response = client.post('/api/auth/register', json=user_data)
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'password' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_register_duplicate_email(self, client, db_session):
        """Test registration with duplicate email."""
        user_data = SAMPLE_USERS[0]
        
        # Register first user
        response1 = client.post('/api/auth/register', json=user_data)
        assert response1.status_code == 201
        
        # Try to register with same email
        response2 = client.post('/api/auth/register', json=user_data)
        
        # Verify error response
        assert response2.status_code == 400
        data = response2.get_json()
        assert data['success'] is False
        assert 'email' in data['message'].lower() or 'already' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_login_success(self, client, db_session):
        """Test successful user login."""
        user_data = SAMPLE_USERS[0]
        
        # Register user first
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code == 201
        
        # Login with credentials
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        response = client.post('/api/auth/login', json=login_data)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'message' in data
        assert 'data' in data
        assert 'user' in data['data']
        assert 'token' in data['data']
        
        # Verify user data
        user = data['data']['user']
        assert user['email'] == user_data['email']
        assert 'id' in user
        assert 'last_login' in user
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_login_invalid_credentials(self, client, db_session):
        """Test login with invalid credentials."""
        user_data = SAMPLE_USERS[0]
        
        # Register user first
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code == 201
        
        # Login with wrong password
        login_data = {
            'email': user_data['email'],
            'password': 'wrong_password'
        }
        response = client.post('/api/auth/login', json=login_data)
        
        # Verify error response
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert 'invalid' in data['message'].lower() or 'credentials' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        response = client.post('/api/auth/login', json=login_data)
        
        # Verify error response
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert 'invalid' in data['message'].lower() or 'credentials' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_login_missing_data(self, client):
        """Test login with missing data."""
        response = client.post('/api/auth/login', json={})
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'required' in data['message'].lower()
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_refresh_token_success(self, client, db_session, auth_headers):
        """Test successful token refresh."""
        user_data = SAMPLE_USERS[0]
        
        # Register and login user
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code == 201
        
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        login_response = client.post('/api/auth/login', json=login_data)
        assert login_response.status_code == 200
        
        token = login_response.get_json()['data']['token']
        headers = auth_headers(token)
        
        # Refresh token
        response = client.post('/api/auth/refresh', headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'token' in data['data']
        assert data['data']['token'] != token  # Should be a new token
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_refresh_token_invalid(self, client, auth_headers):
        """Test token refresh with invalid token."""
        headers = auth_headers('invalid-token')
        
        response = client.post('/api/auth/refresh', headers=headers)
        
        # Verify error response
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_logout_success(self, client, db_session, auth_headers):
        """Test successful logout."""
        user_data = SAMPLE_USERS[0]
        
        # Register and login user
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code == 201
        
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        login_response = client.post('/api/auth/login', json=login_data)
        assert login_response.status_code == 200
        
        token = login_response.get_json()['data']['token']
        headers = auth_headers(token)
        
        # Logout
        response = client.post('/api/auth/logout', headers=headers)
        
        # Verify response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'message' in data
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_logout_without_token(self, client):
        """Test logout without token."""
        response = client.post('/api/auth/logout')
        
        # Should still work (token might be invalid)
        assert response.status_code in [200, 401]
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_register_with_optional_fields(self, client, db_session):
        """Test registration with optional fields."""
        user_data = SAMPLE_USERS[0].copy()
        user_data.update({
            'phone': '+905551234567',
            'city': 'Istanbul',
            'district': 'Kadıköy',
            'latitude': 41.0082,
            'longitude': 29.0156,
            'is_gps_enabled': True
        })
        
        response = client.post('/api/auth/register', json=user_data)
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        
        # Verify optional fields were saved
        user = data['data']['user']
        assert user['location']['city'] == 'Istanbul'
        assert user['location']['district'] == 'Kadıköy'
        assert user['location']['latitude'] == 41.0082
        assert user['location']['longitude'] == 29.0156
        assert user['location']['is_gps_enabled'] is True
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_login_case_insensitive_email(self, client, db_session):
        """Test login with case insensitive email."""
        user_data = SAMPLE_USERS[0]
        
        # Register user
        register_response = client.post('/api/auth/register', json=user_data)
        assert register_response.status_code == 201
        
        # Login with uppercase email
        login_data = {
            'email': user_data['email'].upper(),
            'password': user_data['password']
        }
        response = client.post('/api/auth/login', json=login_data)
        
        # Should still work
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_register_default_language(self, client, db_session):
        """Test registration with default language."""
        user_data = SAMPLE_USERS[0].copy()
        del user_data['language']  # Remove language field
        
        response = client.post('/api/auth/register', json=user_data)
        
        # Verify response
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        
        # Verify default language
        user = data['data']['user']
        assert user['language'] == 'tr'  # Default language
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_register_invalid_json(self, client):
        """Test registration with invalid JSON."""
        response = client.post('/api/auth/register', 
                             data='invalid json', 
                             content_type='application/json')
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    @pytest.mark.unit
    @pytest.mark.api
    def test_login_invalid_json(self, client):
        """Test login with invalid JSON."""
        response = client.post('/api/auth/login', 
                             data='invalid json', 
                             content_type='application/json')
        
        # Verify error response
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
