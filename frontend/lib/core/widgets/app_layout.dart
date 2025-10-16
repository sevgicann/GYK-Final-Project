import 'package:flutter/material.dart';
import 'app_sidebar.dart';

class AppLayout extends StatefulWidget {
  final Widget child;
  final int currentPageIndex;
  final String? pageTitle;
  final List<Widget>? actions;

  const AppLayout({
    super.key,
    required this.child,
    required this.currentPageIndex,
    this.pageTitle,
    this.actions,
  });

  @override
  State<AppLayout> createState() => _AppLayoutState();
}

class _AppLayoutState extends State<AppLayout> {
  bool _isSidebarVisible = true;

  void _toggleSidebar() {
    setState(() {
      _isSidebarVisible = !_isSidebarVisible;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          // Left Sidebar - Conditional rendering
          if (_isSidebarVisible) AppSidebar(
            selectedIndex: widget.currentPageIndex,
            isVisible: _isSidebarVisible,
            onToggle: _toggleSidebar,
          ),

          // Main Content Area
          Expanded(
            child: Column(
              children: [
                // Header (if pageTitle is provided)
                if (widget.pageTitle != null) _buildHeader(),
                
                // Content
                Expanded(child: widget.child),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          // Hamburger menu for mobile/collapsed sidebar
          if (!_isSidebarVisible)
            IconButton(
              onPressed: _toggleSidebar,
              icon: const Icon(Icons.menu),
            ),

          // Page Title
          Text(
            widget.pageTitle!,
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.black87,
            ),
          ),
          
          const Spacer(),

          // Actions
          if (widget.actions != null) ...widget.actions!,
        ],
      ),
    );
  }
}
