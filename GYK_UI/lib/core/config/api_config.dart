class ApiConfig {
  // Backend API base URL
  static const String baseUrl = 'http://localhost:5000';
  
  // API endpoints
  static const String authEndpoint = '$baseUrl/api/auth';
  static const String usersEndpoint = '$baseUrl/api/users';
  static const String productsEndpoint = '$baseUrl/api/products';
  static const String environmentsEndpoint = '$baseUrl/api/environments';
  static const String recommendationsEndpoint = '$baseUrl/api/recommendations';
  
  // Health check endpoint
  static const String healthEndpoint = '$baseUrl/health';
  
  // API timeout settings
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
  
  // Headers
  static const Map<String, String> defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
  
  // Get authorization header
  static Map<String, String> getAuthHeaders(String token) {
    return {
      ...defaultHeaders,
      'Authorization': 'Bearer $token',
    };
  }
}


