import 'package:flutter/material.dart';
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
  bool _isLoading = false;
  bool _isGpsSelected = false;
  bool _isManualSelected = false;
  bool _isManualEntry = false;
  bool _useAverageValues = false;

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
    _useAverageValues = true;
    
    // Ortalama değerleri doldur
    _fillAverageValues();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _scaffoldMessenger = ScaffoldMessenger.of(context);
  }

  void _fillAverageValues() {
    if (_useAverageValues) {
      _phController.text = '6.5';
      _nitrogenController.text = '120';
      _phosphorusController.text = '60';
      _potassiumController.text = '225';
      _humidityController.text = '26';
      _temperatureController.text = '23';
      _rainfallController.text = '850';
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
        // Backend'e temel bilgi gönder
        final response = await _recommendationService.generateRecommendation(
          soilType: _selectedSoilType ?? 'Tınlı Toprak',
          climate: _selectedRegion ?? 'İç Anadolu',
          region: _selectedRegion ?? 'İç Anadolu',
          preferences: {
            'ph': _phController.text.isNotEmpty ? _phController.text : '6.5',
            'nitrogen': _nitrogenController.text.isNotEmpty ? _nitrogenController.text : '120',
            'phosphorus': _phosphorusController.text.isNotEmpty ? _phosphorusController.text : '60',
            'potassium': _potassiumController.text.isNotEmpty ? _potassiumController.text : '225',
            'humidity': _humidityController.text.isNotEmpty ? _humidityController.text : '26',
            'temperature': _temperatureController.text.isNotEmpty ? _temperatureController.text : '23',
            'rainfall': _rainfallController.text.isNotEmpty ? _rainfallController.text : '850',
            'selectedRegion': _selectedRegion,
            'selectedSoilType': _selectedSoilType,
            'selectedFertilizer': _selectedFertilizer,
            'selectedIrrigation': _selectedIrrigation,
            'selectedSunlight': _selectedSunlight,
            'selectedCity': _selectedCity,
          },
        );

        // Backend'den gelen öneri verilerini işle
        if (response['success'] == true) {
          // Sabit ürünler: Domates, Mısır, Pirinç (backend'den gelen veri ile değiştirilebilir)
          final fixedProducts = _productService.getAllProducts()
              .where((product) => ['Domates', 'Mısır', 'Pirinç'].contains(product.name))
              .toList();

          if (mounted) {
            setState(() {
              _recommendedProducts = fixedProducts;
            });
            _showProductRecommendationsBottomSheet();
            
            // Ortam verilerini kaydet
            await _saveEnvironmentDataToMyEnvironments();
            
            // Başarı mesajını göster
            if (_scaffoldMessenger != null) {
              _scaffoldMessenger!.showSnackBar(
                SnackBar(
                  content: Text(response['message'] ?? 'Öneri başarıyla oluşturuldu'),
                  backgroundColor: Colors.green,
                ),
              );
            }
          }
        } else {
          throw Exception(response['message'] ?? 'Öneri oluşturulamadı');
        }
      } catch (e) {
        if (mounted && _scaffoldMessenger != null) {
          _scaffoldMessenger!.showSnackBar(
            SnackBar(
              content: Text('Ürün önerisi alınırken hata oluştu: $e'),
              backgroundColor: AppTheme.errorColor,
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
                  _showCitySelectionDialog();
                },
              ),
            ],
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
                  
                  // Backend'e çevre verilerini gönder (sadece bölge değiştiğinde)
                  if (value != null) {
                    _saveEnvironmentData();
                  }
                },
              ),
            ),
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
                  
                  // Backend'e çevre verilerini gönder (sadece region varsa)
                  if (_selectedRegion != null) {
                    _saveEnvironmentData();
                  }
                },
              ),
            ),
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
                  
                  // Backend'e çevre verilerini gönder (sadece region varsa)
                  if (_selectedRegion != null) {
                    _saveEnvironmentData();
                  }
                },
              ),
            ),
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
                  
                  // Backend'e çevre verilerini gönder (sadece region varsa)
                  if (_selectedRegion != null) {
                    _saveEnvironmentData();
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
                  
                  // Backend'e çevre verilerini gönder (sadece region varsa)
                  if (_selectedRegion != null) {
                    _saveEnvironmentData();
                  }
                },
              ),
            ),
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
                    setState(() {
                      _isManualEntry = false;
                      _useAverageValues = true;
                    });
                    _fillAverageValues();
                    
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
            CustomTextField(
              controller: _phController,
              label: 'pH',
              hint: 'pH',
              keyboardType: TextInputType.number,
              validator: (value) => Validators.range(value, 4.0, 9.0, 'pH'),
              onChanged: (value) {
                if (value.isNotEmpty) {
                  _saveSoilData();
                }
              },
            ),
            CustomTextField(
              controller: _nitrogenController,
              label: 'Azot (ppm)',
              hint: 'Azot (ppm)',
              keyboardType: TextInputType.number,
              validator: (value) => Validators.range(value, 0.0, 300.0, 'Azot'),
              onChanged: (value) {
                if (value.isNotEmpty) {
                  _saveSoilData();
                }
              },
            ),
            CustomTextField(
              controller: _phosphorusController,
              label: 'Fosfor (ppm)',
              hint: 'Fosfor (ppm)',
              keyboardType: TextInputType.number,
              validator: (value) => Validators.range(value, 0.0, 150.0, 'Fosfor'),
              onChanged: (value) {
                if (value.isNotEmpty) {
                  _saveSoilData();
                }
              },
            ),
            CustomTextField(
              controller: _potassiumController,
              label: 'Potasyum (ppm)',
              hint: 'Potasyum (ppm)',
              keyboardType: TextInputType.number,
              validator: (value) => Validators.range(value, 0.0, 400.0, 'Potasyum'),
              onChanged: (value) {
                if (value.isNotEmpty) {
                  _saveSoilData();
                }
              },
            ),
            CustomTextField(
              controller: _humidityController,
              label: 'Nem %',
              hint: 'Nem %',
              keyboardType: TextInputType.number,
              validator: (value) => Validators.range(value, 0.0, 100.0, 'Nem'),
              onChanged: (value) {
                if (value.isNotEmpty) {
                  _saveSoilData();
                }
              },
            ),
            CustomTextField(
              controller: _temperatureController,
              label: 'Sıcaklık °C',
              hint: 'Sıcaklık °C',
              keyboardType: TextInputType.number,
              validator: (value) => Validators.range(value, -10.0, 45.0, 'Sıcaklık'),
              onChanged: (value) {
                if (value.isNotEmpty) {
                  _saveSoilData();
                }
              },
            ),
            CustomTextField(
              controller: _rainfallController,
              label: 'Yağış mm',
              hint: 'Yağış mm',
              keyboardType: TextInputType.number,
              validator: (value) => Validators.range(value, 0.0, 2000.0, 'Yağış'),
              onChanged: (value) {
                if (value.isNotEmpty) {
                  _saveSoilData();
                }
              },
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildGetRecommendationsButton() {
    return CustomButton(
      text: 'Öneri Al',
      icon: Icons.lightbulb_outline,
      onPressed: _handleGetProductRecommendation,
      isLoading: _isLoading,
      isFullWidth: true,
      height: 60,
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
    // Get REAL GPS location
    if (_scaffoldMessenger != null) {
      _scaffoldMessenger!.showSnackBar(
        const SnackBar(
          content: Text('📍 GPS konumunuz alınıyor...'),
          backgroundColor: AppTheme.primaryColor,
        ),
      );
    }
    
    // Get real GPS location
    try {
      final locationData = await _locationService.getCurrentLocation();
      
      if (mounted) {
        if (locationData['success'] == true) {
          setState(() {
            _selectedCity = locationData['city'];
            _selectedRegion = locationData['region'];
            _isGpsSelected = true;
            _isManualSelected = false;
          });
          
          // Backend'e konum bilgilerini gönder
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
          // GPS failed
          if (mounted && _scaffoldMessenger != null) {
            _scaffoldMessenger!.showSnackBar(
              SnackBar(
                content: Text(
                  locationData['message'] ?? 'GPS konumu alınamadı',
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
                const Text(
                  'En Uygun 3 Ürün',
                  style: TextStyle(
                    fontSize: AppTheme.fontSizeXLarge,
                    fontWeight: AppTheme.fontWeightBold,
                    color: AppTheme.textPrimaryColor,
                  ),
                ),
                const Spacer(),
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
          itemCount: _recommendedProducts.length,
          itemBuilder: (context, index) {
            final product = _recommendedProducts[index];
            return Padding(
              padding: const EdgeInsets.only(bottom: AppTheme.paddingSmall), // Küçültüldü
              child: CustomCard(
                child: Padding(
                  padding: const EdgeInsets.all(AppTheme.paddingSmall), // Padding eklendi
                  child: Row(
                    children: [
                      Container(
                        width: 30, // Küçültüldü
                        height: 30, // Küçültüldü
                        decoration: const BoxDecoration(
                          color: AppTheme.primaryColor,
                          shape: BoxShape.circle,
                        ),
                        child: Center(
                          child: Text(
                            '${index + 1}',
                            style: const TextStyle(
                              color: AppTheme.surfaceColor,
                              fontSize: AppTheme.fontSizeMedium, // Küçültüldü
                              fontWeight: AppTheme.fontWeightBold,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: AppTheme.paddingSmall), // Küçültüldü
                      ClipRRect(
                        borderRadius: BorderRadius.circular(AppTheme.borderRadius),
                        child: Image.network(
                          _imageService.getProductImage(product.name),
                          width: 50, // Küçültüldü
                          height: 50, // Küçültüldü
                          fit: BoxFit.cover,
                          errorBuilder: (context, error, stackTrace) => Container(
                            width: 50, // Küçültüldü
                            height: 50, // Küçültüldü
                            color: AppTheme.primaryLightColor.withOpacity(0.2),
                            child: const Icon(Icons.broken_image, color: AppTheme.textSecondaryColor),
                          ),
                        ),
                      ),
                      const SizedBox(width: AppTheme.paddingSmall), // Küçültüldü
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            product.name,
                            style: const TextStyle(
                              fontSize: AppTheme.fontSizeLarge, // Küçültüldü
                              fontWeight: AppTheme.fontWeightBold,
                              color: AppTheme.textPrimaryColor,
                            ),
                          ),
                          const SizedBox(height: 4), // Küçültüldü
                          Text(
                            product.category,
                            style: AppTheme.bodyStyle.copyWith(
                              color: AppTheme.textSecondaryColor,
                              fontSize: AppTheme.fontSizeSmall, // Küçültüldü
                            ),
                          ),
                          const SizedBox(height: 4), // Küçültüldü
                          Text(
                            product.description,
                            style: AppTheme.bodyStyle.copyWith(
                              fontSize: AppTheme.fontSizeSmall, // Küçültüldü
                            ),
                            maxLines: 1, // Tek satır
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: AppTheme.paddingSmall), // Küçültüldü
                    // Add button
                    Container(
                      width: 32, // Küçültüldü
                      height: 32, // Küçültüldü
                      decoration: BoxDecoration(
                        color: Colors.transparent,
                        border: Border.all(
                          color: AppTheme.primaryColor,
                          width: 2,
                        ),
                        borderRadius: BorderRadius.circular(6), // Küçültüldü
                      ),
                      child: IconButton(
                        onPressed: () => _addProductToCart(product),
                        icon: const Icon(
                          Icons.add,
                          color: AppTheme.primaryColor,
                          size: 16, // Küçültüldü
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
}