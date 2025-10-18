import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Optimize edilmiş kart widget'ı - SOLID prensiplerine uygun
class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry? padding;
  final EdgeInsetsGeometry? margin;
  final double? elevation;
  final Color? backgroundColor;
  final BorderRadius? borderRadius;
  final VoidCallback? onTap;

  const AppCard({
    super.key,
    required this.child,
    this.padding,
    this.margin,
    this.elevation,
    this.backgroundColor,
    this.borderRadius,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final card = Card(
      elevation: elevation ?? 2.0,
      color: backgroundColor ?? AppTheme.surfaceColor,
      shape: RoundedRectangleBorder(
        borderRadius: borderRadius ?? BorderRadius.circular(AppTheme.borderRadius),
      ),
      child: Padding(
        padding: padding ?? const EdgeInsets.all(AppTheme.paddingMedium),
        child: child,
      ),
    );

    if (onTap != null) {
      return InkWell(
        onTap: onTap,
        borderRadius: borderRadius ?? BorderRadius.circular(AppTheme.borderRadius),
        splashFactory: NoSplash.splashFactory,
        child: card,
      );
    }

    if (margin != null) {
      return Container(margin: margin, child: card);
    }

    return card;
  }
}

/// İkonlu kart widget'ı - kompozisyon prensibi
class AppIconCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? subtitle;
  final VoidCallback? onTap;
  final Color? iconColor;
  final Color? backgroundColor;

  const AppIconCard({
    super.key,
    required this.icon,
    required this.title,
    this.subtitle,
    this.onTap,
    this.iconColor,
    this.backgroundColor,
  });

  @override
  Widget build(BuildContext context) {
    return AppCard(
      onTap: onTap,
      backgroundColor: backgroundColor,
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(AppTheme.paddingMedium),
            decoration: BoxDecoration(
              color: (iconColor ?? AppTheme.primaryColor).withOpacity(0.1),
              borderRadius: BorderRadius.circular(AppTheme.borderRadius),
            ),
            child: Icon(
              icon,
              color: iconColor ?? AppTheme.primaryColor,
              size: AppTheme.iconSize,
            ),
          ),
          const SizedBox(width: AppTheme.paddingMedium),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: AppTheme.fontSizeMedium,
                    fontWeight: AppTheme.fontWeightBold,
                    color: AppTheme.textPrimaryColor,
                  ),
                ),
                if (subtitle != null) ...[
                  const SizedBox(height: 4.0),
                  Text(
                    subtitle!,
                    style: const TextStyle(
                      fontSize: AppTheme.fontSizeSmall,
                      color: AppTheme.textSecondaryColor,
                    ),
                  ),
                ],
              ],
            ),
          ),
          if (onTap != null)
            const Icon(
              Icons.arrow_forward_ios,
              color: AppTheme.textSecondaryColor,
              size: 16.0,
            ),
        ],
      ),
    );
  }
}

/// İlerleme kartı widget'ı - tek sorumluluk
class AppProgressCard extends StatelessWidget {
  final String title;
  final List<AppProgressStep> steps;
  final int currentStep;

  const AppProgressCard({
    super.key,
    required this.title,
    required this.steps,
    this.currentStep = 0,
  });

  @override
  Widget build(BuildContext context) {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontSize: AppTheme.fontSizeLarge,
              fontWeight: AppTheme.fontWeightBold,
              color: AppTheme.textPrimaryColor,
            ),
          ),
          const SizedBox(height: AppTheme.paddingMedium),
          ...steps.asMap().entries.map((entry) {
            final index = entry.key;
            final step = entry.value;
            final isCompleted = index < currentStep;
            final isCurrent = index == currentStep;
            
            return Padding(
              padding: const EdgeInsets.only(bottom: AppTheme.paddingSmall),
              child: _buildProgressStep(step, isCompleted, isCurrent),
            );
          }),
        ],
      ),
    );
  }

  /// Tek ilerleme adımı - tek sorumluluk
  Widget _buildProgressStep(AppProgressStep step, bool isCompleted, bool isCurrent) {
    return Row(
      children: [
        Container(
          width: 24.0,
          height: 24.0,
          decoration: BoxDecoration(
            color: isCompleted 
                ? AppTheme.primaryColor 
                : isCurrent 
                    ? AppTheme.primaryColor.withOpacity(0.5)
                    : AppTheme.textSecondaryColor,
            shape: BoxShape.circle,
          ),
          child: Center(
            child: isCompleted
                ? const Icon(
                    Icons.check,
                    color: Colors.white,
                    size: 16.0,
                  )
                : Text(
                    (step.number ?? (isCurrent ? '?' : '')).toString(),
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: AppTheme.fontSizeSmall,
                      fontWeight: AppTheme.fontWeightBold,
                    ),
                  ),
          ),
        ),
        const SizedBox(width: AppTheme.paddingMedium),
        Expanded(
          child: Text(
            step.title,
            style: TextStyle(
              fontSize: AppTheme.fontSizeMedium,
              color: isCompleted 
                  ? AppTheme.primaryColor 
                  : AppTheme.textSecondaryColor,
              fontWeight: isCompleted 
                  ? AppTheme.fontWeightBold 
                  : AppTheme.fontWeightLight,
            ),
          ),
        ),
      ],
    );
  }
}

/// İlerleme adımı modeli - tek sorumluluk
class AppProgressStep {
  final String title;
  final int? number;

  const AppProgressStep({
    required this.title,
    this.number,
  });
}
