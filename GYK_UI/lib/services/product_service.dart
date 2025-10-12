import '../models/product.dart';

/// Ürün servisi - Singleton pattern ile tek sorumluluk
class ProductService {
  static final ProductService _instance = ProductService._internal();
  factory ProductService() => _instance;
  ProductService._internal();

  final List<Product> _products = [
    Product(
      id: '1',
      name: 'Havuç',
      category: 'Sebze',
      description: 'Beta karoten açısından zengin kök sebze',
      requirements: const ProductRequirements(
        ph: '6.0–7.5',
        nitrogen: '90–140',
        phosphorus: '35–65',
        potassium: '180–240',
        humidity: '16–24',
        temperature: '15–26',
        rainfall: '400–900',
        notes: 'Bölgeye uygun gübre ve sulama kullanın',
      ),
    ),
    Product(
      id: '2',
      name: 'Domates',
      category: 'Sebze',
      description: 'Lycopene açısından zengin meyve sebze',
      requirements: const ProductRequirements(
        ph: '6.0–6.8',
        nitrogen: '120–180',
        phosphorus: '40–80',
        potassium: '200–300',
        humidity: '60–80',
        temperature: '18–30',
        rainfall: '600–1200',
        notes: 'Düzenli sulama ve güneş ışığı önemli',
      ),
    ),
    Product(
      id: '3',
      name: 'Patates',
      category: 'Sebze',
      description: 'Karbonhidrat açısından zengin yumru sebze',
      requirements: const ProductRequirements(
        ph: '4.8–5.5',
        nitrogen: '100–150',
        phosphorus: '30–60',
        potassium: '150–250',
        humidity: '70–80',
        temperature: '15–20',
        rainfall: '500–800',
        notes: 'Serin iklim ve iyi drenaj gerekli',
      ),
    ),
    Product(
      id: '4',
      name: 'Soğan',
      category: 'Sebze',
      description: 'Antibakteriyel özellikli kök sebze',
      requirements: const ProductRequirements(
        ph: '6.0–7.0',
        nitrogen: '80–120',
        phosphorus: '25–50',
        potassium: '120–180',
        humidity: '60–70',
        temperature: '13–24',
        rainfall: '400–600',
        notes: 'Kuru hava ve güneş ışığı tercih eder',
      ),
    ),
    Product(
      id: '5',
      name: 'Biber',
      category: 'Sebze',
      description: 'C vitamini açısından zengin meyve sebze',
      requirements: const ProductRequirements(
        ph: '6.0–6.8',
        nitrogen: '100–150',
        phosphorus: '35–70',
        potassium: '180–250',
        humidity: '50–70',
        temperature: '20–30',
        rainfall: '600–1000',
        notes: 'Sıcak iklim ve düzenli sulama gerekli',
      ),
    ),
    Product(
      id: '6',
      name: 'Salatalık',
      category: 'Sebze',
      description: 'Su içeriği yüksek meyve sebze',
      requirements: const ProductRequirements(
        ph: '6.0–7.0',
        nitrogen: '80–120',
        phosphorus: '30–60',
        potassium: '150–200',
        humidity: '70–80',
        temperature: '18–25',
        rainfall: '500–800',
        notes: 'Nemli ortam ve düzenli sulama gerekli',
      ),
    ),
    Product(
      id: '7',
      name: 'Marul',
      category: 'Yeşillik',
      description: 'Folik asit açısından zengin yapraklı sebze',
      requirements: const ProductRequirements(
        ph: '6.0–7.0',
        nitrogen: '60–100',
        phosphorus: '20–40',
        potassium: '100–150',
        humidity: '60–70',
        temperature: '15–20',
        rainfall: '400–600',
        notes: 'Serin iklim ve gölgeli alan tercih eder',
      ),
    ),
    Product(
      id: '8',
      name: 'Ispanak',
      category: 'Yeşillik',
      description: 'Demir açısından zengin yapraklı sebze',
      requirements: const ProductRequirements(
        ph: '6.0–7.5',
        nitrogen: '70–110',
        phosphorus: '25–45',
        potassium: '120–180',
        humidity: '60–80',
        temperature: '10–20',
        rainfall: '400–700',
        notes: 'Serin iklim ve nemli toprak gerekli',
      ),
    ),
    Product(
      id: '9',
      name: 'Brokoli',
      category: 'Sebze',
      description: 'Antioksidan açısından zengin çiçek sebze',
      requirements: const ProductRequirements(
        ph: '6.0–7.0',
        nitrogen: '100–150',
        phosphorus: '40–80',
        potassium: '150–250',
        humidity: '60–80',
        temperature: '15–20',
        rainfall: '500–800',
        notes: 'Serin iklim ve organik gübre tercih eder',
      ),
    ),
    Product(
      id: '10',
      name: 'Karnabahar',
      category: 'Sebze',
      description: 'C vitamini açısından zengin çiçek sebze',
      requirements: const ProductRequirements(
        ph: '6.0–7.0',
        nitrogen: '100–150',
        phosphorus: '40–80',
        potassium: '150–250',
        humidity: '60–80',
        temperature: '15–20',
        rainfall: '500–800',
        notes: 'Serin iklim ve düzenli sulama gerekli',
      ),
    ),
    Product(
      id: '11',
      name: 'Mısır',
      category: 'Tahıl',
      description: 'Yüksek verimli tahıl ürünü',
      requirements: const ProductRequirements(
        ph: '6.0–7.0',
        nitrogen: '120–180',
        phosphorus: '40–80',
        potassium: '150–250',
        humidity: '60–80',
        temperature: '20–30',
        rainfall: '500–800',
        notes: 'Sıcak iklim ve düzenli sulama gerekli',
      ),
    ),
    Product(
      id: '12',
      name: 'Pirinç',
      category: 'Tahıl',
      description: 'Su içinde yetişen tahıl ürünü',
      requirements: const ProductRequirements(
        ph: '5.5–7.0',
        nitrogen: '100–150',
        phosphorus: '30–60',
        potassium: '120–200',
        humidity: '80–90',
        temperature: '25–35',
        rainfall: '1000–2000',
        notes: 'Çok su gerektiren, sıcak iklim ürünü',
      ),
    ),
  ];

  List<Product> getAllProducts() {
    return List.unmodifiable(_products);
  }

  Product? getProductById(String id) {
    try {
      return _products.firstWhere((product) => product.id == id);
    } catch (e) {
      return null;
    }
  }

  Product? getProductByName(String name) {
    try {
      return _products.firstWhere((product) => product.name == name);
    } catch (e) {
      return null;
    }
  }

  List<Product> getProductsByCategory(String category) {
    return _products.where((product) => product.category == category).toList();
  }

  List<String> getAllProductNames() {
    return _products.map((product) => product.name).toList();
  }

  List<String> getAllCategories() {
    return _products.map((product) => product.category).toSet().toList();
  }

  List<Product> searchProducts(String query) {
    if (query.isEmpty) return getAllProducts();
    
    final lowercaseQuery = query.toLowerCase();
    return _products.where((product) => _matchesQuery(product, lowercaseQuery)).toList();
  }

  /// Ürün arama sorgusu ile eşleşip eşleşmediğini kontrol eder - tek sorumluluk
  bool _matchesQuery(Product product, String query) {
    return product.name.toLowerCase().contains(query) ||
           product.category.toLowerCase().contains(query) ||
           product.description.toLowerCase().contains(query);
  }

  /// Kategoriye göre ürün sayısını döndürür - tek sorumluluk
  int getProductCountByCategory(String category) {
    return _products.where((product) => product.category == category).length;
  }

  /// En popüler kategorileri döndürür - tek sorumluluk
  List<String> getPopularCategories({int limit = 5}) {
    final categoryCounts = <String, int>{};
    
    for (final product in _products) {
      categoryCounts[product.category] = (categoryCounts[product.category] ?? 0) + 1;
    }
    
    final sortedCategories = categoryCounts.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    
    return sortedCategories.take(limit).map((e) => e.key).toList();
  }
}
