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

  /// Get ML-based product recommendations from environment conditions
  Future<Map<String, dynamic>> getMLProductRecommendations({
    required String region,
    String? soilType,
    String? fertilizer,
    String? irrigation,
    String? sunlight,
    String? ph,
    String? nitrogen,
    String? phosphorus,
    String? potassium,
    String? humidity,
    String? temperature,
    String? rainfall,
    String? city,
  }) async {
    try {
      print('🤖 Getting ML-based product recommendations...');
      print('🌱 Environment data - Region: $region, Soil: $soilType');
      
      // Prepare ML request body with Turkish data (backend will translate)
      final Map<String, dynamic> mlRequestBody = {
        'region': region,
        'language': 'tr', // Turkish response
        'model_type': 'xgboost', // Use XGBoost model (working model)
      };
      
      // Add required parameters with defaults if not provided (keep Turkish)
      mlRequestBody['soil_type'] = soilType ?? 'Tınlı Toprak';
      mlRequestBody['fertilizer_type'] = fertilizer ?? 'Organik Gübre';
      mlRequestBody['irrigation_method'] = irrigation ?? 'Damla Sulama';
      mlRequestBody['weather_condition'] = sunlight ?? 'Güneşli';
      if (ph != null && ph.isNotEmpty) {
        mlRequestBody['soil_ph'] = double.tryParse(ph) ?? 6.5;
      }
      if (nitrogen != null && nitrogen.isNotEmpty) {
        mlRequestBody['nitrogen'] = double.tryParse(nitrogen) ?? 120.0;
      }
      if (phosphorus != null && phosphorus.isNotEmpty) {
        mlRequestBody['phosphorus'] = double.tryParse(phosphorus) ?? 60.0;
      }
      if (potassium != null && potassium.isNotEmpty) {
        mlRequestBody['potassium'] = double.tryParse(potassium) ?? 225.0;
      }
      if (humidity != null && humidity.isNotEmpty) {
        mlRequestBody['moisture'] = double.tryParse(humidity) ?? 26.0;
      }
      if (temperature != null && temperature.isNotEmpty) {
        mlRequestBody['temperature_celsius'] = double.tryParse(temperature) ?? 23.0;
      }
      if (rainfall != null && rainfall.isNotEmpty) {
        mlRequestBody['rainfall_mm'] = double.tryParse(rainfall) ?? 850.0;
      }
      
      print('📊 ML Request body: $mlRequestBody');
      
      // Call ML endpoint
      final response = await _apiService.post(
        'http://localhost:5000/api/ml/predict-crop',
        body: mlRequestBody,
        requireAuth: true, // ML endpoint doesn't require auth
      );

      print('✅ ML recommendations received successfully');
      print('🎯 ML Response: $response');
      
      return response;
    } catch (e) {
      print('❌ Error getting ML recommendations: $e');
      throw Exception('ML tabanlı ürün önerileri alınırken hata oluştu: $e');
    }
  }
}