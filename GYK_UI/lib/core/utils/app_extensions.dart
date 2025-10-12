import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// String extension'ları - tek sorumluluk
extension StringExtensions on String {
  /// E-posta formatını doğrular
  bool get isValidEmail {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(this);
  }
  
  /// Şifre gücünü doğrular
  bool get isValidPassword {
    return length >= 6;
  }
  
  /// İlk harfi büyük yapar
  String get capitalize {
    if (isEmpty) return this;
    return '${this[0].toUpperCase()}${substring(1).toLowerCase()}';
  }
}

/// BuildContext extension'ları - tek sorumluluk
extension BuildContextExtensions on BuildContext {
  /// SnackBar gösterir
  void showSnackBar(String message, {Color? backgroundColor}) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: backgroundColor ?? AppTheme.primaryColor,
      ),
    );
  }
  
  /// Dialog gösterir
  Future<T?> showAppDialog<T>(Widget dialog) {
    return showDialog<T>(
      context: this,
      builder: (context) => dialog,
    );
  }
}
