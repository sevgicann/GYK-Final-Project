import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';

class CustomTextField extends StatefulWidget {
  final String label;
  final TextEditingController? controller;
  final String? hint;
  final TextInputType? keyboardType;
  final bool isPassword;
  final bool isRequired;
  final String? Function(String?)? validator;
  final Widget? prefixIcon;
  final Widget? suffixIcon;
  final int? maxLines;
  final int? maxLength;
  final bool readOnly;
  final VoidCallback? onTap;
  final ValueChanged<String>? onChanged;
  final FocusNode? focusNode;

  const CustomTextField({
    super.key,
    required this.label,
    this.controller,
    this.hint,
    this.keyboardType,
    this.isPassword = false,
    this.isRequired = false,
    this.validator,
    this.prefixIcon,
    this.suffixIcon,
    this.maxLines = 1,
    this.maxLength,
    this.readOnly = false,
    this.onTap,
    this.onChanged,
    this.focusNode,
  });

  @override
  State<CustomTextField> createState() => _CustomTextFieldState();
}

class _CustomTextFieldState extends State<CustomTextField> {
  bool _isPasswordVisible = false;
  late FocusNode _focusNode;

  @override
  void initState() {
    super.initState();
    _focusNode = widget.focusNode ?? FocusNode();
  }

  @override
  void dispose() {
    if (widget.focusNode == null) {
      _focusNode.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildLabel(),
        const SizedBox(height: AppTheme.paddingSmall),
        _buildTextField(),
      ],
    );
  }

  Widget _buildLabel() {
    return Text(
      widget.isRequired ? '${widget.label} *' : widget.label,
      style: AppTheme.labelStyle,
    );
  }

  Widget _buildTextField() {
    return TextFormField(
      controller: widget.controller,
      focusNode: _focusNode,
      keyboardType: widget.keyboardType,
      obscureText: widget.isPassword ? !_isPasswordVisible : false,
      validator: widget.validator,
      maxLines: widget.maxLines,
      maxLength: widget.maxLength,
      readOnly: widget.readOnly,
      onTap: widget.onTap,
      onChanged: widget.onChanged,
      decoration: InputDecoration(
        hintText: widget.hint,
        prefixIcon: widget.prefixIcon,
        suffixIcon: _buildSuffixIcon(),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          borderSide: BorderSide(color: Colors.grey.shade300),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          borderSide: BorderSide(color: Colors.grey.shade300),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          borderSide: const BorderSide(color: AppTheme.primaryLightColor, width: 2),
        ),
        errorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          borderSide: const BorderSide(color: AppTheme.errorColor),
        ),
        focusedErrorBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          borderSide: const BorderSide(color: AppTheme.errorColor, width: 2),
        ),
        filled: true,
        fillColor: AppTheme.surfaceColor,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: AppTheme.paddingMedium,
          vertical: AppTheme.paddingMedium,
        ),
      ),
    );
  }

  Widget? _buildSuffixIcon() {
    if (widget.suffixIcon != null) {
      return widget.suffixIcon;
    }

    if (widget.isPassword) {
      return IconButton(
        icon: Icon(
          _isPasswordVisible ? Icons.visibility : Icons.visibility_off,
          color: Colors.grey,
        ),
        onPressed: () {
          setState(() {
            _isPasswordVisible = !_isPasswordVisible;
          });
        },
      );
    }

    return null;
  }
}

class CustomSearchField extends StatefulWidget {
  final String hint;
  final ValueChanged<String>? onChanged;
  final VoidCallback? onSearch;
  final TextEditingController? controller;
  final Widget? prefixIcon;

  const CustomSearchField({
    super.key,
    this.hint = 'Ara...',
    this.onChanged,
    this.onSearch,
    this.controller,
    this.prefixIcon,
  });

  @override
  State<CustomSearchField> createState() => _CustomSearchFieldState();
}

class _CustomSearchFieldState extends State<CustomSearchField> {
  late TextEditingController _controller;
  bool _hasText = false;

  @override
  void initState() {
    super.initState();
    _controller = widget.controller ?? TextEditingController();
    _controller.addListener(_onTextChanged);
  }

  @override
  void dispose() {
    if (widget.controller == null) {
      _controller.dispose();
    } else {
      _controller.removeListener(_onTextChanged);
    }
    super.dispose();
  }

  void _onTextChanged() {
    setState(() {
      _hasText = _controller.text.isNotEmpty;
    });
    widget.onChanged?.call(_controller.text);
  }

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: _controller,
      onSubmitted: (_) => widget.onSearch?.call(),
      decoration: InputDecoration(
        hintText: widget.hint,
        prefixIcon: widget.prefixIcon ?? const Icon(Icons.search),
        suffixIcon: _hasText
            ? IconButton(
                icon: const Icon(Icons.clear),
                onPressed: () {
                  _controller.clear();
                },
              )
            : null,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          borderSide: BorderSide(color: Colors.grey.shade300),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          borderSide: BorderSide(color: Colors.grey.shade300),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(AppTheme.borderRadius),
          borderSide: const BorderSide(color: AppTheme.primaryLightColor, width: 2),
        ),
        filled: true,
        fillColor: AppTheme.surfaceColor,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: AppTheme.paddingMedium,
          vertical: AppTheme.paddingMedium,
        ),
      ),
    );
  }
}
