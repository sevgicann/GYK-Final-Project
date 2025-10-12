import '../models/region.dart';

class RegionService {
  static final RegionService _instance = RegionService._internal();
  factory RegionService() => _instance;
  RegionService._internal();

  final List<Region> _regions = [
    Region(
      id: '1',
      name: 'İç Anadolu',
      description: 'Karasal iklim, kuru ve sıcak yazlar, soğuk kışlar',
      climateData: const ClimateData(
        averageTemperature: 12.0,
        averageHumidity: 55.0,
        averageRainfall: 400.0,
        soilType: 'Kahverengi toprak',
        seasonality: 'Karasal',
      ),
    ),
    Region(
      id: '2',
      name: 'Marmara',
      description: 'Geçiş iklimi, ılıman ve nemli',
      climateData: const ClimateData(
        averageTemperature: 14.0,
        averageHumidity: 70.0,
        averageRainfall: 700.0,
        soilType: 'Alüvyal toprak',
        seasonality: 'Geçiş',
      ),
    ),
    Region(
      id: '3',
      name: 'Ege',
      description: 'Akdeniz iklimi, sıcak ve kuru yazlar, ılıman kışlar',
      climateData: const ClimateData(
        averageTemperature: 18.0,
        averageHumidity: 65.0,
        averageRainfall: 600.0,
        soilType: 'Terra rossa',
        seasonality: 'Akdeniz',
      ),
    ),
    Region(
      id: '4',
      name: 'Akdeniz',
      description: 'Akdeniz iklimi, çok sıcak yazlar, ılıman kışlar',
      climateData: const ClimateData(
        averageTemperature: 20.0,
        averageHumidity: 60.0,
        averageRainfall: 800.0,
        soilType: 'Terra rossa',
        seasonality: 'Akdeniz',
      ),
    ),
    Region(
      id: '5',
      name: 'Karadeniz',
      description: 'Okyanus iklimi, nemli ve yağışlı',
      climateData: const ClimateData(
        averageTemperature: 13.0,
        averageHumidity: 80.0,
        averageRainfall: 1200.0,
        soilType: 'Podzol toprak',
        seasonality: 'Okyanus',
      ),
    ),
    Region(
      id: '6',
      name: 'Doğu Anadolu',
      description: 'Karasal iklim, çok soğuk kışlar, sıcak yazlar',
      climateData: const ClimateData(
        averageTemperature: 8.0,
        averageHumidity: 50.0,
        averageRainfall: 500.0,
        soilType: 'Kahverengi toprak',
        seasonality: 'Karasal',
      ),
    ),
    Region(
      id: '7',
      name: 'Güneydoğu Anadolu',
      description: 'Karasal iklim, çok sıcak yazlar, soğuk kışlar',
      climateData: const ClimateData(
        averageTemperature: 16.0,
        averageHumidity: 45.0,
        averageRainfall: 300.0,
        soilType: 'Çöl toprağı',
        seasonality: 'Karasal',
      ),
    ),
  ];

  List<Region> getAllRegions() {
    return List.unmodifiable(_regions);
  }

  Region? getRegionById(String id) {
    try {
      return _regions.firstWhere((region) => region.id == id);
    } catch (e) {
      return null;
    }
  }

  Region? getRegionByName(String name) {
    try {
      return _regions.firstWhere((region) => region.name == name);
    } catch (e) {
      return null;
    }
  }

  List<String> getAllRegionNames() {
    return _regions.map((region) => region.name).toList();
  }

  List<Region> getRegionsByClimateType(String climateType) {
    return _regions.where((region) => 
      region.climateData.seasonality.toLowerCase().contains(climateType.toLowerCase())
    ).toList();
  }

  List<Region> searchRegions(String query) {
    if (query.isEmpty) return getAllRegions();
    
    final lowercaseQuery = query.toLowerCase();
    return _regions.where((region) {
      return region.name.toLowerCase().contains(lowercaseQuery) ||
             region.description.toLowerCase().contains(lowercaseQuery) ||
             region.climateData.soilType.toLowerCase().contains(lowercaseQuery);
    }).toList();
  }

  List<Region> getRegionsByTemperatureRange(double minTemp, double maxTemp) {
    return _regions.where((region) {
      final temp = region.climateData.averageTemperature;
      return temp >= minTemp && temp <= maxTemp;
    }).toList();
  }

  List<Region> getRegionsByRainfallRange(double minRainfall, double maxRainfall) {
    return _regions.where((region) {
      final rainfall = region.climateData.averageRainfall;
      return rainfall >= minRainfall && rainfall <= maxRainfall;
    }).toList();
  }
}
