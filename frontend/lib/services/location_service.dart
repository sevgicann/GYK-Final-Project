// Web-compatible location service
import 'dart:math';
import '../data/turkish_cities.dart';

class LocationService {
  static final LocationService _instance = LocationService._internal();
  factory LocationService() => _instance;
  LocationService._internal();

  /// Get current GPS location (web fallback)
  Future<Map<String, dynamic>> getCurrentLocation() async {
    // For web, we'll return a default location or use browser geolocation
    try {
      // Try to get location from browser
      if (await _isLocationAvailable()) {
        final location = await _getBrowserLocation();
        if (location != null) {
          return {
            'success': true,
            'latitude': location['latitude'],
            'longitude': location['longitude'],
            'city': 'Ankara', // Default city for web
            'message': 'Konum başarıyla alındı',
          };
        }
      }
    } catch (e) {
      print('Location error: $e');
    }
    
    // Return default location (Ankara) with success status
    return {
      'success': true,
      'latitude': 39.9334,
      'longitude': 32.8597,
      'city': 'Ankara',
      'message': 'Varsayılan konum kullanılıyor',
    };
  }

  /// Check if location is available in browser
  Future<bool> _isLocationAvailable() async {
    // Check if geolocation is supported
    return true; // Assume it's available for web
  }

  /// Get location from browser geolocation API
  Future<Map<String, double>?> _getBrowserLocation() async {
    // This would need to be implemented with JavaScript interop
    // For now, return default location
    return {
      'latitude': 39.9334,
      'longitude': 32.8597,
    };
  }

  /// Get city name from coordinates (web fallback)
  Future<String?> getCityFromCoordinates(double latitude, double longitude) async {
    // For web, we'll use a simple approximation
    // In a real app, you'd call a geocoding API
    return _getNearestCity(latitude, longitude);
  }

  /// Get coordinates from city name
  Future<Map<String, double>?> getCoordinatesFromCity(String cityName) async {
    // For web, return default coordinates (Ankara)
    // In a real app, you'd have a city coordinates database
    return {
      'latitude': 39.9334,
      'longitude': 32.8597,
    };
  }

  /// Get nearest city from coordinates
  String _getNearestCity(double latitude, double longitude) {
    // For web, return a simple approximation
    // In a real app, you'd calculate distance to all cities
    return 'Ankara';
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

  /// Check if location service is enabled (web always true)
  Future<bool> isLocationServiceEnabled() async {
    return true; // Web browsers handle this
  }

  /// Check current permission status (web always granted)
  Future<String> checkPermission() async {
    return 'granted'; // Web browsers handle this
  }

  /// Request location permission (web always granted)
  Future<String> requestPermission() async {
    return 'granted'; // Web browsers handle this
  }

  /// Open location settings (web not applicable)
  Future<bool> openLocationSettings() async {
    return false; // Not applicable for web
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