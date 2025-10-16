import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class MyEnvironmentsService {
  static const String _savedEnvironmentsKey = 'saved_environments';

  /// Save environment data to the saved environments list
  Future<void> saveEnvironment(Map<String, dynamic> environmentData) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedEnvironmentsJson = prefs.getStringList(_savedEnvironmentsKey) ?? [];
      
      // Generate unique ID
      final environmentId = DateTime.now().millisecondsSinceEpoch.toString();
      
      // Create environment object
      final environment = {
        'id': environmentId,
        'data': environmentData,
        'createdAt': DateTime.now().toIso8601String(),
      };
      
      // Add new environment
      savedEnvironmentsJson.add(jsonEncode(environment));
      await prefs.setStringList(_savedEnvironmentsKey, savedEnvironmentsJson);
      
      print('Environment data saved successfully with ID: $environmentId');
    } catch (e) {
      print('Error saving environment data: $e');
      throw Exception('Ortam verisi kaydedilirken hata oluştu: $e');
    }
  }

  /// Get all saved environments
  Future<List<Map<String, dynamic>>> getSavedEnvironments() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedEnvironmentsJson = prefs.getStringList(_savedEnvironmentsKey) ?? [];
      
      return savedEnvironmentsJson
          .map((json) => Map<String, dynamic>.from(jsonDecode(json)))
          .toList();
    } catch (e) {
      print('Error loading saved environments: $e');
      return [];
    }
  }

  /// Remove an environment from saved environments
  Future<void> removeEnvironment(String environmentId) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedEnvironmentsJson = prefs.getStringList(_savedEnvironmentsKey) ?? [];
      
      // Find and remove the environment
      savedEnvironmentsJson.removeWhere((json) {
        try {
          final environment = Map<String, dynamic>.from(jsonDecode(json));
          return environment['id'] == environmentId;
        } catch (e) {
          return false;
        }
      });
      
      await prefs.setStringList(_savedEnvironmentsKey, savedEnvironmentsJson);
      print('Environment $environmentId removed successfully');
    } catch (e) {
      print('Error removing environment: $e');
      throw Exception('Ortam verisi kaldırılırken hata oluştu: $e');
    }
  }

  /// Check if an environment exists
  Future<bool> isEnvironmentSaved(String environmentId) async {
    try {
      final savedEnvironments = await getSavedEnvironments();
      return savedEnvironments.any((environment) => environment['id'] == environmentId);
    } catch (e) {
      print('Error checking if environment is saved: $e');
      return false;
    }
  }

  /// Clear all saved environments
  Future<void> clearAllEnvironments() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove(_savedEnvironmentsKey);
      print('All saved environments cleared');
    } catch (e) {
      print('Error clearing saved environments: $e');
      throw Exception('Ortam verileri temizlenirken hata oluştu: $e');
    }
  }
}
