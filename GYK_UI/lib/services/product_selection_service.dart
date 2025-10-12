import 'api_service.dart';
import '../core/config/api_config.dart';

class ProductSelectionService {
  static final ProductSelectionService _instance = ProductSelectionService._internal();
  factory ProductSelectionService() => _instance;
  ProductSelectionService._internal();

  final ApiService _apiService = ApiService();

  /// Send product selection to backend
  Future<Map<String, dynamic>> selectProduct({
    required String productName,
    String? productId,
    String? productCategory,
    String? productDescription,
  }) async {
    try {
      print('🌱 Selecting product: $productName');
      print('📦 Product Info - ID: $productId, Category: $productCategory');
      
      // Create body with only non-null values
      final Map<String, dynamic> body = {
        'product_name': productName,
      };
      
      // Add optional fields only if they are not null
      if (productId != null && productId.isNotEmpty) {
        body['product_id'] = productId;
      }
      if (productCategory != null && productCategory.isNotEmpty) {
        body['product_category'] = productCategory;
      }
      if (productDescription != null && productDescription.isNotEmpty) {
        body['product_description'] = productDescription;
      }
      
      final response = await _apiService.post(
        '${ApiConfig.baseUrl}/api/product-selection/select-product',
        body: body,
        requireAuth: true, // Auth required for authenticated users
      );

      print('✅ Product selected successfully');
      return response;
    } catch (e) {
      print('❌ Error selecting product: $e');
      throw Exception('Ürün seçilirken hata oluştu: $e');
    }
  }

  /// Send location selection to backend (GPS or Manual)
  Future<Map<String, dynamic>> selectLocation({
    required String locationType, // 'gps' or 'manual'
    required String city,
    required String region,
    String? district,
    double? latitude,
    double? longitude,
    String? climateZone,
  }) async {
    try {
      print('📍 Selecting location: $city, $region');
      print('🌍 Location Type: $locationType');
      if (latitude != null && longitude != null) {
        print('🗺️ Coordinates: $latitude, $longitude');
      }
      
      // Create body with required fields
      final Map<String, dynamic> body = {
        'location_type': locationType,
        'city': city,
        'region': region,
      };
      
      // Add optional fields only if they are not null and not empty
      if (district != null && district.isNotEmpty) {
        body['district'] = district;
      }
      
      if (latitude != null && longitude != null) {
        body['latitude'] = latitude;
        body['longitude'] = longitude;
      }
      
      if (climateZone != null && climateZone.isNotEmpty) {
        body['climate_zone'] = climateZone;
      }
      
      final response = await _apiService.post(
        '${ApiConfig.baseUrl}/api/product-selection/select-location',
        body: body,
        requireAuth: true, // Auth required for authenticated users
      );

      print('✅ Location selected successfully');
      return response;
    } catch (e) {
      print('❌ Error selecting location: $e');
      throw Exception('Konum seçilirken hata oluştu: $e');
    }
  }

  /// Get environment recommendations based on selected product and location
  Future<Map<String, dynamic>> getEnvironmentRecommendations({
    required String productName,
    required String city,
    required String region,
    String locationType = 'manual',
  }) async {
    try {
      print('🌍 Getting environment recommendations...');
      print('📊 Product: $productName, Location: $city, $region');
      
      // Create body with only non-null, non-empty values
      final Map<String, dynamic> body = {
        'product_name': productName,
        'city': city,
        'region': region,
        'location_type': locationType,
      };
      
      final response = await _apiService.post(
        '${ApiConfig.baseUrl}/api/product-selection/get-environment-recommendations',
        body: body,
        requireAuth: true, // Auth required for authenticated users
      );

      print('✅ Environment recommendations received');
      return response;
    } catch (e) {
      print('❌ Error getting environment recommendations: $e');
      throw Exception('Ortam koşulları önerisi alınırken hata oluştu: $e');
    }
  }
}
