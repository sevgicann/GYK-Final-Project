import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/foundation.dart';

class LanguageService extends ChangeNotifier {
  static final LanguageService _instance = LanguageService._internal();
  factory LanguageService() => _instance;
  LanguageService._internal();

  String _currentLanguage = 'tr'; // Default to Turkish
  
  String get currentLanguage => _currentLanguage;
  
  bool get isTurkish => _currentLanguage == 'tr';
  bool get isEnglish => _currentLanguage == 'en';

  // Initialize language service
  Future<void> initialize() async {
    await _loadStoredLanguage();
  }

  // Load stored language preference
  Future<void> _loadStoredLanguage() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final storedLanguage = prefs.getString('selected_language');
      if (storedLanguage != null) {
        _currentLanguage = storedLanguage;
        print('🌍 Language loaded: $_currentLanguage');
      } else {
        print('🌍 No language preference found, using default: $_currentLanguage');
      }
    } catch (e) {
      print('Error loading language preference: $e');
    }
  }

  // Set language preference
  Future<void> setLanguage(String languageCode) async {
    try {
      if (_currentLanguage != languageCode) {
        _currentLanguage = languageCode;
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('selected_language', languageCode);
        print('🌍 Language changed to: $_currentLanguage');
        notifyListeners(); // Notify listeners about the change
      }
    } catch (e) {
      print('Error saving language preference: $e');
    }
  }

  // Set language from display name
  Future<void> setLanguageFromDisplayName(String displayName) async {
    String languageCode = 'tr'; // Default to Turkish
    
    switch (displayName) {
      case 'Türkçe':
        languageCode = 'tr';
        break;
      case 'English':
        languageCode = 'en';
        break;
      default:
        languageCode = 'tr';
        break;
    }
    
    await setLanguage(languageCode);
  }

  // Get display name for current language
  String get currentLanguageDisplayName {
    switch (_currentLanguage) {
      case 'tr':
        return 'Türkçe';
      case 'en':
        return 'English';
      default:
        return 'Türkçe';
    }
  }
}
