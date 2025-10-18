import 'package:flutter/material.dart';
import '../utils/responsive_utils.dart';

class ResponsiveRow extends StatelessWidget {
  final List<Widget> children;
  final MainAxisAlignment mainAxisAlignment;
  final CrossAxisAlignment crossAxisAlignment;
  final double spacing;

  const ResponsiveRow({
    super.key,
    required this.children,
    this.mainAxisAlignment = MainAxisAlignment.start,
    this.crossAxisAlignment = CrossAxisAlignment.start,
    this.spacing = 8.0,
  });

  @override
  Widget build(BuildContext context) {
    if (ResponsiveUtils.isMobile(context)) {
      // Mobile: Stack vertically
      return Column(
        mainAxisAlignment: mainAxisAlignment,
        crossAxisAlignment: crossAxisAlignment,
        children: children
            .expand((child) => [child, SizedBox(height: spacing)])
            .take(children.length * 2 - 1)
            .toList(),
      );
    } else {
      // Tablet/Desktop: Horizontal row
      return Row(
        mainAxisAlignment: mainAxisAlignment,
        crossAxisAlignment: crossAxisAlignment,
        children: children
            .expand((child) => [child, SizedBox(width: spacing)])
            .take(children.length * 2 - 1)
            .toList(),
      );
    }
  }
}

class ResponsiveGrid extends StatelessWidget {
  final List<Widget> children;
  final double spacing;
  final double runSpacing;
  final int? columns;

  const ResponsiveGrid({
    super.key,
    required this.children,
    this.spacing = 8.0,
    this.runSpacing = 8.0,
    this.columns,
  });

  @override
  Widget build(BuildContext context) {
    int gridColumns;
    if (columns != null) {
      gridColumns = columns!;
    } else {
      if (ResponsiveUtils.isMobile(context)) {
        gridColumns = 1;
      } else if (ResponsiveUtils.isTablet(context)) {
        gridColumns = 2;
      } else {
        gridColumns = 3;
      }
    }
    
    return Wrap(
      spacing: spacing,
      runSpacing: runSpacing,
      children: children.map((child) {
        return SizedBox(
          width: (MediaQuery.of(context).size.width - 
                 ResponsiveUtils.getResponsivePadding(context).horizontal - 
                 spacing * (gridColumns - 1)) / gridColumns,
          child: child,
        );
      }).toList(),
    );
  }
}

class ResponsiveText extends StatelessWidget {
  final String text;
  final TextStyle? style;
  final TextAlign? textAlign;
  final int? maxLines;
  final TextOverflow? overflow;

  const ResponsiveText(
    this.text, {
    super.key,
    this.style,
    this.textAlign,
    this.maxLines,
    this.overflow,
  });

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: style,
      textAlign: textAlign,
      maxLines: maxLines,
      overflow: overflow,
    );
  }
}

class ResponsiveButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final IconData? icon;
  final Color? backgroundColor;
  final Color? textColor;
  final Color? borderColor;
  final bool isOutlined;
  final bool isLoading;
  final double? width;
  final double? height;

  const ResponsiveButton({
    super.key,
    required this.text,
    this.onPressed,
    this.icon,
    this.backgroundColor,
    this.textColor,
    this.borderColor,
    this.isOutlined = false,
    this.isLoading = false,
    this.width,
    this.height,
  });

  @override
  Widget build(BuildContext context) {
    final buttonHeight = height ?? ResponsiveUtils.getResponsiveHeight(
      context,
      mobile: 44,
      tablet: 48,
      desktop: 52,
    );
    
    final fontSize = ResponsiveUtils.getResponsiveFontSize(
      context,
      mobile: 14,
      tablet: 16,
      desktop: 18,
    );
    
    final iconSize = ResponsiveUtils.getResponsiveIconSize(context);
    
    final horizontalPadding = ResponsiveUtils.getResponsiveSpacing(
      context,
      mobile: 12,
      tablet: 16,
      desktop: 20,
    );

    return SizedBox(
      width: width ?? double.infinity,
      height: buttonHeight,
      child: ElevatedButton(
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: isOutlined ? Colors.transparent : backgroundColor,
          foregroundColor: textColor,
          side: isOutlined 
            ? BorderSide(color: borderColor ?? Colors.grey)
            : null,
          padding: EdgeInsets.symmetric(
            horizontal: horizontalPadding,
            vertical: horizontalPadding / 2,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          elevation: isOutlined ? 0 : 2,
        ),
        child: isLoading
          ? SizedBox(
              width: iconSize,
              height: iconSize,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation<Color>(
                  textColor ?? Colors.white,
                ),
              ),
            )
          : Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (icon != null) ...[
                  Icon(icon, size: iconSize),
                  SizedBox(width: horizontalPadding / 2),
                ],
                ResponsiveText(
                  text,
                  style: TextStyle(fontSize: fontSize),
                ),
              ],
            ),
      ),
    );
  }
}
