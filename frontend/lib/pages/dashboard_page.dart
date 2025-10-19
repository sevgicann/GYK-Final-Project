import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../core/theme/app_theme.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_button.dart';
import '../core/widgets/app_card.dart';
import '../core/widgets/app_sidebar.dart';
import '../core/language/language_service.dart';
import '../core/language/translations.dart';
import '../core/utils/responsive_utils.dart';
import '../core/widgets/responsive_widgets.dart';
import '../services/my_products_service.dart';
import '../services/my_environments_service.dart';
import '../models/product.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  int _selectedIndex = 0; // Dashboard seçili
  final LanguageService _languageService = LanguageService();
  bool _isSidebarVisible = false; // Sidebar başlangıçta kapalı
  bool _hasUnreadNotification = true; // Bildirim durumu
  
  // History için servisler
  final MyProductsService _myProductsService = MyProductsService();
  final MyEnvironmentsService _myEnvironmentsService = MyEnvironmentsService();
  List<Product> _recentProducts = [];
  List<Map<String, dynamic>> _recentEnvironments = [];
  bool _isLoadingHistory = false;

  @override
  void initState() {
    super.initState();
    _languageService.initialize().then((_) {
      // Initialize and add listener after language is loaded
      _languageService.addListener(_onLanguageChanged);
      // Trigger initial rebuild to show correct language
      if (mounted) {
        setState(() {});
      }
    });
    // Load history data
    _loadHistoryData();
    // Load notification status
    _loadNotificationStatus();
  }

  @override
  void dispose() {
    _languageService.removeListener(_onLanguageChanged);
    super.dispose();
  }

  void _onLanguageChanged() {
    if (mounted) {
      setState(() {
        // Trigger rebuild when language changes
      });
    }
  }

  // Load history data
  Future<void> _loadHistoryData() async {
    setState(() {
      _isLoadingHistory = true;
    });

    try {
      // Load recent products (last 5)
      final products = await _myProductsService.getSavedProducts();
      _recentProducts = products.take(5).toList();

      // Load recent environments (last 5)
      final environments = await _myEnvironmentsService.getSavedEnvironments();
      _recentEnvironments = environments.take(5).toList();
      
      // Test için eğer veri yoksa örnek veri ekle
      if (_recentProducts.isEmpty && _recentEnvironments.isEmpty) {
        _addSampleHistoryData();
      }
      
      print('History loaded: ${_recentProducts.length} products, ${_recentEnvironments.length} environments');
    } catch (e) {
      print('Error loading history data: $e');
      // Hata durumunda da örnek veri ekle
      _addSampleHistoryData();
    } finally {
      if (mounted) {
        setState(() {
          _isLoadingHistory = false;
        });
      }
    }
  }

  /// Bildirim durumunu SharedPreferences'dan yükle
  Future<void> _loadNotificationStatus() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final hasSeenNotification = prefs.getBool('notification_seen') ?? false;
      if (mounted) {
        setState(() {
          _hasUnreadNotification = !hasSeenNotification;
        });
      }
    } catch (e) {
      print('Error loading notification status: $e');
    }
  }

  /// Bildirim durumunu SharedPreferences'a kaydet
  Future<void> _markNotificationAsSeen() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool('notification_seen', true);
      if (mounted) {
        setState(() {
          _hasUnreadNotification = false;
        });
      }
    } catch (e) {
      print('Error saving notification status: $e');
    }
  }

  // Test için örnek veri ekle
  void _addSampleHistoryData() {
    _recentProducts = [
      Product(
        id: '1',
        name: 'Domates',
        category: 'Sebze',
        description: 'Lycopene açısından zengin sebze',
        requirements: ProductRequirements(
          ph: '6.0-7.0',
          nitrogen: '120',
          phosphorus: '60',
          potassium: '225',
          humidity: '60-80',
          temperature: '18-25',
          rainfall: '100-150',
          notes: 'Sıcak ve nemli iklim',
        ),
      ),
      Product(
        id: '2',
        name: 'Mısır',
        category: 'Tahıl',
        description: 'Yüksek verimli tahıl ürünü',
        requirements: ProductRequirements(
          ph: '5.8-7.0',
          nitrogen: '150',
          phosphorus: '80',
          potassium: '300',
          humidity: '50-70',
          temperature: '20-30',
          rainfall: '120-200',
          notes: 'Bol güneşli ve sıcak iklim',
        ),
      ),
    ];
    
    _recentEnvironments = [
      {
        'id': '1',
        'data': {
          'region': 'Ege',
          'soilType': 'Kumlu Toprak',
        },
        'createdAt': DateTime.now().toIso8601String(),
      },
      {
        'id': '2',
        'data': {
          'region': 'Akdeniz',
          'soilType': 'Tınlı Toprak',
        },
        'createdAt': DateTime.now().toIso8601String(),
      },
    ];
  }

  // Toggle sidebar visibility
  void _toggleSidebar() {
    setState(() {
      _isSidebarVisible = !_isSidebarVisible;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: Stack(
        children: [
          // Main Content Area - Always takes full width
          _buildMainContent(),
          
          // Sidebar Overlay - Only visible when _isSidebarVisible is true
          if (_isSidebarVisible) _buildSidebarOverlay(),
        ],
      ),
    );
  }

  Widget _buildSidebarOverlay() {
    return GestureDetector(
      onTap: _toggleSidebar, // Tap outside to close
      behavior: HitTestBehavior.translucent,
      child: Stack(
        children: [
          // Semi-transparent background overlay
          Container(
            color: Colors.transparent,
            width: double.infinity,
            height: double.infinity,
          ),
          
          // Sidebar positioned on the left
          Positioned(
            left: 0,
            top: 0,
            bottom: 0,
            child: GestureDetector(
              onTap: () {}, // Prevent sidebar tap from closing
              behavior: HitTestBehavior.translucent,
          child: Container(
            width: 250, // Fixed width for sidebar
            child: AppSidebar(
                  selectedIndex: _selectedIndex,
                  isVisible: _isSidebarVisible,
                  onToggle: _toggleSidebar,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMainContent() {
    return Container(
      color: const Color(0xFFF8F8F8), // Off-white background
      child: Column(
        children: [
          // Header
          _buildHeader(),
          
          // Main Content
          Expanded(
            child: Padding(
              padding: ResponsiveUtils.getResponsivePadding(context),
              child: ResponsiveUtils.isMobile(context) 
                ? _buildMobileLayout()
                : _buildDesktopLayout(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: const EdgeInsets.all(AppTheme.paddingLarge),
      decoration: const BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black12,
            blurRadius: 4,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          // Hamburger menu - Always visible
          IconButton(
            onPressed: _toggleSidebar,
            icon: const Icon(
              Icons.menu,
              color: AppTheme.textPrimaryColor,
            ),
          ),
          
          Text(
            Translations.get('dashboard', _languageService.currentLanguage),
            style: const TextStyle(
              fontSize: AppTheme.fontSizeXLarge,
              fontWeight: AppTheme.fontWeightBold,
              color: AppTheme.textPrimaryColor,
            ),
          ),
          const Spacer(),
          
          // Header Icons
          Row(
            children: [
              Stack(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: AppTheme.primaryColor,
                      shape: BoxShape.circle,
                    ),
                    child: IconButton(
                      onPressed: _showNotifications,
                      icon: const Icon(
                        Icons.notifications,
                        color: Colors.white,
                      ),
                    ),
                  ),
                  // Bildirim sayısı badge'i
                  if (_hasUnreadNotification)
                    Positioned(
                      right: 0,
                      top: 0,
                      child: Container(
                        width: 16,
                        height: 16,
                        decoration: const BoxDecoration(
                          color: Colors.red,
                          shape: BoxShape.circle,
                        ),
                        child: const Center(
                          child: Text(
                            '1',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMobileLayout() {
    return SingleChildScrollView(
      child: Column(
        children: [
          // Crop Recommendation Card
          _buildCropRecommendationCard(),
          
          SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
            context,
            mobile: 16,
            tablet: 20,
            desktop: 24,
          )),
          
          // Environment Recommendation Card
          _buildEnvironmentRecommendationCard(),
          
          SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
            context,
            mobile: 16,
            tablet: 20,
            desktop: 24,
          )),
          
          
          // History Card
          _buildHistoryCard(),
        ],
      ),
    );
  }

  Widget _buildDesktopLayout() {
    return Row(
      children: [
        // Left Side - Two Cards Stacked
        Expanded(
          flex: 2,
          child: Column(
            children: [
              // Crop Recommendation Card
              Expanded(
                child: _buildCropRecommendationCard(),
              ),
              
              SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
                context,
                mobile: 16,
                tablet: 20,
                desktop: 24,
              )),
              
              // Environment Recommendation Card
              Expanded(
                child: _buildEnvironmentRecommendationCard(),
              ),
            ],
          ),
        ),
        
        SizedBox(width: ResponsiveUtils.getResponsiveSpacing(
          context,
          mobile: 16,
          tablet: 20,
          desktop: 24,
        )),
        
        // Right Side - History Only
        Expanded(
          flex: 1,
          child: _buildHistoryCard(),
        ),
      ],
    );
  }

  Widget _buildCropRecommendationCard() {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ResponsiveText(
            Translations.get('crop_recommendation', _languageService.currentLanguage),
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
          
          // Main Content
          ResponsiveUtils.isMobile(context) 
            ? _buildMobileCropCard()
            : _buildDesktopCropCard(),
        ],
      ),
    );
  }

  Widget _buildMobileCropCard() {
    return Column(
      children: [
        // Plant Illustration
        Container(
          width: 80,
          height: 80,
          decoration: BoxDecoration(
            color: AppTheme.primaryLightColor.withOpacity(0.3),
            shape: BoxShape.circle,
          ),
          child: Icon(
            Icons.eco,
            size: 40,
            color: AppTheme.primaryColor,
          ),
        ),
        
        SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
          context,
          mobile: 12,
          tablet: 16,
          desktop: 20,
        )),
        
        // Description
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ResponsiveText(
              Translations.get('crop_description', _languageService.currentLanguage),
              style: TextStyle(
                fontSize: ResponsiveUtils.getResponsiveFontSize(
                  context,
                  mobile: 14,
                  tablet: 16,
                  desktop: 18,
                ),
                color: AppTheme.textSecondaryColor,
                height: 1.5,
              ),
            ),
            
            SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
              context,
              mobile: 12,
              tablet: 16,
              desktop: 20,
            )),
            
            // Action Button
            SizedBox(
              width: double.infinity,
              child: AppButton(
                text: Translations.get('get_recommendations', _languageService.currentLanguage),
                type: AppButtonType.primary,
                onPressed: () {
                  Navigator.pushNamed(context, AppRouter.productSelection);
                },
                icon: Icons.arrow_forward,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildDesktopCropCard() {
    return Expanded(
      child: Row(
        children: [
          // Plant Illustration
          Expanded(
            flex: 2,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: ResponsiveUtils.getResponsiveWidth(
                    context,
                    mobile: 80,
                    tablet: 100,
                    desktop: 120,
                  ),
                  height: ResponsiveUtils.getResponsiveWidth(
                    context,
                    mobile: 80,
                    tablet: 100,
                    desktop: 120,
                  ),
                  decoration: BoxDecoration(
                    color: AppTheme.primaryLightColor.withOpacity(0.3),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    Icons.eco,
                    size: ResponsiveUtils.getResponsiveIconSize(context) * 2,
                    color: AppTheme.primaryColor,
                  ),
                ),
              ],
            ),
          ),
          
          SizedBox(width: ResponsiveUtils.getResponsiveSpacing(
            context,
            mobile: 12,
            tablet: 16,
            desktop: 20,
          )),
          
          // Description
          Expanded(
            flex: 3,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ResponsiveText(
                  Translations.get('crop_description', _languageService.currentLanguage),
                  style: TextStyle(
                    fontSize: ResponsiveUtils.getResponsiveFontSize(
                      context,
                      mobile: 14,
                      tablet: 16,
                      desktop: 18,
                    ),
                    color: AppTheme.textSecondaryColor,
                    height: 1.5,
                  ),
                ),
                
                SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
                  context,
                  mobile: 12,
                  tablet: 16,
                  desktop: 20,
                )),
                
                // Action Button
                AppButton(
                  text: Translations.get('get_recommendations', _languageService.currentLanguage),
                  type: AppButtonType.primary,
                  onPressed: () {
                    Navigator.pushNamed(context, AppRouter.environmentRecommendation);
                  },
                  icon: Icons.arrow_forward,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEnvironmentRecommendationCard() {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          ResponsiveText(
            Translations.get('environment_recommendation', _languageService.currentLanguage),
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
          
          // Main Content
          ResponsiveUtils.isMobile(context) 
            ? _buildMobileEnvironmentCard()
            : _buildDesktopEnvironmentCard(),
        ],
      ),
    );
  }

  Widget _buildMobileEnvironmentCard() {
    return Column(
      children: [
        // Environment Illustration
        Container(
          width: 80,
          height: 80,
          decoration: BoxDecoration(
            color: Colors.blue.withOpacity(0.3),
            shape: BoxShape.circle,
          ),
          child: Icon(
            Icons.wb_sunny,
            size: 40,
            color: Colors.blue,
          ),
        ),
        
        SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
          context,
          mobile: 12,
          tablet: 16,
          desktop: 20,
        )),
        
        // Description
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ResponsiveText(
              Translations.get('environment_description', _languageService.currentLanguage),
              style: TextStyle(
                fontSize: ResponsiveUtils.getResponsiveFontSize(
                  context,
                  mobile: 14,
                  tablet: 16,
                  desktop: 18,
                ),
                color: AppTheme.textSecondaryColor,
                height: 1.5,
              ),
            ),
            
            SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
              context,
              mobile: 12,
              tablet: 16,
              desktop: 20,
            )),
            
            // Action Button
            SizedBox(
              width: double.infinity,
              child: AppButton(
                text: Translations.get('get_recommendations', _languageService.currentLanguage),
                type: AppButtonType.primary,
                onPressed: () {
                  Navigator.pushNamed(context, AppRouter.productSelection);
                },
                icon: Icons.arrow_forward,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildDesktopEnvironmentCard() {
    return Expanded(
      child: Row(
        children: [
          // Environment Illustration
          Expanded(
            flex: 2,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: ResponsiveUtils.getResponsiveWidth(
                    context,
                    mobile: 80,
                    tablet: 100,
                    desktop: 120,
                  ),
                  height: ResponsiveUtils.getResponsiveWidth(
                    context,
                    mobile: 80,
                    tablet: 100,
                    desktop: 120,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.blue.withOpacity(0.3),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    Icons.wb_sunny,
                    size: ResponsiveUtils.getResponsiveIconSize(context) * 2,
                    color: Colors.blue,
                  ),
                ),
              ],
            ),
          ),
          
          SizedBox(width: ResponsiveUtils.getResponsiveSpacing(
            context,
            mobile: 12,
            tablet: 16,
            desktop: 20,
          )),
          
          // Description
          Expanded(
            flex: 3,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ResponsiveText(
                  Translations.get('environment_description', _languageService.currentLanguage),
                  style: TextStyle(
                    fontSize: ResponsiveUtils.getResponsiveFontSize(
                      context,
                      mobile: 14,
                      tablet: 16,
                      desktop: 18,
                    ),
                    color: AppTheme.textSecondaryColor,
                    height: 1.5,
                  ),
                ),
                
                SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
                  context,
                  mobile: 12,
                  tablet: 16,
                  desktop: 20,
                )),
                
                // Action Button
                AppButton(
                  text: Translations.get('get_recommendations', _languageService.currentLanguage),
                  type: AppButtonType.primary,
                  onPressed: () {
                    Navigator.pushNamed(context, AppRouter.productSelection);
                  },
                  icon: Icons.arrow_forward,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }


  Widget _buildHistoryCard() {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // History Title
          Row(
            children: [
              Icon(
                Icons.history,
                color: AppTheme.primaryColor,
                size: ResponsiveUtils.getResponsiveIconSize(context),
              ),
              SizedBox(width: ResponsiveUtils.getResponsiveSpacing(
                context,
                mobile: 8,
                tablet: 12,
                desktop: 16,
              )),
              ResponsiveText(
                'History',
                style: TextStyle(
                  fontSize: ResponsiveUtils.getResponsiveFontSize(
                    context,
                    mobile: 16,
                    tablet: 18,
                    desktop: 20,
                  ),
                  fontWeight: AppTheme.fontWeightBold,
                  color: AppTheme.textPrimaryColor,
                ),
              ),
            ],
          ),
          
          SizedBox(height: ResponsiveUtils.getResponsiveSpacing(
            context,
            mobile: 12,
            tablet: 16,
            desktop: 20,
          )),
          
          // History Content
          SizedBox(
            height: 250, // Sabit yükseklik
            child: _isLoadingHistory
                ? const Center(
                    child: CircularProgressIndicator(
                      color: AppTheme.primaryColor,
                    ),
                  )
                : _buildHistoryList(),
          ),
        ],
      ),
    );
  }

  Widget _buildHistoryList() {
    final allHistory = <Map<String, dynamic>>[];
    
    // Add recent products
    for (var product in _recentProducts) {
      allHistory.add({
        'type': 'product',
        'title': product.name,
        'subtitle': product.category,
        'icon': Icons.eco,
        'color': AppTheme.primaryColor,
        'data': product,
      });
    }
    
    // Add recent environments
    for (var environment in _recentEnvironments) {
      final data = environment['data'] as Map<String, dynamic>? ?? {};
      allHistory.add({
        'type': 'environment',
        'title': 'Ortam Önerisi',
        'subtitle': '${data['region'] ?? 'Bilinmeyen'} - ${data['soilType'] ?? 'Bilinmeyen'}',
        'icon': Icons.location_on,
        'color': Colors.blue,
        'data': environment,
      });
    }
    
    // Sort by date (most recent first)
    allHistory.sort((a, b) {
      if (a['type'] == 'product' && b['type'] == 'environment') return -1;
      if (a['type'] == 'environment' && b['type'] == 'product') return 1;
      return 0; // Keep original order within same type
    });
    
    if (allHistory.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.history,
              size: 48,
              color: AppTheme.textSecondaryColor.withOpacity(0.5),
            ),
            const SizedBox(height: 16),
            Text(
              'Henüz geçmiş verisi yok',
              style: TextStyle(
                fontSize: AppTheme.fontSizeMedium,
                color: AppTheme.textSecondaryColor,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Ürün veya ortam önerisi yapın',
              style: TextStyle(
                fontSize: AppTheme.fontSizeSmall,
                color: AppTheme.textSecondaryColor.withOpacity(0.7),
              ),
            ),
          ],
        ),
      );
    }
    
    // First two cards side by side, then remaining cards in pairs
    return Column(
      children: [
        // First two cards side by side
        if (allHistory.length >= 2)
          Row(
            children: [
              Expanded(
                child: _buildVerticalHistoryItem(allHistory[0]),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _buildVerticalHistoryItem(allHistory[1]),
              ),
            ],
          ),
        
        // Remaining cards in pairs
        if (allHistory.length > 2)
          ..._buildRemainingCardsInPairs(allHistory.skip(2).toList()),
      ],
    );
  }

  List<Widget> _buildRemainingCardsInPairs(List<Map<String, dynamic>> remainingCards) {
    List<Widget> widgets = [];
    
    for (int i = 0; i < remainingCards.length; i += 2) {
      if (i + 1 < remainingCards.length) {
        // Two cards side by side
        widgets.add(
          Row(
            children: [
              Expanded(
                child: _buildVerticalHistoryItem(remainingCards[i]),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _buildVerticalHistoryItem(remainingCards[i + 1]),
              ),
            ],
          ),
        );
      } else {
        // Single card
        widgets.add(_buildVerticalHistoryItem(remainingCards[i]));
      }
    }
    
    return widgets;
  }

  Widget _buildVerticalHistoryItem(Map<String, dynamic> item) {
    return Container(
      height: 80, // Sabit yükseklik
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: item['color'].withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: item['color'].withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          // Icon
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: item['color'],
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(
              item['icon'],
              color: Colors.white,
              size: 20,
            ),
          ),
          const SizedBox(width: 12),
          // Content
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  item['title'],
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: AppTheme.fontWeightBold,
                    color: AppTheme.textPrimaryColor,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 4),
                Text(
                  item['subtitle'],
                  style: const TextStyle(
                    fontSize: 12,
                    color: AppTheme.textSecondaryColor,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
          // Arrow
          Icon(
            Icons.arrow_forward_ios,
            color: AppTheme.textSecondaryColor.withOpacity(0.5),
            size: 16,
          ),
        ],
      ),
    );
  }



  Widget _buildHistoryItem(Map<String, dynamic> item) {
    return Container(
      margin: const EdgeInsets.only(bottom: 6), // Küçültüldü
      padding: const EdgeInsets.all(8), // Küçültüldü
      decoration: BoxDecoration(
        color: item['color'].withOpacity(0.1),
        borderRadius: BorderRadius.circular(8), // Daha az yuvarlak (kareye yakın)
        border: Border.all(
          color: item['color'].withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Container(
            width: 24, // Küçültüldü
            height: 24, // Küçültüldü
            decoration: BoxDecoration(
              color: item['color'],
              borderRadius: BorderRadius.circular(4), // Daha az yuvarlak
            ),
            child: Icon(
              item['icon'],
              color: Colors.white,
              size: 14, // Küçültüldü
            ),
          ),
          const SizedBox(width: 8), // Küçültüldü
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  item['title'],
                  style: const TextStyle(
                    fontSize: 13, // Küçültüldü
                    fontWeight: AppTheme.fontWeightBold,
                    color: AppTheme.textPrimaryColor,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  item['subtitle'],
                  style: const TextStyle(
                    fontSize: 11, // Küçültüldü
                    color: AppTheme.textSecondaryColor,
                  ),
                ),
              ],
            ),
          ),
          Icon(
            Icons.arrow_forward_ios,
            size: 12, // Küçültüldü
            color: AppTheme.textSecondaryColor.withOpacity(0.5),
          ),
        ],
      ),
    );
  }

  // Navigation Methods

  // Action Methods
  void _showUserProfile() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(Translations.get('user_profile_coming_soon', _languageService.currentLanguage))),
    );
  }


  void _showNotifications() {
    // Bildirimi okundu olarak işaretle ve kalıcı olarak kaydet
    _markNotificationAsSeen();
    
    // Bildirim mesajını göster
    showDialog(
      context: context,
      barrierColor: Colors.transparent,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Row(
            children: [
              Icon(
                Icons.notifications_active,
                color: AppTheme.primaryColor,
                size: 24,
              ),
              const SizedBox(width: 8),
              const Text('Bildirim'),
            ],
          ),
          content: const Text(
            'IoT cihaz entegrasyonu yakında aktif olacak!',
            style: TextStyle(fontSize: 16),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text(
                'Tamam',
                style: TextStyle(color: AppTheme.primaryColor),
              ),
            ),
          ],
        );
      },
    );
  }



}
