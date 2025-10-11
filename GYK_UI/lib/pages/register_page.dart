import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/validation/validators.dart';
import '../core/navigation/app_router.dart';
import '../widgets/custom_text_field.dart';
import '../widgets/custom_dropdown.dart';
import '../widgets/custom_button.dart';
import '../widgets/custom_card.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  
  String _selectedLanguage = 'Türkçe';
  bool _isLoading = false;

  final List<String> _languages = [
    'Türkçe',
    'English',
    'العربية',
    'Français',
  ];

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppTheme.paddingLarge),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const SizedBox(height: AppTheme.paddingLarge),
                
                // Dil Seçici
                _buildLanguageSelector(),
                
                const SizedBox(height: AppTheme.paddingXLarge),
                
                // Logo ve Marka
                _buildBrandSection(),
                
                const SizedBox(height: AppTheme.paddingXLarge * 2),
                
                // Form Alanları
                _buildFormFields(),
                
                const SizedBox(height: AppTheme.paddingXLarge),
                
                // Hesap Oluştur Butonu
                _buildCreateAccountButton(),
                
                const SizedBox(height: AppTheme.paddingLarge),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildLanguageSelector() {
    return CustomDropdown<String>(
      label: 'Dil Seçin',
      value: _selectedLanguage,
      items: _languages,
      onChanged: (value) {
        if (value != null) {
          setState(() {
            _selectedLanguage = value;
          });
        }
      },
    );
  }

  Widget _buildBrandSection() {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: AppTheme.iconSize,
              height: AppTheme.iconSize,
              decoration: const BoxDecoration(
                color: AppTheme.primaryLightColor,
                shape: BoxShape.circle,
              ),
              child: const Icon(
                Icons.eco,
                color: AppTheme.surfaceColor,
                size: AppTheme.iconSizeSmall,
              ),
            ),
            const SizedBox(width: AppTheme.paddingMedium),
            const Text(
              'Terramind',
              style: AppTheme.titleStyle,
            ),
          ],
        ),
        const SizedBox(height: AppTheme.paddingSmall),
        const Text(
          'Akıllı Tarım Çözümleri',
          style: AppTheme.subtitleStyle,
        ),
      ],
    );
  }

  Widget _buildFormFields() {
    return Column(
      children: [
        CustomTextField(
          label: 'Ad Soyad',
          controller: _nameController,
          validator: Validators.name,
          isRequired: true,
        ),
        const SizedBox(height: AppTheme.paddingLarge),
        CustomTextField(
          label: 'E-posta',
          controller: _emailController,
          keyboardType: TextInputType.emailAddress,
          validator: Validators.email,
          isRequired: true,
        ),
        const SizedBox(height: AppTheme.paddingLarge),
        CustomTextField(
          label: 'Şifre',
          controller: _passwordController,
          isPassword: true,
          validator: Validators.password,
          isRequired: true,
        ),
        const SizedBox(height: AppTheme.paddingLarge),
        CustomTextField(
          label: 'Şifre Tekrar',
          controller: _confirmPasswordController,
          isPassword: true,
          validator: (value) => Validators.confirmPassword(value, _passwordController.text),
          isRequired: true,
        ),
      ],
    );
  }

  Widget _buildCreateAccountButton() {
    return CustomButton(
      text: 'Hesap Oluştur',
      onPressed: _handleCreateAccount,
      isLoading: _isLoading,
      isFullWidth: true,
    );
  }

  Future<void> _handleCreateAccount() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // Simüle edilmiş API çağrısı
      await Future.delayed(const Duration(seconds: 1));
      
      // Başarılı kayıt sonrası direkt ürün seçimi sayfasına yönlendir
      if (mounted) {
        AppRouter.navigateAndReplace(context, AppRouter.productSelection);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Hesap oluşturulurken hata oluştu: $e'),
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
