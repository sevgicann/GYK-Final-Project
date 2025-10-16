import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_button.dart';
import '../core/widgets/app_card.dart';
import '../core/widgets/app_sidebar.dart';
import '../core/language/language_service.dart';
import '../core/language/translations.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  int _selectedIndex = 0; // Dashboard seçili
  final LanguageService _languageService = LanguageService();
  bool _isSidebarVisible = true; // Sidebar görünürlük durumu

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
      body: Row(
        children: [
          // Left Sidebar - Conditional rendering
          if (_isSidebarVisible) AppSidebar(
          selectedIndex: _selectedIndex,
          isVisible: _isSidebarVisible,
          onToggle: _toggleSidebar,
        ),
          
          // Main Content Area
          Expanded(
            child: _buildMainContent(),
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
              padding: const EdgeInsets.all(AppTheme.paddingXLarge),
              child: Row(
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
                        
                        const SizedBox(height: AppTheme.paddingLarge),
                        
                        // Environment Recommendation Card
                        Expanded(
                          child: _buildEnvironmentRecommendationCard(),
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(width: AppTheme.paddingLarge),
                  
                  // Right Side - Weather and Documents
                  Expanded(
                    flex: 1,
                    child: Column(
                      children: [
                        // Weather Card
                        Expanded(
                          child: _buildWeatherCard(),
                        ),
                        
                        const SizedBox(height: AppTheme.paddingLarge),
                        
                        // Documents Card
                        Expanded(
                          child: _buildDocumentsCard(),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
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
          // Hamburger menu for mobile/collapsed sidebar
          if (!_isSidebarVisible)
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
              Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: AppTheme.primaryColor,
                  shape: BoxShape.circle,
                ),
                child: IconButton(
                  onPressed: () => _showNotifications(),
                  icon: const Icon(
                    Icons.notifications,
                    color: Colors.white,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildCropRecommendationCard() {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            Translations.get('crop_recommendation', _languageService.currentLanguage),
            style: const TextStyle(
              fontSize: AppTheme.fontSizeXLarge,
              fontWeight: AppTheme.fontWeightBold,
              color: AppTheme.textPrimaryColor,
            ),
          ),
          
          const SizedBox(height: AppTheme.paddingLarge),
          
          // Main Content
          Expanded(
            child: Row(
              children: [
                // Plant Illustration
                Expanded(
                  flex: 2,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        width: 120,
                        height: 120,
                        decoration: BoxDecoration(
                          color: AppTheme.primaryLightColor.withOpacity(0.3),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(
                          Icons.eco,
                          size: 60,
                          color: AppTheme.primaryColor,
                        ),
                      ),
                    ],
                  ),
                ),
                
                const SizedBox(width: AppTheme.paddingLarge),
                
                // Description
                Expanded(
                  flex: 3,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        Translations.get('crop_description', _languageService.currentLanguage),
                        style: const TextStyle(
                          fontSize: AppTheme.fontSizeMedium,
                          color: AppTheme.textSecondaryColor,
                          height: 1.5,
                        ),
                      ),
                      
                      const SizedBox(height: AppTheme.paddingLarge),
                      
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
          Text(
            Translations.get('environment_recommendation', _languageService.currentLanguage),
            style: const TextStyle(
              fontSize: AppTheme.fontSizeXLarge,
              fontWeight: AppTheme.fontWeightBold,
              color: AppTheme.textPrimaryColor,
            ),
          ),
          
          const SizedBox(height: AppTheme.paddingLarge),
          
          // Main Content
          Expanded(
            child: Row(
              children: [
                // Environment Illustration
                Expanded(
                  flex: 2,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        width: 120,
                        height: 120,
                        decoration: BoxDecoration(
                          color: Colors.blue.withOpacity(0.3),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(
                          Icons.wb_sunny,
                          size: 60,
                          color: Colors.blue,
                        ),
                      ),
                    ],
                  ),
                ),
                
                const SizedBox(width: AppTheme.paddingLarge),
                
                // Description
                Expanded(
                  flex: 3,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        Translations.get('environment_description', _languageService.currentLanguage),
                        style: const TextStyle(
                          fontSize: AppTheme.fontSizeMedium,
                          color: AppTheme.textSecondaryColor,
                          height: 1.5,
                        ),
                      ),
                      
                      const SizedBox(height: AppTheme.paddingLarge),
                      
                      // Action Button
                      AppButton(
                        text: Translations.get('analyze_environment', _languageService.currentLanguage),
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
          ),
        ],
      ),
    );
  }

  Widget _buildWeatherCard() {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            Translations.get('weather', _languageService.currentLanguage),
            style: const TextStyle(
              fontSize: AppTheme.fontSizeLarge,
              fontWeight: AppTheme.fontWeightBold,
              color: AppTheme.textPrimaryColor,
            ),
          ),
          
          const SizedBox(height: AppTheme.paddingLarge),
          
          // Temperature
          Row(
            children: [
              const Text(
                '20°',
                style: TextStyle(
                  fontSize: 48,
                  fontWeight: AppTheme.fontWeightBold,
                  color: AppTheme.textPrimaryColor,
                ),
              ),
              const SizedBox(width: AppTheme.paddingMedium),
              const Icon(
                Icons.wb_sunny,
                size: 40,
                color: Colors.orange,
              ),
            ],
          ),
          
          const SizedBox(height: AppTheme.paddingMedium),
          
          Text(
            Translations.get('light_rain', _languageService.currentLanguage),
            style: const TextStyle(
              fontSize: AppTheme.fontSizeMedium,
              color: AppTheme.textSecondaryColor,
            ),
          ),
          
          const Text(
            '15° / 22°',
            style: TextStyle(
              fontSize: AppTheme.fontSizeSmall,
              color: AppTheme.textSecondaryColor,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDocumentsCard() {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            Translations.get('documents', _languageService.currentLanguage),
            style: const TextStyle(
              fontSize: AppTheme.fontSizeLarge,
              fontWeight: AppTheme.fontWeightBold,
              color: AppTheme.textPrimaryColor,
            ),
          ),
          
          const SizedBox(height: AppTheme.paddingLarge),
          
          // Document Icon and Lines
          Row(
            children: [
              Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: AppTheme.primaryColor,
                  borderRadius: BorderRadius.circular(AppTheme.borderRadius),
                ),
                child: const Icon(
                  Icons.description,
                  color: Colors.white,
                  size: 24,
                ),
              ),
              
              const SizedBox(width: AppTheme.paddingMedium),
              
              // Document Lines
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      height: 4,
                      width: double.infinity,
                      color: AppTheme.primaryLightColor.withOpacity(0.5),
                      margin: const EdgeInsets.only(bottom: 4),
                    ),
                    Container(
                      height: 4,
                      width: double.infinity * 0.8,
                      color: AppTheme.primaryLightColor.withOpacity(0.5),
                      margin: const EdgeInsets.only(bottom: 4),
                    ),
                    Container(
                      height: 4,
                      width: double.infinity * 0.6,
                      color: AppTheme.primaryLightColor.withOpacity(0.5),
                    ),
                  ],
                ),
              ),
            ],
          ),
          
          const SizedBox(height: AppTheme.paddingLarge),
          
          Text(
            Translations.get('documentation_coming_soon', _languageService.currentLanguage),
            style: const TextStyle(
              fontSize: AppTheme.fontSizeSmall,
              color: AppTheme.textSecondaryColor,
              fontStyle: FontStyle.italic,
            ),
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
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(Translations.get('no_notifications', _languageService.currentLanguage))),
    );
  }



}
