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

  // GET request with retry logic
  Future<Map<String, dynamic>> get(
    String endpoint, {
    bool requireAuth = false,
    Map<String, String>? queryParams,
    int maxRetries = 2,
  }) async {
    int attempt = 0;
    
    while (attempt <= maxRetries) {
      try {
        Uri uri = Uri.parse(endpoint);
        
        if (queryParams != null && queryParams.isNotEmpty) {
          uri = uri.replace(queryParameters: queryParams);
        }

        print('🚀 API GET Request: $uri (Attempt ${attempt + 1}/${maxRetries + 1})');
        print('🔐 Require Auth: $requireAuth');

        final response = await http.get(
          uri,
          headers: _getHeaders(includeAuth: requireAuth),
        ).timeout(ApiConfig.connectTimeout);

        print('✅ API Response: ${response.statusCode}');
        print('📄 Response Body: ${response.body}');

        return _handleResponse(response);
      } catch (e) {
        attempt++;
        print('❌ API Error (Attempt $attempt): $e');
        
        // If this is the last attempt, throw the error
        if (attempt > maxRetries) {
          throw _handleError(e);
        }
        
        // Wait before retrying (exponential backoff)
        await Future.delayed(Duration(seconds: attempt * 2));
        print('🔄 Retrying request...');
      }
    }
    
    // This should never be reached, but just in case
    throw ApiException('Tüm deneme sayısı tükendi');
  }

  // POST request with retry logic
  Future<Map<String, dynamic>> post(
    String endpoint, {
    Map<String, dynamic>? body,
    bool requireAuth = false,
    int maxRetries = 2,
  }) async {
    int attempt = 0;
    
    while (attempt <= maxRetries) {
      try {
        print('🚀 API POST Request: $endpoint (Attempt ${attempt + 1}/${maxRetries + 1})');
        print('📦 Request Body: $body');
        print('🔐 Require Auth: $requireAuth');
        print('📋 Headers: ${_getHeaders(includeAuth: requireAuth)}');
        
        final response = await http.post(
          Uri.parse(endpoint),
          headers: _getHeaders(includeAuth: requireAuth),
          body: body != null ? json.encode(body) : null,
        ).timeout(ApiConfig.connectTimeout);

        print('✅ API Response: ${response.statusCode}');
        print('📄 Response Body: ${response.body}');
        print('📋 Response Headers: ${response.headers}');

        return _handleResponse(response);
      } catch (e) {
        attempt++;
        print('❌ API Error (Attempt $attempt): $e');
        print('❌ Error type: ${e.runtimeType}');
        
        // If this is the last attempt, throw the error
        if (attempt > maxRetries) {
          throw _handleError(e);
        }
        
        // Wait before retrying (exponential backoff)
        await Future.delayed(Duration(seconds: attempt * 2));
        print('🔄 Retrying request...');
      }
    }
    
    // This should never be reached, but just in case
    throw ApiException('Tüm deneme sayısı tükendi');
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

    print('📊 Processing response: Status=$statusCode, Body=$body');

    // Parse JSON response
    Map<String, dynamic> jsonResponse;
    try {
      jsonResponse = json.decode(body);
    } catch (e) {
      print('❌ JSON Parse Error: $e');
      throw ApiException('Geçersiz API yanıtı: $e');
    }

    // Check for successful status codes
    if (statusCode >= 200 && statusCode < 300) {
      print('✅ Success response received');
      return jsonResponse;
    } else {
      // Handle error responses with better error messages
      final message = jsonResponse['message'] ?? 'Bilinmeyen hata oluştu';
      final error = jsonResponse['error'] ?? '';
      final details = jsonResponse['details'] ?? '';
      
      // Combine error information for better debugging
      String fullErrorMessage = message;
      if (error.isNotEmpty) {
        fullErrorMessage += ' (Teknik Hata: $error)';
      }
      if (details.isNotEmpty) {
        fullErrorMessage += ' - $details';
      }
      
      print('❌ Error response: $fullErrorMessage');
      print('🔍 Full error details: ${jsonResponse.toString()}');
      
      switch (statusCode) {
        case 400:
          throw BadRequestException('Geçersiz istek gönderildi: $fullErrorMessage', details);
        case 401:
          throw UnauthorizedException('Giriş yapmanız gerekiyor: $fullErrorMessage', details);
        case 403:
          throw ForbiddenException('Bu işlem için yetkiniz yok: $fullErrorMessage', details);
        case 404:
          throw NotFoundException('İstenen kaynak bulunamadı: $fullErrorMessage', details);
        case 422:
          throw ValidationException('Girilen bilgiler hatalı: $fullErrorMessage', details, jsonResponse['errors']);
        case 429:
          throw RateLimitException('Çok fazla istek gönderildi, lütfen bekleyin: $fullErrorMessage', details);
        case 500:
          // Special handling for 500 errors - provide user-friendly message
          String userMessage = 'Sunucu hatası oluştu. Lütfen tekrar deneyin.';
          if (error.contains('NoneType') && error.contains('strip')) {
            userMessage = 'Konum bilgileri işlenirken hata oluştu. Lütfen bilgilerinizi kontrol edip tekrar deneyin.';
          }
          throw ServerException('$userMessage Teknik detay: $fullErrorMessage', details);
        default:
          throw ApiException('HTTP $statusCode hatası: $fullErrorMessage', details);
      }
    }
  }

  // Handle network and other errors
  ApiException _handleError(dynamic error) {
    print('🔍 Error details: $error');
    print('🔍 Error type: ${error.runtimeType}');
    
    if (error is SocketException) {
      return ApiException('İnternet bağlantısı başarısız. Lütfen bağlantınızı kontrol edin ve tekrar deneyin.');
    } else if (error is HttpException) {
      return ApiException('Sunucu ile iletişim hatası: ${error.message}');
    } else if (error is FormatException) {
      return ApiException('Sunucudan gelen yanıt formatı hatalı. Lütfen tekrar deneyin.');
    } else if (error.toString().contains('TimeoutException')) {
      return ApiException('İstek zaman aşımına uğradı. Lütfen tekrar deneyin.');
    } else if (error is ApiException) {
      // Re-throw ApiException as-is (already handled)
      return error;
    } else {
      return ApiException('Beklenmeyen bir hata oluştu: ${error.toString()}');
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


