import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import '../core/config/api_config.dart';

class PDFService {
  static const String _baseUrl = ApiConfig.baseUrl;
  
  /// Generate environment recommendation PDF
  static Future<Map<String, dynamic>> generateEnvironmentReport({
    required String crop,
    required String location,
    required String region,
    required String soilType,
    required String irrigationMethod,
    required String fertilizerType,
    required String sunlight,
    String? token,
  }) async {
    try {
      final url = Uri.parse('$_baseUrl/api/pdf/generate-environment-report');
      
      final headers = <String, String>{
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };
      
      final body = {
        'crop': crop,
        'location': location,
        'region': region,
        'soil_type': soilType,
        'irrigation_method': irrigationMethod,
        'fertilizer_type': fertilizerType,
        'sunlight': sunlight,
      };
      
      print('📄 Generating environment PDF report...');
      print('  Crop: $crop');
      print('  Location: $location');
      print('  Region: $region');
      
      final response = await http.post(
        url,
        headers: headers,
        body: json.encode(body),
      );
      
      if (response.statusCode == 200) {
        // PDF file received
        final pdfBytes = response.bodyBytes;
        
        // Save PDF to device
        final fileName = 'environment_report_${crop.toLowerCase()}_${DateTime.now().millisecondsSinceEpoch}.pdf';
        final savedPath = await _savePdfToDevice(pdfBytes, fileName);
        
        return {
          'success': true,
          'file_path': savedPath,
          'file_name': fileName,
          'message': 'PDF raporu başarıyla oluşturuldu',
        };
      } else {
        // Error response
        final errorData = response.body;
        return {
          'success': false,
          'error': 'HTTP ${response.statusCode}',
          'message': 'PDF oluşturulurken hata oluştu: HTTP ${response.statusCode}',
          'details': errorData,
        };
      }
    } catch (e) {
      print('❌ Error generating environment PDF: $e');
      return {
        'success': false,
        'error': e.toString(),
        'message': 'PDF oluşturulurken hata oluştu: $e',
      };
    }
  }
  
  /// Generate crop recommendation PDF using LLM
  static Future<Map<String, dynamic>> generateCropRecommendationReport({
    required String location,
    required String region,
    required String soilType,
    required String sunlight,
    required String irrigationMethod,
    required String fertilizer,
    required double ph,
    required double nitrogen,
    required double phosphorus,
    required double potassium,
    required double humidity,
    required double temperature,
    required double rainfall,
    required List<Map<String, dynamic>> recommendations,
    String? token,
  }) async {
    try {
      final url = Uri.parse('$_baseUrl/api/pdf/generate-crop-recommendation');
      
      final headers = <String, String>{
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };
      
      final body = {
        'location': location,
        'region': region,
        'soil_type': soilType,
        'sunlight': sunlight,
        'irrigation_method': irrigationMethod,
        'fertilizer_type': fertilizer,
        'ph': ph,
        'nitrogen': nitrogen,
        'phosphorus': phosphorus,
        'potassium': potassium,
        'humidity': humidity,
        'temperature': temperature,
        'rainfall': rainfall,
        'recommendations': recommendations,
      };
      
      print('📄 Generating crop PDF report...');
      print('  URL: $url');
      print('  Location: $location');
      print('  Region: $region');
      print('  Recommendations: ${recommendations.length} crops');
      
      final response = await http.post(
        url,
        headers: headers,
        body: json.encode(body),
      ).timeout(
        const Duration(seconds: 30),
        onTimeout: () {
          throw Exception('Request timeout - PDF generation took too long');
        },
      );
      
      print('📄 Response received:');
      print('  Status Code: ${response.statusCode}');
      print('  Response Body: ${response.body}');
      
      if (response.statusCode == 200) {
        final responseData = json.decode(response.body);
        
        if (responseData['success'] == true) {
          // Check if we have PDF content (base64 encoded)
          if (responseData['pdf_content'] != null) {
            // Save PDF to device
            final pdfBytes = base64Decode(responseData['pdf_content']);
            final filename = responseData['filename'] ?? 'crop_recommendation.pdf';
            final saved = await _savePdfToDevice(pdfBytes, filename);
            
            return {
              'success': true,
              'message': responseData['message'] ?? 'PDF raporu başarıyla oluşturuldu',
              'filename': filename,
              'saved': saved,
              'content_type': 'application/pdf',
            };
          } else if (responseData['content'] != null) {
            // Fallback to text content
            return {
              'success': true,
              'message': responseData['message'] ?? 'PDF raporu başarıyla oluşturuldu',
              'content': responseData['content'],
              'filename': responseData['filename'],
            };
          } else {
            return {
              'success': false,
              'error': 'No Content',
              'message': 'PDF içeriği alınamadı',
            };
          }
        } else {
          return {
            'success': false,
            'error': 'PDF Generation Failed',
            'message': responseData['message'] ?? 'PDF oluşturulurken hata oluştu',
            'details': responseData,
          };
        }
      } else {
        // Error response
        final errorData = response.body;
        print('❌ PDF generation failed:');
        print('  Status Code: ${response.statusCode}');
        print('  Response Body: $errorData');
        
        return {
          'success': false,
          'error': 'HTTP ${response.statusCode}',
          'message': 'PDF oluşturulurken hata oluştu: HTTP ${response.statusCode}',
          'details': errorData,
        };
      }
    } catch (e) {
      print('❌ Error generating crop PDF: $e');
      print('❌ Error type: ${e.runtimeType}');
      
      // Check if it's a network error
      if (e.toString().contains('Failed to fetch') || 
          e.toString().contains('ClientException')) {
        return {
          'success': false,
          'error': 'Network Error',
          'message': 'Backend sunucusuna bağlanılamadı. Lütfen backend\'in çalıştığından emin olun.',
          'details': e.toString(),
        };
      }
      
      return {
        'success': false,
        'error': e.toString(),
        'message': 'PDF oluşturulurken hata oluştu: $e',
      };
    }
  }
  
  /// Save PDF bytes to device storage
  static Future<String> _savePdfToDevice(Uint8List pdfBytes, String fileName) async {
    try {
      // Request storage permission
      final permission = await Permission.storage.request();
      if (!permission.isGranted) {
        throw Exception('Storage permission not granted');
      }
      
      // Get downloads directory
      Directory? directory;
      if (Platform.isAndroid) {
        directory = await getExternalStorageDirectory();
        if (directory != null) {
          directory = Directory('${directory.path}/Download');
          if (!await directory.exists()) {
            await directory.create(recursive: true);
          }
        }
      } else {
        directory = await getApplicationDocumentsDirectory();
      }
      
      if (directory == null) {
        throw Exception('Could not access storage directory');
      }
      
      // Create file
      final file = File('${directory.path}/$fileName');
      await file.writeAsBytes(pdfBytes);
      
      print('✅ PDF saved to: ${file.path}');
      return file.path;
    } catch (e) {
      print('❌ Error saving PDF: $e');
      throw Exception('Failed to save PDF: $e');
    }
  }
  
  /// Check PDF service health
  static Future<Map<String, dynamic>> checkHealth() async {
    try {
      final url = Uri.parse('$_baseUrl/api/pdf/health');
      
      final response = await http.get(url);
      
      if (response.statusCode == 200) {
        return {
          'success': true,
          'status': 'healthy',
          'message': 'PDF service is operational',
        };
      } else {
        return {
          'success': false,
          'status': 'unhealthy',
          'message': 'PDF service is not operational',
          'error': 'HTTP ${response.statusCode}',
        };
      }
    } catch (e) {
      return {
        'success': false,
        'status': 'error',
        'message': 'Could not check PDF service health',
        'error': e.toString(),
      };
    }
  }
}
