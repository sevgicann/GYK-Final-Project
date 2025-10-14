"""
i18n (Internationalization) Module
Handles translation between Turkish and English for ML model integration
Following canonical contract approach - model always sees English
"""

# ============================================================================
# CANONICAL MAPPINGS (TR ↔ EN)
# ============================================================================

# Field names mapping (TR → EN)
FIELD_NAMES_TR_TO_EN = {
    'toprak_ph': 'soil_ph',
    'azot': 'nitrogen',
    'fosfor': 'phosphorus',
    'potasyum': 'potassium',
    'nem': 'moisture',
    'sicaklik': 'temperature_celsius',
    'yagis': 'rainfall_mm',
    'bolge': 'region',
    'toprak_tipi': 'soil_type',
    'gubre_tipi': 'fertilizer_type',
    'sulama_yontemi': 'irrigation_method',
    'hava_durumu': 'weather_condition',
    'urun': 'crop',
}

# Categorical values mapping (TR → EN)
CATEGORIES = {
    'crop': {
        'bugday': 'wheat', 'arpa': 'barley', 'misir': 'maize', 'pirinc': 'rice',
        'patates': 'potato', 'domates': 'tomato', 'biber': 'pepper',
        'patlican': 'eggplant', 'salatalik': 'cucumber', 'kabak': 'pumpkin',
        'kavun': 'melon', 'karpuz': 'watermelon', 'uzum': 'grapes',
        'elma': 'apple', 'armut': 'pear', 'kiraz': 'cherry',
    },
    'region': {
        'marmara': 'Marmara', 'ege': 'Aegean', 'akdeniz': 'Mediterranean',
        'karadeniz': 'Black Sea', 'ic anadolu': 'Central Anatolia',
        'dogu anadolu': 'Eastern Anatolia', 'guneydogu anadolu': 'Southeastern Anatolia',
    },
    'soil_type': {
        'kumlu': 'sandy', 'killi': 'clayey', 'tinli': 'loamy', 'siltli': 'silty',
    },
    'fertilizer_type': {
        'azotlu': 'nitrogenous', 'fosforlu': 'phosphatic', 'potasyumlu': 'potassic',
        'organik': 'organic', 'kimyasal': 'chemical', 'yok': 'none',
    },
    'irrigation_method': {
        'damla': 'drip', 'yagmurlama': 'sprinkler', 'salma': 'flood', 'yok': 'none',
    },
    'weather_condition': {
        'gunesli': 'sunny', 'bulutlu': 'cloudy', 'yagmurlu': 'rainy',
    },
}

# Reverse mappings (EN → TR)
FIELD_NAMES_EN_TO_TR = {v: k for k, v in FIELD_NAMES_TR_TO_EN.items()}
CATEGORIES_EN_TO_TR = {
    category: {v: k for k, v in mappings.items()}
    for category, mappings in CATEGORIES.items()
}

# ============================================================================
# ADAPTER FUNCTIONS
# ============================================================================

def adapt_request(data: dict, source_lang: str = 'tr') -> dict:
    """
    Adapt incoming request to canonical English format
    
    Args:
        data: Request data (possibly in Turkish)
        source_lang: Source language ('tr' or 'en')
        
    Returns:
        Canonical English format data
    """
    if source_lang == 'en':
        return data  # Already canonical
    
    adapted = {}
    
    for key, value in data.items():
        # 1. Translate field names (TR → EN)
        canonical_key = FIELD_NAMES_TR_TO_EN.get(key.lower(), key)
        
        # 2. Translate categorical values if applicable
        if isinstance(value, str):
            value_lower = value.lower().strip()
            canonical_value = value  # Default to original
            
            # Try to find in categorical mappings
            for category, mappings in CATEGORIES.items():
                if value_lower in mappings:
                    canonical_value = mappings[value_lower]
                    break
            
            adapted[canonical_key] = canonical_value
        else:
            adapted[canonical_key] = value
    
    return adapted


def adapt_response(data: dict, target_lang: str = 'tr') -> dict:
    """
    Adapt canonical English response to target language
    
    Args:
        data: Response data in canonical English
        target_lang: Target language ('tr' or 'en')
        
    Returns:
        Localized response data
    """
    if target_lang == 'en':
        return data  # Already canonical
    
    adapted = {}
    
    for key, value in data.items():
        # 1. Translate field names (EN → TR) if requested
        # For now, keep field names in English for API consistency
        
        # 2. Translate categorical values
        if isinstance(value, str):
            value_lower = value.lower().strip()
            
            # Check categorical mappings
            for category, mappings in CATEGORIES_EN_TO_TR.items():
                if category in key.lower():
                    localized_value = mappings.get(value_lower, value)
                    adapted[key] = localized_value.title() if localized_value else value
                    break
            else:
                adapted[key] = value
        else:
            adapted[key] = value
    
    return adapted


def get_field_options(field_name: str, language: str = 'tr') -> list:
    """
    Get available options for a categorical field
    
    Args:
        field_name: Field name (crop, region, soil_type, etc.)
        language: Target language ('tr' or 'en')
        
    Returns:
        List of options in target language
    """
    if field_name not in CATEGORIES:
        return []
    
    if language == 'en':
        return sorted(set(CATEGORIES[field_name].values()))
    else:  # Turkish
        return sorted(set(CATEGORIES[field_name].keys()))


def detect_language(data: dict) -> str:
    """
    Detect if request data is in Turkish or English
    
    Args:
        data: Request data
        
    Returns:
        Detected language code ('tr' or 'en')
    """
    # Check field names
    for key in data.keys():
        if key.lower() in FIELD_NAMES_TR_TO_EN:
            return 'tr'
    
    # Check categorical values
    for value in data.values():
        if isinstance(value, str):
            value_lower = value.lower().strip()
            for mappings in CATEGORIES.values():
                if value_lower in mappings:
                    return 'tr'
    
    return 'en'  # Default to English


# ============================================================================
# DECORATOR FOR AUTO-TRANSLATION
# ============================================================================

def with_i18n(func):
    """
    Decorator to automatically handle i18n for API endpoints
    
    Usage:
        @with_i18n
        def predict_crop(data):
            # data will be in canonical English
            # return value will be translated to user's language
    """
    from functools import wraps
    from flask import request
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json() if request.is_json else {}
        
        # Get target language from request
        target_lang = data.pop('language', 'tr')
        
        # Detect source language and adapt to canonical
        source_lang = detect_language(data)
        canonical_data = adapt_request(data, source_lang)
        
        # Call original function with canonical data
        result = func(canonical_data, *args, **kwargs)
        
        # Adapt response to target language
        if isinstance(result, dict):
            result['data'] = adapt_response(result.get('data', {}), target_lang)
        
        return result
    
    return wrapper

