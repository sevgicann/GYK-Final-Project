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
  bool _isSidebarVisible = false; // Sidebar başlangıçta kapalı

  void _toggleSidebar() {
    setState(() {
      _isSidebarVisible = !_isSidebarVisible;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Main Content Area - Always takes full width
          _buildMainContent(),
          
          // Sidebar Overlay - Only visible when _isSidebarVisible is true
          if (_isSidebarVisible) _buildSidebarOverlay(),
        ],
      ),
    );
  }

  Widget _buildMainContent() {
    return Column(
      children: [
        // Header (if pageTitle is provided)
        if (widget.pageTitle != null) _buildHeader(),
        
        // Content
        Expanded(child: widget.child),
      ],
    );
  }

  Widget _buildSidebarOverlay() {
    return GestureDetector(
      onTap: _toggleSidebar, // Tap outside to close
      behavior: HitTestBehavior.translucent,
      child: Stack(
        children: [
          // Semi-transparent background overlay
          Container(
            color: Colors.transparent,
            width: double.infinity,
            height: double.infinity,
          ),
          
          // Sidebar positioned on the left
          Positioned(
            left: 0,
            top: 0,
            bottom: 0,
            child: GestureDetector(
              onTap: () {}, // Prevent sidebar tap from closing
              behavior: HitTestBehavior.translucent,
              child: Container(
                width: 250, // Fixed width for sidebar
                child: AppSidebar(
                  selectedIndex: widget.currentPageIndex,
                  isVisible: _isSidebarVisible,
                  onToggle: _toggleSidebar,
                ),
              ),
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
          // Hamburger menu - Always visible
          IconButton(
            onPressed: _toggleSidebar,
            icon: const Icon(Icons.menu),
          ),

          // Page Title
          Expanded(
            child: Text(
              widget.pageTitle!,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.black87,
              ),
              overflow: TextOverflow.ellipsis,
            ),
          ),

          // Actions
          if (widget.actions != null) ...widget.actions!,
        ],
      ),
    );
  }
}
