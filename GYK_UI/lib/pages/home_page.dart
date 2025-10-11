import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/navigation/app_router.dart';
import '../widgets/custom_button.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_icon_button.dart';

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
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text(
          'Terramind - Akıllı Tarım',
          style: TextStyle(
            color: AppTheme.textPrimaryColor,
            fontWeight: AppTheme.fontWeightBold,
            fontSize: AppTheme.fontSizeXLarge,
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Padding(
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
              
              const Spacer(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildProgressCard() {
    return ProgressCard(
      title: '',
      currentStep: _currentStep,
      totalSteps: 2,
      stepLabels: const ['Ürün', 'Ortam'],
    );
  }

  Widget _buildWelcomeMessage() {
    return const Text(
      'Hoş geldiniz!',
      style: AppTheme.headingStyle,
    );
  }

  Widget _buildLocationInfoCard() {
    return InfoCard(
      title: 'Konum ve İklim Bilgileri',
      description: 'Önerileri iyileştirmek için konumunuzu ve çevre koşullarınızı belirleyin.',
      icon: Icons.check,
      iconColor: AppTheme.primaryLightColor,
    );
  }

  Widget _buildLocationOptions() {
    return Row(
      children: [
        Expanded(
          child: CustomIconButton(
            icon: Icons.gps_fixed,
            tooltip: 'GPS Konumunu Kullan',
            isSelected: _isGpsSelected,
            onPressed: () {
              setState(() {
                _isGpsSelected = true;
                _isManualSelected = false;
              });
              _showLocationDialog('GPS');
            },
          ),
        ),
        const SizedBox(width: AppTheme.paddingMedium),
        Expanded(
          child: CustomIconButton(
            icon: Icons.location_city,
            tooltip: 'Şehri Manuel Seç',
            isSelected: _isManualSelected,
            onPressed: () {
              setState(() {
                _isGpsSelected = false;
                _isManualSelected = true;
              });
              _showLocationDialog('Manuel');
            },
          ),
        ),
      ],
    );
  }

  Widget _buildMainActionButtons() {
    return Row(
      children: [
        // Ürün → Ortam Önerisi Butonu (Büyük ve Varsayılan)
        Expanded(
          flex: 2,
          child: CustomButton(
            text: 'Ürün → Ortam\nÖnerisi',
            icon: Icons.lightbulb_outline,
            onPressed: () {
              AppRouter.navigateTo(context, AppRouter.productSelection);
            },
            isFullWidth: true,
            height: 90,
          ),
        ),
        
        const SizedBox(width: AppTheme.paddingMedium),
        
        // Ortam → Ürün Önerisi Butonu (Ters Yön)
        Expanded(
          flex: 2,
          child: CustomButton(
            text: 'Ortam → Ürün\nÖnerisi',
            icon: Icons.search,
            onPressed: () {
              AppRouter.navigateTo(context, AppRouter.environmentRecommendation);
            },
            isFullWidth: true,
            height: 90,
            type: ButtonType.outline,
          ),
        ),
      ],
    );
  }

  void _showLocationDialog(String type) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('${type == 'GPS' ? 'GPS' : 'Manuel'} Konum Seçimi'),
          content: Text(
            type == 'GPS' 
                ? 'GPS konumunuz alınıyor...' 
                : 'Şehir seçimi için lütfen bekleyiniz.',
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Tamam'),
            ),
          ],
        );
      },
    );
  }
}
