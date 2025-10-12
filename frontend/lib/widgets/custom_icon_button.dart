import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';

class CustomIconButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback? onPressed;
  final String? tooltip;
  final Color? color;
  final double? size;
  final bool isSelected;
  final EdgeInsetsGeometry? padding;

  const CustomIconButton({
    super.key,
    required this.icon,
    this.onPressed,
    this.tooltip,
    this.color,
    this.size,
    this.isSelected = false,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        padding: padding ?? const EdgeInsets.all(AppTheme.paddingMedium),
        decoration: BoxDecoration(
          color: isSelected ? AppTheme.primaryColor : AppTheme.surfaceColor,
          border: Border.all(
            color: isSelected ? AppTheme.primaryColor : AppTheme.primaryLightColor,
            width: 2,
          ),
          borderRadius: BorderRadius.circular(AppTheme.borderRadiusLarge),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              color: isSelected ? AppTheme.surfaceColor : AppTheme.primaryLightColor,
              size: size ?? AppTheme.iconSize,
            ),
            if (tooltip != null) ...[
              const SizedBox(height: AppTheme.paddingSmall),
              Text(
                tooltip!,
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: isSelected ? AppTheme.surfaceColor : AppTheme.primaryLightColor,
                  fontSize: AppTheme.fontSizeSmall,
                  fontWeight: AppTheme.fontWeightMedium,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
