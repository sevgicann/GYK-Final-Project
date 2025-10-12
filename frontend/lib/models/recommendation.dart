import 'product.dart';
import 'region.dart';

class Recommendation {
  final Product product;
  final Region region;
  final ProductRequirements requirements;
  final String additionalNotes;
  final DateTime createdAt;

  const Recommendation({
    required this.product,
    required this.region,
    required this.requirements,
    required this.additionalNotes,
    required this.createdAt,
  });

  factory Recommendation.fromJson(Map<String, dynamic> json) {
    return Recommendation(
      product: Product.fromJson(json['product'] as Map<String, dynamic>),
      region: Region.fromJson(json['region'] as Map<String, dynamic>),
      requirements: ProductRequirements.fromJson(json['requirements'] as Map<String, dynamic>),
      additionalNotes: json['additionalNotes'] as String,
      createdAt: DateTime.parse(json['createdAt'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'product': product.toJson(),
      'region': region.toJson(),
      'requirements': requirements.toJson(),
      'additionalNotes': additionalNotes,
      'createdAt': createdAt.toIso8601String(),
    };
  }

  String get title => '${product.name} için önerilen koşullar';
  String get regionNote => 'Bölge: ${region.name}';
}
