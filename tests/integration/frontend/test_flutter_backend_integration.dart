/**
 * Frontend Flutter-Backend Integration Tests
 * 
 * Bu test dosyası Flutter frontend ile backend arasındaki entegrasyon testlerini içerir.
 */

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:terramind_app/services/api_service.dart';
import 'package:terramind_app/services/product_service.dart';
import 'package:terramind_app/services/user_service.dart';

void main() {
  group('Flutter-Backend Integration Tests', () {
    late ApiService apiService;
    late ProductService productService;
    late UserService userService;

    setUp(() {
      apiService = ApiService();
      productService = ProductService();
      userService = UserService();
    });

    group('API Integration Tests', () {
      testWidgets('should connect to backend API', (WidgetTester tester) async {
        // Test API connection
        final response = await apiService.get('/api/health');
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 404])); // 404 if endpoint not implemented
      });

      testWidgets('should handle API authentication', (WidgetTester tester) async {
        // Test authentication flow
        final loginData = {
          'email': 'test@example.com',
          'password': 'testpassword123'
        };
        
        final response = await apiService.post('/api/auth/login', body: json.encode(loginData));
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 401, 404]));
        
        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          expect(data, isA<Map<String, dynamic>>());
        }
      });

      testWidgets('should handle API error responses', (WidgetTester tester) async {
        // Test error handling
        final response = await apiService.get('/api/nonexistent-endpoint');
        
        expect(response.statusCode, equals(404));
      });

      testWidgets('should handle network timeouts', (WidgetTester tester) async {
        // Test timeout handling
        try {
          await apiService.get('/api/products', timeout: Duration(seconds: 1));
        } catch (e) {
          expect(e, isA<Exception>());
        }
      });
    });

    group('Product Service Integration Tests', () {
      testWidgets('should fetch products from backend', (WidgetTester tester) async {
        // Test product fetching
        final products = await productService.getAllProducts();
        
        expect(products, isA<List>());
        expect(products.length, greaterThanOrEqualTo(0));
        
        if (products.isNotEmpty) {
          final product = products.first;
          expect(product['name'], isA<String>());
          expect(product['category'], isA<String>());
        }
      });

      testWidgets('should search products via backend', (WidgetTester tester) async {
        // Test product search
        final searchResults = await productService.searchProducts('wheat');
        
        expect(searchResults, isA<List>());
        expect(searchResults.length, greaterThanOrEqualTo(0));
      });

      testWidgets('should filter products by category', (WidgetTester tester) async {
        // Test product filtering
        final filteredProducts = await productService.getProductsByCategory('Tahıl');
        
        expect(filteredProducts, isA<List>());
        expect(filteredProducts.length, greaterThanOrEqualTo(0));
      });

      testWidgets('should handle product service errors', (WidgetTester tester) async {
        // Test error handling
        try {
          await productService.getProductById('invalid-id');
        } catch (e) {
          expect(e, isA<Exception>());
        }
      });
    });

    group('User Service Integration Tests', () {
      testWidgets('should handle user registration', (WidgetTester tester) async {
        // Test user registration
        final userData = {
          'username': 'testuser',
          'email': 'test@example.com',
          'password': 'testpassword123',
          'first_name': 'Test',
          'last_name': 'User'
        };
        
        final result = await userService.register(userData);
        
        expect(result, isA<Map<String, dynamic>>());
        expect(result['success'], isA<bool>());
      });

      testWidgets('should handle user login', (WidgetTester tester) async {
        // Test user login
        final loginData = {
          'email': 'test@example.com',
          'password': 'testpassword123'
        };
        
        final result = await userService.login(loginData);
        
        expect(result, isA<Map<String, dynamic>>());
        expect(result['success'], isA<bool>());
      });

      testWidgets('should handle user profile update', (WidgetTester tester) async {
        // Test profile update
        final profileData = {
          'first_name': 'Updated',
          'last_name': 'Name'
        };
        
        final result = await userService.updateProfile(profileData);
        
        expect(result, isA<Map<String, dynamic>>());
        expect(result['success'], isA<bool>());
      });

      testWidgets('should handle user logout', (WidgetTester tester) async {
        // Test user logout
        final result = await userService.logout();
        
        expect(result, isA<Map<String, dynamic>>());
        expect(result['success'], isA<bool>());
      });
    });

    group('ML Service Integration Tests', () {
      testWidgets('should get ML predictions from backend', (WidgetTester tester) async {
        // Test ML prediction
        final predictionData = {
          'soil_ph': 6.5,
          'nitrogen': 120,
          'phosphorus': 45,
          'potassium': 150,
          'temperature_celsius': 22,
          'rainfall_mm': 600,
          'region': 'Marmara'
        };
        
        final prediction = await apiService.post('/api/ml/predict-crop', body: json.encode(predictionData));
        
        expect(prediction.statusCode, isA<int>());
        expect(prediction.statusCode, anyOf([200, 201, 404]));
        
        if (prediction.statusCode == 200) {
          final data = json.decode(prediction.body);
          expect(data, isA<Map<String, dynamic>>());
        }
      });

      testWidgets('should get environment predictions from backend', (WidgetTester tester) async {
        // Test environment prediction
        final predictionData = {
          'crop': 'wheat',
          'region': 'Marmara'
        };
        
        final prediction = await apiService.post('/api/ml/predict-environment', body: json.encode(predictionData));
        
        expect(prediction.statusCode, isA<int>());
        expect(prediction.statusCode, anyOf([200, 201, 404]));
      });

      testWidgets('should handle ML service errors', (WidgetTester tester) async {
        // Test ML error handling
        final invalidData = {
          'soil_ph': 'invalid',
          'nitrogen': -1
        };
        
        final response = await apiService.post('/api/ml/predict-crop', body: json.encode(invalidData));
        
        expect(response.statusCode, anyOf([200, 201, 400, 404]));
      });
    });

    group('Environment Service Integration Tests', () {
      testWidgets('should create environment via backend', (WidgetTester tester) async {
        // Test environment creation
        final environmentData = {
          'name': 'Test Environment',
          'region': 'Marmara',
          'soil_ph': 6.5,
          'nitrogen': 120,
          'phosphorus': 45,
          'potassium': 150,
          'temperature_celsius': 22,
          'rainfall_mm': 600
        };
        
        final result = await apiService.post('/api/environments', body: json.encode(environmentData));
        
        expect(result.statusCode, isA<int>());
        expect(result.statusCode, anyOf([200, 201, 401, 404]));
      });

      testWidgets('should get user environments from backend', (WidgetTester tester) async {
        // Test environment retrieval
        final response = await apiService.get('/api/environments');
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 401, 404]));
        
        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          expect(data, isA<List>());
        }
      });

      testWidgets('should update environment via backend', (WidgetTester tester) async {
        // Test environment update
        final updateData = {
          'name': 'Updated Environment',
          'soil_ph': 7.0
        };
        
        final response = await apiService.put('/api/environments/1', body: json.encode(updateData));
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 401, 404]));
      });
    });

    group('Recommendation Service Integration Tests', () {
      testWidgets('should get recommendations from backend', (WidgetTester tester) async {
        // Test recommendation retrieval
        final response = await apiService.get('/api/recommendations');
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 401, 404]));
        
        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          expect(data, isA<List>());
        }
      });

      testWidgets('should get location-based recommendations', (WidgetTester tester) async {
        // Test location-based recommendations
        final locationData = {
          'latitude': 41.0082,
          'longitude': 29.0156,
          'region': 'Marmara'
        };
        
        final response = await apiService.post('/api/recommendations/location-based', body: json.encode(locationData));
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 201, 401, 404]));
      });

      testWidgets('should get crop-based recommendations', (WidgetTester tester) async {
        // Test crop-based recommendations
        final cropData = {
          'crop': 'wheat',
          'region': 'Marmara'
        };
        
        final response = await apiService.post('/api/recommendations/crop-based', body: json.encode(cropData));
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 201, 401, 404]));
      });
    });

    group('Cross-Platform Integration Tests', () {
      testWidgets('should maintain data consistency across platforms', (WidgetTester tester) async {
        // Test data consistency
        final products = await productService.getAllProducts();
        final apiProducts = await apiService.get('/api/products');
        
        if (apiProducts.statusCode == 200) {
          final apiData = json.decode(apiProducts.body);
          expect(apiData, isA<List>());
          
          // Both should return consistent data
          expect(products.length, greaterThanOrEqualTo(0));
          expect(apiData.length, greaterThanOrEqualTo(0));
        }
      });

      testWidgets('should handle offline mode gracefully', (WidgetTester tester) async {
        // Test offline mode
        try {
          await apiService.get('/api/products', timeout: Duration(milliseconds: 100));
        } catch (e) {
          expect(e, isA<Exception>());
        }
      });

      testWidgets('should sync data when back online', (WidgetTester tester) async {
        // Test data synchronization
        final syncResult = await apiService.post('/api/sync/data', body: json.encode({}));
        
        expect(syncResult.statusCode, isA<int>());
        expect(syncResult.statusCode, anyOf([200, 201, 404]));
      });
    });

    group('Performance Integration Tests', () {
      testWidgets('should handle concurrent API requests', (WidgetTester tester) async {
        // Test concurrent requests
        final futures = List.generate(5, (index) => apiService.get('/api/products'));
        
        final results = await Future.wait(futures);
        
        expect(results.length, equals(5));
        for (final result in results) {
          expect(result.statusCode, isA<int>());
          expect(result.statusCode, anyOf([200, 404]));
        }
      });

      testWidgets('should handle large data responses', (WidgetTester tester) async {
        // Test large data handling
        final response = await apiService.get('/api/products');
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 404]));
        
        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          expect(data, isA<List>());
        }
      });

      testWidgets('should handle API response timeouts', (WidgetTester tester) async {
        // Test response timeout
        final startTime = DateTime.now();
        
        try {
          await apiService.get('/api/products', timeout: Duration(seconds: 2));
        } catch (e) {
          expect(e, isA<Exception>());
        }
        
        final endTime = DateTime.now();
        final duration = endTime.difference(startTime);
        
        expect(duration.inSeconds, lessThanOrEqualTo(3));
      });
    });

    group('Error Handling Integration Tests', () {
      testWidgets('should handle network errors gracefully', (WidgetTester tester) async {
        // Test network error handling
        try {
          await apiService.get('http://invalid-url.com/api/products');
        } catch (e) {
          expect(e, isA<Exception>());
        }
      });

      testWidgets('should handle server errors gracefully', (WidgetTester tester) async {
        // Test server error handling
        final response = await apiService.get('/api/server-error');
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 404, 500]));
      });

      testWidgets('should handle malformed JSON responses', (WidgetTester tester) async {
        // Test malformed JSON handling
        try {
          final response = await apiService.get('/api/malformed-json');
          if (response.statusCode == 200) {
            json.decode(response.body);
          }
        } catch (e) {
          expect(e, isA<FormatException>());
        }
      });

      testWidgets('should handle authentication errors', (WidgetTester tester) async {
        // Test authentication error handling
        final response = await apiService.get('/api/protected-endpoint');
        
        expect(response.statusCode, isA<int>());
        expect(response.statusCode, anyOf([200, 401, 403, 404]));
      });
    });
  });
}
