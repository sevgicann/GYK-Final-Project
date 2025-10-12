import 'api_service.dart';
import '../core/config/api_config.dart';

class RecommendationService {
  static final RecommendationService _instance = RecommendationService._internal();
  factory RecommendationService() => _instance;
  RecommendationService._internal();

  final ApiService _apiService = ApiService();

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