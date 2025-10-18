import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/product.dart';

class MyProductsService {
  static const String _savedProductsKey = 'saved_products';

  /// Save a product to the saved products list
  Future<void> saveProduct(Product product) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedProductsJson = prefs.getStringList(_savedProductsKey) ?? [];
      
      // Check if product already exists
      final existingProducts = savedProductsJson
          .map((json) => Product.fromJson(jsonDecode(json)))
          .toList();
      
      if (existingProducts.any((p) => p.id == product.id)) {
        print('Product ${product.name} already exists in saved products');
        return;
      }
      
      // Add new product
      savedProductsJson.add(jsonEncode(product.toJson()));
      await prefs.setStringList(_savedProductsKey, savedProductsJson);
      
      print('Product ${product.name} saved successfully');
    } catch (e) {
      print('Error saving product: $e');
      throw Exception('Ürün kaydedilirken hata oluştu: $e');
    }
  }

  /// Get all saved products
  Future<List<Product>> getSavedProducts() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedProductsJson = prefs.getStringList(_savedProductsKey) ?? [];
      
      return savedProductsJson
          .map((json) => Product.fromJson(jsonDecode(json)))
          .toList();
    } catch (e) {
      print('Error loading saved products: $e');
      return [];
    }
  }

  /// Remove a product from saved products
  Future<void> removeProduct(String productId) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedProductsJson = prefs.getStringList(_savedProductsKey) ?? [];
      
      // Find and remove the product
      savedProductsJson.removeWhere((json) {
        try {
          final product = Product.fromJson(jsonDecode(json));
          return product.id == productId;
        } catch (e) {
          return false;
        }
      });
      
      await prefs.setStringList(_savedProductsKey, savedProductsJson);
      print('Product $productId removed successfully');
    } catch (e) {
      print('Error removing product: $e');
      throw Exception('Ürün kaldırılırken hata oluştu: $e');
    }
  }

  /// Check if a product is saved
  Future<bool> isProductSaved(String productId) async {
    try {
      final savedProducts = await getSavedProducts();
      return savedProducts.any((product) => product.id == productId);
    } catch (e) {
      print('Error checking if product is saved: $e');
      return false;
    }
  }

  /// Clear all saved products
  Future<void> clearAllProducts() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove(_savedProductsKey);
      print('All saved products cleared');
    } catch (e) {
      print('Error clearing saved products: $e');
      throw Exception('Ürünler temizlenirken hata oluştu: $e');
    }
  }
}
