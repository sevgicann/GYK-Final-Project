import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';

class CustomDropdown<T> extends StatelessWidget {
  final String label;
  final T? value;
  final List<T> items;
  final ValueChanged<T?>? onChanged;
  final String Function(T)? itemBuilder;
  final Widget? prefixIcon;
  final String? hint;
  final bool isRequired;
  final String? errorText;

  const CustomDropdown({
    super.key,
    required this.label,
    required this.value,
    required this.items,
    this.onChanged,
    this.itemBuilder,
    this.prefixIcon,
    this.hint,
    this.isRequired = false,
    this.errorText,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildLabel(),
        const SizedBox(height: AppTheme.paddingSmall),
        _buildDropdown(),
        if (errorText != null) ...[
          const SizedBox(height: AppTheme.paddingSmall),
          _buildErrorText(),
        ],
      ],
    );
  }

  Widget _buildLabel() {
    return Text(
      isRequired ? '$label *' : label,
      style: AppTheme.labelStyle,
    );
  }

  Widget _buildDropdown() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(
        horizontal: AppTheme.paddingMedium,
        vertical: AppTheme.paddingSmall,
      ),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        border: Border.all(
          color: errorText != null ? AppTheme.errorColor : Colors.grey.shade300,
        ),
        borderRadius: BorderRadius.circular(AppTheme.borderRadius),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<T>(
          value: value,
          isExpanded: true,
          icon: const Icon(Icons.keyboard_arrow_down, color: Colors.grey),
          hint: hint != null ? Text(hint!) : null,
          items: items.map((T item) {
            return DropdownMenuItem<T>(
              value: item,
              child: _buildDropdownItem(item),
            );
          }).toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }

  Widget _buildDropdownItem(T item) {
    if (itemBuilder != null) {
      return Text(itemBuilder!(item));
    }

    if (item is String) {
      return _buildStringItem(item as String);
    }

    return Text(item.toString());
  }

  Widget _buildStringItem(String item) {
    // Özel durumlar için ikon ekleme
    Widget? icon;
    if (item == 'Türkçe') {
      icon = const Icon(Icons.flag, color: Colors.red, size: 20);
    }

    if (icon != null) {
      return Row(
        children: [
          icon,
          const SizedBox(width: AppTheme.paddingSmall),
          Text(item),
        ],
      );
    }

    return Text(item);
  }

  Widget _buildErrorText() {
    return Text(
      errorText!,
      style: const TextStyle(
        color: AppTheme.errorColor,
        fontSize: AppTheme.fontSizeSmall,
      ),
    );
  }
}

class CustomSearchableDropdown<T> extends StatefulWidget {
  final String label;
  final T? value;
  final List<T> items;
  final ValueChanged<T?>? onChanged;
  final String Function(T)? itemBuilder;
  final String Function(T)? searchBuilder;
  final Widget? prefixIcon;
  final String? hint;
  final bool isRequired;
  final String? errorText;

  const CustomSearchableDropdown({
    super.key,
    required this.label,
    required this.value,
    required this.items,
    this.onChanged,
    this.itemBuilder,
    this.searchBuilder,
    this.prefixIcon,
    this.hint,
    this.isRequired = false,
    this.errorText,
  });

  @override
  State<CustomSearchableDropdown<T>> createState() => _CustomSearchableDropdownState<T>();
}

class _CustomSearchableDropdownState<T> extends State<CustomSearchableDropdown<T>> {
  final TextEditingController _searchController = TextEditingController();
  List<T> _filteredItems = [];
  bool _isExpanded = false;

  @override
  void initState() {
    super.initState();
    _filteredItems = widget.items;
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildLabel(),
        const SizedBox(height: AppTheme.paddingSmall),
        _buildDropdown(),
        if (widget.errorText != null) ...[
          const SizedBox(height: AppTheme.paddingSmall),
          _buildErrorText(),
        ],
      ],
    );
  }

  Widget _buildLabel() {
    return Text(
      widget.isRequired ? '${widget.label} *' : widget.label,
      style: AppTheme.labelStyle,
    );
  }

  Widget _buildDropdown() {
    return Container(
      decoration: BoxDecoration(
        border: Border.all(
          color: widget.errorText != null ? AppTheme.errorColor : Colors.grey.shade300,
        ),
        borderRadius: BorderRadius.circular(AppTheme.borderRadius),
      ),
      child: Column(
        children: [
          _buildDropdownHeader(),
          if (_isExpanded) _buildDropdownContent(),
        ],
      ),
    );
  }

  Widget _buildDropdownHeader() {
    return InkWell(
      onTap: () {
        setState(() {
          _isExpanded = !_isExpanded;
        });
      },
      splashFactory: NoSplash.splashFactory,
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(
          horizontal: AppTheme.paddingMedium,
          vertical: AppTheme.paddingMedium,
        ),
        child: Row(
          children: [
            if (widget.prefixIcon != null) ...[
              widget.prefixIcon!,
              const SizedBox(width: AppTheme.paddingSmall),
            ],
            Expanded(
              child: Text(
                widget.value != null
                    ? (widget.itemBuilder?.call(widget.value!) ?? widget.value.toString())
                    : (widget.hint ?? 'Seçiniz'),
                style: TextStyle(
                  color: widget.value != null ? Colors.black : Colors.grey,
                  fontSize: AppTheme.fontSizeMedium,
                ),
              ),
            ),
            Icon(
              _isExpanded ? Icons.keyboard_arrow_up : Icons.keyboard_arrow_down,
              color: Colors.grey,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDropdownContent() {
    return Container(
      constraints: const BoxConstraints(maxHeight: 200),
      child: Column(
        children: [
          _buildSearchField(),
          Expanded(
            child: ListView.builder(
              shrinkWrap: true,
              itemCount: _filteredItems.length,
              itemBuilder: (context, index) {
                final item = _filteredItems[index];
                final isSelected = item == widget.value;
                
                return InkWell(
                  onTap: () {
                    widget.onChanged?.call(item);
                    setState(() {
                      _isExpanded = false;
                    });
                  },
                  splashFactory: NoSplash.splashFactory,
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppTheme.paddingMedium,
                      vertical: AppTheme.paddingMedium,
                    ),
                    decoration: BoxDecoration(
                      color: isSelected ? AppTheme.cardColor : Colors.transparent,
                    ),
                    child: Row(
                      children: [
                        if (isSelected)
                          const Icon(
                            Icons.check,
                            color: AppTheme.primaryColor,
                            size: 20,
                          ),
                        if (isSelected) const SizedBox(width: AppTheme.paddingSmall),
                        Expanded(
                          child: Text(
                            widget.itemBuilder?.call(item) ?? item.toString(),
                            style: TextStyle(
                              color: isSelected ? AppTheme.primaryColor : Colors.black,
                              fontWeight: isSelected ? AppTheme.fontWeightBold : AppTheme.fontWeightLight,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchField() {
    return Container(
      padding: const EdgeInsets.all(AppTheme.paddingSmall),
      child: TextField(
        controller: _searchController,
        decoration: const InputDecoration(
          hintText: 'Ara...',
          prefixIcon: Icon(Icons.search),
          border: OutlineInputBorder(),
          contentPadding: EdgeInsets.symmetric(
            horizontal: AppTheme.paddingMedium,
            vertical: AppTheme.paddingSmall,
          ),
        ),
        onChanged: _filterItems,
      ),
    );
  }

  Widget _buildErrorText() {
    return Text(
      widget.errorText!,
      style: const TextStyle(
        color: AppTheme.errorColor,
        fontSize: AppTheme.fontSizeSmall,
      ),
    );
  }

  void _filterItems(String query) {
    setState(() {
      if (query.isEmpty) {
        _filteredItems = widget.items;
      } else {
        _filteredItems = widget.items.where((item) {
          final searchText = widget.searchBuilder?.call(item) ?? 
                           widget.itemBuilder?.call(item) ?? 
                           item.toString();
          return searchText.toLowerCase().contains(query.toLowerCase());
        }).toList();
      }
    });
  }
}
