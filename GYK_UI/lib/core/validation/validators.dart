class Validators {
  // Email validation
  static String? email(String? value) {
    if (value == null || value.isEmpty) {
      return 'E-posta gereklidir';
    }
    
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    if (!emailRegex.hasMatch(value)) {
      return 'Geçerli bir e-posta adresi girin';
    }
    
    return null;
  }

  // Password validation
  static String? password(String? value) {
    if (value == null || value.isEmpty) {
      return 'Şifre gereklidir';
    }
    
    if (value.length < 6) {
      return 'Şifre en az 6 karakter olmalıdır';
    }
    
    if (value.length > 50) {
      return 'Şifre en fazla 50 karakter olabilir';
    }
    
    return null;
  }

  // Confirm password validation
  static String? confirmPassword(String? value, String? password) {
    if (value == null || value.isEmpty) {
      return 'Şifre tekrarı gereklidir';
    }
    
    if (value != password) {
      return 'Şifreler eşleşmiyor';
    }
    
    return null;
  }

  // Name validation
  static String? name(String? value) {
    if (value == null || value.isEmpty) {
      return 'Ad Soyad gereklidir';
    }
    
    if (value.length < 2) {
      return 'Ad Soyad en az 2 karakter olmalıdır';
    }
    
    if (value.length > 50) {
      return 'Ad Soyad en fazla 50 karakter olabilir';
    }
    
    // Sadece harf ve boşluk karakterlerine izin ver
    final nameRegex = RegExp(r'^[a-zA-ZğüşıöçĞÜŞİÖÇ\s]+$');
    if (!nameRegex.hasMatch(value)) {
      return 'Ad Soyad sadece harf içerebilir';
    }
    
    return null;
  }

  // Required field validation
  static String? required(String? value, String fieldName) {
    if (value == null || value.isEmpty) {
      return '$fieldName gereklidir';
    }
    return null;
  }

  // Phone number validation
  static String? phoneNumber(String? value) {
    if (value == null || value.isEmpty) {
      return 'Telefon numarası gereklidir';
    }
    
    // Türkiye telefon numarası formatı
    final phoneRegex = RegExp(r'^(\+90|0)?[5][0-9]{9}$');
    if (!phoneRegex.hasMatch(value.replaceAll(' ', '').replaceAll('-', ''))) {
      return 'Geçerli bir telefon numarası girin';
    }
    
    return null;
  }

  // Numeric validation
  static String? numeric(String? value, String fieldName) {
    if (value == null || value.isEmpty) {
      return '$fieldName gereklidir';
    }
    
    if (double.tryParse(value) == null) {
      return '$fieldName sayısal bir değer olmalıdır';
    }
    
    return null;
  }

  // Range validation
  static String? range(String? value, double min, double max, String fieldName) {
    final numericError = numeric(value, fieldName);
    if (numericError != null) return numericError;
    
    final numValue = double.parse(value!);
    if (numValue < min || numValue > max) {
      return '$fieldName $min ile $max arasında olmalıdır';
    }
    
    return null;
  }

  // URL validation
  static String? url(String? value) {
    if (value == null || value.isEmpty) {
      return 'URL gereklidir';
    }
    
    final urlRegex = RegExp(
      r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    );
    
    if (!urlRegex.hasMatch(value)) {
      return 'Geçerli bir URL girin';
    }
    
    return null;
  }

  // Custom validation
  static String? custom(String? value, bool Function(String) validator, String errorMessage) {
    if (value == null || value.isEmpty) {
      return 'Bu alan gereklidir';
    }
    
    if (!validator(value)) {
      return errorMessage;
    }
    
    return null;
  }

  // Multiple validators
  static String? multiple(String? value, List<String? Function(String?)> validators) {
    for (final validator in validators) {
      final result = validator(value);
      if (result != null) {
        return result;
      }
    }
    return null;
  }
}

class FormValidator {
  final Map<String, String? Function(String?)> _validators = {};

  FormValidator addField(String fieldName, String? Function(String?) validator) {
    _validators[fieldName] = validator;
    return this;
  }

  Map<String, String?> validate(Map<String, String?> values) {
    final errors = <String, String?>{};
    
    for (final entry in _validators.entries) {
      final fieldName = entry.key;
      final validator = entry.value;
      final value = values[fieldName];
      
      final error = validator(value);
      if (error != null) {
        errors[fieldName] = error;
      }
    }
    
    return errors;
  }

  bool isValid(Map<String, String?> values) {
    return validate(values).isEmpty;
  }
}
