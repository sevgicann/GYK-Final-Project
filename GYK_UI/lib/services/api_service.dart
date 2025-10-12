import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../core/config/api_config.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  String? _authToken;

  // Set authentication token
  void setAuthToken(String token) {
    _authToken = token;
  }

  // Clear authentication token
  void clearAuthToken() {
    _authToken = null;
  }

  // Get headers with optional auth token
  Map<String, String> _getHeaders({bool includeAuth = false}) {
    final headers = Map<String, String>.from(ApiConfig.defaultHeaders);
    
    if (includeAuth && _authToken != null) {
      headers['Authorization'] = 'Bearer $_authToken';
    }
    
    return headers;
  }

  // GET request
  Future<Map<String, dynamic>> get(
    String endpoint, {
    bool requireAuth = false,
    Map<String, String>? queryParams,
  }) async {
    try {
      Uri uri = Uri.parse(endpoint);
      
      if (queryParams != null && queryParams.isNotEmpty) {
        uri = uri.replace(queryParameters: queryParams);
      }

      final response = await http.get(
        uri,
        headers: _getHeaders(includeAuth: requireAuth),
      ).timeout(ApiConfig.connectTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  // POST request
  Future<Map<String, dynamic>> post(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requireAuth = false,
  }) async {
    try {
      final response = await http.post(
        Uri.parse(endpoint),
        headers: _getHeaders(includeAuth: requireAuth),
        body: body != null ? json.encode(body) : null,
      ).timeout(ApiConfig.connectTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  // PUT request
  Future<Map<String, dynamic>> put(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requireAuth = true,
  }) async {
    try {
      final response = await http.put(
        Uri.parse(endpoint),
        headers: _getHeaders(includeAuth: requireAuth),
        body: body != null ? json.encode(body) : null,
      ).timeout(ApiConfig.connectTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  // DELETE request
  Future<Map<String, dynamic>> delete(
    String endpoint, {
    bool requireAuth = true,
  }) async {
    try {
      final response = await http.delete(
        Uri.parse(endpoint),
        headers: _getHeaders(includeAuth: requireAuth),
      ).timeout(ApiConfig.connectTimeout);

      return _handleResponse(response);
    } catch (e) {
      throw _handleError(e);
    }
  }

  // Handle HTTP response
  Map<String, dynamic> _handleResponse(http.Response response) {
    final statusCode = response.statusCode;
    final body = response.body;

    // Parse JSON response
    Map<String, dynamic> jsonResponse;
    try {
      jsonResponse = json.decode(body);
    } catch (e) {
      throw ApiException('Invalid JSON response: $e');
    }

    // Check for successful status codes
    if (statusCode >= 200 && statusCode < 300) {
      return jsonResponse;
    } else {
      // Handle error responses
      final message = jsonResponse['message'] ?? 'Unknown error occurred';
      final details = jsonResponse['details'] ?? '';
      
      switch (statusCode) {
        case 400:
          throw BadRequestException(message, details);
        case 401:
          throw UnauthorizedException(message, details);
        case 403:
          throw ForbiddenException(message, details);
        case 404:
          throw NotFoundException(message, details);
        case 422:
          throw ValidationException(message, details, jsonResponse['errors']);
        case 429:
          throw RateLimitException(message, details);
        case 500:
          throw ServerException(message, details);
        default:
          throw ApiException('HTTP $statusCode: $message', details);
      }
    }
  }

  // Handle network and other errors
  ApiException _handleError(dynamic error) {
    if (error is SocketException) {
      return ApiException('Network connection failed. Please check your internet connection.');
    } else if (error is HttpException) {
      return ApiException('HTTP error: ${error.message}');
    } else if (error is FormatException) {
      return ApiException('Invalid response format');
    } else if (error is ApiException) {
      return error;
    } else {
      return ApiException('Unexpected error: ${error.toString()}');
    }
  }

  // Health check
  Future<bool> healthCheck() async {
    try {
      final response = await get(ApiConfig.healthEndpoint);
      return response['status'] == 'OK';
    } catch (e) {
      return false;
    }
  }
}

// Custom exception classes
class ApiException implements Exception {
  final String message;
  final String? details;

  ApiException(this.message, [this.details]);

  @override
  String toString() => details != null ? '$message: $details' : message;
}

class BadRequestException extends ApiException {
  BadRequestException(String message, [String? details]) : super(message, details);
}

class UnauthorizedException extends ApiException {
  UnauthorizedException(String message, [String? details]) : super(message, details);
}

class ForbiddenException extends ApiException {
  ForbiddenException(String message, [String? details]) : super(message, details);
}

class NotFoundException extends ApiException {
  NotFoundException(String message, [String? details]) : super(message, details);
}

class ValidationException extends ApiException {
  final Map<String, dynamic>? errors;
  
  ValidationException(String message, [String? details, this.errors]) : super(message, details);
}

class RateLimitException extends ApiException {
  RateLimitException(String message, [String? details]) : super(message, details);
}

class ServerException extends ApiException {
  ServerException(String message, [String? details]) : super(message, details);
}


