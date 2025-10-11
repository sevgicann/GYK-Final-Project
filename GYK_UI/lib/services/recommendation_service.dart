import '../models/product.dart';
import '../models/region.dart';
import '../models/recommendation.dart';
import 'product_service.dart';
import 'region_service.dart';

class RecommendationService {
  static final RecommendationService _instance = RecommendationService._internal();
  factory RecommendationService() => _instance;
  RecommendationService._internal();

  final ProductService _productService = ProductService();
  final RegionService _regionService = RegionService();

  /// Ürün seçimine göre çevre koşulları önerisi
  Recommendation getProductRecommendation(String productName, String regionName) {
    final product = _productService.getProductByName(productName);
    final region = _regionService.getRegionByName(regionName);

    if (product == null) {
      throw ArgumentError('Ürün bulunamadı: $productName');
    }

    if (region == null) {
      throw ArgumentError('Bölge bulunamadı: $regionName');
    }

    // Bölgeye özel ek notlar
    final additionalNotes = _generateRegionSpecificNotes(product, region);

    return Recommendation(
      product: product,
      region: region,
      requirements: product.requirements,
      additionalNotes: additionalNotes,
      createdAt: DateTime.now(),
    );
  }

  /// Çevre koşullarına göre uygun ürünler önerisi
  List<Product> getProductRecommendationsForEnvironment({
    required double ph,
    required double nitrogen,
    required double phosphorus,
    required double potassium,
    required double humidity,
    required double temperature,
    required double rainfall,
    required String region,
  }) {
    return getEnvironmentRecommendation(
      ph: ph,
      temperature: temperature,
      humidity: humidity,
      rainfall: rainfall,
      regionName: region,
    );
  }

  /// Çevre koşullarına göre uygun ürünler önerisi
  List<Product> getEnvironmentRecommendation({
    required double ph,
    required double temperature,
    required double humidity,
    required double rainfall,
    String? regionName,
  }) {
    final allProducts = _productService.getAllProducts();
    final suitableProducts = <Product>[];

    for (final product in allProducts) {
      if (_isProductSuitableForEnvironment(
        product: product,
        ph: ph,
        temperature: temperature,
        humidity: humidity,
        rainfall: rainfall,
        regionName: regionName,
      )) {
        suitableProducts.add(product);
      }
    }

    // Uygunluk skoruna göre sırala
    suitableProducts.sort((a, b) {
      final scoreA = _calculateSuitabilityScore(a, ph, temperature, humidity, rainfall);
      final scoreB = _calculateSuitabilityScore(b, ph, temperature, humidity, rainfall);
      return scoreB.compareTo(scoreA);
    });

    return suitableProducts;
  }

  /// Ürünün çevre koşullarına uygunluğunu kontrol et
  bool _isProductSuitableForEnvironment({
    required Product product,
    required double ph,
    required double temperature,
    required double humidity,
    required double rainfall,
    String? regionName,
  }) {
    final requirements = product.requirements;

    // pH kontrolü
    if (!_isValueInRange(ph, requirements.ph)) return false;

    // Sıcaklık kontrolü
    if (!_isValueInRange(temperature, requirements.temperature)) return false;

    // Nem kontrolü
    if (!_isValueInRange(humidity, requirements.humidity)) return false;

    // Yağış kontrolü
    if (!_isValueInRange(rainfall, requirements.rainfall)) return false;

    return true;
  }

  /// Değerin belirtilen aralıkta olup olmadığını kontrol et
  bool _isValueInRange(double value, String range) {
    try {
      // String'den sayısal değerleri çıkar
      final cleanRange = range.replaceAll(RegExp(r'[^\d.–-]'), '');
      final parts = cleanRange.split(RegExp(r'[–-]'));
      if (parts.length != 2) return false;

      final min = double.parse(parts[0].trim());
      final max = double.parse(parts[1].trim());

      return value >= min && value <= max;
    } catch (e) {
      // Hata durumunda true döndür (daha esnek)
      return true;
    }
  }

  /// Uygunluk skorunu hesapla (0-100)
  double _calculateSuitabilityScore(
    Product product,
    double ph,
    double temperature,
    double humidity,
    double rainfall,
  ) {
    final requirements = product.requirements;
    double score = 0;

    // pH skoru (25 puan)
    if (_isValueInRange(ph, requirements.ph)) {
      score += 25;
    } else {
      score += _calculateProximityScore(ph, requirements.ph) * 25;
    }

    // Sıcaklık skoru (25 puan)
    if (_isValueInRange(temperature, requirements.temperature)) {
      score += 25;
    } else {
      score += _calculateProximityScore(temperature, requirements.temperature) * 25;
    }

    // Nem skoru (25 puan)
    if (_isValueInRange(humidity, requirements.humidity)) {
      score += 25;
    } else {
      score += _calculateProximityScore(humidity, requirements.humidity) * 25;
    }

    // Yağış skoru (25 puan)
    if (_isValueInRange(rainfall, requirements.rainfall)) {
      score += 25;
    } else {
      score += _calculateProximityScore(rainfall, requirements.rainfall) * 25;
    }

    return score;
  }

  /// Yakınlık skorunu hesapla (0-1)
  double _calculateProximityScore(double value, String range) {
    try {
      final parts = range.split('–');
      if (parts.length != 2) return 0;

      final min = double.parse(parts[0].trim());
      final max = double.parse(parts[1].trim());
      final center = (min + max) / 2;
      final rangeSize = max - min;

      final distance = (value - center).abs();
      final normalizedDistance = distance / rangeSize;

      return (1 - normalizedDistance).clamp(0.0, 1.0);
    } catch (e) {
      return 0;
    }
  }

  /// Bölgeye özel notlar oluştur
  String _generateRegionSpecificNotes(Product product, Region region) {
    final baseNotes = product.requirements.notes;
    final regionClimate = region.climateData;

    String additionalNotes = '';

    // Bölgeye özel öneriler
    if (regionClimate.seasonality == 'Karasal') {
      additionalNotes += 'Karasal iklim için ek sulama gerekebilir. ';
    } else if (regionClimate.seasonality == 'Akdeniz') {
      additionalNotes += 'Akdeniz iklimi için yaz aylarında dikkatli sulama yapın. ';
    } else if (regionClimate.seasonality == 'Okyanus') {
      additionalNotes += 'Nemli iklim için drenaj önemlidir. ';
    }

    // Toprak tipine göre öneriler
    if (regionClimate.soilType.contains('Kahverengi')) {
      additionalNotes += 'Kahverengi toprak için organik gübre kullanın. ';
    } else if (regionClimate.soilType.contains('Alüvyal')) {
      additionalNotes += 'Alüvyal toprak verimli, ek gübreye ihtiyaç az. ';
    }

    return baseNotes + (additionalNotes.isNotEmpty ? ' ' + additionalNotes : '');
  }

  /// Popüler ürünleri getir
  List<Product> getPopularProducts() {
    final allProducts = _productService.getAllProducts();
    // Basit bir popülerlik algoritması (gerçek uygulamada kullanıcı verilerine dayalı olmalı)
    return allProducts.take(5).toList();
  }

  /// Mevsimsel öneriler
  List<Product> getSeasonalRecommendations(String season) {
    final allProducts = _productService.getAllProducts();
    
    // Mevsimsel filtreleme (basit örnek)
    switch (season.toLowerCase()) {
      case 'spring':
        return allProducts.where((p) => 
          p.name == 'Havuç' || p.name == 'Marul' || p.name == 'Ispanak'
        ).toList();
      case 'summer':
        return allProducts.where((p) => 
          p.name == 'Domates' || p.name == 'Biber' || p.name == 'Salatalık'
        ).toList();
      case 'autumn':
        return allProducts.where((p) => 
          p.name == 'Patates' || p.name == 'Soğan' || p.name == 'Karnabahar'
        ).toList();
      case 'winter':
        return allProducts.where((p) => 
          p.name == 'Brokoli' || p.name == 'Ispanak' || p.name == 'Karnabahar'
        ).toList();
      default:
        return allProducts;
    }
  }
}
