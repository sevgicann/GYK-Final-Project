import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/navigation/app_router.dart';
import '../models/product.dart';
import '../services/product_service.dart';
import '../services/image_service.dart';
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

  Product? _selectedProduct;
  String? _selectedCity;
  String? _selectedRegion;
  bool _isGpsSelected = false;
  bool _isManualSelected = false;
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppTheme.textPrimaryColor),
          onPressed: () => AppRouter.goBack(context),
        ),
        title: const Text(
          'Ürün Seçiminden Ortam Koşulları Önerisi',
          style: TextStyle(
            color: AppTheme.textPrimaryColor,
            fontWeight: AppTheme.fontWeightBold,
            fontSize: AppTheme.fontSizeLarge,
          ),
        ),
        centerTitle: true,
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
      ),
      body: SafeArea(
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
          onChanged: (value) {
            if (value != null) {
              setState(() {
                _selectedProduct = _productService.getProductByName(value);
              });
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
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(AppTheme.paddingMedium),
        decoration: BoxDecoration(
          color: isSelected ? AppTheme.primaryColor : AppTheme.surfaceColor,
          border: Border.all(
            color: isSelected ? AppTheme.primaryColor : AppTheme.primaryLightColor,
            width: 2,
          ),
          borderRadius: BorderRadius.circular(AppTheme.borderRadiusLarge),
        ),
        child: Column(
          children: [
            Icon(
              icon,
              color: isSelected ? AppTheme.surfaceColor : AppTheme.primaryLightColor,
              size: AppTheme.iconSize,
            ),
            const SizedBox(height: AppTheme.paddingSmall),
            Text(
              title,
              textAlign: TextAlign.center,
              style: TextStyle(
                color: isSelected ? AppTheme.surfaceColor : AppTheme.primaryLightColor,
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
      text: 'Öneri Al',
      icon: Icons.lightbulb_outline,
      onPressed: canGetRecommendation ? _handleGetRecommendation : null,
      isLoading: _isLoading,
      isFullWidth: true,
    );
  }

  void _handleGpsLocation() {
    // GPS konumu simülasyonu
    setState(() {
      _isLoading = true;
    });

    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        setState(() {
          _selectedCity = 'İstanbul'; // Simüle edilmiş GPS konumu
          _selectedRegion = TurkishCities.getRegionByCity(_selectedCity!);
          _isLoading = false;
        });
      }
    });
  }

  void _showCitySelectionDialog() {
    showDialog(
      context: context,
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
                  onTap: () {
                    setState(() {
                      _selectedCity = city;
                      _selectedRegion = TurkishCities.getRegionByCity(city);
                    });
                    Navigator.of(context).pop();
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
      // Simüle edilmiş API çağrısı
      await Future.delayed(const Duration(seconds: 1));
      
      // Direkt çevre önerilerini göster
      if (mounted) {
        _showEnvironmentRecommendations();
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

  void _showEnvironmentRecommendations() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildRecommendationsBottomSheet(),
    );
  }

  Widget _buildRecommendationsBottomSheet() {
    return Container(
      height: MediaQuery.of(context).size.height * 0.8,
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
              child: _buildRecommendationsContent(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRecommendationsContent() {
    if (_selectedProduct == null) return const SizedBox.shrink();

    final product = _selectedProduct!;
    final requirements = product.requirements;

    final items = [
      RecommendationItem(label: 'Toprak pH', value: requirements.ph),
      RecommendationItem(label: 'Azot (ppm)', value: requirements.nitrogen),
      RecommendationItem(label: 'Fosfor (ppm)', value: requirements.phosphorus),
      RecommendationItem(label: 'Potasyum (ppm)', value: requirements.potassium),
      RecommendationItem(label: 'Nem %', value: requirements.humidity),
      RecommendationItem(label: 'Sıcaklık °C', value: requirements.temperature),
      RecommendationItem(label: 'Yağış mm', value: requirements.rainfall),
    ];

    return RecommendationCard(
      title: '${product.name} için önerilen koşullar',
      items: items,
      notes: requirements.notes,
      region: 'Bölge: $_selectedRegion',
    );
  }
}
