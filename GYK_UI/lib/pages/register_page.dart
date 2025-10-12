import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/validation/validators.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_button.dart';
import '../core/utils/app_extensions.dart';
import '../services/auth_service.dart';

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
  bool _obscurePassword = true;
  bool _obscureConfirmPassword = true;
  
  final _authService = AuthService();

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
                
                // Giriş Yap Seçeneği
                _buildLoginOption(),
                
                const SizedBox(height: AppTheme.paddingLarge),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildLanguageSelector() {
    return DropdownButtonFormField<String>(
      initialValue: _selectedLanguage,
      decoration: const InputDecoration(
        labelText: 'Dil Seçin',
        prefixIcon: Icon(
          Icons.language,
          color: AppTheme.primaryColor,
        ),
        border: OutlineInputBorder(),
        filled: true,
        fillColor: AppTheme.surfaceColor,
      ),
      items: _languages.map((String language) {
        return DropdownMenuItem<String>(
          value: language,
          child: Text(language),
        );
      }).toList(),
      onChanged: (String? newValue) {
        if (newValue != null) {
          setState(() {
            _selectedLanguage = newValue;
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
        TextFormField(
          controller: _nameController,
          decoration: const InputDecoration(
            labelText: 'Ad Soyad',
            prefixIcon: Icon(
              Icons.person_outline,
              color: AppTheme.primaryColor,
            ),
            border: OutlineInputBorder(),
            filled: true,
            fillColor: AppTheme.surfaceColor,
          ),
          validator: Validators.name,
        ),
        const SizedBox(height: AppTheme.paddingLarge),
        TextFormField(
          controller: _emailController,
          keyboardType: TextInputType.emailAddress,
          decoration: const InputDecoration(
            labelText: 'E-posta',
            prefixIcon: Icon(
              Icons.email_outlined,
              color: AppTheme.primaryColor,
            ),
            border: OutlineInputBorder(),
            filled: true,
            fillColor: AppTheme.surfaceColor,
          ),
          validator: Validators.email,
        ),
        const SizedBox(height: AppTheme.paddingLarge),
        TextFormField(
          controller: _passwordController,
          obscureText: _obscurePassword,
          decoration: InputDecoration(
            labelText: 'Şifre',
            prefixIcon: const Icon(
              Icons.lock_outline,
              color: AppTheme.primaryColor,
            ),
            border: const OutlineInputBorder(),
            filled: true,
            fillColor: AppTheme.surfaceColor,
            suffixIcon: IconButton(
              icon: Icon(
                _obscurePassword ? Icons.visibility_off : Icons.visibility,
                color: AppTheme.textSecondaryColor,
              ),
              onPressed: () {
                setState(() {
                  _obscurePassword = !_obscurePassword;
                });
              },
            ),
          ),
          validator: Validators.password,
        ),
        const SizedBox(height: AppTheme.paddingLarge),
        TextFormField(
          controller: _confirmPasswordController,
          obscureText: _obscureConfirmPassword,
          decoration: InputDecoration(
            labelText: 'Şifre Tekrar',
            prefixIcon: const Icon(
              Icons.lock_outline,
              color: AppTheme.primaryColor,
            ),
            border: const OutlineInputBorder(),
            filled: true,
            fillColor: AppTheme.surfaceColor,
            suffixIcon: IconButton(
              icon: Icon(
                _obscureConfirmPassword ? Icons.visibility_off : Icons.visibility,
                color: AppTheme.textSecondaryColor,
              ),
              onPressed: () {
                setState(() {
                  _obscureConfirmPassword = !_obscureConfirmPassword;
                });
              },
            ),
          ),
          validator: (value) => Validators.confirmPassword(value, _passwordController.text),
        ),
      ],
    );
  }

  Widget _buildCreateAccountButton() {
    return AppButton(
      text: 'Hesap Oluştur',
      onPressed: _handleCreateAccount,
      isLoading: _isLoading,
      isFullWidth: true,
    );
  }

  Widget _buildLoginOption() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Text(
          'Zaten hesabınız var mı? ',
          style: TextStyle(
            fontSize: AppTheme.fontSizeMedium,
            color: AppTheme.textSecondaryColor,
          ),
        ),
        GestureDetector(
          onTap: () => Navigator.pushNamed(context, AppRouter.login),
          child: const Text(
            'Giriş Yap',
            style: TextStyle(
              fontSize: AppTheme.fontSizeMedium,
              color: AppTheme.primaryColor,
              fontWeight: AppTheme.fontWeightBold,
              decoration: TextDecoration.underline,
            ),
          ),
        ),
      ],
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
      print('🚀 Starting registration process...');
      
      // Backend'e register isteği gönder
      final user = await _authService.register(
        name: _nameController.text.trim(),
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );

      print('✅ Registration successful for user: ${user.name}');
      
      // Başarılı kayıt sonrası ürün seçimi sayfasına yönlendir
      if (mounted) {
        context.showSnackBar('Hesap başarıyla oluşturuldu! Hoş geldin ${user.name}');
        AppRouter.navigateAndReplace(context, AppRouter.productSelection);
      }
    } catch (e) {
      print('❌ Registration error: $e');
      if (mounted) {
        context.showSnackBar('Hesap oluşturulurken hata oluştu: $e');
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
