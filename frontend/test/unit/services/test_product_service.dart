/**
 * Unit tests for ProductService
 * 
 * Bu test dosyası ProductService sınıfı için birim testlerini içerir.
 */

import 'package:flutter_test/flutter_test.dart';
import 'package:terramind_app/services/product_service.dart';
import 'package:terramind_app/models/product.dart';

void main() {
  group('ProductService Tests', () {
    late ProductService productService;

    setUp(() {
      productService = ProductService();
    });

    test('should return singleton instance', () {
      // Test singleton pattern
      final instance1 = ProductService();
      final instance2 = ProductService();
      
      expect(identical(instance1, instance2), isTrue);
    });

    test('should return all products', () {
      // Test getAllProducts method
      final products = productService.getAllProducts();
      
      expect(products, isA<List<Product>>());
      expect(products.length, greaterThan(0));
      
      // Verify first product has required fields
      final firstProduct = products.first;
      expect(firstProduct.id, isNotNull);
      expect(firstProduct.name, isNotEmpty);
      expect(firstProduct.category, isNotEmpty);
      expect(firstProduct.description, isNotEmpty);
      expect(firstProduct.requirements, isNotNull);
    });

    test('should return product by ID', () {
      // Test getProductById method
      final products = productService.getAllProducts();
      final firstProduct = products.first;
      
      final foundProduct = productService.getProductById(firstProduct.id);
      
      expect(foundProduct, isNotNull);
      expect(foundProduct!.id, equals(firstProduct.id));
      expect(foundProduct.name, equals(firstProduct.name));
    });

    test('should return null for non-existent product ID', () {
      // Test getProductById with non-existent ID
      final foundProduct = productService.getProductById('non-existent-id');
      
      expect(foundProduct, isNull);
    });

    test('should return product by name', () {
      // Test getProductByName method
      final products = productService.getAllProducts();
      final firstProduct = products.first;
      
      final foundProduct = productService.getProductByName(firstProduct.name);
      
      expect(foundProduct, isNotNull);
      expect(foundProduct!.name, equals(firstProduct.name));
    });

    test('should return null for non-existent product name', () {
      // Test getProductByName with non-existent name
      final foundProduct = productService.getProductByName('Non-existent Product');
      
      expect(foundProduct, isNull);
    });

    test('should return products by category', () {
      // Test getProductsByCategory method
      final allProducts = productService.getAllProducts();
      final firstCategory = allProducts.first.category;
      
      final categoryProducts = productService.getProductsByCategory(firstCategory);
      
      expect(categoryProducts, isA<List<Product>>());
      expect(categoryProducts.length, greaterThan(0));
      
      // Verify all products belong to the specified category
      for (final product in categoryProducts) {
        expect(product.category, equals(firstCategory));
      }
    });

    test('should return empty list for non-existent category', () {
      // Test getProductsByCategory with non-existent category
      final categoryProducts = productService.getProductsByCategory('Non-existent Category');
      
      expect(categoryProducts, isEmpty);
    });

    test('should return all product names', () {
      // Test getAllProductNames method
      final productNames = productService.getAllProductNames();
      
      expect(productNames, isA<List<String>>());
      expect(productNames.length, greaterThan(0));
      
      // Verify all names are non-empty strings
      for (final name in productNames) {
        expect(name, isNotEmpty);
      }
    });

    test('should return all categories', () {
      // Test getAllCategories method
      final categories = productService.getAllCategories();
      
      expect(categories, isA<List<String>>());
      expect(categories.length, greaterThan(0));
      
      // Verify all categories are non-empty strings
      for (final category in categories) {
        expect(category, isNotEmpty);
      }
      
      // Verify categories are unique
      final uniqueCategories = categories.toSet();
      expect(uniqueCategories.length, equals(categories.length));
    });

    test('should search products by name', () {
      // Test searchProducts method with name
      final products = productService.getAllProducts();
      final firstProduct = products.first;
      final searchQuery = firstProduct.name.substring(0, 3); // First 3 characters
      
      final searchResults = productService.searchProducts(searchQuery);
      
      expect(searchResults, isA<List<Product>>());
      expect(searchResults.length, greaterThan(0));
      
      // Verify search results contain the query
      final foundProduct = searchResults.any((product) => product.id == firstProduct.id);
      expect(foundProduct, isTrue);
    });

    test('should search products by category', () {
      // Test searchProducts method with category
      final products = productService.getAllProducts();
      final firstCategory = products.first.category;
      
      final searchResults = productService.searchProducts(firstCategory);
      
      expect(searchResults, isA<List<Product>>());
      expect(searchResults.length, greaterThan(0));
      
      // Verify all results belong to the searched category
      for (final product in searchResults) {
        expect(product.category, equals(firstCategory));
      }
    });

    test('should search products by description', () {
      // Test searchProducts method with description
      final products = productService.getAllProducts();
      final firstProduct = products.first;
      final searchQuery = firstProduct.description.split(' ').first; // First word
      
      final searchResults = productService.searchProducts(searchQuery);
      
      expect(searchResults, isA<List<Product>>());
      expect(searchResults.length, greaterThan(0));
      
      // Verify search results contain the query in description
      final foundProduct = searchResults.any((product) => 
          product.description.toLowerCase().contains(searchQuery.toLowerCase()));
      expect(foundProduct, isTrue);
    });

    test('should return all products for empty search query', () {
      // Test searchProducts method with empty query
      final searchResults = productService.searchProducts('');
      final allProducts = productService.getAllProducts();
      
      expect(searchResults.length, equals(allProducts.length));
    });

    test('should return empty list for non-matching search query', () {
      // Test searchProducts method with non-matching query
      final searchResults = productService.searchProducts('xyz123nonexistent');
      
      expect(searchResults, isEmpty);
    });

    test('should perform case-insensitive search', () {
      // Test case-insensitive search
      final products = productService.getAllProducts();
      final firstProduct = products.first;
      final searchQuery = firstProduct.name.toUpperCase();
      
      final searchResults = productService.searchProducts(searchQuery);
      
      expect(searchResults.length, greaterThan(0));
      
      // Verify the original product is found
      final foundProduct = searchResults.any((product) => product.id == firstProduct.id);
      expect(foundProduct, isTrue);
    });

    test('should return product count by category', () {
      // Test getProductCountByCategory method
      final allProducts = productService.getAllProducts();
      final categories = allProducts.map((p) => p.category).toSet();
      
      for (final category in categories) {
        final count = productService.getProductCountByCategory(category);
        final actualCount = allProducts.where((p) => p.category == category).length;
        
        expect(count, equals(actualCount));
      }
    });

    test('should return zero count for non-existent category', () {
      // Test getProductCountByCategory with non-existent category
      final count = productService.getProductCountByCategory('Non-existent Category');
      
      expect(count, equals(0));
    });

    test('should have valid product requirements', () {
      // Test that all products have valid requirements
      final products = productService.getAllProducts();
      
      for (final product in products) {
        expect(product.requirements, isNotNull);
        expect(product.requirements.ph, isNotEmpty);
        expect(product.requirements.nitrogen, isNotEmpty);
        expect(product.requirements.phosphorus, isNotEmpty);
        expect(product.requirements.potassium, isNotEmpty);
        expect(product.requirements.humidity, isNotEmpty);
        expect(product.requirements.temperature, isNotEmpty);
        expect(product.requirements.rainfall, isNotEmpty);
      }
    });

    test('should have unique product IDs', () {
      // Test that all products have unique IDs
      final products = productService.getAllProducts();
      final ids = products.map((p) => p.id).toList();
      final uniqueIds = ids.toSet();
      
      expect(uniqueIds.length, equals(ids.length));
    });

    test('should have unique product names', () {
      // Test that all products have unique names
      final products = productService.getAllProducts();
      final names = products.map((p) => p.name).toList();
      final uniqueNames = names.toSet();
      
      expect(uniqueNames.length, equals(names.length));
    });
  });
}
