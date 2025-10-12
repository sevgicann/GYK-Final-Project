class Product {
  final String id;
  final String name;
  final String category;
  final String description;
  final ProductRequirements requirements;

  const Product({
    required this.id,
    required this.name,
    required this.category,
    required this.description,
    required this.requirements,
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'] as String,
      name: json['name'] as String,
      category: json['category'] as String,
      description: json['description'] as String,
      requirements: ProductRequirements.fromJson(json['requirements'] as Map<String, dynamic>),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'category': category,
      'description': description,
      'requirements': requirements.toJson(),
    };
  }

  @override
  String toString() => name;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Product && runtimeType == other.runtimeType && id == other.id;

  @override
  int get hashCode => id.hashCode;
}

class ProductRequirements {
  final String ph;
  final String nitrogen;
  final String phosphorus;
  final String potassium;
  final String humidity;
  final String temperature;
  final String rainfall;
  final String notes;

  const ProductRequirements({
    required this.ph,
    required this.nitrogen,
    required this.phosphorus,
    required this.potassium,
    required this.humidity,
    required this.temperature,
    required this.rainfall,
    required this.notes,
  });

  factory ProductRequirements.fromJson(Map<String, dynamic> json) {
    return ProductRequirements(
      ph: json['ph'] as String,
      nitrogen: json['nitrogen'] as String,
      phosphorus: json['phosphorus'] as String,
      potassium: json['potassium'] as String,
      humidity: json['humidity'] as String,
      temperature: json['temperature'] as String,
      rainfall: json['rainfall'] as String,
      notes: json['notes'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'ph': ph,
      'nitrogen': nitrogen,
      'phosphorus': phosphorus,
      'potassium': potassium,
      'humidity': humidity,
      'temperature': temperature,
      'rainfall': rainfall,
      'notes': notes,
    };
  }
}
