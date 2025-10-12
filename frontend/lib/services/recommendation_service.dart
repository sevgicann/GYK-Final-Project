import 'api_service.dart';
import '../core/config/api_config.dart';

class RecommendationService {
  static final RecommendationService _instance = RecommendationService._internal();
  factory RecommendationService() => _instance;
  RecommendationService._internal();

  final ApiService _apiService = ApiService();

  /// Save location data to backend
  Future<Map<String, dynamic>> saveLocationData({
    required String locationType,
    required String city,
    required String region,
    String? district,
    double? latitude,
    double? longitude,
  }) async {
    try {
      print('📍 Saving location data...');
      print('🗺️ Location - Type: $locationType, City: $city, Region: $region');
      
      // Create body with only non-null values
      final Map<String, dynamic> body = {
        'location_type': locationType,
        'city': city,
        'region': region,
      };
      
      if (district != null && district.isNotEmpty) {
        body['district'] = district;
      }
      
      if (latitude != null && longitude != null) {
        body['latitude'] = latitude;
        body['longitude'] = longitude;
      }
      
      final response = await _apiService.post(
        '${ApiConfig.recommendationsEndpoint}/test-post',
        body: {
          'data_type': 'location',
          ...body,
        },
        requireAuth: true,
      );

      print('✅ Location data saved successfully');
      return response;
    } catch (e) {
      print('❌ Error saving location data: $e');
      throw Exception('Konum bilgileri kaydedilirken hata oluştu: $e');
    }
  }

  /// Save environment data to backend
  Future<Map<String, dynamic>> saveEnvironmentData({
    required String region,
    String? soilType,
    String? fertilizer,
    String? irrigation,
    String? sunlight,
  }) async {
    try {
      print('🌍 Saving environment data...');
      print('🌱 Environment - Region: $region');
      
      // Create body with only non-null values
      final Map<String, dynamic> body = {
        'region': region,
      };
      
      if (soilType != null && soilType.isNotEmpty) {
        body['soil_type'] = soilType;
      }
      if (fertilizer != null && fertilizer.isNotEmpty) {
        body['fertilizer'] = fertilizer;
      }
      if (irrigation != null && irrigation.isNotEmpty) {
        body['irrigation'] = irrigation;
      }
      if (sunlight != null && sunlight.isNotEmpty) {
        body['sunlight'] = sunlight;
      }
      
      final response = await _apiService.post(
        '${ApiConfig.recommendationsEndpoint}/test-post',
        body: {
          'data_type': 'environment',
          ...body,
        },
        requireAuth: true,
      );

      print('✅ Environment data saved successfully');
      return response;
    } catch (e) {
      print('❌ Error saving environment data: $e');
      throw Exception('Çevre bilgileri kaydedilirken hata oluştu: $e');
    }
  }

  /// Save soil data to backend
  Future<Map<String, dynamic>> saveSoilData({
    required bool isManualEntry,
    String? ph,
    String? nitrogen,
    String? phosphorus,
    String? potassium,
    String? humidity,
    String? temperature,
    String? rainfall,
  }) async {
    try {
      print('🌿 Saving soil data...');
      print('🔧 Soil - Method: ${isManualEntry ? 'Manuel' : 'Ortalama'}');
      
      // Create body with only non-null values
      final Map<String, dynamic> body = {
        'is_manual_entry': isManualEntry,
      };
      
      if (ph != null && ph.isNotEmpty) {
        body['ph'] = ph;
      }
      if (nitrogen != null && nitrogen.isNotEmpty) {
        body['nitrogen'] = nitrogen;
      }
      if (phosphorus != null && phosphorus.isNotEmpty) {
        body['phosphorus'] = phosphorus;
      }
      if (potassium != null && potassium.isNotEmpty) {
        body['potassium'] = potassium;
      }
      if (humidity != null && humidity.isNotEmpty) {
        body['humidity'] = humidity;
      }
      if (temperature != null && temperature.isNotEmpty) {
        body['temperature'] = temperature;
      }
      if (rainfall != null && rainfall.isNotEmpty) {
        body['rainfall'] = rainfall;
      }
      
      final response = await _apiService.post(
        '${ApiConfig.recommendationsEndpoint}/test-post',
        body: {
          'data_type': 'soil',
          ...body,
        },
        requireAuth: true,
      );

      print('✅ Soil data saved successfully');
      return response;
    } catch (e) {
      print('❌ Error saving soil data: $e');
      throw Exception('Toprak verileri kaydedilirken hata oluştu: $e');
    }
  }

  /// Generate recommendation based on user input
  Future<Map<String, dynamic>> generateRecommendation({
    required String soilType,
    required String climate,
    required String region,
    Map<String, dynamic>? preferences,
  }) async {
    try {
      print('🌱 Generating recommendation...');
      print('📊 Input - Soil: $soilType, Climate: $climate, Region: $region');
      
      final response = await _apiService.post(
        '${ApiConfig.recommendationsEndpoint}/test-post',
        body: {
          'soil_type': soilType,
          'climate': climate,
          'region': region,
          'preferences': preferences ?? {},
        },
        requireAuth: false, // No JWT token required for test endpoint
      );

      print('✅ Recommendation generated successfully');
      return response;
    } catch (e) {
      print('❌ Error generating recommendation: $e');
      throw Exception('Öneri oluşturulurken hata oluştu: $e');
    }
  }

  /// Get user's recommendation history
  Future<List<Map<String, dynamic>>> getUserRecommendations() async {
    try {
      print('📋 Getting user recommendations...');
      
      final response = await _apiService.get(
        ApiConfig.recommendationsEndpoint,
        requireAuth: true,
      );

      print('✅ User recommendations retrieved');
      return List<Map<String, dynamic>>.from(response['data']['recommendations']);
    } catch (e) {
      print('❌ Error getting user recommendations: $e');
      throw Exception('Öneri geçmişi alınırken hata oluştu: $e');
    }
  }

  /// Save recommendation to user's history
  Future<void> saveRecommendation(Map<String, dynamic> recommendation) async {
    try {
      print('💾 Saving recommendation...');
      
      await _apiService.post(
        ApiConfig.recommendationsEndpoint,
        body: recommendation,
        requireAuth: true,
      );

      print('✅ Recommendation saved successfully');
    } catch (e) {
      print('❌ Error saving recommendation: $e');
      throw Exception('Öneri kaydedilirken hata oluştu: $e');
    }
  }
}