/**
 * Unit tests for Product model
 * 
 * Bu test dosyası Product modeli için birim testlerini içerir.
 */

import 'package:flutter_test/flutter_test.dart';
import 'package:terramind_app/models/product.dart';

void main() {
  group('Product Model Tests', () {
    test('should create product with required fields', () {
      // Test product creation with required fields
      const product = Product(
        id: '1',
        name: 'Test Product',
        category: 'Test Category',
        description: 'Test Description',
        requirements: ProductRequirements(
          ph: '6.0-7.0',
          nitrogen: '100-150',
          phosphorus: '40-60',
          potassium: '120-200',
          humidity: '60-80',
          temperature: '20-25',
          rainfall: '500-800',
          notes: 'Test notes',
        ),
      );

      // Verify product properties
      expect(product.id, equals('1'));
      expect(product.name, equals('Test Product'));
      expect(product.category, equals('Test Category'));
      expect(product.description, equals('Test Description'));
      expect(product.requirements, isNotNull);
    });

    test('should create product requirements with all fields', () {
      // Test ProductRequirements creation
      const requirements = ProductRequirements(
        ph: '6.0-7.0',
        nitrogen: '100-150',
        phosphorus: '40-60',
        potassium: '120-200',
        humidity: '60-80',
        temperature: '20-25',
        rainfall: '500-800',
        notes: 'Test requirements notes',
      );

      // Verify requirements properties
      expect(requirements.ph, equals('6.0-7.0'));
      expect(requirements.nitrogen, equals('100-150'));
      expect(requirements.phosphorus, equals('40-60'));
      expect(requirements.potassium, equals('120-200'));
      expect(requirements.humidity, equals('60-80'));
      expect(requirements.temperature, equals('20-25'));
      expect(requirements.rainfall, equals('500-800'));
      expect(requirements.notes, equals('Test requirements notes'));
    });

    test('should create product with optional fields', () {
      // Test product creation with optional fields
      const product = Product(
        id: '2',
        name: 'Optional Product',
        category: 'Optional Category',
        description: 'Optional Description',
        imageUrl: 'https://example.com/image.jpg',
        requirements: ProductRequirements(
          ph: '5.5-6.5',
          nitrogen: '80-120',
          phosphorus: '30-50',
          potassium: '100-180',
          humidity: '50-70',
          temperature: '18-28',
          rainfall: '400-1000',
          notes: 'Optional notes',
        ),
      );

      // Verify product properties
      expect(product.id, equals('2'));
      expect(product.name, equals('Optional Product'));
      expect(product.category, equals('Optional Category'));
      expect(product.description, equals('Optional Description'));
      expect(product.imageUrl, equals('https://example.com/image.jpg'));
    });

    test('should handle empty notes in requirements', () {
      // Test ProductRequirements with empty notes
      const requirements = ProductRequirements(
        ph: '6.0-7.0',
        nitrogen: '100-150',
        phosphorus: '40-60',
        potassium: '120-200',
        humidity: '60-80',
        temperature: '20-25',
        rainfall: '500-800',
        notes: '',
      );

      // Verify empty notes are handled
      expect(requirements.notes, equals(''));
    });

    test('should handle null imageUrl', () {
      // Test product with null imageUrl
      const product = Product(
        id: '3',
        name: 'No Image Product',
        category: 'No Image Category',
        description: 'No Image Description',
        imageUrl: null,
        requirements: ProductRequirements(
          ph: '6.0-7.0',
          nitrogen: '100-150',
          phosphorus: '40-60',
          potassium: '120-200',
          humidity: '60-80',
          temperature: '20-25',
          rainfall: '500-800',
          notes: 'No image notes',
        ),
      );

      // Verify null imageUrl is handled
      expect(product.imageUrl, isNull);
    });

    test('should create product with extreme values', () {
      // Test product with extreme values
      const product = Product(
        id: '4',
        name: 'Extreme Product',
        category: 'Extreme Category',
        description: 'Extreme Description with very long text that might cause issues',
        imageUrl: 'https://very-long-url.com/very-long-path/image.jpg',
        requirements: ProductRequirements(
          ph: '0.0-14.0',
          nitrogen: '0-1000',
          phosphorus: '0-1000',
          potassium: '0-1000',
          humidity: '0-100',
          temperature: '-50-100',
          rainfall: '0-5000',
          notes: 'Extreme notes with very long text that might cause issues in the application',
        ),
      );

      // Verify extreme values are handled
      expect(product.name, equals('Extreme Product'));
      expect(product.description.length, greaterThan(50));
      expect(product.imageUrl!.length, greaterThan(50));
      expect(product.requirements.notes.length, greaterThan(50));
    });

    test('should handle special characters in text fields', () {
      // Test product with special characters
      const product = Product(
        id: '5',
        name: 'Özel Karakterli Ürün',
        category: 'Kategori & Klasör',
        description: 'Açıklama: "Özel karakterler" & semboller!',
        requirements: ProductRequirements(
          ph: '6.0-7.0',
          nitrogen: '100-150',
          phosphorus: '40-60',
          potassium: '120-200',
          humidity: '60-80',
          temperature: '20-25',
          rainfall: '500-800',
          notes: 'Notlar: Türkçe karakterler (ç, ğ, ı, ö, ş, ü)',
        ),
      );

      // Verify special characters are handled
      expect(product.name, contains('Özel'));
      expect(product.category, contains('&'));
      expect(product.description, contains('"'));
      expect(product.requirements.notes, contains('ç'));
    });

    test('should maintain immutability', () {
      // Test that Product is immutable
      const product = Product(
        id: '6',
        name: 'Immutable Product',
        category: 'Immutable Category',
        description: 'Immutable Description',
        requirements: ProductRequirements(
          ph: '6.0-7.0',
          nitrogen: '100-150',
          phosphorus: '40-60',
          potassium: '120-200',
          humidity: '60-80',
          temperature: '20-25',
          rainfall: '500-800',
          notes: 'Immutable notes',
        ),
      );

      // Verify product is immutable (compile-time check)
      expect(product.id, equals('6'));
      expect(product.name, equals('Immutable Product'));
    });

    test('should handle numeric ranges in requirements', () {
      // Test various numeric range formats
      const requirements = ProductRequirements(
        ph: '6.0-7.0',
        nitrogen: '100-150',
        phosphorus: '40-60',
        potassium: '120-200',
        humidity: '60-80',
        temperature: '20-25',
        rainfall: '500-800',
        notes: 'Numeric range test',
      );

      // Verify numeric ranges are stored as strings
      expect(requirements.ph, isA<String>());
      expect(requirements.nitrogen, isA<String>());
      expect(requirements.phosphorus, isA<String>());
      expect(requirements.potassium, isA<String>());
      expect(requirements.humidity, isA<String>());
      expect(requirements.temperature, isA<String>());
      expect(requirements.rainfall, isA<String>());

      // Verify range format
      expect(requirements.ph, contains('-'));
      expect(requirements.nitrogen, contains('-'));
      expect(requirements.phosphorus, contains('-'));
      expect(requirements.potassium, contains('-'));
      expect(requirements.humidity, contains('-'));
      expect(requirements.temperature, contains('-'));
      expect(requirements.rainfall, contains('-'));
    });

    test('should create multiple products with different data', () {
      // Test creating multiple products
      const products = [
        Product(
          id: '1',
          name: 'Product 1',
          category: 'Category 1',
          description: 'Description 1',
          requirements: ProductRequirements(
            ph: '6.0-7.0',
            nitrogen: '100-150',
            phosphorus: '40-60',
            potassium: '120-200',
            humidity: '60-80',
            temperature: '20-25',
            rainfall: '500-800',
            notes: 'Notes 1',
          ),
        ),
        Product(
          id: '2',
          name: 'Product 2',
          category: 'Category 2',
          description: 'Description 2',
          requirements: ProductRequirements(
            ph: '5.5-6.5',
            nitrogen: '80-120',
            phosphorus: '30-50',
            potassium: '100-180',
            humidity: '50-70',
            temperature: '18-28',
            rainfall: '400-1000',
            notes: 'Notes 2',
          ),
        ),
      ];

      // Verify both products are created correctly
      expect(products.length, equals(2));
      expect(products[0].name, equals('Product 1'));
      expect(products[1].name, equals('Product 2'));
      expect(products[0].category, equals('Category 1'));
      expect(products[1].category, equals('Category 2'));
    });

    test('should handle empty string values', () {
      // Test product with empty string values
      const product = Product(
        id: '',
        name: '',
        category: '',
        description: '',
        requirements: ProductRequirements(
          ph: '',
          nitrogen: '',
          phosphorus: '',
          potassium: '',
          humidity: '',
          temperature: '',
          rainfall: '',
          notes: '',
        ),
      );

      // Verify empty strings are handled
      expect(product.id, equals(''));
      expect(product.name, equals(''));
      expect(product.category, equals(''));
      expect(product.description, equals(''));
      expect(product.requirements.ph, equals(''));
      expect(product.requirements.nitrogen, equals(''));
      expect(product.requirements.phosphorus, equals(''));
      expect(product.requirements.potassium, equals(''));
      expect(product.requirements.humidity, equals(''));
      expect(product.requirements.temperature, equals(''));
      expect(product.requirements.rainfall, equals(''));
      expect(product.requirements.notes, equals(''));
    });

    test('should handle very long string values', () {
      // Test product with very long string values
      const longString = 'A' * 1000; // 1000 character string
      
      const product = Product(
        id: longString,
        name: longString,
        category: longString,
        description: longString,
        requirements: ProductRequirements(
          ph: longString,
          nitrogen: longString,
          phosphorus: longString,
          potassium: longString,
          humidity: longString,
          temperature: longString,
          rainfall: longString,
          notes: longString,
        ),
      );

      // Verify long strings are handled
      expect(product.id.length, equals(1000));
      expect(product.name.length, equals(1000));
      expect(product.category.length, equals(1000));
      expect(product.description.length, equals(1000));
      expect(product.requirements.ph.length, equals(1000));
      expect(product.requirements.nitrogen.length, equals(1000));
      expect(product.requirements.phosphorus.length, equals(1000));
      expect(product.requirements.potassium.length, equals(1000));
      expect(product.requirements.humidity.length, equals(1000));
      expect(product.requirements.temperature.length, equals(1000));
      expect(product.requirements.rainfall.length, equals(1000));
      expect(product.requirements.notes.length, equals(1000));
    });
  });
}
