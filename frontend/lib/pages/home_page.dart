import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_button.dart';
import '../core/widgets/app_card.dart';
import '../core/widgets/app_layout.dart';
import '../core/utils/app_extensions.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _currentStep = 1; // 1: Ürün, 2: Ortam
  bool _isGpsSelected = false;
  bool _isManualSelected = true;

  @override
  Widget build(BuildContext context) {
    return AppLayout(
      currentPageIndex: 0, // Home page index
      pageTitle: 'Terramind - Akıllı Tarım',
      child: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppTheme.paddingLarge),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Ana Butonlar - En Üstte
              _buildMainActionButtons(),
              
              const SizedBox(height: AppTheme.paddingXLarge),
              
              // İlerleme Çubuğu
              _buildProgressCard(),
              
              const SizedBox(height: AppTheme.paddingXLarge),
              
              // Hoş Geldiniz Mesajı
              _buildWelcomeMessage(),
              
              const SizedBox(height: AppTheme.paddingXLarge),
              
              // Konum ve İklim Bilgileri Kartı
              _buildLocationInfoCard(),
              
              const SizedBox(height: AppTheme.paddingXLarge),
              
              // Konum Seçenekleri
              _buildLocationOptions(),
              
              const SizedBox(height: AppTheme.paddingXLarge),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildProgressCard() {
    return AppProgressCard(
      title: 'İlerleme Durumu',
      currentStep: _currentStep,
      steps: const [
        AppProgressStep(title: 'Ürün Seçimi', number: 1),
        AppProgressStep(title: 'Çevre Önerileri', number: 2),
      ],
    );
  }

  Widget _buildWelcomeMessage() {
    return const Text(
      'Hoş geldiniz!',
      style: TextStyle(
        fontSize: AppTheme.fontSizeXXLarge,
        fontWeight: AppTheme.fontWeightBold,
        color: AppTheme.textPrimaryColor,
      ),
    );
  }

  Widget _buildLocationInfoCard() {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(
                Icons.info_outline,
                color: AppTheme.primaryColor,
                size: AppTheme.iconSize,
              ),
              const SizedBox(width: AppTheme.paddingSmall),
              const Text(
                'Konum ve İklim Bilgileri',
                style: TextStyle(
                  fontSize: AppTheme.fontSizeLarge,
                  fontWeight: AppTheme.fontWeightBold,
                  color: AppTheme.textPrimaryColor,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppTheme.paddingMedium),
          const Text(
            'Önerileri iyileştirmek için konumunuzu ve çevre koşullarınızı belirleyin.',
            style: TextStyle(
              fontSize: AppTheme.fontSizeMedium,
              color: AppTheme.textSecondaryColor,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLocationOptions() {
    return Row(
      children: [
        Expanded(
          child: AppButton(
            text: 'GPS Konumu',
            type: _isGpsSelected ? AppButtonType.primary : AppButtonType.outline,
            onPressed: () {
              setState(() {
                _isGpsSelected = true;
                _isManualSelected = false;
              });
              context.showSnackBar('GPS konumu seçildi');
            },
            icon: Icons.my_location,
          ),
        ),
        const SizedBox(width: AppTheme.paddingMedium),
        Expanded(
          child: AppButton(
            text: 'Manuel Seçim',
            type: _isManualSelected ? AppButtonType.primary : AppButtonType.outline,
            onPressed: () {
              setState(() {
                _isManualSelected = true;
                _isGpsSelected = false;
              });
              _showLocationDialog();
            },
            icon: Icons.location_searching,
          ),
        ),
      ],
    );
  }

  Widget _buildMainActionButtons() {
    return Column(
      children: [
        AppIconCard(
          icon: Icons.eco,
          title: 'Ürün Seçimi',
          subtitle: 'Hangi ürünü yetiştirmek istiyorsunuz?',
          onTap: () => Navigator.pushNamed(context, AppRouter.productSelection),
        ),
        const SizedBox(height: AppTheme.paddingMedium),
        AppIconCard(
          icon: Icons.location_on,
          title: 'Çevre Önerileri',
          subtitle: 'Bölgenize uygun öneriler alın',
          onTap: () => Navigator.pushNamed(context, AppRouter.environmentRecommendation),
        ),
        const SizedBox(height: AppTheme.paddingMedium),
        AppIconCard(
          icon: Icons.psychology,
          title: 'Tarım Önerisi',
          subtitle: 'Backend\'den akıllı öneriler alın',
          onTap: () => AppRouter.navigateTo(context, AppRouter.environmentRecommendation),
        ),
      ],
    );
  }

  void _showLocationDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Konum Seçin'),
        content: const Text('Lütfen konumunuzu seçin'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('İptal'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              context.showSnackBar('Konum seçildi');
            },
            child: const Text('Seç'),
          ),
        ],
      ),
    );
  }
}
