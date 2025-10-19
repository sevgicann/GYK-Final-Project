// Real GPS location service with geolocator
import 'dart:math';
import 'package:geolocator/geolocator.dart';
import '../data/turkish_cities.dart';

class LocationService {
  static final LocationService _instance = LocationService._internal();
  factory LocationService() => _instance;
  LocationService._internal();

  /// Get current GPS location using geolocator
  Future<Map<String, dynamic>> getCurrentLocation() async {
    try {
      print('📍 Requesting GPS location...');
      
      // Check if location services are enabled
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        print('❌ Location services are disabled');
        return {
          'success': false,
          'message': 'Konum servisleri kapalı. Lütfen konum servislerini açın.',
        };
      }

      // Check location permission
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          print('❌ Location permission denied');
          return {
            'success': false,
            'message': 'Konum izni reddedildi. Lütfen uygulama ayarlarından konum iznini verin.',
          };
        }
      }

      if (permission == LocationPermission.deniedForever) {
        print('❌ Location permission permanently denied');
        return {
          'success': false,
          'message': 'Konum izni kalıcı olarak reddedildi. Lütfen uygulama ayarlarından konum iznini verin.',
        };
      }

      // Get current position
      print('🌍 Getting current position...');
      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 10),
      );

      print('✅ GPS coordinates obtained: ${position.latitude}, ${position.longitude}');

      // Get city name from coordinates
      String cityName = await _getCityFromCoordinates(position.latitude, position.longitude);
      String regionName = TurkishCities.getRegionByCity(cityName);

      print('🏙️ Detected city: $cityName, region: $regionName');

      return {
        'success': true,
        'latitude': position.latitude,
        'longitude': position.longitude,
        'city': cityName,
        'region': regionName,
        'message': 'GPS konumu başarıyla alındı: $cityName',
      };

    } catch (e) {
      print('❌ Error getting GPS location: $e');
      
      // Return error with fallback to manual selection
      return {
        'success': false,
        'message': 'GPS konumu alınamadı: ${e.toString()}. Lütfen manuel olarak şehir seçin.',
      };
    }
  }

  /// Get city name from coordinates using distance calculation
  Future<String> _getCityFromCoordinates(double latitude, double longitude) async {
    print('🗺️ Finding nearest city for coordinates: $latitude, $longitude');
    
    // Turkish cities with their approximate coordinates
    final Map<String, Map<String, double>> cityCoordinates = {
      'İstanbul': {'lat': 41.0082, 'lon': 28.9784},
      'Ankara': {'lat': 39.9334, 'lon': 32.8597},
      'İzmir': {'lat': 38.4192, 'lon': 27.1287},
      'Bursa': {'lat': 40.1826, 'lon': 29.0665},
      'Antalya': {'lat': 36.8969, 'lon': 30.7133},
      'Adana': {'lat': 37.0000, 'lon': 35.3213},
      'Konya': {'lat': 37.8667, 'lon': 32.4833},
      'Gaziantep': {'lat': 37.0662, 'lon': 37.3833},
      'Şanlıurfa': {'lat': 37.1591, 'lon': 38.7969},
      'Kocaeli': {'lat': 40.8533, 'lon': 29.8815},
      'Mersin': {'lat': 36.8000, 'lon': 34.6333},
      'Diyarbakır': {'lat': 37.9144, 'lon': 40.2306},
      'Hatay': {'lat': 36.4018, 'lon': 36.3498},
      'Manisa': {'lat': 38.6191, 'lon': 27.4289},
      'Kayseri': {'lat': 38.7312, 'lon': 35.4787},
      'Samsun': {'lat': 41.2928, 'lon': 36.3313},
      'Balıkesir': {'lat': 39.6484, 'lon': 27.8826},
      'Kahramanmaraş': {'lat': 37.5858, 'lon': 36.9371},
      'Van': {'lat': 38.4891, 'lon': 43.4089},
      'Denizli': {'lat': 37.7765, 'lon': 29.0864},
      'Trabzon': {'lat': 41.0015, 'lon': 39.7178},
      'Ordu': {'lat': 40.9839, 'lon': 37.8764},
      'Afyonkarahisar': {'lat': 38.7507, 'lon': 30.5567},
      'Eskişehir': {'lat': 39.7767, 'lon': 30.5206},
      'Zonguldak': {'lat': 41.4564, 'lon': 31.7987},
      'Muğla': {'lat': 37.2153, 'lon': 28.3636},
      'Aydın': {'lat': 37.8560, 'lon': 27.8416},
      'Tekirdağ': {'lat': 40.9833, 'lon': 27.5167},
      'Sakarya': {'lat': 40.7889, 'lon': 30.4053},
      'Çanakkale': {'lat': 40.1553, 'lon': 26.4142},
      'Muş': {'lat': 38.9462, 'lon': 41.7539},
      'Isparta': {'lat': 37.7648, 'lon': 30.5566},
      'Tunceli': {'lat': 39.1079, 'lon': 39.5401},
      'Bingöl': {'lat': 38.8847, 'lon': 40.4981},
      'Bilecik': {'lat': 40.1501, 'lon': 29.9831},
      'Burdur': {'lat': 37.7206, 'lon': 30.2906},
      'Çankırı': {'lat': 40.6013, 'lon': 33.6134},
      'Çorum': {'lat': 40.5506, 'lon': 34.9556},
      'Edirne': {'lat': 41.6771, 'lon': 26.5557},
      'Elazığ': {'lat': 38.6810, 'lon': 39.2264},
      'Erzincan': {'lat': 39.7500, 'lon': 39.5000},
      'Erzurum': {'lat': 39.9334, 'lon': 41.2767},
      'Giresun': {'lat': 40.9128, 'lon': 38.3895},
      'Gümüşhane': {'lat': 40.4603, 'lon': 39.5086},
      'Hakkâri': {'lat': 37.5833, 'lon': 43.7333},
      'Kars': {'lat': 40.6013, 'lon': 43.0975},
      'Kastamonu': {'lat': 41.3887, 'lon': 33.7827},
      'Kırklareli': {'lat': 41.7350, 'lon': 27.2256},
      'Kırşehir': {'lat': 39.1425, 'lon': 34.1709},
      'Kocaeli': {'lat': 40.8533, 'lon': 29.8815},
      'Malatya': {'lat': 38.3552, 'lon': 38.3095},
      'Nevşehir': {'lat': 38.6939, 'lon': 34.6857},
      'Niğde': {'lat': 37.9667, 'lon': 34.6833},
      'Rize': {'lat': 41.0201, 'lon': 40.5234},
      'Siirt': {'lat': 37.9274, 'lon': 41.9403},
      'Sinop': {'lat': 42.0231, 'lon': 35.1531},
      'Sivas': {'lat': 39.7477, 'lon': 37.0179},
      'Tokat': {'lat': 40.3167, 'lon': 36.5500},
      'Uşak': {'lat': 38.6823, 'lon': 29.4082},
      'Yozgat': {'lat': 39.8181, 'lon': 34.8147},
      'Artvin': {'lat': 41.1828, 'lon': 41.8183},
      'Bartın': {'lat': 41.6344, 'lon': 32.3375},
      'Bayburt': {'lat': 40.2552, 'lon': 40.2249},
      'Düzce': {'lat': 40.8438, 'lon': 31.1565},
      'Karabük': {'lat': 41.2061, 'lon': 32.6204},
      'Kırıkkale': {'lat': 39.8468, 'lon': 33.4988},
      'Kilis': {'lat': 36.7184, 'lon': 37.1212},
      'Osmaniye': {'lat': 37.0742, 'lon': 36.2478},
      'Yalova': {'lat': 40.6550, 'lon': 29.2769},
      'Ardahan': {'lat': 41.1105, 'lon': 42.7022},
      'Iğdır': {'lat': 39.9200, 'lon': 44.0048},
    };

    String nearestCity = 'Ankara'; // Default fallback
    double minDistance = double.infinity;

    for (String city in cityCoordinates.keys) {
      final coords = cityCoordinates[city]!;
      double distance = _calculateDistance(
        latitude, longitude,
        coords['lat']!, coords['lon']!
      );
      
      if (distance < minDistance) {
        minDistance = distance;
        nearestCity = city;
      }
    }

    print('🏙️ Nearest city found: $nearestCity (distance: ${minDistance.toStringAsFixed(1)} km)');
    return nearestCity;
  }

  /// Get city name from coordinates (public method)
  Future<String?> getCityFromCoordinates(double latitude, double longitude) async {
    return await _getCityFromCoordinates(latitude, longitude);
  }

  /// Get coordinates from city name
  Future<Map<String, double>?> getCoordinatesFromCity(String cityName) async {
    // Turkish cities with their approximate coordinates
    final Map<String, Map<String, double>> cityCoordinates = {
      'İstanbul': {'lat': 41.0082, 'lon': 28.9784},
      'Ankara': {'lat': 39.9334, 'lon': 32.8597},
      'İzmir': {'lat': 38.4192, 'lon': 27.1287},
      'Bursa': {'lat': 40.1826, 'lon': 29.0665},
      'Antalya': {'lat': 36.8969, 'lon': 30.7133},
      'Adana': {'lat': 37.0000, 'lon': 35.3213},
      'Konya': {'lat': 37.8667, 'lon': 32.4833},
      'Gaziantep': {'lat': 37.0662, 'lon': 37.3833},
      'Şanlıurfa': {'lat': 37.1591, 'lon': 38.7969},
      'Kocaeli': {'lat': 40.8533, 'lon': 29.8815},
      'Mersin': {'lat': 36.8000, 'lon': 34.6333},
      'Diyarbakır': {'lat': 37.9144, 'lon': 40.2306},
      'Hatay': {'lat': 36.4018, 'lon': 36.3498},
      'Manisa': {'lat': 38.6191, 'lon': 27.4289},
      'Kayseri': {'lat': 38.7312, 'lon': 35.4787},
      'Samsun': {'lat': 41.2928, 'lon': 36.3313},
      'Balıkesir': {'lat': 39.6484, 'lon': 27.8826},
      'Kahramanmaraş': {'lat': 37.5858, 'lon': 36.9371},
      'Van': {'lat': 38.4891, 'lon': 43.4089},
      'Denizli': {'lat': 37.7765, 'lon': 29.0864},
      'Trabzon': {'lat': 41.0015, 'lon': 39.7178},
      'Ordu': {'lat': 40.9839, 'lon': 37.8764},
      'Afyonkarahisar': {'lat': 38.7507, 'lon': 30.5567},
      'Eskişehir': {'lat': 39.7767, 'lon': 30.5206},
      'Zonguldak': {'lat': 41.4564, 'lon': 31.7987},
      'Muğla': {'lat': 37.2153, 'lon': 28.3636},
      'Aydın': {'lat': 37.8560, 'lon': 27.8416},
      'Tekirdağ': {'lat': 40.9833, 'lon': 27.5167},
      'Sakarya': {'lat': 40.7889, 'lon': 30.4053},
      'Çanakkale': {'lat': 40.1553, 'lon': 26.4142},
      'Muş': {'lat': 38.9462, 'lon': 41.7539},
      'Isparta': {'lat': 37.7648, 'lon': 30.5566},
      'Tunceli': {'lat': 39.1079, 'lon': 39.5401},
      'Bingöl': {'lat': 38.8847, 'lon': 40.4981},
      'Bilecik': {'lat': 40.1501, 'lon': 29.9831},
      'Burdur': {'lat': 37.7206, 'lon': 30.2906},
      'Çankırı': {'lat': 40.6013, 'lon': 33.6134},
      'Çorum': {'lat': 40.5506, 'lon': 34.9556},
      'Edirne': {'lat': 41.6771, 'lon': 26.5557},
      'Elazığ': {'lat': 38.6810, 'lon': 39.2264},
      'Erzincan': {'lat': 39.7500, 'lon': 39.5000},
      'Erzurum': {'lat': 39.9334, 'lon': 41.2767},
      'Giresun': {'lat': 40.9128, 'lon': 38.3895},
      'Gümüşhane': {'lat': 40.4603, 'lon': 39.5086},
      'Hakkâri': {'lat': 37.5833, 'lon': 43.7333},
      'Kars': {'lat': 40.6013, 'lon': 43.0975},
      'Kastamonu': {'lat': 41.3887, 'lon': 33.7827},
      'Kırklareli': {'lat': 41.7350, 'lon': 27.2256},
      'Kırşehir': {'lat': 39.1425, 'lon': 34.1709},
      'Malatya': {'lat': 38.3552, 'lon': 38.3095},
      'Nevşehir': {'lat': 38.6939, 'lon': 34.6857},
      'Niğde': {'lat': 37.9667, 'lon': 34.6833},
      'Rize': {'lat': 41.0201, 'lon': 40.5234},
      'Siirt': {'lat': 37.9274, 'lon': 41.9403},
      'Sinop': {'lat': 42.0231, 'lon': 35.1531},
      'Sivas': {'lat': 39.7477, 'lon': 37.0179},
      'Tokat': {'lat': 40.3167, 'lon': 36.5500},
      'Uşak': {'lat': 38.6823, 'lon': 29.4082},
      'Yozgat': {'lat': 39.8181, 'lon': 34.8147},
      'Artvin': {'lat': 41.1828, 'lon': 41.8183},
      'Bartın': {'lat': 41.6344, 'lon': 32.3375},
      'Bayburt': {'lat': 40.2552, 'lon': 40.2249},
      'Düzce': {'lat': 40.8438, 'lon': 31.1565},
      'Karabük': {'lat': 41.2061, 'lon': 32.6204},
      'Kırıkkale': {'lat': 39.8468, 'lon': 33.4988},
      'Kilis': {'lat': 36.7184, 'lon': 37.1212},
      'Osmaniye': {'lat': 37.0742, 'lon': 36.2478},
      'Yalova': {'lat': 40.6550, 'lon': 29.2769},
      'Ardahan': {'lat': 41.1105, 'lon': 42.7022},
      'Iğdır': {'lat': 39.9200, 'lon': 44.0048},
    };

    final coords = cityCoordinates[cityName];
    if (coords != null) {
      return {
        'latitude': coords['lat']!,
        'longitude': coords['lon']!,
      };
    }
    return null;
  }

  /// Calculate distance between two coordinates
  double _calculateDistance(double lat1, double lon1, double lat2, double lon2) {
    const double earthRadius = 6371; // km
    
    final dLat = _degreesToRadians(lat2 - lat1);
    final dLon = _degreesToRadians(lon2 - lon1);
    
    final a = sin(dLat / 2) * sin(dLat / 2) +
        cos(_degreesToRadians(lat1)) * cos(_degreesToRadians(lat2)) * sin(dLon / 2) * sin(dLon / 2);
    final c = 2 * asin(sqrt(a));
    
    return earthRadius * c;
  }

  /// Convert degrees to radians
  double _degreesToRadians(double degrees) {
    return degrees * (pi / 180);
  }

  /// Check if location service is enabled
  Future<bool> isLocationServiceEnabled() async {
    return await Geolocator.isLocationServiceEnabled();
  }

  /// Check current permission status
  Future<String> checkPermission() async {
    LocationPermission permission = await Geolocator.checkPermission();
    switch (permission) {
      case LocationPermission.always:
      case LocationPermission.whileInUse:
        return 'granted';
      case LocationPermission.denied:
        return 'denied';
      case LocationPermission.deniedForever:
        return 'deniedForever';
      case LocationPermission.unableToDetermine:
        return 'unableToDetermine';
    }
  }

  /// Request location permission
  Future<String> requestPermission() async {
    LocationPermission permission = await Geolocator.requestPermission();
    switch (permission) {
      case LocationPermission.always:
      case LocationPermission.whileInUse:
        return 'granted';
      case LocationPermission.denied:
        return 'denied';
      case LocationPermission.deniedForever:
        return 'deniedForever';
      case LocationPermission.unableToDetermine:
        return 'unableToDetermine';
    }
  }

  /// Open location settings
  Future<bool> openLocationSettings() async {
    return await Geolocator.openLocationSettings();
  }

  /// Get all Turkish cities
  List<Map<String, dynamic>> getAllCities() {
    return TurkishCities.cities.map((city) => {'name': city}).toList();
  }

  /// Search cities by name
  List<Map<String, dynamic>> searchCities(String query) {
    if (query.isEmpty) return getAllCities();
    
    return TurkishCities.cities.where((city) {
      return city.toLowerCase().contains(query.toLowerCase());
    }).map((city) => {'name': city}).toList();
  }

  /// Get city by name
  Map<String, dynamic>? getCityByName(String cityName) {
    try {
      final city = TurkishCities.cities.firstWhere(
        (city) => city.toLowerCase() == cityName.toLowerCase(),
      );
      return {'name': city};
    } catch (e) {
      return null;
    }
  }
}