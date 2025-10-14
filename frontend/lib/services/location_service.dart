import 'package:geolocator/geolocator.dart';
import 'package:geocoding/geocoding.dart';
import '../data/turkish_cities.dart';

class LocationService {
  static final LocationService _instance = LocationService._internal();
  factory LocationService() => _instance;
  LocationService._internal();

  /// Get current GPS location with permission handling
  Future<Map<String, dynamic>> getCurrentLocation() async {
    try {
      print('📍 Checking location permissions...');
      
      // Check if location services are enabled
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        throw Exception('Konum servisleri kapalı. Lütfen GPS\'i açın.');
      }

      // Check and request permission
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          throw Exception('Konum izni reddedildi.');
        }
      }
      
      if (permission == LocationPermission.deniedForever) {
        throw Exception('Konum izni kalıcı olarak reddedildi. Lütfen ayarlardan izin verin.');
      }

      print('✅ Location permission granted, getting position...');

      // Get current position
      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 10),
      );

      print('📍 GPS Coordinates: ${position.latitude}, ${position.longitude}');

      // Reverse geocoding to get city name
      String city = 'İstanbul'; // Default fallback
      String region = 'Marmara'; // Default fallback
      
      try {
        List<Placemark> placemarks = await placemarkFromCoordinates(
          position.latitude,
          position.longitude,
        );
        
        if (placemarks.isNotEmpty) {
          Placemark place = placemarks.first;
          print('📍 Placemark: ${place.locality}, ${place.administrativeArea}');
          
          // Try to get city from placemark
          String? detectedCity = place.locality ?? place.administrativeArea;
          
          if (detectedCity != null) {
            // Normalize Turkish city name
            city = _normalizeCityName(detectedCity);
            region = TurkishCities.getRegionByCity(city);
            print('✅ Detected City: $city, Region: $region');
          }
        }
      } catch (e) {
        print('⚠️ Geocoding failed, using coordinates to determine region: $e');
        // Fallback: Determine region from coordinates
        final regionFromCoords = _getRegionFromCoordinates(
          position.latitude,
          position.longitude,
        );
        if (regionFromCoords != null) {
          region = regionFromCoords['region']!;
          city = regionFromCoords['city']!;
          print('✅ Region from coordinates: $city, $region');
        }
      }

      return {
        'success': true,
        'latitude': position.latitude,
        'longitude': position.longitude,
        'city': city,
        'region': region,
        'accuracy': position.accuracy,
        'timestamp': position.timestamp?.toIso8601String(),
      };
    } catch (e) {
      print('❌ Error getting location: $e');
      return {
        'success': false,
        'error': e.toString(),
        'message': 'GPS konumu alınamadı: $e',
      };
    }
  }

  /// Normalize Turkish city names
  String _normalizeCityName(String cityName) {
    // Remove Turkish characters and normalize
    final normalized = cityName.trim();
    
    // Common city name mappings
    final Map<String, String> cityMappings = {
      'istanbul': 'İstanbul',
      'ankara': 'Ankara',
      'izmir': 'İzmir',
      'bursa': 'Bursa',
      'antalya': 'Antalya',
      'adana': 'Adana',
      'konya': 'Konya',
      'şanlıurfa': 'Şanlıurfa',
      'gaziantep': 'Gaziantep',
      'kayseri': 'Kayseri',
      'trabzon': 'Trabzon',
      'erzurum': 'Erzurum',
      'diyarbakır': 'Diyarbakır',
      'samsun': 'Samsun',
      'denizli': 'Denizli',
      'mersin': 'Mersin',
      'eskişehir': 'Eskişehir',
      'malatya': 'Malatya',
      'kahramanmaraş': 'Kahramanmaraş',
      'ağrı': 'Ağrı',
      'van': 'Van',
      'mardin': 'Mardin',
      'batman': 'Batman',
      'şırnak': 'Şırnak',
      'hatay': 'Hatay',
      'osmaniye': 'Osmaniye',
      'kocaeli': 'Kocaeli',
      'sakarya': 'Sakarya',
      'tekirdağ': 'Tekirdağ',
      'edirne': 'Edirne',
      'kırklareli': 'Kırklareli',
      'çanakkale': 'Çanakkale',
      'balıkesir': 'Balıkesir',
      'manisa': 'Manisa',
      'aydın': 'Aydın',
      'muğla': 'Muğla',
    };
    
    // Check if we have a mapping for this city
    final lowerCity = normalized.toLowerCase();
    if (cityMappings.containsKey(lowerCity)) {
      return cityMappings[lowerCity]!;
    }
    
    // If not found, return as is (capitalized)
    return normalized;
  }

  /// Determine region from GPS coordinates (approximate)
  Map<String, String>? _getRegionFromCoordinates(double lat, double lng) {
    // Turkey's approximate regional boundaries
    // Marmara Region
    if (lat >= 40.0 && lat <= 42.0 && lng >= 26.0 && lng <= 30.5) {
      return {'region': 'Marmara', 'city': 'İstanbul'};
    }
    // Aegean Region
    if (lat >= 37.0 && lat <= 40.0 && lng >= 26.0 && lng <= 30.0) {
      return {'region': 'Aegean', 'city': 'İzmir'};
    }
    // Mediterranean Region
    if (lat >= 36.0 && lat <= 38.0 && lng >= 28.0 && lng <= 36.0) {
      return {'region': 'Mediterranean', 'city': 'Antalya'};
    }
    // Central Anatolia
    if (lat >= 38.0 && lat <= 41.0 && lng >= 31.0 && lng <= 38.0) {
      return {'region': 'Central Anatolia', 'city': 'Ankara'};
    }
    // Black Sea Region
    if (lat >= 40.0 && lat <= 42.0 && lng >= 31.0 && lng <= 42.0) {
      return {'region': 'Black Sea', 'city': 'Samsun'};
    }
    // Eastern Anatolia
    if (lat >= 38.0 && lat <= 42.0 && lng >= 38.0 && lng <= 45.0) {
      return {'region': 'Eastern Anatolia', 'city': 'Erzurum'};
    }
    // Southeastern Anatolia
    if (lat >= 36.0 && lat <= 39.0 && lng >= 36.0 && lng <= 43.0) {
      return {'region': 'Southeastern Anatolia', 'city': 'Gaziantep'};
    }
    
    // Default to Marmara if can't determine
    return {'region': 'Marmara', 'city': 'İstanbul'};
  }

  /// Check if location services are enabled
  Future<bool> isLocationServiceEnabled() async {
    return await Geolocator.isLocationServiceEnabled();
  }

  /// Check current permission status
  Future<LocationPermission> checkPermission() async {
    return await Geolocator.checkPermission();
  }

  /// Request location permission
  Future<LocationPermission> requestPermission() async {
    return await Geolocator.requestPermission();
  }

  /// Open location settings
  Future<bool> openLocationSettings() async {
    return await Geolocator.openLocationSettings();
  }
}

