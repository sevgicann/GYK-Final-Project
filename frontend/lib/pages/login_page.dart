import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/validation/validators.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_button.dart';
import '../core/utils/app_extensions.dart';
import '../services/auth_service.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _authService = AuthService();
  
  bool _isLoading = false;
  bool _obscurePassword = true;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppTheme.textPrimaryColor),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppTheme.paddingLarge),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const SizedBox(height: AppTheme.paddingXLarge),
                
                // Logo ve Marka
                _buildBrandSection(),
                
                const SizedBox(height: AppTheme.paddingXLarge * 2),
                
                // Form Alanları
                _buildFormFields(),
                
                const SizedBox(height: AppTheme.paddingXLarge),
                
                // Giriş Yap Butonu
                _buildLoginButton(),
                
                const SizedBox(height: AppTheme.paddingLarge),
                
                // Kayıt Ol Seçeneği
                _buildRegisterOption(),
                
                const SizedBox(height: AppTheme.paddingLarge),
              ],
            ),
          ),
        ),
      ),
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
              style: TextStyle(
                fontSize: AppTheme.fontSizeTitle,
                fontWeight: AppTheme.fontWeightBold,
                color: AppTheme.textPrimaryColor,
              ),
            ),
          ],
        ),
        const SizedBox(height: AppTheme.paddingSmall),
        const Text(
          'Akıllı Tarım Çözümleri',
          style: TextStyle(
            fontSize: AppTheme.fontSizeXLarge,
            fontWeight: AppTheme.fontWeightMedium,
            color: AppTheme.textSecondaryColor,
          ),
        ),
      ],
    );
  }

  Widget _buildFormFields() {
    return Column(
      children: [
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
        ),
      ],
    );
  }

  Widget _buildLoginButton() {
    return AppButton(
      text: 'Giriş Yap',
      onPressed: _handleLogin,
      isLoading: _isLoading,
      isFullWidth: true,
    );
  }

  Widget _buildRegisterOption() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Text(
          'Hesabınız yok mu? ',
          style: TextStyle(
            fontSize: AppTheme.fontSizeMedium,
            color: AppTheme.textSecondaryColor,
          ),
        ),
        GestureDetector(
          onTap: () => Navigator.of(context).pop(),
          child: const Text(
            'Kayıt Ol',
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

  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      print('🚀 Starting login process...');
      
      // Backend'e login isteği gönder
      final user = await _authService.login(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );

      print('✅ Login successful for user: ${user.name}');
      
      // Başarılı giriş sonrası ürün seçimi sayfasına yönlendir
      if (mounted) {
        context.showSnackBar('Giriş başarılı! Hoş geldin ${user.name}');
        AppRouter.navigateAndReplace(context, AppRouter.productSelection);
      }
    } catch (e) {
      print('❌ Login error: $e');
      if (mounted) {
        context.showSnackBar('Giriş yapılırken hata oluştu: $e');
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
