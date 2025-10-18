import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';
import '../core/navigation/app_router.dart';
import '../core/widgets/app_layout.dart';
import '../models/product.dart';
import '../services/product_service.dart';
import '../services/image_service.dart';
import '../services/my_products_service.dart';
import '../widgets/custom_card.dart';

class MyProductsPage extends StatefulWidget {
  const MyProductsPage({super.key});

  @override
  State<MyProductsPage> createState() => _MyProductsPageState();
}

class _MyProductsPageState extends State<MyProductsPage> {
  final ProductService _productService = ProductService();
  final ImageService _imageService = ImageService();
  final MyProductsService _myProductsService = MyProductsService();
  
  List<Product> _savedProducts = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadSavedProducts();
  }

  Future<void> _loadSavedProducts() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final products = await _myProductsService.getSavedProducts();
      setState(() {
        _savedProducts = products;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      print('Error loading saved products: $e');
    }
  }

  Future<void> _removeProduct(Product product) async {
    try {
      await _myProductsService.removeProduct(product.id);
      setState(() {
        _savedProducts.removeWhere((p) => p.id == product.id);
      });
      
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            '${product.name} ürünlerimden kaldırıldı',
            style: const TextStyle(color: Colors.white),
          ),
          backgroundColor: AppTheme.primaryColor,
          duration: const Duration(seconds: 2),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Ürün kaldırılırken hata oluştu: $e'),
          backgroundColor: AppTheme.errorColor,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return AppLayout(
      currentPageIndex: 3, // My Products index
      pageTitle: 'Ürünlerim',
      child: SafeArea(
        child: Column(
          children: [
            // Header with Add Product Button
            Container(
              padding: const EdgeInsets.all(AppTheme.paddingLarge),
              child: Row(
                children: [
                  Expanded(
                    child: Text(
                      'Kayıtlı Ürünlerim',
                      style: const TextStyle(
                        fontSize: AppTheme.fontSizeXLarge,
                        fontWeight: AppTheme.fontWeightBold,
                        color: AppTheme.textPrimaryColor,
                      ),
                    ),
                  ),
                  ElevatedButton.icon(
                    onPressed: () {
                      AppRouter.navigateTo(context, AppRouter.environmentRecommendation);
                    },
                    icon: const Icon(Icons.add, size: 18),
                    label: const Text('Yeni Ürün Ekle'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.primaryColor,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(AppTheme.borderRadius),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            
            // Content
            Expanded(
              child: _isLoading
                  ? const Center(
                      child: CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation<Color>(AppTheme.primaryColor),
                      ),
                    )
                  : _savedProducts.isEmpty
                      ? _buildEmptyState()
                      : _buildProductsList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.inventory_2_outlined,
            size: 80,
            color: AppTheme.textSecondaryColor.withOpacity(0.5),
          ),
          const SizedBox(height: AppTheme.paddingLarge),
          Text(
            'Henüz kayıtlı ürününüz yok',
            style: TextStyle(
              fontSize: AppTheme.fontSizeLarge,
              fontWeight: AppTheme.fontWeightMedium,
              color: AppTheme.textSecondaryColor,
            ),
          ),
          const SizedBox(height: AppTheme.paddingSmall),
          Text(
            'Ortam koşullarından ürün önerisi alarak\nürünlerinizi buraya ekleyebilirsiniz',
            textAlign: TextAlign.center,
            style: AppTheme.bodyStyle.copyWith(
              color: AppTheme.textSecondaryColor,
            ),
          ),
          const SizedBox(height: AppTheme.paddingXLarge),
          ElevatedButton.icon(
            onPressed: () {
              AppRouter.navigateTo(context, AppRouter.environmentRecommendation);
            },
            icon: const Icon(Icons.add),
            label: const Text('Ürün Ekle'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryColor,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(
                horizontal: AppTheme.paddingXLarge,
                vertical: AppTheme.paddingMedium,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProductsList() {
    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: AppTheme.paddingLarge),
      itemCount: _savedProducts.length,
      itemBuilder: (context, index) {
        final product = _savedProducts[index];
        return Padding(
          padding: const EdgeInsets.only(bottom: AppTheme.paddingLarge),
          child: _buildProductCard(product),
        );
      },
    );
  }

  Widget _buildProductCard(Product product) {
    return CustomCard(
      child: Row(
        children: [
          // Product Image
          ClipRRect(
            borderRadius: BorderRadius.circular(AppTheme.borderRadius),
            child: Image.network(
              _imageService.getProductImage(product.name),
              width: 80,
              height: 80,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) => Container(
                width: 80,
                height: 80,
                color: AppTheme.primaryLightColor.withOpacity(0.2),
                child: const Icon(Icons.broken_image, color: AppTheme.textSecondaryColor),
              ),
            ),
          ),
          const SizedBox(width: AppTheme.paddingLarge),
          
          // Product Details
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  product.name,
                  style: const TextStyle(
                    fontSize: AppTheme.fontSizeXLarge,
                    fontWeight: AppTheme.fontWeightBold,
                    color: AppTheme.textPrimaryColor,
                  ),
                ),
                const SizedBox(height: AppTheme.paddingSmall),
                Text(
                  product.category,
                  style: AppTheme.bodyStyle.copyWith(color: AppTheme.textSecondaryColor),
                ),
                const SizedBox(height: AppTheme.paddingSmall),
                Text(
                  product.description,
                  style: AppTheme.bodyStyle,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: AppTheme.paddingSmall),
                Row(
                  children: [
                    Icon(
                      Icons.calendar_today,
                      size: 14,
                      color: AppTheme.textSecondaryColor,
                    ),
                    const SizedBox(width: AppTheme.paddingSmall),
                    Text(
                      'Eklendi: ${_formatDate(DateTime.now())}',
                      style: AppTheme.bodyStyle.copyWith(
                        color: AppTheme.textSecondaryColor,
                        fontSize: AppTheme.fontSizeSmall,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          
          // Remove Button
          const SizedBox(width: AppTheme.paddingMedium),
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: AppTheme.errorColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: IconButton(
              onPressed: () => _removeProduct(product),
              icon: const Icon(
                Icons.delete_outline,
                color: AppTheme.errorColor,
                size: 20,
              ),
              padding: EdgeInsets.zero,
            ),
          ),
        ],
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }
}
