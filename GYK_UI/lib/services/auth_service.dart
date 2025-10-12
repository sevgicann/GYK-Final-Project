import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';
import '../core/config/api_config.dart';
import '../models/user.dart';

class AuthService {
  static final AuthService _instance = AuthService._internal();
  factory AuthService() => _instance;
  AuthService._internal();

  final ApiService _apiService = ApiService();
  User? _currentUser;
  String? _authToken;

  // Get current user
  User? get currentUser => _currentUser;

  // Check if user is logged in
  bool get isLoggedIn => _authToken != null && _currentUser != null;

  // Initialize auth service
  Future<void> initialize() async {
    await _loadStoredAuth();
  }

  // Load stored authentication data
  Future<void> _loadStoredAuth() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('auth_token');
      final userJson = prefs.getString('user_data');

      if (token != null && userJson != null) {
        _authToken = token;
        _currentUser = User.fromJson(userJson);
        _apiService.setAuthToken(token);
      }
    } catch (e) {
      // Clear invalid stored data
      await clearAuth();
    }
  }

  // Store authentication data
  Future<void> _storeAuth(String token, User user) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', token);
      await prefs.setString('user_data', user.toJson());
    } catch (e) {
      throw Exception('Failed to store authentication data: $e');
    }
  }

  // Register new user
  Future<User> register({
    required String email,
    required String password,
    required String firstName,
    required String lastName,
    String? phone,
  }) async {
    try {
      final response = await _apiService.post(
        '${ApiConfig.authEndpoint}/register',
        body: {
          'email': email,
          'password': password,
          'first_name': firstName,
          'last_name': lastName,
          'phone': phone,
        },
      );

      final user = User.fromJson(response['user']);
      final token = response['access_token'];

      _currentUser = user;
      _authToken = token;
      _apiService.setAuthToken(token);

      await _storeAuth(token, user);

      return user;
    } catch (e) {
      throw Exception('Registration failed: $e');
    }
  }

  // Login user
  Future<User> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _apiService.post(
        '${ApiConfig.authEndpoint}/login',
        body: {
          'email': email,
          'password': password,
        },
      );

      final user = User.fromJson(response['user']);
      final token = response['access_token'];

      _currentUser = user;
      _authToken = token;
      _apiService.setAuthToken(token);

      await _storeAuth(token, user);

      return user;
    } catch (e) {
      throw Exception('Login failed: $e');
    }
  }

  // Logout user
  Future<void> logout() async {
    try {
      if (_authToken != null) {
        await _apiService.post(
          '${ApiConfig.authEndpoint}/logout',
          requireAuth: true,
        );
      }
    } catch (e) {
      // Continue with logout even if API call fails
    } finally {
      await clearAuth();
    }
  }

  // Clear authentication data
  Future<void> clearAuth() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('auth_token');
      await prefs.remove('user_data');
    } catch (e) {
      // Ignore errors when clearing
    }

    _currentUser = null;
    _authToken = null;
    _apiService.clearAuthToken();
  }

  // Refresh token
  Future<void> refreshToken() async {
    try {
      final response = await _apiService.post(
        '${ApiConfig.authEndpoint}/refresh',
        requireAuth: true,
      );

      final token = response['access_token'];
      _authToken = token;
      _apiService.setAuthToken(token);

      // Update stored token
      if (_currentUser != null) {
        await _storeAuth(token, _currentUser!);
      }
    } catch (e) {
      // If refresh fails, logout user
      await clearAuth();
      throw Exception('Token refresh failed: $e');
    }
  }

  // Update user profile
  Future<User> updateProfile({
    String? firstName,
    String? lastName,
    String? phone,
  }) async {
    try {
      final body = <String, dynamic>{};
      if (firstName != null) body['first_name'] = firstName;
      if (lastName != null) body['last_name'] = lastName;
      if (phone != null) body['phone'] = phone;

      final response = await _apiService.put(
        '${ApiConfig.usersEndpoint}/profile',
        body: body,
        requireAuth: true,
      );

      final user = User.fromJson(response['user']);
      _currentUser = user;

      // Update stored user data
      if (_authToken != null) {
        await _storeAuth(_authToken!, user);
      }

      return user;
    } catch (e) {
      throw Exception('Profile update failed: $e');
    }
  }

  // Change password
  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
  }) async {
    try {
      await _apiService.put(
        '${ApiConfig.usersEndpoint}/change-password',
        body: {
          'current_password': currentPassword,
          'new_password': newPassword,
        },
        requireAuth: true,
      );
    } catch (e) {
      throw Exception('Password change failed: $e');
    }
  }

  // Delete account
  Future<void> deleteAccount() async {
    try {
      await _apiService.delete(
        '${ApiConfig.usersEndpoint}/profile',
        requireAuth: true,
      );
    } finally {
      await clearAuth();
    }
  }
}


