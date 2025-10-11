import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';

enum ButtonType { primary, secondary, outline, text }

class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final ButtonType type;
  final IconData? icon;
  final bool isLoading;
  final bool isFullWidth;
  final double? width;
  final double? height;
  final EdgeInsetsGeometry? padding;

  const CustomButton({
    super.key,
    required this.text,
    this.onPressed,
    this.type = ButtonType.primary,
    this.icon,
    this.isLoading = false,
    this.isFullWidth = false,
    this.width,
    this.height,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    final buttonStyle = _getButtonStyle();
    final textStyle = _getTextStyle();

    Widget buttonChild = _buildButtonChild(textStyle);

    if (isLoading) {
      buttonChild = _buildLoadingChild();
    }

    if (isFullWidth) {
      return SizedBox(
        width: double.infinity,
        height: height ?? AppTheme.buttonHeight,
        child: _buildButton(buttonStyle, buttonChild),
      );
    }

    return SizedBox(
      width: width,
      height: height ?? AppTheme.buttonHeight,
      child: _buildButton(buttonStyle, buttonChild),
    );
  }

  Widget _buildButton(ButtonStyle style, Widget child) {
    if (type == ButtonType.text) {
      return TextButton(
        onPressed: isLoading ? null : onPressed,
        style: style,
        child: child,
      );
    }

    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: style,
      child: child,
    );
  }

  Widget _buildButtonChild(TextStyle textStyle) {
    if (icon != null) {
      return Column(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: textStyle.color, size: AppTheme.iconSizeSmall),
          const SizedBox(height: 4),
          Flexible(
            child: Text(
              text,
              style: textStyle,
              textAlign: TextAlign.center,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      );
    }

    return Text(
      text,
      style: textStyle,
      textAlign: TextAlign.center,
      maxLines: 2,
      overflow: TextOverflow.ellipsis,
    );
  }

  Widget _buildLoadingChild() {
    return const SizedBox(
      width: 20,
      height: 20,
      child: CircularProgressIndicator(
        strokeWidth: 2,
        valueColor: AlwaysStoppedAnimation<Color>(AppTheme.surfaceColor),
      ),
    );
  }

  ButtonStyle _getButtonStyle() {
    switch (type) {
      case ButtonType.primary:
        return ElevatedButton.styleFrom(
          backgroundColor: AppTheme.primaryColor,
          foregroundColor: AppTheme.surfaceColor,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          ),
          elevation: 0,
          padding: padding ?? const EdgeInsets.symmetric(
            horizontal: AppTheme.paddingLarge,
            vertical: AppTheme.paddingMedium,
          ),
        );
      case ButtonType.secondary:
        return ElevatedButton.styleFrom(
          backgroundColor: AppTheme.primaryLightColor,
          foregroundColor: AppTheme.surfaceColor,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          ),
          elevation: 0,
          padding: padding ?? const EdgeInsets.symmetric(
            horizontal: AppTheme.paddingLarge,
            vertical: AppTheme.paddingMedium,
          ),
        );
      case ButtonType.outline:
        return ElevatedButton.styleFrom(
          backgroundColor: AppTheme.surfaceColor,
          foregroundColor: AppTheme.primaryColor,
          side: const BorderSide(color: AppTheme.primaryColor, width: 2),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          ),
          elevation: 0,
          padding: padding ?? const EdgeInsets.symmetric(
            horizontal: AppTheme.paddingLarge,
            vertical: AppTheme.paddingMedium,
          ),
        );
      case ButtonType.text:
        return TextButton.styleFrom(
          foregroundColor: AppTheme.primaryColor,
          padding: padding ?? const EdgeInsets.symmetric(
            horizontal: AppTheme.paddingLarge,
            vertical: AppTheme.paddingMedium,
          ),
        );
    }
  }

  TextStyle _getTextStyle() {
    switch (type) {
      case ButtonType.primary:
      case ButtonType.secondary:
        return AppTheme.buttonStyle;
      case ButtonType.outline:
        return AppTheme.buttonStyle.copyWith(color: AppTheme.primaryColor);
      case ButtonType.text:
        return AppTheme.labelStyle.copyWith(color: AppTheme.primaryColor);
    }
  }
}
