import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';

class CustomCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry? padding;
  final EdgeInsetsGeometry? margin;
  final Color? backgroundColor;
  final List<BoxShadow>? boxShadow;
  final BorderRadius? borderRadius;
  final Border? border;
  final VoidCallback? onTap;

  const CustomCard({
    super.key,
    required this.child,
    this.padding,
    this.margin,
    this.backgroundColor,
    this.boxShadow,
    this.borderRadius,
    this.border,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    Widget card = Container(
      padding: padding ?? const EdgeInsets.all(AppTheme.paddingLarge),
      margin: margin,
      decoration: BoxDecoration(
        color: backgroundColor ?? AppTheme.surfaceColor,
        borderRadius: borderRadius ?? BorderRadius.circular(AppTheme.borderRadiusLarge),
        boxShadow: boxShadow ?? AppTheme.cardShadow,
        border: border,
      ),
      child: child,
    );

    if (onTap != null) {
      return InkWell(
        onTap: onTap,
        borderRadius: borderRadius ?? BorderRadius.circular(AppTheme.borderRadiusLarge),
        splashFactory: NoSplash.splashFactory,
        child: card,
      );
    }

    return card;
  }
}

class InfoCard extends StatelessWidget {
  final String title;
  final String description;
  final IconData? icon;
  final Color? iconColor;
  final Color? backgroundColor;
  final VoidCallback? onTap;
  final Widget? child;

  const InfoCard({
    super.key,
    required this.title,
    required this.description,
    this.icon,
    this.iconColor,
    this.backgroundColor,
    this.onTap,
    this.child,
  });

  @override
  Widget build(BuildContext context) {
    return CustomCard(
      backgroundColor: backgroundColor,
      onTap: onTap,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              if (icon != null) ...[
                Container(
                  width: AppTheme.iconSize,
                  height: AppTheme.iconSize,
                  decoration: BoxDecoration(
                    color: iconColor ?? AppTheme.primaryLightColor,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    icon,
                    color: AppTheme.surfaceColor,
                    size: AppTheme.iconSizeSmall,
                  ),
                ),
                const SizedBox(width: AppTheme.paddingMedium),
              ],
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(
                    fontSize: AppTheme.fontSizeXLarge,
                    fontWeight: AppTheme.fontWeightExtraBold,
                    color: AppTheme.textPrimaryColor,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppTheme.paddingMedium),
          Text(
            description,
            style: AppTheme.bodyStyle,
          ),
          if (child != null) ...[
            const SizedBox(height: AppTheme.paddingMedium),
            child!,
          ],
        ],
      ),
    );
  }
}

class RecommendationCard extends StatelessWidget {
  final String title;
  final List<RecommendationItem> items;
  final String? notes;
  final String? region;
  final Color? backgroundColor;
  final Color? borderColor;
  final Color? textColor;

  const RecommendationCard({
    super.key,
    required this.title,
    required this.items,
    this.notes,
    this.region,
    this.backgroundColor,
    this.borderColor,
    this.textColor,
  });

  @override
  Widget build(BuildContext context) {
    final bgColor = backgroundColor ?? AppTheme.recommendationCardColor;
    final borderCol = borderColor ?? AppTheme.recommendationBorderColor;
    final txtColor = textColor ?? AppTheme.recommendationTextColor;

    return CustomCard(
      backgroundColor: bgColor,
      border: Border.all(color: borderCol, width: 1),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: TextStyle(
              fontSize: AppTheme.fontSizeLarge,
              fontWeight: AppTheme.fontWeightExtraBold,
              color: txtColor,
            ),
          ),
          const SizedBox(height: AppTheme.paddingMedium),
          
          ...items.map((item) => _buildRecommendationItem(item, txtColor)),
          
          if (notes != null || region != null) ...[
            const SizedBox(height: AppTheme.paddingMedium),
            _buildNotesSection(notes, region, txtColor),
          ],
        ],
      ),
    );
  }

  Widget _buildRecommendationItem(RecommendationItem item, Color textColor) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppTheme.paddingSmall),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            '${item.label}:',
            style: TextStyle(
              fontSize: AppTheme.fontSizeMedium,
              color: textColor,
              fontWeight: AppTheme.fontWeightMedium,
            ),
          ),
          Text(
            item.value,
            style: TextStyle(
              fontSize: AppTheme.fontSizeMedium,
              color: textColor,
              fontWeight: AppTheme.fontWeightBold,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNotesSection(String? notes, String? region, Color textColor) {
    return Container(
      padding: const EdgeInsets.all(AppTheme.paddingMedium),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor.withOpacity(0.7),
        borderRadius: BorderRadius.circular(AppTheme.borderRadius),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (notes != null) ...[
            const Text(
              'Notlar:',
              style: TextStyle(
                fontWeight: AppTheme.fontWeightBold,
                color: AppTheme.recommendationTextColor,
              ),
            ),
            const SizedBox(height: AppTheme.paddingSmall),
            Text(
              notes,
              style: TextStyle(
                color: textColor,
                fontSize: AppTheme.fontSizeMedium,
              ),
            ),
          ],
          if (region != null) ...[
            if (notes != null) const SizedBox(height: AppTheme.paddingSmall),
            Text(
              'Bölge: $region',
              style: TextStyle(
                color: textColor,
                fontSize: AppTheme.fontSizeMedium,
                fontWeight: AppTheme.fontWeightMedium,
              ),
            ),
          ],
        ],
      ),
    );
  }
}

class RecommendationItem {
  final String label;
  final String value;

  const RecommendationItem({
    required this.label,
    required this.value,
  });
}

class ProgressCard extends StatelessWidget {
  final String title;
  final int currentStep;
  final int totalSteps;
  final List<String> stepLabels;
  final Color? activeColor;
  final Color? inactiveColor;

  const ProgressCard({
    super.key,
    required this.title,
    required this.currentStep,
    required this.totalSteps,
    required this.stepLabels,
    this.activeColor,
    this.inactiveColor,
  });

  @override
  Widget build(BuildContext context) {
    final activeCol = activeColor ?? AppTheme.primaryLightColor;
    final inactiveCol = inactiveColor ?? Colors.grey.shade300;

    return CustomCard(
      backgroundColor: AppTheme.cardColor,
      child: Column(
        children: [
          Text(
            title,
            style: const TextStyle(
              fontSize: AppTheme.fontSizeLarge,
              fontWeight: AppTheme.fontWeightBold,
              color: AppTheme.textPrimaryColor,
            ),
          ),
          const SizedBox(height: AppTheme.paddingLarge),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: _buildProgressSteps(activeCol, inactiveCol),
          ),
        ],
      ),
    );
  }

  List<Widget> _buildProgressSteps(Color activeColor, Color inactiveColor) {
    final steps = <Widget>[];
    
    for (int i = 0; i < totalSteps; i++) {
      final isActive = i < currentStep;
      final isCurrent = i == currentStep - 1;
      
      steps.add(_buildProgressStep(
        stepLabels[i],
        i + 1,
        isActive,
        isCurrent,
        activeColor,
        inactiveColor,
      ));
      
      if (i < totalSteps - 1) {
        steps.add(const SizedBox(width: AppTheme.paddingLarge));
        steps.add(Container(
          width: 30,
          height: 2,
          color: activeColor,
        ));
        steps.add(const SizedBox(width: AppTheme.paddingLarge));
      }
    }
    
    return steps;
  }

  Widget _buildProgressStep(
    String label,
    int stepNumber,
    bool isActive,
    bool isCurrent,
    Color activeColor,
    Color inactiveColor,
  ) {
    return Row(
      children: [
        Container(
          width: AppTheme.iconSize,
          height: AppTheme.iconSize,
          decoration: BoxDecoration(
            color: isActive ? activeColor : inactiveColor,
            shape: BoxShape.circle,
          ),
          child: Center(
            child: Text(
              stepNumber.toString(),
              style: TextStyle(
                color: isActive ? AppTheme.surfaceColor : Colors.grey.shade600,
                fontSize: AppTheme.fontSizeSmall,
                fontWeight: AppTheme.fontWeightBold,
              ),
            ),
          ),
        ),
        const SizedBox(width: AppTheme.paddingSmall),
        Text(
          label,
          style: TextStyle(
            color: isActive ? AppTheme.textPrimaryColor : Colors.grey.shade600,
            fontWeight: AppTheme.fontWeightMedium,
            fontSize: AppTheme.fontSizeMedium,
          ),
        ),
      ],
    );
  }
}
