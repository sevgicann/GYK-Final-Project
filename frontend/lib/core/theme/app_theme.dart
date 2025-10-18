import 'package:flutter/material.dart';

class AppTheme {
  // Renk Paleti
  static const Color primaryColor = Color(0xFF2E7D32);
  static const Color primaryLightColor = Color(0xFF4CAF50);
  static const Color primaryDarkColor = Color(0xFF1B5E20);
  static const Color backgroundColor = Color(0xFFF8FDF8);
  static const Color surfaceColor = Colors.white;
  static const Color cardColor = Color(0xFFE8F5E8);
  static const Color recommendationCardColor = Color(0xFFE3F2FD);
  static const Color recommendationBorderColor = Color(0xFF2196F3);
  static const Color recommendationTextColor = Color(0xFF1976D2);
  static const Color textPrimaryColor = Color(0xFF2E7D32);
  static const Color textSecondaryColor = Color(0xFF666666);
  static const Color borderColor = Color(0xFFE0E0E0);
  static const Color errorColor = Color(0xFFE53935);
  static const Color successColor = Color(0xFF4CAF50);

  // Boyutlar
  static const double borderRadius = 8.0;
  static const double borderRadiusLarge = 12.0;
  static const double borderRadiusXLarge = 25.0;
  static const double paddingSmall = 8.0;
  static const double paddingMedium = 16.0;
  static const double paddingLarge = 24.0;
  static const double paddingXLarge = 32.0;
  static const double buttonHeight = 50.0;
  static const double iconSize = 24.0;
  static const double iconSizeSmall = 16.0;

  // Font Boyutları
  static const double fontSizeXSmall = 10.0;
  static const double fontSizeSmall = 12.0;
  static const double fontSizeMedium = 14.0;
  static const double fontSizeLarge = 16.0;
  static const double fontSizeXLarge = 18.0;
  static const double fontSizeXXLarge = 24.0;
  static const double fontSizeTitle = 28.0;

  // Font Ağırlıkları
  static const FontWeight fontWeightLight = FontWeight.w400;
  static const FontWeight fontWeightMedium = FontWeight.w500;
  static const FontWeight fontWeightBold = FontWeight.w600;
  static const FontWeight fontWeightExtraBold = FontWeight.bold;

  // Gölgeler
  static List<BoxShadow> get cardShadow => [
    BoxShadow(
      color: Colors.grey.withOpacity(0.1),
      spreadRadius: 1,
      blurRadius: 10,
      offset: const Offset(0, 2),
    ),
  ];

  // Tema
  static ThemeData get lightTheme {
    return ThemeData(
      primarySwatch: Colors.green,
      primaryColor: primaryColor,
      scaffoldBackgroundColor: backgroundColor,
      fontFamily: 'Roboto',
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(
          color: textPrimaryColor,
          fontWeight: fontWeightBold,
          fontSize: fontSizeXLarge,
        ),
        iconTheme: IconThemeData(color: textPrimaryColor),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          foregroundColor: surfaceColor,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(borderRadius),
          ),
          textStyle: const TextStyle(
            fontSize: fontSizeLarge,
            fontWeight: fontWeightBold,
          ),
        ),
      ),
      splashFactory: NoSplash.splashFactory,
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surfaceColor,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(borderRadius),
          borderSide: BorderSide(color: Colors.grey.shade300),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(borderRadius),
          borderSide: BorderSide(color: Colors.grey.shade300),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(borderRadius),
          borderSide: const BorderSide(color: primaryLightColor, width: 2),
        ),
        contentPadding: const EdgeInsets.symmetric(
          horizontal: paddingMedium,
          vertical: paddingMedium,
        ),
      ),
    );
  }

  // Metin Stilleri
  static const TextStyle titleStyle = TextStyle(
    fontSize: fontSizeTitle,
    fontWeight: fontWeightExtraBold,
    color: primaryDarkColor,
  );

  static const TextStyle subtitleStyle = TextStyle(
    fontSize: fontSizeLarge,
    color: textPrimaryColor,
    fontWeight: fontWeightLight,
  );

  static const TextStyle headingStyle = TextStyle(
    fontSize: fontSizeXXLarge,
    fontWeight: fontWeightExtraBold,
    color: textPrimaryColor,
  );

  static const TextStyle bodyStyle = TextStyle(
    fontSize: fontSizeMedium,
    color: textSecondaryColor,
    height: 1.4,
  );

  static const TextStyle labelStyle = TextStyle(
    fontSize: fontSizeLarge,
    fontWeight: fontWeightMedium,
    color: textPrimaryColor,
  );

  static const TextStyle buttonStyle = TextStyle(
    fontSize: fontSizeLarge,
    fontWeight: fontWeightBold,
    color: surfaceColor,
  );

  static const TextStyle recommendationTitleStyle = TextStyle(
    fontSize: fontSizeLarge,
    fontWeight: fontWeightExtraBold,
    color: recommendationTextColor,
  );

  static const TextStyle recommendationItemStyle = TextStyle(
    fontSize: fontSizeMedium,
    color: recommendationTextColor,
    fontWeight: fontWeightMedium,
  );

  static const TextStyle recommendationValueStyle = TextStyle(
    fontSize: fontSizeMedium,
    color: recommendationTextColor,
    fontWeight: fontWeightBold,
  );
}
