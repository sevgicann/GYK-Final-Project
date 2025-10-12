class User {
  final String id;
  final String firstName;
  final String lastName;
  final String email;
  final String? phone;
  final DateTime createdAt;
  final DateTime updatedAt;
  final UserPreferences? preferences;

  const User({
    required this.id,
    required this.firstName,
    required this.lastName,
    required this.email,
    this.phone,
    required this.createdAt,
    required this.updatedAt,
    this.preferences,
  });

  // Computed property for full name
  String get name => '$firstName $lastName';

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id']?.toString() ?? '',
      firstName: json['first_name'] ?? json['firstName'] ?? '',
      lastName: json['last_name'] ?? json['lastName'] ?? '',
      email: json['email'] ?? '',
      phone: json['phone'],
      createdAt: DateTime.parse(json['created_at'] ?? json['createdAt'] ?? DateTime.now().toIso8601String()),
      updatedAt: DateTime.parse(json['updated_at'] ?? json['updatedAt'] ?? DateTime.now().toIso8601String()),
      preferences: json['preferences'] != null 
          ? UserPreferences.fromJson(json['preferences'] as Map<String, dynamic>)
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'first_name': firstName,
      'last_name': lastName,
      'email': email,
      'phone': phone,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'preferences': preferences?.toJson(),
    };
  }

  User copyWith({
    String? id,
    String? firstName,
    String? lastName,
    String? email,
    String? phone,
    DateTime? createdAt,
    DateTime? updatedAt,
    UserPreferences? preferences,
  }) {
    return User(
      id: id ?? this.id,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      email: email ?? this.email,
      phone: phone ?? this.phone,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      preferences: preferences ?? this.preferences,
    );
  }
}

class UserPreferences {
  final String selectedRegion;
  final bool useGpsLocation;
  final String theme;
  final List<String> favoriteProducts;

  const UserPreferences({
    required this.selectedRegion,
    required this.useGpsLocation,
    required this.theme,
    required this.favoriteProducts,
  });

  factory UserPreferences.fromJson(Map<String, dynamic> json) {
    return UserPreferences(
      selectedRegion: json['selectedRegion'] as String,
      useGpsLocation: json['useGpsLocation'] as bool,
      theme: json['theme'] as String,
      favoriteProducts: List<String>.from(json['favoriteProducts'] as List),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'selectedRegion': selectedRegion,
      'useGpsLocation': useGpsLocation,
      'theme': theme,
      'favoriteProducts': favoriteProducts,
    };
  }

  UserPreferences copyWith({
    String? selectedRegion,
    bool? useGpsLocation,
    String? theme,
    List<String>? favoriteProducts,
  }) {
    return UserPreferences(
      selectedRegion: selectedRegion ?? this.selectedRegion,
      useGpsLocation: useGpsLocation ?? this.useGpsLocation,
      theme: theme ?? this.theme,
      favoriteProducts: favoriteProducts ?? this.favoriteProducts,
    );
  }
}
