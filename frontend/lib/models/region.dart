class Region {
  final String id;
  final String name;
  final String description;
  final ClimateData climateData;

  const Region({
    required this.id,
    required this.name,
    required this.description,
    required this.climateData,
  });

  factory Region.fromJson(Map<String, dynamic> json) {
    return Region(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String,
      climateData: ClimateData.fromJson(json['climateData'] as Map<String, dynamic>),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'climateData': climateData.toJson(),
    };
  }

  @override
  String toString() => name;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Region && runtimeType == other.runtimeType && id == other.id;

  @override
  int get hashCode => id.hashCode;
}

class ClimateData {
  final double averageTemperature;
  final double averageHumidity;
  final double averageRainfall;
  final String soilType;
  final String seasonality;

  const ClimateData({
    required this.averageTemperature,
    required this.averageHumidity,
    required this.averageRainfall,
    required this.soilType,
    required this.seasonality,
  });

  factory ClimateData.fromJson(Map<String, dynamic> json) {
    return ClimateData(
      averageTemperature: (json['averageTemperature'] as num).toDouble(),
      averageHumidity: (json['averageHumidity'] as num).toDouble(),
      averageRainfall: (json['averageRainfall'] as num).toDouble(),
      soilType: json['soilType'] as String,
      seasonality: json['seasonality'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'averageTemperature': averageTemperature,
      'averageHumidity': averageHumidity,
      'averageRainfall': averageRainfall,
      'soilType': soilType,
      'seasonality': seasonality,
    };
  }
}
