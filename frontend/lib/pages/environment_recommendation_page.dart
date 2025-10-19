import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../core/theme/app_theme.dart';
import '../core/validation/validators.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_layout.dart';
import '../core/utils/responsive_utils.dart';
import '../core/widgets/responsive_widgets.dart';
import '../widgets/custom_text_field.dart';
import '../widgets/custom_button.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_dropdown.dart';
import '../widgets/custom_icon_button.dart';
import '../services/recommendation_service.dart';
import '../services/product_service.dart';
import '../services/region_service.dart';
import '../services/image_service.dart';
import '../services/location_service.dart';
import '../services/my_products_service.dart';
import '../services/my_environments_service.dart';
import '../services/pdf_service.dart';
import '../models/product.dart';
import '../data/turkish_cities.dart';

class EnvironmentRecommendationPage extends StatefulWidget {
  const EnvironmentRecommendationPage({super.key});

  @override
  State<EnvironmentRecommendationPage> createState() => _EnvironmentRecommendationPageState();
}

class _EnvironmentRecommendationPageState extends State<EnvironmentRecommendationPage> {
  final _formKey = GlobalKey<FormState>();
  final _phController = TextEditingController();
  final _nitrogenController = TextEditingController();
  final _phosphorusController = TextEditingController();
  final _potassiumController = TextEditingController();
  final _humidityController = TextEditingController();
  final _temperatureController = TextEditingController();
  final _rainfallController = TextEditingController();

  String? _selectedRegion;
  String? _selectedSoilType;
  String? _selectedFertilizer;
  String? _selectedIrrigation;
  String? _selectedSunlight;
  String? _selectedCity;
  List<Product> _recommendedProducts = [];
  List<double> _mlConfidenceScores = [];
  bool _isLoading = false;
  bool _isGpsSelected = false;
  bool _isManualSelected = false;
  bool _isManualEntry = false;
  bool _useAverageValues = false;

  // Form validation states
  Map<String, String?> _fieldErrors = {};
  bool _isFormValid = false;
  bool _hasAttemptedSubmit = false; // Butona tıklanıp tıklanmadığını takip et

  final RecommendationService _recommendationService = RecommendationService();
  final RegionService _regionService = RegionService();
  final ImageService _imageService = ImageService();
  final ProductService _productService = ProductService();
  final LocationService _locationService = LocationService();
  final MyProductsService _myProductsService = MyProductsService();
  final MyEnvironmentsService _myEnvironmentsService = MyEnvironmentsService();
  
  // ScaffoldMessenger referansını kaydet
  ScaffoldMessengerState? _scaffoldMessenger;

  @override
  void initState() {
    super.initState();
    _isManualSelected = true;
    _isManualEntry = true; // Manuel giriş varsayılan olarak aktif
    _useAverageValues = false; // Ortalama değerler inaktif
    
    // Ortalama değerleri doldur
    _fillAverageValues();
    
    // Form validasyonunu başlat
    _validateForm();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _scaffoldMessenger = ScaffoldMessenger.of(context);
  }

  void _fillAverageValues() {
    if (_useAverageValues) {
      // Backend'den dinamik ortalama değerleri çek
      _loadAverageSoilData();
    } else {
      // Manuel giriş için değerleri temizle ama placeholder'lar görünecek
      _phController.clear();
      _nitrogenController.clear();
      _phosphorusController.clear();
      _potassiumController.clear();
      _humidityController.clear();
      _temperatureController.clear();
      _rainfallController.clear();
    }
  }

  Future<void> _loadAverageSoilData() async {
    try {
      print('🌱 Loading average soil data...');
      
      // Şimdilik çevre koşullarına göre basit ortalama değerler kullan
      Map<String, double> averageValues = _getAverageValuesForConditions(
        soilType: _selectedSoilType,
        region: _selectedRegion,
        fertilizerType: _selectedFertilizer,
        irrigationMethod: _selectedIrrigation,
        weatherCondition: _selectedSunlight,
      );
      
      print('📊 Average soil data calculated:');
      print('  - pH: ${averageValues['ph']}');
      print('  - Nitrogen: ${averageValues['nitrogen']}');
      print('  - Phosphorus: ${averageValues['phosphorus']}');
      print('  - Potassium: ${averageValues['potassium']}');
      print('  - Moisture: ${averageValues['moisture']}');
      print('  - Temperature: ${averageValues['temperature']}');
      print('  - Rainfall: ${averageValues['rainfall']}');
      
      // Değerleri form alanlarına doldur
      if (mounted) {
        setState(() {
          _phController.text = averageValues['ph']?.toString() ?? '6.5';
          _nitrogenController.text = averageValues['nitrogen']?.toString() ?? '120';
          _phosphorusController.text = averageValues['phosphorus']?.toString() ?? '60';
          _potassiumController.text = averageValues['potassium']?.toString() ?? '225';
          _humidityController.text = averageValues['moisture']?.toString() ?? '26';
          _temperatureController.text = averageValues['temperature']?.toString() ?? '23';
          _rainfallController.text = averageValues['rainfall']?.toString() ?? '850';
        });
        
        // Başarı mesajı göster
        if (_scaffoldMessenger != null) {
          _scaffoldMessenger!.showSnackBar(
            SnackBar(
              content: Text(
                'Ortalama değerler yüklendi (${_selectedRegion ?? "Genel"} bölgesi)',
                style: const TextStyle(color: Colors.white),
              ),
              backgroundColor: Colors.green,
              duration: const Duration(seconds: 3),
            ),
          );
        }
      }
    } catch (e) {
      print('❌ Error loading average soil data: $e');
      
      // Hata durumunda varsayılan değerleri kullan
      if (mounted) {
        setState(() {
          _phController.text = '6.5';
          _nitrogenController.text = '120';
          _phosphorusController.text = '60';
          _potassiumController.text = '225';
          _humidityController.text = '26';
          _temperatureController.text = '23';
          _rainfallController.text = '850';
        });
        
        if (_scaffoldMessenger != null) {
          _scaffoldMessenger!.showSnackBar(
            SnackBar(
              content: Text(
                'Ortalama veriler yüklenemedi, varsayılan değerler kullanılıyor',
                style: const TextStyle(color: Colors.white),
              ),
              backgroundColor: AppTheme.errorColor,
              duration: const Duration(seconds: 4),
            ),
          );
        }
      }
    }
  }

  Map<String, double> _getAverageValuesForConditions({
    String? soilType,
    String? region,
    String? fertilizerType,
    String? irrigationMethod,
    String? weatherCondition,
  }) {
    // Bölgeye göre temel değerler
    Map<String, Map<String, double>> regionValues = {
      'İç Anadolu': {
        'ph': 7.2, 'nitrogen': 110, 'phosphorus': 55, 'potassium': 200,
        'moisture': 22, 'temperature': 25, 'rainfall': 400
      },
      'Marmara': {
        'ph': 6.8, 'nitrogen': 130, 'phosphorus': 65, 'potassium': 250,
        'moisture': 28, 'temperature': 22, 'rainfall': 700
      },
      'Ege': {
        'ph': 7.0, 'nitrogen': 125, 'phosphorus': 60, 'potassium': 230,
        'moisture': 25, 'temperature': 24, 'rainfall': 600
      },
      'Akdeniz': {
        'ph': 7.5, 'nitrogen': 140, 'phosphorus': 70, 'potassium': 280,
        'moisture': 30, 'temperature': 26, 'rainfall': 800
      },
      'Karadeniz': {
        'ph': 6.5, 'nitrogen': 150, 'phosphorus': 75, 'potassium': 300,
        'moisture': 35, 'temperature': 20, 'rainfall': 1200
      },
      'Doğu Anadolu': {
        'ph': 7.8, 'nitrogen': 100, 'phosphorus': 50, 'potassium': 180,
        'moisture': 20, 'temperature': 18, 'rainfall': 300
      },
      'Güneydoğu Anadolu': {
        'ph': 8.0, 'nitrogen': 90, 'phosphorus': 45, 'potassium': 160,
        'moisture': 18, 'temperature': 28, 'rainfall': 250
      },
    };
    
    // Varsayılan değerler
    Map<String, double> defaultValues = {
      'ph': 6.5, 'nitrogen': 120, 'phosphorus': 60, 'potassium': 225,
      'moisture': 26, 'temperature': 23, 'rainfall': 850
    };
    
    // Bölgeye göre değerleri al
    Map<String, double> baseValues = regionValues[region] ?? defaultValues;
    
    // Toprak tipine göre ayarlamalar
    if (soilType == 'Killi Toprak') {
      baseValues['ph'] = (baseValues['ph']! + 0.3).clamp(6.0, 8.5);
      baseValues['nitrogen'] = (baseValues['nitrogen']! * 1.1).roundToDouble();
    } else if (soilType == 'Kumlu Toprak') {
      baseValues['ph'] = (baseValues['ph']! - 0.2).clamp(6.0, 8.5);
      baseValues['nitrogen'] = (baseValues['nitrogen']! * 0.9).roundToDouble();
    } else if (soilType == 'Asitli Toprak') {
      baseValues['ph'] = (baseValues['ph']! - 0.5).clamp(5.0, 7.0);
    }
    
    // Gübre tipine göre ayarlamalar
    if (fertilizerType == 'Organik Gübre') {
      baseValues['nitrogen'] = (baseValues['nitrogen']! * 1.2).roundToDouble();
      baseValues['phosphorus'] = (baseValues['phosphorus']! * 1.1).roundToDouble();
    }
    
    // Sulama yöntemine göre ayarlamalar
    if (irrigationMethod == 'Damla Sulama') {
      baseValues['moisture'] = (baseValues['moisture']! * 1.1).clamp(15.0, 40.0);
    }
    
    return baseValues;
  }

  /// Form validasyonu yap
  void _validateForm() {
    Map<String, String?> errors = {};
    bool isValid = true;

    // Zorunlu çevre verilerini kontrol et
    if (_selectedRegion == null || _selectedRegion!.isEmpty) {
      errors['region'] = 'Bu alanı doldurunuz';
      isValid = false;
    }

    if (_selectedSoilType == null || _selectedSoilType!.isEmpty) {
      errors['soilType'] = 'Bu alanı doldurunuz';
      isValid = false;
    }

    if (_selectedFertilizer == null || _selectedFertilizer!.isEmpty) {
      errors['fertilizer'] = 'Bu alanı doldurunuz';
      isValid = false;
    }

    if (_selectedIrrigation == null || _selectedIrrigation!.isEmpty) {
      errors['irrigation'] = 'Bu alanı doldurunuz';
      isValid = false;
    }

    if (_selectedSunlight == null || _selectedSunlight!.isEmpty) {
      errors['sunlight'] = 'Bu alanı doldurunuz';
      isValid = false;
    }

    // Konum kontrolü
    if (!_isGpsSelected && !_isManualSelected) {
      errors['location'] = 'Bu alanı doldurunuz';
      isValid = false;
    }

    if (_isManualSelected && (_selectedCity == null || _selectedCity!.isEmpty)) {
      errors['city'] = 'Bu alanı doldurunuz';
      isValid = false;
    }

    // Toprak parametreleri kontrolü (sadece manuel giriş seçiliyse)
    if (_isManualEntry && !_useAverageValues) {
      if (_phController.text.isEmpty) {
        errors['ph'] = 'Bu alanı doldurunuz';
        isValid = false;
      }
      if (_nitrogenController.text.isEmpty) {
        errors['nitrogen'] = 'Bu alanı doldurunuz';
        isValid = false;
      }
      if (_phosphorusController.text.isEmpty) {
        errors['phosphorus'] = 'Bu alanı doldurunuz';
        isValid = false;
      }
      if (_potassiumController.text.isEmpty) {
        errors['potassium'] = 'Bu alanı doldurunuz';
        isValid = false;
      }
      if (_humidityController.text.isEmpty) {
        errors['humidity'] = 'Bu alanı doldurunuz';
        isValid = false;
      }
      if (_temperatureController.text.isEmpty) {
        errors['temperature'] = 'Bu alanı doldurunuz';
        isValid = false;
      }
      if (_rainfallController.text.isEmpty) {
        errors['rainfall'] = 'Bu alanı doldurunuz';
        isValid = false;
      }
    }

    setState(() {
      _fieldErrors = errors;
      _isFormValid = isValid;
    });
  }

  /// Belirli bir alanın hata mesajını al (sadece butona tıklandıktan sonra)
  String? _getFieldError(String fieldName) {
    return _hasAttemptedSubmit ? _fieldErrors[fieldName] : null;
  }

  /// Alan değişikliğinde validasyon yap
  void _onFieldChanged() {
    _validateForm();
  }

  @override
  void dispose() {
    _phController.dispose();
    _nitrogenController.dispose();
    _phosphorusController.dispose();
    _potassiumController.dispose();
    _humidityController.dispose();
    _temperatureController.dispose();
    _rainfallController.dispose();
    super.dispose();
  }

  Future<void> _handleGetProductRecommendation() async {
    // Butona tıklandığını işaretle
    setState(() {
      _hasAttemptedSubmit = true;
    });
    
    // Form validasyonunu kontrol et
    if (!_isFormValid) {
      if (_scaffoldMessenger != null) {
        _scaffoldMessenger!.showSnackBar(
          const SnackBar(
            content: Text('Lütfen tüm zorunlu alanları doldurun'),
            backgroundColor: AppTheme.errorColor,
          ),
        );
      }
      return;
    }

    // Eğer manuel giriş seçiliyse ve değerler boşsa, ortalama değerleri kullan
    if (_isManualEntry && _phController.text.isEmpty) {
      if (_scaffoldMessenger != null) {
        _scaffoldMessenger!.showSnackBar(
          const SnackBar(
            content: Text('Lütfen toprak parametrelerini girin veya ortalama değerleri kullanın'),
            backgroundColor: AppTheme.errorColor,
          ),
        );
      }
      return;
    }

    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
        _recommendedProducts = [];
      });

      try {
        // Kullanıcının girdiği tüm değerleri logla
        print('📊 Kullanıcı Girişleri:');
        print('  - Bölge: ${_selectedRegion ?? "Seçilmedi"}');
        print('  - Toprak Tipi: ${_selectedSoilType ?? "Seçilmedi"}');
        print('  - Gübre: ${_selectedFertilizer ?? "Seçilmedi"}');
        print('  - Sulama: ${_selectedIrrigation ?? "Seçilmedi"}');
        print('  - Güneş Işığı: ${_selectedSunlight ?? "Seçilmedi"}');
        print('  - Şehir: ${_selectedCity ?? "Seçilmedi"}');
        print('  - pH: ${_phController.text.isNotEmpty ? _phController.text : "Ortalama (6.5)"}');
        print('  - Azot: ${_nitrogenController.text.isNotEmpty ? _nitrogenController.text : "Ortalama (120)"}');
        print('  - Fosfor: ${_phosphorusController.text.isNotEmpty ? _phosphorusController.text : "Ortalama (60)"}');
        print('  - Potasyum: ${_potassiumController.text.isNotEmpty ? _potassiumController.text : "Ortalama (225)"}');
        print('  - Nem: ${_humidityController.text.isNotEmpty ? _humidityController.text : "Ortalama (26)"}');
        print('  - Sıcaklık: ${_temperatureController.text.isNotEmpty ? _temperatureController.text : "Ortalama (23)"}');
        print('  - Yağış: ${_rainfallController.text.isNotEmpty ? _rainfallController.text : "Ortalama (850)"}');
        
        // ML modelinden ürün önerileri al
        final mlResponse = await _recommendationService.getMLProductRecommendations(
          region: _selectedRegion ?? 'İç Anadolu',
          soilType: _selectedSoilType,
          fertilizer: _selectedFertilizer,
          irrigation: _selectedIrrigation,
          sunlight: _selectedSunlight,
          ph: _phController.text.isNotEmpty ? _phController.text : '6.5',
          nitrogen: _nitrogenController.text.isNotEmpty ? _nitrogenController.text : '120',
          phosphorus: _phosphorusController.text.isNotEmpty ? _phosphorusController.text : '60',
          potassium: _potassiumController.text.isNotEmpty ? _potassiumController.text : '225',
          humidity: _humidityController.text.isNotEmpty ? _humidityController.text : '26',
          temperature: _temperatureController.text.isNotEmpty ? _temperatureController.text : '23',
          rainfall: _rainfallController.text.isNotEmpty ? _rainfallController.text : '850',
          city: _selectedCity,
        );

        print('🤖 ML Response received: $mlResponse');

        // ML'den gelen önerileri işle
        if (mlResponse['success'] == true && mlResponse['data'] != null) {
          final mlData = mlResponse['data'];
          final top3Predictions = mlData['top_3_predictions'] as List<dynamic>?;
          final predictedCrop = mlData['predicted_crop'] as String?;
          final confidence = mlData['confidence'] as double?;
          final modelUsed = mlData['model_used'] as String?;
          
          print('🎯 ML Tahmin Sonuçları:');
          print('  - Ana Tahmin: ${predictedCrop ?? "Bilinmiyor"}');
          print('  - Güven Skoru: ${confidence != null ? (confidence * 100).toStringAsFixed(1) + "%" : "Bilinmiyor"}');
          print('  - Kullanılan Model: ${modelUsed ?? "Bilinmiyor"}');
          print('  - Top 3 Öneri:');
          
          if (top3Predictions != null && top3Predictions.isNotEmpty) {
            // ML'den gelen ürün isimlerini Product objelerine çevir
            final mlRecommendedProducts = <Product>[];
            final mlConfidenceScores = <double>[];
            
            for (int i = 0; i < top3Predictions.length; i++) {
              var prediction = top3Predictions[i];
              if (prediction is List && prediction.length >= 2) {
                final cropName = prediction[0] as String;
                final confidence = prediction[1] as double;
                
                print('    ${i + 1}. ${cropName}: ${(confidence * 100).toStringAsFixed(1)}%');
                
                // Türkçe ürün isimlerini İngilizce'ye çevir
                String turkishCropName = _translateCropNameToTurkish(cropName);
                
                // Ürün listesinde bu isimle eşleşen ürünü bul
                final matchingProducts = _productService.getAllProducts()
                    .where((product) => product.name.toLowerCase().contains(turkishCropName.toLowerCase()) ||
                                       turkishCropName.toLowerCase().contains(product.name.toLowerCase()))
              .toList();
                
                if (matchingProducts.isNotEmpty) {
                  mlRecommendedProducts.add(matchingProducts.first);
                  mlConfidenceScores.add(confidence);
                } else {
                  // Eğer tam eşleşme yoksa, genel bir ürün oluştur
                  mlRecommendedProducts.add(Product(
                    id: cropName,
                    name: turkishCropName,
                    category: 'ML Önerisi',
                    description: 'ML modeli tarafından önerilen ürün (${(confidence * 100).toStringAsFixed(1)}% güven)',
                    requirements: ProductRequirements(
                      ph: '6.0-7.0',
                      nitrogen: '100-150',
                      phosphorus: '50-80',
                      potassium: '200-300',
                      humidity: '60-80',
                      temperature: '20-30',
                      rainfall: '500-1000',
                      notes: 'ML modeli tarafından önerilen genel koşullar',
                    ),
                  ));
                  mlConfidenceScores.add(confidence);
                }
              }
            }

          if (mounted) {
            setState(() {
                _recommendedProducts = mlRecommendedProducts;
                _mlConfidenceScores = mlConfidenceScores;
            });
            _showProductRecommendationsBottomSheet();
            
            // Ortam verilerini kaydet
            await _saveEnvironmentDataToMyEnvironments();
            
            // History'ye ortam→ürün önerisini kaydet
            await _saveEnvironmentProductRecommendation(mlRecommendedProducts, mlConfidenceScores);
            
              // Başarı mesaj sonuçları göster
              if (_scaffoldMessenger != null) {
                _scaffoldMessenger!.showSnackBar(
                  const SnackBar(
                    content: Text(
                      '✅ Öneriler hesaplandı! En uygun ürünler belirlendi.'
                    ),
                    backgroundColor: Colors.green,
                    duration: Duration(seconds: 3),
                  ),
                );
              }
          }
        } else {
            throw Exception('ML modelinden geçerli öneri alınamadı');
          }
        } else {
          throw Exception(mlResponse['message'] ?? 'ML önerisi alınamadı');
        }
      } catch (e) {
        print('❌ ML recommendation error: $e');
        
        if (mounted && _scaffoldMessenger != null) {
          _scaffoldMessenger!.showSnackBar(
            SnackBar(
              content: Text('ML modeli bağlantısında hata oluştu: $e'),
              backgroundColor: AppTheme.errorColor,
              duration: const Duration(seconds: 5),
            ),
          );
        }
      } finally {
        if (mounted) {
          setState(() {
            _isLoading = false;
          });
        }
      }
    }
  }

  // Ortam koşullarından ürün önerisini SharedPreferences'a kaydet
  Future<void> _saveEnvironmentProductRecommendation(List<Product> products, List<double> confidenceScores) async {
    if (products.isEmpty) return;
    
    try {
      final prefs = await SharedPreferences.getInstance();
      
      // En yüksek güven skorlu ürünü bul
      final bestProductIndex = confidenceScores.indexOf(confidenceScores.reduce((a, b) => a > b ? a : b));
      final bestProduct = products[bestProductIndex];
      final bestConfidence = confidenceScores[bestProductIndex];
      
      // Ortam→ürün önerisi verilerini hazırla
      final environmentProductData = {
        'timestamp': DateTime.now().toIso8601String(),
        'type': 'environment_to_product',
        'environment': {
          'region': _selectedRegion ?? 'Bilinmeyen',
          'soilType': _selectedSoilType ?? 'Bilinmeyen',
          'fertilizer': _selectedFertilizer ?? 'Bilinmeyen',
          'irrigation': _selectedIrrigation ?? 'Bilinmeyen',
          'sunlight': _selectedSunlight ?? 'Bilinmeyen',
          'city': _selectedCity ?? 'Bilinmeyen',
          'ph': _phController.text.isNotEmpty ? _phController.text : '6.5',
          'nitrogen': _nitrogenController.text.isNotEmpty ? _nitrogenController.text : '120',
          'phosphorus': _phosphorusController.text.isNotEmpty ? _phosphorusController.text : '60',
          'potassium': _potassiumController.text.isNotEmpty ? _potassiumController.text : '225',
          'humidity': _humidityController.text.isNotEmpty ? _humidityController.text : '26',
          'temperature': _temperatureController.text.isNotEmpty ? _temperatureController.text : '23',
          'rainfall': _rainfallController.text.isNotEmpty ? _rainfallController.text : '850',
        },
        'product': {
          'name': bestProduct.name,
          'category': bestProduct.category,
          'confidence': bestConfidence,
        },
      };
      
      // Mevcut geçmişi al
      final existingHistory = prefs.getStringList('environment_product_history') ?? [];
      
      // Yeni veriyi ekle
      existingHistory.insert(0, json.encode(environmentProductData));
      
      // Son 10 kaydı tut
      if (existingHistory.length > 10) {
        existingHistory.removeRange(10, existingHistory.length);
      }
      
      // Kaydet
      await prefs.setStringList('environment_product_history', existingHistory);
      
      print('✅ Environment product recommendation saved to history');
    } catch (e) {
      print('❌ Error saving environment product recommendation: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return AppLayout(
      currentPageIndex: 1, // Product Recommendation index
      pageTitle: 'Ortam Koşullarından Ürün Tahmini',
      actions: [
        // Reverse Butonu
        IconButton(
          icon: const Icon(Icons.swap_horiz, color: AppTheme.textPrimaryColor),
          onPressed: () {
            AppRouter.navigateTo(context, AppRouter.productSelection);
          },
          tooltip: 'Ürün Seçiminden Ortam Koşulları Önerisi',
        ),
      ],
      child: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppTheme.paddingLarge),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Konum ve İklim Bilgileri
                _buildLocationAndClimateSection(),

                const SizedBox(height: AppTheme.paddingXLarge),

                // Seçilen Konum Gösterimi
                if (_selectedCity != null) _buildSelectedLocationCard(),

                const SizedBox(height: AppTheme.paddingXLarge),

                // Çevre Verileri
                _buildEnvironmentDataSection(),

                const SizedBox(height: AppTheme.paddingXLarge),

                // Toprak Verisi Toplama
                _buildSoilDataCollectionSection(),

                const SizedBox(height: AppTheme.paddingXLarge),

                // Toprak Parametreleri (isteğe bağlı)
                _buildSoilParametersSection(),

                const SizedBox(height: AppTheme.paddingXLarge),

                // Ürün Önerilerini Al Butonu
                _buildGetRecommendationsButton(),

                const SizedBox(height: AppTheme.paddingXLarge),

              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildLocationAndClimateSection() {
    return CustomCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 24,
                height: 24,
                decoration: const BoxDecoration(
                  color: AppTheme.primaryLightColor,
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.check,
                  color: AppTheme.surfaceColor,
                  size: AppTheme.iconSizeSmall,
                ),
              ),
              const SizedBox(width: AppTheme.paddingMedium),
              const Text(
                'Konum ve İklim Bilgileri',
                style: TextStyle(
                  fontSize: AppTheme.fontSizeXLarge,
                  fontWeight: AppTheme.fontWeightBold,
                  color: AppTheme.textPrimaryColor,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppTheme.paddingMedium),
          const Text(
            'Önerileri iyileştirmek için konumunuzu ve çevre koşullarınızı belirleyin.',
            style: AppTheme.bodyStyle,
          ),
          const SizedBox(height: AppTheme.paddingLarge),
          Row(
            children: [
              _buildLocationOption(
                icon: Icons.gps_fixed,
                title: 'GPS Konumunu Kullan',
                isSelected: _isGpsSelected,
                onTap: () {
                  setState(() {
                    _isGpsSelected = true;
                    _isManualSelected = false;
                  });
                  _onFieldChanged(); // Form validasyonunu güncelle
                  _handleGpsLocation();
                },
              ),
              const SizedBox(width: AppTheme.paddingMedium),
              _buildLocationOption(
                icon: Icons.location_city,
                title: 'Şehri Manuel Seç',
                isSelected: _isManualSelected,
                onTap: () {
                  setState(() {
                    _isGpsSelected = false;
                    _isManualSelected = true;
                  });
                  _onFieldChanged(); // Form validasyonunu güncelle
                  _showCitySelectionDialog();
                },
              ),
            ],
          ),
          
          // Konum hata mesajı
          Padding(
            padding: const EdgeInsets.only(top: 8),
            child: _buildFieldError('location'),
          ),
        ],
      ),
    );
  }

  Widget _buildEnvironmentDataSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Çevre Verileri',
          style: TextStyle(
            fontSize: AppTheme.fontSizeXLarge,
            fontWeight: AppTheme.fontWeightBold,
            color: AppTheme.textPrimaryColor,
          ),
        ),
        const SizedBox(height: AppTheme.paddingMedium),
        
        // İlk satır - 3 dropdown
        Row(
          children: [
            Expanded(
              child: CustomDropdown<String>(
                label: 'Bölge',
                value: _selectedRegion,
                items: const ['İç Anadolu', 'Marmara', 'Ege', 'Akdeniz', 'Karadeniz', 'Doğu Anadolu', 'Güneydoğu Anadolu'],
                hint: 'Bölge seçiniz',
                onChanged: (value) {
                  setState(() {
                    _selectedRegion = value;
                  });
                  
                  // Form validasyonunu güncelle
                  _onFieldChanged();
                  
                  // Backend'e çevre verilerini gönder (sadece bölge değiştiğinde)
                  if (value != null) {
                    _saveEnvironmentData();
                    
                    // Ortalama değerler kullanılıyorsa, yeni bölge için ortalama değerleri yükle
                    if (_useAverageValues) {
                      _loadAverageSoilData();
                    }
                  }
                },
              ),
            ),
            // Bölge hata mesajı
            _buildFieldError('region'),
            const SizedBox(width: AppTheme.paddingMedium),
            Expanded(
              child: CustomDropdown<String>(
                label: 'Toprak Tipi',
                value: _selectedSoilType,
                items: const ['Killi Toprak', 'Kumlu Toprak', 'Tınlı Toprak', 'Kireçli Toprak', 'Asitli Toprak'],
                hint: 'Toprak tipi seçiniz',
                onChanged: (value) {
                  setState(() {
                    _selectedSoilType = value;
                  });
                  
                  // Form validasyonunu güncelle
                  _onFieldChanged();
                  
                  // Backend'e çevre verilerini gönder (sadece region varsa)
                  if (_selectedRegion != null) {
                    _saveEnvironmentData();
                    
                    // Ortalama değerler kullanılıyorsa, yeni toprak tipi için ortalama değerleri yükle
                    if (_useAverageValues) {
                      _loadAverageSoilData();
                    }
                  }
                },
              ),
            ),
            // Toprak tipi hata mesajı
            _buildFieldError('soilType'),
            const SizedBox(width: AppTheme.paddingMedium),
            Expanded(
              child: CustomDropdown<String>(
                label: 'Gübre',
                value: _selectedFertilizer,
                items: const ['Potasyum Nitrat', 'Amonyum Sülfat', 'Üre', 'Kompost', 'Organik Gübre'],
                hint: 'Gübre seçiniz',
                onChanged: (value) {
                  setState(() {
                    _selectedFertilizer = value;
                  });
                  
                  // Form validasyonunu güncelle
                  _onFieldChanged();
                  
                  // Backend'e çevre verilerini gönder (sadece region varsa)
                  if (_selectedRegion != null) {
                    _saveEnvironmentData();
                    
                    // Ortalama değerler kullanılıyorsa, yeni gübre tipi için ortalama değerleri yükle
                    if (_useAverageValues) {
                      _loadAverageSoilData();
                    }
                  }
                },
              ),
            ),
            // Gübre hata mesajı
            _buildFieldError('fertilizer'),
          ],
        ),
        
        const SizedBox(height: AppTheme.paddingMedium),
        
        // İkinci satır - 2 dropdown
        Row(
          children: [
            Expanded(
              child: CustomDropdown<String>(
                label: 'Sulama Yöntemi',
                value: _selectedIrrigation,
                items: const ['Salma Sulama', 'Damla Sulama', 'Yağmurlama', 'Sprinkler', 'Mikro Sulama'],
                hint: 'Sulama yöntemi seçiniz',
                onChanged: (value) {
                  setState(() {
                    _selectedIrrigation = value;
                  });
                  
                  // Form validasyonunu güncelle
                  _onFieldChanged();
                  
                  // Backend'e çevre verilerini gönder (sadece region varsa)
                  if (_selectedRegion != null) {
                    _saveEnvironmentData();
                    
                    // Ortalama değerler kullanılıyorsa, yeni sulama yöntemi için ortalama değerleri yükle
                    if (_useAverageValues) {
                      _loadAverageSoilData();
                    }
                  }
                },
              ),
            ),
            const SizedBox(width: AppTheme.paddingMedium),
            Expanded(
              child: CustomDropdown<String>(
                label: 'Güneş Işığı',
                value: _selectedSunlight,
                items: const ['Güneşli', 'Kısmi Gölge', 'Gölgeli', 'Tam Gölge'],
                hint: 'Güneş ışığı seçiniz',
                onChanged: (value) {
                  setState(() {
                    _selectedSunlight = value;
                  });
                  
                  // Form validasyonunu güncelle
                  _onFieldChanged();
                  
                  // Backend'e çevre verilerini gönder (sadece region varsa)
                  if (_selectedRegion != null) {
                    _saveEnvironmentData();
                    
                    // Ortalama değerler kullanılıyorsa, yeni güneş ışığı durumu için ortalama değerleri yükle
                    if (_useAverageValues) {
                      _loadAverageSoilData();
                    }
                  }
                },
              ),
            ),
            const SizedBox(width: AppTheme.paddingMedium),
            const Expanded(child: SizedBox()), // Boş alan
          ],
        ),
        
        // İkinci satır hata mesajları
        Row(
          children: [
            Expanded(child: _buildFieldError('irrigation')),
            const SizedBox(width: AppTheme.paddingMedium),
            Expanded(child: _buildFieldError('sunlight')),
            const SizedBox(width: AppTheme.paddingMedium),
            const Expanded(child: SizedBox()), // Boş alan
          ],
        ),
      ],
    );
  }

  Widget _buildSoilDataCollectionSection() {
    return CustomCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 24,
                height: 24,
                decoration: const BoxDecoration(
                  color: AppTheme.primaryLightColor,
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.check,
                  color: AppTheme.surfaceColor,
                  size: AppTheme.iconSizeSmall,
                ),
              ),
              const SizedBox(width: AppTheme.paddingMedium),
              const Text(
                'Toprak Verisi Toplama',
                style: TextStyle(
                  fontSize: AppTheme.fontSizeXLarge,
                  fontWeight: AppTheme.fontWeightBold,
                  color: AppTheme.textPrimaryColor,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppTheme.paddingMedium),
          const Text(
            'Toprak verilerini manuel olarak girin veya ortalama tahminleri kullanın.',
            style: AppTheme.bodyStyle,
          ),
          const SizedBox(height: AppTheme.paddingLarge),
          Row(
            children: [
              Expanded(
                child: CustomButton(
                  text: 'Manuel Giriş',
                  icon: Icons.edit,
                  onPressed: () async {
                    setState(() {
                      _isManualEntry = true;
                      _useAverageValues = false;
                    });
                    _onFieldChanged(); // Form validasyonunu güncelle
                    _fillAverageValues();
                    
                    // Backend'e toprak verilerini gönder
                    await _saveSoilData();
                  },
                  type: _isManualEntry ? ButtonType.primary : ButtonType.outline,
                  isFullWidth: true,
                ),
              ),
              const SizedBox(width: AppTheme.paddingMedium),
              Expanded(
                child: CustomButton(
                  text: 'Ortalama Değerleri Kullan',
                  icon: Icons.trending_up,
                  onPressed: () async {
                    // Çevre koşulları kontrolü
                    if (_selectedRegion == null || _selectedRegion!.isEmpty ||
                        _selectedSoilType == null || _selectedSoilType!.isEmpty ||
                        _selectedFertilizer == null || _selectedFertilizer!.isEmpty ||
                        _selectedIrrigation == null || _selectedIrrigation!.isEmpty ||
                        _selectedSunlight == null || _selectedSunlight!.isEmpty) {
                      
                      if (_scaffoldMessenger != null) {
                        _scaffoldMessenger!.showSnackBar(
                          const SnackBar(
                            content: Text('Ortalama değerleri kullanmak için önce çevre koşullarını doldurunuz'),
                            backgroundColor: AppTheme.errorColor,
                          ),
                        );
                      }
                      return;
                    }
                    
                    setState(() {
                      _isManualEntry = false; // Manuel giriş inaktif olsun
                      _useAverageValues = true;
                    });
                    _onFieldChanged(); // Form validasyonunu güncelle
                    
                    // Backend'den dinamik ortalama değerleri yükle
                    await _loadAverageSoilData();
                    
                    // Backend'e toprak verilerini gönder
                    await _saveSoilData();
                  },
                  type: _useAverageValues ? ButtonType.primary : ButtonType.outline,
                  isFullWidth: true,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSoilParametersSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        ResponsiveText(
          'Toprak Parametreleri (isteğe bağlı):',
          style: TextStyle(
            fontSize: ResponsiveUtils.getResponsiveFontSize(
              context,
              mobile: 18,
              tablet: 20,
              desktop: 24,
            ),
            fontWeight: AppTheme.fontWeightBold,
            color: AppTheme.textPrimaryColor,
          ),
        ),
        SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
          context,
          mobile: 12,
          tablet: 16,
          desktop: 20,
        )),
        
        // Responsive Grid for soil parameters
        ResponsiveGrid(
          spacing: ResponsiveUtils.getResponsiveSpacing(
            context,
            mobile: 8,
            tablet: 12,
            desktop: 16,
          ),
          runSpacing: ResponsiveUtils.getResponsiveSpacing(
            context,
            mobile: 8,
            tablet: 12,
            desktop: 16,
          ),
          children: [
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                CustomTextField(
                  controller: _phController,
                  label: 'pH',
                  hint: 'pH',
                  keyboardType: TextInputType.number,
                  validator: (value) => Validators.range(value, 4.0, 9.0, 'pH'),
                  onChanged: (value) {
                    _onFieldChanged(); // Form validasyonunu güncelle
                    if (value.isNotEmpty) {
                      _saveSoilData();
                    }
                  },
                ),
                _buildFieldError('ph'),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                CustomTextField(
                  controller: _nitrogenController,
                  label: 'Azot (ppm)',
                  hint: 'Azot (ppm)',
                  keyboardType: TextInputType.number,
                  validator: (value) => Validators.range(value, 0.0, 300.0, 'Azot'),
                  onChanged: (value) {
                    _onFieldChanged(); // Form validasyonunu güncelle
                    if (value.isNotEmpty) {
                      _saveSoilData();
                    }
                  },
                ),
                _buildFieldError('nitrogen'),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                CustomTextField(
                  controller: _phosphorusController,
                  label: 'Fosfor (ppm)',
                  hint: 'Fosfor (ppm)',
                  keyboardType: TextInputType.number,
                  validator: (value) => Validators.range(value, 0.0, 150.0, 'Fosfor'),
                  onChanged: (value) {
                    _onFieldChanged(); // Form validasyonunu güncelle
                    if (value.isNotEmpty) {
                      _saveSoilData();
                    }
                  },
                ),
                _buildFieldError('phosphorus'),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                CustomTextField(
                  controller: _potassiumController,
                  label: 'Potasyum (ppm)',
                  hint: 'Potasyum (ppm)',
                  keyboardType: TextInputType.number,
                  validator: (value) => Validators.range(value, 0.0, 400.0, 'Potasyum'),
                  onChanged: (value) {
                    _onFieldChanged(); // Form validasyonunu güncelle
                    if (value.isNotEmpty) {
                      _saveSoilData();
                    }
                  },
                ),
                _buildFieldError('potassium'),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                CustomTextField(
                  controller: _humidityController,
                  label: 'Nem %',
                  hint: 'Nem %',
                  keyboardType: TextInputType.number,
                  validator: (value) => Validators.range(value, 0.0, 100.0, 'Nem'),
                  onChanged: (value) {
                    _onFieldChanged(); // Form validasyonunu güncelle
                    if (value.isNotEmpty) {
                      _saveSoilData();
                    }
                  },
                ),
                _buildFieldError('humidity'),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                CustomTextField(
                  controller: _temperatureController,
                  label: 'Sıcaklık °C',
                  hint: 'Sıcaklık °C',
                  keyboardType: TextInputType.number,
                  validator: (value) => Validators.range(value, -10.0, 45.0, 'Sıcaklık'),
                  onChanged: (value) {
                    _onFieldChanged(); // Form validasyonunu güncelle
                    if (value.isNotEmpty) {
                      _saveSoilData();
                    }
                  },
                ),
                _buildFieldError('temperature'),
              ],
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                CustomTextField(
                  controller: _rainfallController,
                  label: 'Yağış mm',
                  hint: 'Yağış mm',
                  keyboardType: TextInputType.number,
                  validator: (value) => Validators.range(value, 0.0, 2000.0, 'Yağış'),
                  onChanged: (value) {
                    _onFieldChanged(); // Form validasyonunu güncelle
                    if (value.isNotEmpty) {
                      _saveSoilData();
                    }
                  },
                ),
                _buildFieldError('rainfall'),
              ],
            ),
          ],
        ),
        
      ],
    );
  }

  /// Hata mesajı chip'i oluştur
  Widget _buildErrorChip(String message) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: AppTheme.errorColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppTheme.errorColor.withOpacity(0.3)),
      ),
      child: Text(
        message,
        style: const TextStyle(
          color: AppTheme.errorColor,
          fontSize: AppTheme.fontSizeSmall,
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }

  /// Standart hata mesajı widget'ı oluştur
  Widget _buildFieldError(String fieldName) {
    return _getFieldError(fieldName) != null
        ? Padding(
            padding: const EdgeInsets.only(top: 4),
            child: Text(
              'Bu alanı doldurunuz',
              style: const TextStyle(
                color: AppTheme.errorColor,
                fontSize: AppTheme.fontSizeSmall,
              ),
            ),
          )
        : const SizedBox.shrink();
  }

  Widget _buildGetRecommendationsButton() {
    return CustomButton(
      text: 'Öneri Al',
      icon: Icons.lightbulb_outline,
      onPressed: _handleGetProductRecommendation,
      isLoading: _isLoading,
      isFullWidth: true,
      height: 60,
      type: ButtonType.primary,
    );
  }


  Widget _buildSelectedLocationCard() {
    if (_selectedCity == null) return const SizedBox.shrink();

    return CustomCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                width: 24,
                height: 24,
                decoration: const BoxDecoration(
                  color: AppTheme.primaryLightColor,
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.location_on,
                  color: AppTheme.surfaceColor,
                  size: AppTheme.iconSizeSmall,
                ),
              ),
              const SizedBox(width: AppTheme.paddingMedium),
              const Text(
                'Seçilen Konum',
                style: TextStyle(
                  fontSize: AppTheme.fontSizeXLarge,
                  fontWeight: AppTheme.fontWeightBold,
                  color: AppTheme.textPrimaryColor,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppTheme.paddingMedium),
          Row(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(AppTheme.borderRadius),
                child: Image.asset(
                  _imageService.getCityImage(_selectedCity!),
                  width: 80,
                  height: 80,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) => Container(
                    width: 80,
                    height: 80,
                    color: AppTheme.primaryLightColor.withOpacity(0.2),
                    child: const Icon(Icons.location_city, color: AppTheme.textSecondaryColor),
                  ),
                ),
              ),
              const SizedBox(width: AppTheme.paddingLarge),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _selectedCity!,
                      style: const TextStyle(
                        fontSize: AppTheme.fontSizeXLarge,
                        fontWeight: AppTheme.fontWeightBold,
                        color: AppTheme.textPrimaryColor,
                      ),
                    ),
                    const SizedBox(height: AppTheme.paddingSmall),
                    Text(
                      'Bölge: $_selectedRegion',
                      style: AppTheme.bodyStyle.copyWith(color: AppTheme.textSecondaryColor),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildLocationOption({
    required IconData icon,
    required String title,
    required bool isSelected,
    required VoidCallback onTap,
  }) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppTheme.borderRadiusLarge),
        splashFactory: NoSplash.splashFactory,
        child: Container(
          padding: EdgeInsets.all(ResponsiveUtils.getResponsiveSpacing(
            context,
            mobile: 12,
            tablet: 16,
            desktop: 20,
          )),
          decoration: BoxDecoration(
            color: isSelected ? AppTheme.primaryColor : AppTheme.surfaceColor,
            border: Border.all(
              color: isSelected ? AppTheme.primaryColor : AppTheme.primaryLightColor,
              width: 2,
            ),
            borderRadius: BorderRadius.circular(AppTheme.borderRadiusLarge),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                color: isSelected ? AppTheme.surfaceColor : AppTheme.primaryLightColor,
                size: ResponsiveUtils.getResponsiveIconSize(context) * 1.2,
              ),
              SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
                context,
                mobile: 8,
                tablet: 12,
                desktop: 16,
              )),
              ResponsiveText(
                title,
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: isSelected ? AppTheme.surfaceColor : AppTheme.primaryLightColor,
                  fontSize: ResponsiveUtils.getResponsiveFontSize(
                    context,
                    mobile: 12,
                    tablet: 14,
                    desktop: 16,
                  ),
                  fontWeight: AppTheme.fontWeightMedium,
                ),
              ),
          ],
        ),
      ),
    ),
    );
  }

  void _handleGpsLocation() async {
    // Show loading message
    if (_scaffoldMessenger != null) {
      _scaffoldMessenger!.showSnackBar(
        const SnackBar(
          content: Text('📍 GPS konumunuz alınıyor...'),
          backgroundColor: AppTheme.primaryColor,
        ),
      );
    }
    
    try {
      // Get real GPS location using geolocator
      final locationData = await _locationService.getCurrentLocation();
      
      if (mounted) {
        if (locationData['success'] == true) {
          // GPS location successfully obtained
          setState(() {
            _selectedCity = locationData['city'];
            _selectedRegion = locationData['region'];
            _isGpsSelected = true;
            _isManualSelected = false;
          });
          _onFieldChanged(); // Update form validation
          
          // Send location data to backend
          try {
            await _recommendationService.saveLocationData(
              locationType: 'gps',
              city: _selectedCity!,
              region: _selectedRegion!,
              latitude: locationData['latitude'],
              longitude: locationData['longitude'],
            );
            
            if (mounted && _scaffoldMessenger != null) {
              _scaffoldMessenger!.showSnackBar(
                SnackBar(
                  content: Text(
                    '✅ GPS konumu alındı: $_selectedCity ($_selectedRegion)',
                    style: const TextStyle(color: Colors.white),
                  ),
                  backgroundColor: AppTheme.primaryColor,
                  duration: const Duration(seconds: 3),
                ),
              );
            }
          } catch (e) {
            print('❌ Error saving GPS location: $e');
            if (mounted && _scaffoldMessenger != null) {
              _scaffoldMessenger!.showSnackBar(
                SnackBar(
                  content: Text('⚠️ GPS konumu alındı ancak kaydedilemedi: $e'),
                  backgroundColor: AppTheme.errorColor,
                ),
              );
            }
          }
        } else {
          // GPS failed - show error with manual option
          if (mounted && _scaffoldMessenger != null) {
            _scaffoldMessenger!.showSnackBar(
              SnackBar(
                content: Text(
                  (locationData['message'] as String?) ?? 'GPS konumu alınamadı',
                  style: const TextStyle(color: Colors.white),
                ),
                backgroundColor: AppTheme.errorColor,
                duration: const Duration(seconds: 5),
                action: SnackBarAction(
                  label: 'Manuel Seç',
                  textColor: Colors.white,
                  onPressed: () {
                    setState(() {
                      _isManualSelected = true;
                      _isGpsSelected = false;
                    });
                    _showCitySelectionDialog();
                  },
                ),
              ),
            );
          }
        }
      }
    } catch (e) {
      print('❌ Error getting GPS location: $e');
      if (mounted && _scaffoldMessenger != null) {
        _scaffoldMessenger!.showSnackBar(
          SnackBar(
            content: Text(
              'GPS hatası: $e',
              style: const TextStyle(color: Colors.white),
            ),
            backgroundColor: AppTheme.errorColor,
            duration: const Duration(seconds: 4),
            action: SnackBarAction(
              label: 'Manuel Seç',
              textColor: Colors.white,
              onPressed: () {
                setState(() {
                  _isManualSelected = true;
                  _isGpsSelected = false;
                });
                _showCitySelectionDialog();
              },
            ),
          ),
        );
      }
    }
  }

  Future<void> _saveEnvironmentData() async {
    if (_selectedRegion == null) return;
    
    try {
      await _recommendationService.saveEnvironmentData(
        region: _selectedRegion!,
        soilType: _selectedSoilType,
        fertilizer: _selectedFertilizer,
        irrigation: _selectedIrrigation,
        sunlight: _selectedSunlight,
      );
      
      // Mesaj service katmanında yazdırılıyor, burada tekrar yazdırmaya gerek yok
    } catch (e) {
      print('❌ Error saving environment data: $e');
    }
  }

  Future<void> _saveSoilData() async {
    try {
      await _recommendationService.saveSoilData(
        isManualEntry: _isManualEntry,
        ph: _phController.text.isNotEmpty ? _phController.text : null,
        nitrogen: _nitrogenController.text.isNotEmpty ? _nitrogenController.text : null,
        phosphorus: _phosphorusController.text.isNotEmpty ? _phosphorusController.text : null,
        potassium: _potassiumController.text.isNotEmpty ? _potassiumController.text : null,
        humidity: _humidityController.text.isNotEmpty ? _humidityController.text : null,
        temperature: _temperatureController.text.isNotEmpty ? _temperatureController.text : null,
        rainfall: _rainfallController.text.isNotEmpty ? _rainfallController.text : null,
      );
      
      // Mesaj service katmanında yazdırılıyor, burada tekrar yazdırmaya gerek yok
    } catch (e) {
      print('❌ Error saving soil data: $e');
    }
  }

  void _showCitySelectionDialog() {
    showDialog(
      context: context,
      barrierColor: Colors.transparent,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Şehir Seçin'),
          content: SizedBox(
            width: double.maxFinite,
            height: 400,
            child: ListView.builder(
              itemCount: TurkishCities.cities.length,
              itemBuilder: (context, index) {
                final city = TurkishCities.cities[index];
                return ListTile(
                  title: Text(city),
                  subtitle: Text(TurkishCities.getRegionByCity(city)),
                  onTap: () async {
                    setState(() {
                      _selectedCity = city;
                      _selectedRegion = TurkishCities.getRegionByCity(city);
                    });
                    _onFieldChanged(); // Form validasyonunu güncelle
                    Navigator.of(context).pop();
                    
                    // Backend'e manuel konum bilgilerini gönder
                    try {
                      await _recommendationService.saveLocationData(
                        locationType: 'manual',
                        city: city,
                        region: TurkishCities.getRegionByCity(city),
                      );
                      
                      if (mounted && _scaffoldMessenger != null) {
                        _scaffoldMessenger!.showSnackBar(
                          SnackBar(
                            content: Text('Konum seçildi ve kaydedildi: $city'),
                            backgroundColor: AppTheme.primaryColor,
                          ),
                        );
                      }
                    } catch (e) {
                      print('❌ Error saving manual location: $e');
                      if (mounted && _scaffoldMessenger != null) {
                        _scaffoldMessenger!.showSnackBar(
                          SnackBar(
                            content: Text('Konum seçildi ancak kaydedilemedi: $e'),
                            backgroundColor: AppTheme.errorColor,
                          ),
                        );
                      }
                    }
                  },
                );
              },
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('İptal'),
            ),
          ],
        );
      },
    );
  }

  void _showProductRecommendationsBottomSheet() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      barrierColor: Colors.transparent,
      builder: (context) => _buildProductRecommendationsBottomSheet(),
    );
  }

  Widget _buildProductRecommendationsBottomSheet() {
    return Container(
      height: MediaQuery.of(context).size.height * 0.6,
      decoration: BoxDecoration(
        color: Colors.lightBlue.shade50, // Açık mavi background
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(AppTheme.borderRadiusLarge),
          topRight: Radius.circular(AppTheme.borderRadiusLarge),
        ),
      ),
      child: Column(
        children: [
          // Handle bar
          Container(
            width: 40,
            height: 4,
            margin: const EdgeInsets.symmetric(vertical: AppTheme.paddingMedium),
            decoration: BoxDecoration(
              color: Colors.grey.shade300,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          
          // Header
          Padding(
            padding: const EdgeInsets.all(AppTheme.paddingLarge),
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'En Uygun 3 Ürün',
                  style: TextStyle(
                    fontSize: AppTheme.fontSizeXLarge,
                    fontWeight: AppTheme.fontWeightBold,
                    color: AppTheme.textPrimaryColor,
                  ),
                ),
                      if (_mlConfidenceScores.isNotEmpty)
                        Text(
                          'ML Modeli ile Gerçek Tahmin Sonuçları (${_mlConfidenceScores.length} öneri)',
                          style: const TextStyle(
                            fontSize: AppTheme.fontSizeSmall,
                            color: AppTheme.textSecondaryColor,
                          ),
                        ),
                    ],
                  ),
                ),
                IconButton(
                  onPressed: () => Navigator.pop(context),
                  icon: const Icon(Icons.close),
                ),
              ],
            ),
          ),
          
          // Content
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: AppTheme.paddingLarge),
              child: _buildProductRecommendationsContent(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProductRecommendationsContent() {
    if (_recommendedProducts.isEmpty) {
      return const Center(
        child: Text(
          'Ürün önerisi bulunamadı.',
          style: AppTheme.bodyStyle,
        ),
      );
    }

    // Ürünleri confidence score'a göre sırala (büyükten küçüğe)
    List<Map<String, dynamic>> sortedProducts = [];
    for (int i = 0; i < _recommendedProducts.length; i++) {
      final confidenceScore = i < _mlConfidenceScores.length 
          ? _mlConfidenceScores[i] 
          : 0.0;
      sortedProducts.add({
        'product': _recommendedProducts[i],
        'confidence': confidenceScore,
        'originalIndex': i,
      });
    }
    
    // Confidence score'a göre sırala (büyükten küçüğe)
    sortedProducts.sort((a, b) => b['confidence'].compareTo(a['confidence']));

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Bu koşullara en uygun ürünler:',
          style: TextStyle(
            fontSize: AppTheme.fontSizeLarge,
            fontWeight: AppTheme.fontWeightMedium,
            color: AppTheme.textSecondaryColor,
          ),
        ),
        const SizedBox(height: AppTheme.paddingLarge),
        
        ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: sortedProducts.length,
          itemBuilder: (context, index) {
            final productData = sortedProducts[index];
            final product = productData['product'];
            final confidenceScore = productData['confidence'];
            
            return Padding(
              padding: const EdgeInsets.only(bottom: AppTheme.paddingSmall),
              child: CustomCard(
                child: Padding(
                  padding: const EdgeInsets.all(AppTheme.paddingSmall),
                  child: Row(
                    children: [
                      // Sıralama numarası
                      Container(
                        width: 30,
                        height: 30,
                        decoration: BoxDecoration(
                          color: _getRankingColor(index),
                          shape: BoxShape.circle,
                        ),
                        child: Center(
                          child: Text(
                            '${index + 1}',
                            style: const TextStyle(
                              color: AppTheme.surfaceColor,
                              fontSize: AppTheme.fontSizeMedium,
                              fontWeight: AppTheme.fontWeightBold,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: AppTheme.paddingSmall),
                      
                      // Ürün resmi
                      ClipRRect(
                        borderRadius: BorderRadius.circular(AppTheme.borderRadius),
                        child: Image.network(
                          _imageService.getProductImage(product.name),
                          width: 50,
                          height: 50,
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) => Container(
                            width: 50,
                            height: 50,
                            color: AppTheme.primaryLightColor.withOpacity(0.2),
                            child: const Icon(Icons.broken_image, color: AppTheme.textSecondaryColor),
                          ),
                        ),
                      ),
                      const SizedBox(width: AppTheme.paddingSmall),
                      
                      // Ürün bilgileri
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            product.name,
                            style: const TextStyle(
                                fontSize: AppTheme.fontSizeLarge,
                              fontWeight: AppTheme.fontWeightBold,
                              color: AppTheme.textPrimaryColor,
                            ),
                          ),
                            const SizedBox(height: 4),
                            
                            // Güven skoru göster
                            if (_mlConfidenceScores.isNotEmpty)
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                decoration: BoxDecoration(
                                  color: _getConfidenceColor(confidenceScore),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  '${(confidenceScore * 100).toStringAsFixed(1)}% güven',
                                  style: const TextStyle(
                                    color: AppTheme.surfaceColor,
                                    fontSize: AppTheme.fontSizeSmall,
                                    fontWeight: AppTheme.fontWeightMedium,
                                  ),
                                ),
                              )
                            else
                          Text(
                            product.category,
                            style: AppTheme.bodyStyle.copyWith(
                              color: AppTheme.textSecondaryColor,
                                  fontSize: AppTheme.fontSizeSmall,
                            ),
                          ),
                            
                            const SizedBox(height: 4),
                          Text(
                            product.description,
                            style: AppTheme.bodyStyle.copyWith(
                                fontSize: AppTheme.fontSizeSmall,
                            ),
                              maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                    ),
                      const SizedBox(width: AppTheme.paddingSmall),
                      
                      // Ekle butonu
                    Container(
                        width: 32,
                        height: 32,
                      decoration: BoxDecoration(
                        color: Colors.transparent,
                        border: Border.all(
                          color: AppTheme.primaryColor,
                          width: 2,
                        ),
                          borderRadius: BorderRadius.circular(6),
                      ),
                      child: IconButton(
                        onPressed: () => _addProductToCart(product),
                        icon: const Icon(
                          Icons.add,
                          color: AppTheme.primaryColor,
                            size: 16,
                        ),
                        padding: EdgeInsets.zero,
                        splashColor: Colors.transparent,
                        highlightColor: Colors.transparent,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            );
          },
        ),
      ],
    );
  }

  void _addProductToCart(Product product) async {
    try {
      // Save product to My Products
      await _myProductsService.saveProduct(product);
      
      // Show success message
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            '${product.name} ürünlerime eklendi',
            style: const TextStyle(color: Colors.white),
          ),
          backgroundColor: AppTheme.primaryColor,
          duration: const Duration(seconds: 2),
        ),
      );
      
      print('Added ${product.name} to My Products');
      
      // Navigate to My Products page
      Navigator.pushNamed(context, '/my-products');
    } catch (e) {
      // Show error message
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Ürün eklenirken hata oluştu: $e',
            style: const TextStyle(color: Colors.white),
          ),
          backgroundColor: AppTheme.errorColor,
          duration: const Duration(seconds: 3),
        ),
      );
      
      print('Error adding product to My Products: $e');
    }
  }

  Future<void> _saveEnvironmentDataToMyEnvironments() async {
    try {
      // Ortam verilerini hazırla
      final environmentData = {
        'ph': _phController.text.isNotEmpty ? _phController.text : '6.5',
        'nitrogen': _nitrogenController.text.isNotEmpty ? _nitrogenController.text : '120',
        'phosphorus': _phosphorusController.text.isNotEmpty ? _phosphorusController.text : '60',
        'potassium': _potassiumController.text.isNotEmpty ? _potassiumController.text : '225',
        'humidity': _humidityController.text.isNotEmpty ? _humidityController.text : '26',
        'temperature': _temperatureController.text.isNotEmpty ? _temperatureController.text : '23',
        'rainfall': _rainfallController.text.isNotEmpty ? _rainfallController.text : '850',
        'region': _selectedRegion ?? 'İç Anadolu',
        'soilType': _selectedSoilType ?? 'Tınlı Toprak',
        'fertilizer': _selectedFertilizer ?? 'Organik',
        'irrigation': _selectedIrrigation ?? 'Damla Sulama',
        'sunlight': _selectedSunlight ?? 'Tam Güneş',
        'city': _selectedCity ?? 'Ankara',
      };

      // Ortam verilerini kaydet
      await _myEnvironmentsService.saveEnvironment(environmentData);
      
      print('Environment data saved to My Environments successfully');
    } catch (e) {
      print('Error saving environment data to My Environments: $e');
      // Hata durumunda kullanıcıya bildirim gösterme, sadece logla
    }
  }

  /// ML modelinden gelen İngilizce ürün isimlerini Türkçe'ye çevir
  String _translateCropNameToTurkish(String englishCropName) {
    final cropTranslations = {
      'corn': 'Mısır',
      'wheat': 'Buğday',
      'rice': 'Pirinç',
      'tomato': 'Domates',
      'potato': 'Patates',
      'soybean': 'Soya',
      'cotton': 'Pamuk',
      'barley': 'Arpa',
      'sunflower': 'Ayçiçeği',
      'sugar beet': 'Şeker Pancarı',
      'sugarcane': 'Şeker Kamışı',
      'carrot': 'Havuç',
      'onion': 'Soğan',
      'cabbage': 'Lahana',
      'lettuce': 'Marul',
      'spinach': 'Ispanak',
      'pepper': 'Biber',
      'cucumber': 'Salatalık',
      'eggplant': 'Patlıcan',
      'peas': 'Bezelye',
      'beans': 'Fasulye',
      'lentils': 'Mercimek',
      'chickpeas': 'Nohut',
      'apple': 'Elma',
      'pear': 'Armut',
      'cherry': 'Kiraz',
      'grape': 'Üzüm',
      'olive': 'Zeytin',
      'almond': 'Badem',
      'walnut': 'Ceviz',
      'hazelnut': 'Fındık',
      // Backend'den gelen Türkçe isimler için
      'misir': 'Mısır',
      'bugday': 'Buğday',
      'pirinç': 'Pirinç',
      'domates': 'Domates',
      'patates': 'Patates',
      'soya': 'Soya',
      'pamuk': 'Pamuk',
      'arpa': 'Arpa',
      'ayçiçeği': 'Ayçiçeği',
      'şeker pancarı': 'Şeker Pancarı',
      'şeker kamışı': 'Şeker Kamışı',
      'havuç': 'Havuç',
      'soğan': 'Soğan',
      'lahana': 'Lahana',
      'marul': 'Marul',
      'ıspanak': 'Ispanak',
      'biber': 'Biber',
      'salatalık': 'Salatalık',
      'patlıcan': 'Patlıcan',
      'bezelye': 'Bezelye',
      'fasulye': 'Fasulye',
      'mercimek': 'Mercimek',
      'nohut': 'Nohut',
      'elma': 'Elma',
      'armut': 'Armut',
      'kiraz': 'Kiraz',
      'üzüm': 'Üzüm',
      'zeytin': 'Zeytin',
      'badem': 'Badem',
      'ceviz': 'Ceviz',
      'fındık': 'Fındık',
    };
    
    return cropTranslations[englishCropName.toLowerCase()] ?? englishCropName;
  }

  /// Türkçe bölge isimlerini İngilizce'ye çevir
  String _translateRegionToEnglish(String turkishRegion) {
    final regionTranslations = {
      'İç Anadolu': 'Central Anatolia',
      'Marmara': 'Marmara',
      'Ege': 'Aegean',
      'Akdeniz': 'Mediterranean',
      'Karadeniz': 'Black Sea',
      'Doğu Anadolu': 'Eastern Anatolia',
      'Güneydoğu Anadolu': 'Southeastern Anatolia',
    };
    
    return regionTranslations[turkishRegion] ?? turkishRegion;
  }

  /// Türkçe toprak tipini İngilizce'ye çevir
  String _translateSoilTypeToEnglish(String turkishSoilType) {
    final soilTranslations = {
      'Killi Toprak': 'Clay',
      'Kumlu Toprak': 'Sandy',
      'Tınlı Toprak': 'Loamy',
      'Siltli Toprak': 'Silty',
      'Kireçli Toprak': 'Loamy', // Fallback
      'Asitli Toprak': 'Sandy', // Fallback
    };
    
    return soilTranslations[turkishSoilType] ?? turkishSoilType;
  }

  /// Türkçe gübre tipini İngilizce'ye çevir
  String _translateFertilizerToEnglish(String turkishFertilizer) {
    final fertilizerTranslations = {
      'Potasyum Nitrat': 'Potassium Nitrate',
      'Amonyum Sülfat': 'Ammonium Sulphate',
      'Üre': 'Urea',
      'Kompost': 'Urea', // Fallback
      'Organik Gübre': 'Urea', // Fallback
    };
    
    return fertilizerTranslations[turkishFertilizer] ?? turkishFertilizer;
  }

  /// Türkçe sulama yöntemini İngilizce'ye çevir
  String _translateIrrigationToEnglish(String turkishIrrigation) {
    final irrigationTranslations = {
      'Salma Sulama': 'Flood Irrigation',
      'Damla Sulama': 'Drip Irrigation',
      'Yağmurlama': 'Sprinkler Irrigation',
      'Sprinkler': 'Sprinkler Irrigation',
      'Mikro Sulama': 'Micro Irrigation',
    };
    
    return irrigationTranslations[turkishIrrigation] ?? turkishIrrigation;
  }

  /// Türkçe hava durumunu İngilizce'ye çevir
  String _translateWeatherToEnglish(String turkishWeather) {
    final weatherTranslations = {
      'Güneşli': 'sunny',
      'Kısmi Gölge': 'partially cloudy',
      'Gölgeli': 'cloudy',
      'Tam Gölge': 'shady',
    };
    
    return weatherTranslations[turkishWeather] ?? turkishWeather;
  }

  /// Sıralama pozisyonuna göre renk döndür
  Color _getRankingColor(int index) {
    // Tüm sıralama numaraları yeşil yuvarlak daire içinde aynı renk
    return AppTheme.primaryColor;
  }

  /// Güven skoruna göre renk döndür
  Color _getConfidenceColor(double confidence) {
    if (confidence >= 0.8) {
      return Colors.green; // Yüksek güven
    } else if (confidence >= 0.6) {
      return Colors.orange; // Orta güven
    } else {
      return Colors.red; // Düşük güven
    }
  }


}