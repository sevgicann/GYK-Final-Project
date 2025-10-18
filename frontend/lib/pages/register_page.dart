import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/validation/validators.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_button.dart';
import '../core/utils/app_extensions.dart';
import '../services/auth_service.dart';
import '../core/language/language_service.dart';
import '../core/language/translations.dart';

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
  final _languageService = LanguageService();

  final List<String> _languages = [
    'Türkçe',
    'English',
    'العربية',
    'Français',
  ];

  @override
  void initState() {
    super.initState();
    _languageService.initialize().then((_) {
      _languageService.addListener(_onLanguageChanged);
      // Load current language and set the dropdown value
      setState(() {
        _selectedLanguage = _languageService.currentLanguageDisplayName;
      });
    });
  }

  @override
  void dispose() {
    _languageService.removeListener(_onLanguageChanged);
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  void _onLanguageChanged() {
    if (mounted) {
      setState(() {
        // Trigger rebuild when language changes
      });
    }
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
      decoration: InputDecoration(
        labelText: Translations.get('select_language', _languageService.currentLanguage),
        prefixIcon: const Icon(
          Icons.language,
          color: AppTheme.primaryColor,
        ),
        border: const OutlineInputBorder(),
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
          // Save language preference
          _languageService.setLanguageFromDisplayName(newValue);
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
        Text(
          Translations.get('smart_agriculture_solutions', _languageService.currentLanguage),
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
          decoration: InputDecoration(
            labelText: Translations.get('full_name', _languageService.currentLanguage),
            prefixIcon: const Icon(
              Icons.person_outline,
              color: AppTheme.primaryColor,
            ),
            border: const OutlineInputBorder(),
            filled: true,
            fillColor: AppTheme.surfaceColor,
          ),
          validator: Validators.name,
        ),
        const SizedBox(height: AppTheme.paddingLarge),
        TextFormField(
          controller: _emailController,
          keyboardType: TextInputType.emailAddress,
          decoration: InputDecoration(
            labelText: Translations.get('email', _languageService.currentLanguage),
            prefixIcon: const Icon(
              Icons.email_outlined,
              color: AppTheme.primaryColor,
            ),
            border: const OutlineInputBorder(),
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
            labelText: Translations.get('password', _languageService.currentLanguage),
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
            labelText: Translations.get('confirm_password', _languageService.currentLanguage),
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
      text: Translations.get('register_button', _languageService.currentLanguage),
      onPressed: _handleCreateAccount,
      isLoading: _isLoading,
      isFullWidth: true,
    );
  }

  Widget _buildLoginOption() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          Translations.get('already_have_account', _languageService.currentLanguage),
          style: const TextStyle(
            fontSize: AppTheme.fontSizeMedium,
            color: AppTheme.textSecondaryColor,
          ),
        ),
        GestureDetector(
          onTap: () => Navigator.pushNamed(context, AppRouter.login),
          child: Text(
            Translations.get('login', _languageService.currentLanguage),
            style: const TextStyle(
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
        context.showSnackBar(Translations.get('register_success', _languageService.currentLanguage));
        AppRouter.navigateAndReplace(context, AppRouter.productSelection);
      }
    } catch (e) {
      print('❌ Registration error: $e');
      if (mounted) {
        context.showSnackBar('${Translations.get('register_error', _languageService.currentLanguage)} $e');
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
