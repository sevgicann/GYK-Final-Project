import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';
import '../language/language_service.dart';
import '../language/translations.dart';
import '../../services/auth_service.dart';
import '../../models/user.dart';

class AppSidebar extends StatefulWidget {
  final int selectedIndex;
  final bool isVisible;
  final VoidCallback onToggle;

  const AppSidebar({
    super.key,
    required this.selectedIndex,
    required this.isVisible,
    required this.onToggle,
  });

  @override
  State<AppSidebar> createState() => _AppSidebarState();
}

class _AppSidebarState extends State<AppSidebar> {
  final LanguageService _languageService = LanguageService();
  final AuthService _authService = AuthService();
  User? _currentUser;

  @override
  void initState() {
    super.initState();
    _languageService.initialize().then((_) {
      _languageService.addListener(_onLanguageChanged);
      if (mounted) {
        setState(() {});
      }
    });
    
    // Load current user information
    _loadCurrentUser();
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

  Future<void> _loadCurrentUser() async {
    try {
      // Get current user from AuthService
      final user = await _authService.getCurrentUser();
      if (mounted) {
        setState(() {
          _currentUser = user;
        });
      }
    } catch (e) {
      print('Error loading current user: $e');
      // If no user is logged in, redirect to login
      if (mounted) {
        AppRouter.navigateAndReplace(context, AppRouter.login);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 250,
      color: const Color(0xFFE8F5E8), // Light green
      child: Column(
        children: [
          // TerraMind Logo
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AppTheme.paddingLarge,
              vertical: AppTheme.paddingMedium,
            ),
            child: Row(
              children: [
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: AppTheme.primaryColor,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.eco,
                    color: Colors.white,
                    size: 24,
                  ),
                ),
                const SizedBox(width: AppTheme.paddingMedium),
                const Text(
                  'TerraMind',
                  style: TextStyle(
                    fontSize: AppTheme.fontSizeXLarge,
                    fontWeight: AppTheme.fontWeightBold,
                    color: AppTheme.textPrimaryColor,
                  ),
                ),
              ],
            ),
          ),
          
          // User Info in Sidebar
          Container(
            margin: const EdgeInsets.only(
              left: AppTheme.paddingMedium,
              right: AppTheme.paddingMedium,
              top: AppTheme.paddingMedium,
              bottom: AppTheme.paddingMedium,
            ),
            padding: const EdgeInsets.symmetric(
              horizontal: AppTheme.paddingSmall,
              vertical: AppTheme.paddingSmall,
            ),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.8),
              borderRadius: BorderRadius.circular(AppTheme.borderRadius),
              border: Border.all(
                color: AppTheme.borderColor.withOpacity(0.5),
                width: 0.5,
              ),
            ),
            child: Row(
              children: [
                // User Avatar
                Container(
                  width: 24,
                  height: 24,
                  decoration: BoxDecoration(
                    color: AppTheme.primaryColor,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.person,
                    color: Colors.white,
                    size: 14,
                  ),
                ),
                const SizedBox(width: AppTheme.paddingSmall),
                
                // User Details
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        _currentUser?.name ?? 'Kullanıcı',
                        style: const TextStyle(
                          fontSize: AppTheme.fontSizeXSmall,
                          fontWeight: AppTheme.fontWeightMedium,
                          color: AppTheme.textPrimaryColor,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                      Text(
                        _currentUser?.email ?? 'email@example.com',
                        style: const TextStyle(
                          fontSize: 9,
                          color: AppTheme.textSecondaryColor,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Navigation Items
          Expanded(
            child: ListView(
              padding: const EdgeInsets.symmetric(horizontal: AppTheme.paddingMedium),
              children: [
                _buildNavigationItem(
                  icon: Icons.dashboard,
                  title: Translations.get('dashboard', _languageService.currentLanguage),
                  index: 0,
                  isSelected: widget.selectedIndex == 0,
                ),
                _buildNavigationItem(
                  icon: Icons.agriculture,
                  title: Translations.get('crop', _languageService.currentLanguage),
                  index: 1,
                  isSelected: widget.selectedIndex == 1,
                ),
                _buildNavigationItem(
                  icon: Icons.public,
                  title: Translations.get('soil', _languageService.currentLanguage),
                  index: 2,
                  isSelected: widget.selectedIndex == 2,
                ),
                _buildNavigationItem(
                  icon: Icons.inventory_2,
                  title: Translations.get('my_products', _languageService.currentLanguage),
                  index: 3,
                  isSelected: widget.selectedIndex == 3,
                ),
                _buildNavigationItem(
                  icon: Icons.eco,
                  title: Translations.get('my_environments', _languageService.currentLanguage),
                  index: 4,
                  isSelected: widget.selectedIndex == 4,
                ),
                _buildNavigationItem(
                  icon: Icons.description,
                  title: Translations.get('documents', _languageService.currentLanguage),
                  index: 5,
                  isSelected: widget.selectedIndex == 5,
                ),
                _buildNavigationItem(
                  icon: Icons.shopping_cart,
                  title: Translations.get('cart', _languageService.currentLanguage),
                  index: 6,
                  isSelected: widget.selectedIndex == 6,
                ),
              ],
            ),
          ),

          // Bottom Menu Icon - Toggle Sidebar
          GestureDetector(
            onTap: widget.onToggle,
            child: Container(
              padding: const EdgeInsets.all(AppTheme.paddingLarge),
              child: Icon(
                widget.isVisible ? Icons.menu_open : Icons.menu,
                color: AppTheme.textSecondaryColor,
                size: 24,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNavigationItem({
    required IconData icon,
    required String title,
    required int index,
    required bool isSelected,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: AppTheme.paddingSmall),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => _handleNavigation(index),
          borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          child: Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AppTheme.paddingMedium,
              vertical: AppTheme.paddingLarge,
            ),
            decoration: BoxDecoration(
              color: isSelected ? AppTheme.primaryColor : Colors.transparent,
              borderRadius: BorderRadius.circular(AppTheme.borderRadius),
            ),
            child: Row(
              children: [
                Icon(
                  icon,
                  color: isSelected ? Colors.white : AppTheme.textSecondaryColor,
                  size: 20,
                ),
                const SizedBox(width: AppTheme.paddingMedium),
                Text(
                  title,
                  style: TextStyle(
                    color: isSelected ? Colors.white : AppTheme.textSecondaryColor,
                    fontSize: AppTheme.fontSizeMedium,
                    fontWeight: AppTheme.fontWeightMedium,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _handleNavigation(int index) {
    switch (index) {
      case 0: // Dashboard
        AppRouter.navigateAndReplace(context, AppRouter.dashboard);
        break;
      case 1: // Product Recommendation
        AppRouter.navigateTo(context, AppRouter.productSelection);
        break;
      case 2: // Environment Recommendation
        AppRouter.navigateTo(context, AppRouter.environmentRecommendation);
        break;
      case 3: // My Products
        _showMyProductsPlaceholder();
        break;
      case 4: // My Environments
        _showMyEnvironmentsPlaceholder();
        break;
      case 5: // Documents
        _showDocumentsPlaceholder();
        break;
      case 6: // Cart
        _showCartPlaceholder();
        break;
    }
  }

  void _showMyProductsPlaceholder() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(Translations.get('my_products', _languageService.currentLanguage)),
        content: Text(Translations.get('my_products_message', _languageService.currentLanguage)),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(Translations.get('ok', _languageService.currentLanguage)),
          ),
        ],
      ),
    );
  }

  void _showMyEnvironmentsPlaceholder() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(Translations.get('my_environments', _languageService.currentLanguage)),
        content: Text(Translations.get('my_environments_message', _languageService.currentLanguage)),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(Translations.get('ok', _languageService.currentLanguage)),
          ),
        ],
      ),
    );
  }

  void _showDocumentsPlaceholder() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(Translations.get('documents_title', _languageService.currentLanguage)),
        content: Text(Translations.get('documents_message', _languageService.currentLanguage)),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(Translations.get('ok', _languageService.currentLanguage)),
          ),
        ],
      ),
    );
  }

  void _showCartPlaceholder() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(Translations.get('cart', _languageService.currentLanguage)),
        content: Text(Translations.get('cart_message', _languageService.currentLanguage)),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(Translations.get('ok', _languageService.currentLanguage)),
          ),
        ],
      ),
    );
  }

}
