class User {
  final String id;
  final String name;
  final String email;
  final String language;
  final DateTime createdAt;
  final UserPreferences preferences;

  const User({
    required this.id,
    required this.name,
    required this.email,
    required this.language,
    required this.createdAt,
    required this.preferences,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
      language: json['language'] as String,
      createdAt: DateTime.parse(json['createdAt'] as String),
      preferences: UserPreferences.fromJson(json['preferences'] as Map<String, dynamic>),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'language': language,
      'createdAt': createdAt.toIso8601String(),
      'preferences': preferences.toJson(),
    };
  }

  User copyWith({
    String? id,
    String? name,
    String? email,
    String? language,
    DateTime? createdAt,
    UserPreferences? preferences,
  }) {
    return User(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      language: language ?? this.language,
      createdAt: createdAt ?? this.createdAt,
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
