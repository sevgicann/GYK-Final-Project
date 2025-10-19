import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_layout.dart';
import '../models/product.dart';
import '../services/product_service.dart';
import '../services/image_service.dart';
import '../services/product_selection_service.dart';
import '../services/location_service.dart';
import '../data/turkish_cities.dart';
import '../widgets/custom_button.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_dropdown.dart';

class ProductSelectionPage extends StatefulWidget {
  const ProductSelectionPage({super.key});

  @override
  State<ProductSelectionPage> createState() => _ProductSelectionPageState();
}

class _ProductSelectionPageState extends State<ProductSelectionPage> {
  final ProductService _productService = ProductService();
  final ImageService _imageService = ImageService();
  final ProductSelectionService _productSelectionService = ProductSelectionService();
  final LocationService _locationService = LocationService();

  Product? _selectedProduct;
  String? _selectedCity;
  String? _selectedRegion;
  bool _isGpsSelected = false;
  bool _isManualSelected = false;
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return AppLayout(
      currentPageIndex: 2, // Environment Recommendation index
      pageTitle: 'Ürün Seçiminden Ortam Koşulları Önerisi',
      actions: [
        // Reverse Butonu
        IconButton(
          icon: const Icon(Icons.swap_horiz, color: AppTheme.textPrimaryColor),
          onPressed: () {
            AppRouter.navigateTo(context, AppRouter.environmentRecommendation);
          },
          tooltip: 'Ortam Koşullarından Ürün Tahmini',
        ),
      ],
      child: SafeArea(
        child: Column(
          children: [
            // Scrollable Content 
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(AppTheme.paddingLarge),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Ürün Seçimi Bölümü
                    _buildProductSelectionSection(),
                    
                    const SizedBox(height: AppTheme.paddingXLarge),
                    
                    // Seçilen Ürün Gösterimi
                    if (_selectedProduct != null) _buildSelectedProductCard(),
                    
                    const SizedBox(height: AppTheme.paddingXLarge),
                    
                    // Konum Seçimi Bölümü
                    _buildLocationSelectionSection(),
                    
                    const SizedBox(height: AppTheme.paddingXLarge),
                    
                    // Seçilen Konum Gösterimi
                    if (_selectedCity != null) _buildSelectedLocationCard(),
                    
                    const SizedBox(height: AppTheme.paddingXLarge),
                  ],
                ),
              ),
            ),
            
            // Fixed Bottom Button
            Container(
              padding: const EdgeInsets.all(AppTheme.paddingLarge),
              child: _buildGetRecommendationButton(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProductSelectionSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Hangi ürünü yetiştirmek istiyorsunuz?',
          style: TextStyle(
            fontSize: AppTheme.fontSizeXLarge,
            fontWeight: AppTheme.fontWeightBold,
            color: AppTheme.textPrimaryColor,
          ),
        ),
        const SizedBox(height: AppTheme.paddingMedium),
        
        CustomDropdown<String>(
          label: 'Ürün Seçin',
          value: _selectedProduct?.name,
          items: _productService.getAllProductNames(),
          hint: 'Ürün seçiniz',
          onChanged: (value) async {
            if (value != null) {
              setState(() {
                _selectedProduct = _productService.getProductByName(value);
              });
              
              // Send product selection to backend
              try {
                await _productSelectionService.selectProduct(
                  productName: _selectedProduct!.name,
                  productId: _selectedProduct!.id,
                  productCategory: _selectedProduct!.category,
                  productDescription: _selectedProduct!.description,
                );
              } catch (e) {
                print('❌ Error sending product selection to backend: $e');
                // Don't show error to user, just log it
              }
            }
          },
        ),
      ],
    );
  }

  Widget _buildSelectedProductCard() {
    if (_selectedProduct == null) return const SizedBox.shrink();

    return CustomCard(
      child: Column(
        children: [
          Row(
            children: [
              // Ürün Görseli
              Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(AppTheme.borderRadius),
                  image: DecorationImage(
                    image: NetworkImage(_imageService.getProductImage(_selectedProduct!.name)),
                    fit: BoxFit.cover,
                  ),
                ),
                child: _imageService.isImageLoaded
                    ? null
                    : const Center(
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          valueColor: AlwaysStoppedAnimation<Color>(AppTheme.primaryColor),
                        ),
                      ),
              ),
              const SizedBox(width: AppTheme.paddingMedium),
              
              // Ürün Bilgileri
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _selectedProduct!.name,
                      style: const TextStyle(
                        fontSize: AppTheme.fontSizeLarge,
                        fontWeight: AppTheme.fontWeightBold,
                        color: AppTheme.textPrimaryColor,
                      ),
                    ),
                    const SizedBox(height: AppTheme.paddingSmall),
                    Text(
                      _selectedProduct!.category,
                      style: AppTheme.bodyStyle,
                    ),
                    const SizedBox(height: AppTheme.paddingSmall),
                    Text(
                      _selectedProduct!.description,
                      style: AppTheme.bodyStyle,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
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

  Widget _buildLocationSelectionSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Konum bilgilerinizi girin',
          style: TextStyle(
            fontSize: AppTheme.fontSizeXLarge,
            fontWeight: AppTheme.fontWeightBold,
            color: AppTheme.textPrimaryColor,
          ),
        ),
        const SizedBox(height: AppTheme.paddingMedium),
        
        // Konum Seçenekleri
        Row(
          children: [
            Expanded(
              child: _buildLocationOption(
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
            ),
            const SizedBox(width: AppTheme.paddingMedium),
            Expanded(
              child: _buildLocationOption(
                icon: Icons.location_city,
                title: 'Şehri Manuel Seç',
                isSelected: _isManualSelected,
                isSecondButton: true, // İkinci buton her zaman yeşil
                onTap: () {
                  setState(() {
                    _isGpsSelected = false;
                    _isManualSelected = true;
                  });
                  _showCitySelectionDialog();
                },
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildLocationOption({
    required IconData icon,
    required String title,
    required bool isSelected,
    required VoidCallback onTap,
    bool isSecondButton = false, // İkinci buton için parametre
  }) {
    // İkinci buton her zaman yeşil olsun
    final shouldBeGreen = isSelected || isSecondButton;
    
    return GestureDetector(
      onTap: onTap,
      behavior: HitTestBehavior.translucent,
      child: Container(
        padding: const EdgeInsets.all(AppTheme.paddingMedium),
        decoration: BoxDecoration(
          color: shouldBeGreen ? AppTheme.primaryColor : AppTheme.surfaceColor,
          border: Border.all(
            color: shouldBeGreen ? AppTheme.primaryColor : AppTheme.primaryLightColor,
            width: 2,
          ),
          borderRadius: BorderRadius.circular(AppTheme.borderRadiusLarge),
        ),
        child: Column(
          children: [
            Icon(
              icon,
              color: shouldBeGreen ? AppTheme.surfaceColor : AppTheme.primaryLightColor,
              size: AppTheme.iconSize,
            ),
            const SizedBox(height: AppTheme.paddingSmall),
            Text(
              title,
              textAlign: TextAlign.center,
              style: TextStyle(
                color: shouldBeGreen ? AppTheme.surfaceColor : AppTheme.primaryLightColor,
                fontSize: AppTheme.fontSizeSmall,
                fontWeight: AppTheme.fontWeightMedium,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSelectedLocationCard() {
    if (_selectedCity == null) return const SizedBox.shrink();

    return CustomCard(
      child: Column(
        children: [
          Row(
            children: [
              // Şehir Görseli
              Container(
                width: 80,
                height: 60,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(AppTheme.borderRadius),
                  image: DecorationImage(
                    image: NetworkImage(_imageService.getCityImage(_selectedCity!)),
                    fit: BoxFit.cover,
                  ),
                ),
              ),
              const SizedBox(width: AppTheme.paddingMedium),
              
              // Şehir Bilgileri
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _selectedCity!,
                      style: const TextStyle(
                        fontSize: AppTheme.fontSizeLarge,
                        fontWeight: AppTheme.fontWeightBold,
                        color: AppTheme.textPrimaryColor,
                      ),
                    ),
                    const SizedBox(height: AppTheme.paddingSmall),
                    Text(
                      'Bölge: $_selectedRegion',
                      style: AppTheme.bodyStyle,
                    ),
                    const SizedBox(height: AppTheme.paddingSmall),
                    Row(
                      children: [
                        Icon(
                          _isGpsSelected ? Icons.gps_fixed : Icons.location_city,
                          color: AppTheme.primaryColor,
                          size: 16,
                        ),
                        const SizedBox(width: AppTheme.paddingSmall),
                        Text(
                          _isGpsSelected ? 'GPS ile belirlendi' : 'Manuel seçildi',
                          style: AppTheme.bodyStyle,
                        ),
                      ],
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

  Widget _buildGetRecommendationButton() {
    final canGetRecommendation = _selectedProduct != null && _selectedCity != null;
    
    return CustomButton(
      text: 'Önerileri Al',
      icon: Icons.lightbulb_outline,
      onPressed: canGetRecommendation ? _handleGetRecommendation : null,
      isLoading: _isLoading,
      isFullWidth: true,
    );
  }

  void _handleGpsLocation() async {
    // Get REAL GPS location
    setState(() {
      _isLoading = true;
    });

    try {
      // Get real GPS location
      final locationData = await _locationService.getCurrentLocation();
      
      if (mounted) {
        if (locationData['success'] == true) {
          setState(() {
            _selectedCity = locationData['city'];
            _selectedRegion = locationData['region'];
            _isGpsSelected = true;
            _isManualSelected = false;
            _isLoading = false;
          });
          
          // Show success message
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                '📍 GPS konumu alındı: $_selectedCity ($_selectedRegion)',
                style: const TextStyle(color: Colors.white),
              ),
              backgroundColor: AppTheme.primaryColor,
              duration: const Duration(seconds: 3),
            ),
          );
          
          // Send GPS location selection to backend
          try {
            await _productSelectionService.selectLocation(
              locationType: 'gps',
              city: _selectedCity!,
              region: _selectedRegion!,
              latitude: locationData['latitude'],
              longitude: locationData['longitude'],
              climateZone: _selectedRegion!,
            );
            print('✅ GPS location sent to backend: $_selectedCity, $_selectedRegion');
          } catch (e) {
            print('❌ Error sending GPS location to backend: $e');
            // Don't show error to user, just log it
          }
        } else {
          // GPS failed, show error
          setState(() {
            _isLoading = false;
            _isGpsSelected = false;
          });
          
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                (locationData['message'] as String?) ?? 'GPS konumu alınamadı',
                style: const TextStyle(color: Colors.white),
              ),
              backgroundColor: AppTheme.errorColor,
              duration: const Duration(seconds: 4),
              action: SnackBarAction(
                label: 'Manuel Seç',
                textColor: Colors.white,
                onPressed: () {
                  _showCitySelectionDialog();
                },
              ),
            ),
          );
        }
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoading = false;
          _isGpsSelected = false;
        });
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'GPS hatası: $e',
              style: const TextStyle(color: Colors.white),
            ),
            backgroundColor: AppTheme.errorColor,
            action: SnackBarAction(
              label: 'Manuel Seç',
              textColor: Colors.white,
              onPressed: () {
                _showCitySelectionDialog();
              },
            ),
          ),
        );
        print('❌ Error in GPS location: $e');
      }
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
                      _isManualSelected = true;
                      _isGpsSelected = false;
                    });
                    Navigator.of(context).pop();
                    
                    // Send manual location selection to backend
                    try {
                      await _productSelectionService.selectLocation(
                        locationType: 'manual',
                        city: city,
                        region: TurkishCities.getRegionByCity(city),
                        climateZone: TurkishCities.getRegionByCity(city),
                      );
                    } catch (e) {
                      print('❌ Error sending manual location to backend: $e');
                      // Don't show error to user, just log it
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

  Future<void> _handleGetRecommendation() async {
    if (_selectedProduct == null || _selectedCity == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Lütfen ürün ve konum seçiniz'),
          backgroundColor: AppTheme.errorColor,
        ),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // Get environment recommendations from backend
      final response = await _productSelectionService.getEnvironmentRecommendations(
        productName: _selectedProduct!.name,
        city: _selectedCity!,
        region: _selectedRegion!,
        locationType: _isGpsSelected ? 'gps' : 'manual',
      );
      
      if (mounted) {
        // Show success message
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Öneriler başarıyla alındı: ${_selectedProduct!.name} için ${_selectedCity!}'),
            backgroundColor: AppTheme.successColor,
          ),
        );
        
        // Show environment recommendations
        _showEnvironmentRecommendations(response);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Öneri alınırken hata oluştu: $e'),
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

  void _showEnvironmentRecommendations([Map<String, dynamic>? responseData]) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      barrierColor: Colors.transparent,
      builder: (context) => _buildRecommendationsBottomSheet(responseData),
    );
  }

  Widget _buildRecommendationsBottomSheet([Map<String, dynamic>? responseData]) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.6,
      decoration: const BoxDecoration(
        color: AppTheme.backgroundColor,
        borderRadius: BorderRadius.only(
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
                  'Çevre Önerileri',
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
              child: _buildRecommendationsContent(responseData),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRecommendationsContent([Map<String, dynamic>? responseData]) {
    if (_selectedProduct == null) return const SizedBox.shrink();

    final product = _selectedProduct!;
    
    // Model sonuçları varsa onları kullan, yoksa ürün gereksinimlerini kullan
    List<RecommendationItem> items;
    String? notes;
    String? region;
    
    if (responseData != null && responseData['success'] == true) {
      final data = responseData['data'];
      final recommendations = data['recommendations'] as Map<String, dynamic>?;
      
      // Model sonuçlarından sadece gerçek değerleri al
      items = [];
      
      if (recommendations != null) {
        // Toprak önerileri
        final soilRecs = recommendations['soil_recommendations'] as Map<String, dynamic>?;
        if (soilRecs != null) {
          if (soilRecs['ph_level'] != null) {
            items.add(RecommendationItem(
              label: 'Toprak pH', 
              value: soilRecs['ph_level'].toString()
            ));
          }
          if (soilRecs['soil_type'] != null) {
            items.add(RecommendationItem(
              label: 'Toprak Tipi', 
              value: soilRecs['soil_type'].toString()
            ));
          }
          if (soilRecs['drainage'] != null) {
            items.add(RecommendationItem(
              label: 'Drenaj', 
              value: soilRecs['drainage'].toString()
            ));
          }
          if (soilRecs['organic_matter'] != null) {
            items.add(RecommendationItem(
              label: 'Organik Madde', 
              value: soilRecs['organic_matter'].toString()
            ));
          }
        }
        
        // Çevre koşulları
        final envRecs = recommendations['environmental_conditions'] as Map<String, dynamic>?;
        if (envRecs != null) {
          if (envRecs['temperature'] != null) {
            items.add(RecommendationItem(
              label: 'Sıcaklık', 
              value: envRecs['temperature'].toString()
            ));
          }
          if (envRecs['humidity'] != null) {
            items.add(RecommendationItem(
              label: 'Nem', 
              value: envRecs['humidity'].toString()
            ));
          }
          if (envRecs['sunlight'] != null) {
            items.add(RecommendationItem(
              label: 'Güneş Işığı', 
              value: envRecs['sunlight'].toString()
            ));
          }
          if (envRecs['rainfall'] != null) {
            items.add(RecommendationItem(
              label: 'Yağış', 
              value: envRecs['rainfall'].toString()
            ));
          }
        }
        
        // Tarım uygulamaları
        final farmingRecs = recommendations['farming_practices'] as Map<String, dynamic>?;
        if (farmingRecs != null) {
          if (farmingRecs['irrigation'] != null) {
            items.add(RecommendationItem(
              label: 'Sulama', 
              value: farmingRecs['irrigation'].toString()
            ));
          }
          if (farmingRecs['fertilizer'] != null) {
            items.add(RecommendationItem(
              label: 'Gübreleme', 
              value: farmingRecs['fertilizer'].toString()
            ));
          }
          if (farmingRecs['planting_season'] != null) {
            items.add(RecommendationItem(
              label: 'Dikim Zamanı', 
              value: farmingRecs['planting_season'].toString()
            ));
          }
          if (farmingRecs['harvest_time'] != null) {
            items.add(RecommendationItem(
              label: 'Hasat Zamanı', 
              value: farmingRecs['harvest_time'].toString()
            ));
          }
        }
        
        // Bölgesel uyarlamalar
        final regionalRecs = recommendations['regional_adaptations'] as Map<String, dynamic>?;
        if (regionalRecs != null) {
          if (regionalRecs['climate_considerations'] != null) {
            items.add(RecommendationItem(
              label: 'İklim Önerileri', 
              value: regionalRecs['climate_considerations'].toString()
            ));
          }
          if (regionalRecs['local_pests'] != null) {
            items.add(RecommendationItem(
              label: 'Zararlı Kontrolü', 
              value: regionalRecs['local_pests'].toString()
            ));
          }
          if (regionalRecs['weather_protection'] != null) {
            items.add(RecommendationItem(
              label: 'Hava Koruması', 
              value: regionalRecs['weather_protection'].toString()
            ));
          }
        }
      }
      
      notes = 'Önerilen Koşullar';
      region = 'Bölge: ${data['location']?.toString() ?? _selectedRegion}';
    } else {
      // Fallback: Ürün gereksinimlerini kullan
    final requirements = product.requirements;
      items = [
      RecommendationItem(label: 'Toprak pH', value: requirements.ph),
      RecommendationItem(label: 'Azot (ppm)', value: requirements.nitrogen),
      RecommendationItem(label: 'Fosfor (ppm)', value: requirements.phosphorus),
      RecommendationItem(label: 'Potasyum (ppm)', value: requirements.potassium),
      RecommendationItem(label: 'Nem %', value: requirements.humidity),
      RecommendationItem(label: 'Sıcaklık °C', value: requirements.temperature),
      RecommendationItem(label: 'Yağış mm', value: requirements.rainfall),
    ];
      notes = requirements.notes;
      region = 'Bölge: $_selectedRegion';
    }

    return RecommendationCard(
      title: '${product.name} için önerilen koşullar',
      items: items,
      notes: notes,
      region: region,
    );
  }
}

class RecommendationItem {
  final String label;
  final String value;

  RecommendationItem({required this.label, required this.value});
}

class RecommendationCard extends StatelessWidget {
  final String title;
  final List<RecommendationItem> items;
  final String? notes;
  final String? region;

  const RecommendationCard({
    super.key,
    required this.title,
    required this.items,
    this.notes,
    this.region,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppTheme.paddingLarge),
      decoration: BoxDecoration(
        color: Colors.blue.shade50,
        borderRadius: BorderRadius.circular(AppTheme.borderRadius),
        border: Border.all(color: Colors.blue.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Başlık
          Text(
            title,
            style: const TextStyle(
              fontSize: AppTheme.fontSizeLarge,
              fontWeight: AppTheme.fontWeightBold,
              color: Colors.blue,
            ),
          ),
          const SizedBox(height: AppTheme.paddingMedium),
          
          // Parametreler
          ...items.map((item) => Padding(
            padding: const EdgeInsets.only(bottom: AppTheme.paddingSmall),
            child: Row(
              children: [
                Expanded(
                  flex: 2,
                  child: Text(
                    item.label,
                    style: const TextStyle(
                      fontSize: AppTheme.fontSizeMedium,
                      fontWeight: AppTheme.fontWeightMedium,
                      color: Colors.blue,
                    ),
                  ),
                ),
                Expanded(
                  flex: 3,
                  child: Text(
                    item.value,
                    style: const TextStyle(
                      fontSize: AppTheme.fontSizeMedium,
                      color: AppTheme.textSecondaryColor,
                    ),
                  ),
                ),
              ],
            ),
          )).toList(),
          
          // Notlar
          if (notes != null) ...[
            const SizedBox(height: AppTheme.paddingMedium),
            Container(
              padding: const EdgeInsets.all(AppTheme.paddingMedium),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(AppTheme.borderRadius),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Notlar:',
                    style: TextStyle(
                      fontSize: AppTheme.fontSizeMedium,
                      fontWeight: AppTheme.fontWeightBold,
                      color: Colors.blue,
                    ),
                  ),
                  const SizedBox(height: AppTheme.paddingSmall),
                  Text(
                    notes!,
                    style: const TextStyle(
                      fontSize: AppTheme.fontSizeSmall,
                      color: AppTheme.textSecondaryColor,
                    ),
                  ),
                  if (region != null) ...[
                    const SizedBox(height: AppTheme.paddingSmall),
                    Text(
                      region!,
                      style: const TextStyle(
                        fontSize: AppTheme.fontSizeSmall,
                        color: AppTheme.textSecondaryColor,
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
}