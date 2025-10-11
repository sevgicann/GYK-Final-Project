class ImageService {
  static final ImageService _instance = ImageService._internal();
  factory ImageService() => _instance;
  ImageService._internal();

  // Ürün görselleri için placeholder URL'ler
  // Gerçek uygulamada bu URL'ler gerçek görsellerle değiştirilecek
  final Map<String, String> _productImages = {
    'Havuç': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=300&fit=crop&auto=format',
    'Domates': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300&h=300&fit=crop&auto=format',
    'Patates': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300&h=300&fit=crop&auto=format',
    'Soğan': 'https://images.unsplash.com/photo-1518977956812-cd3dbadaaf31?w=300&h=300&fit=crop&auto=format',
    'Biber': 'https://images.unsplash.com/photo-1566385101042-1a0aa0c1268c?w=300&h=300&fit=crop&auto=format',
    'Salatalık': 'https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=300&h=300&fit=crop&auto=format',
    'Marul': 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=300&h=300&fit=crop&auto=format',
    'Ispanak': 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=300&h=300&fit=crop&auto=format',
    'Brokoli': 'https://images.unsplash.com/photo-1584270354949-c26b0d5b4a0c?w=300&h=300&fit=crop&auto=format',
    'Karnabahar': 'https://images.unsplash.com/photo-1584270354949-c26b0d5b4a0c?w=300&h=300&fit=crop&auto=format',
    'Mısır': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=300&h=300&fit=crop&auto=format',
    'Pirinç': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=300&fit=crop&auto=format',
  };

  // Varsayılan ürün görseli
  static const String defaultProductImage = 'https://images.unsplash.com/photo-1584270354949-c26b0d5b4a0c?w=300&h=300&fit=crop&auto=format';

  String getProductImage(String productName) {
    return _productImages[productName] ?? defaultProductImage;
  }

  // Şehir görselleri için placeholder URL'ler
  final Map<String, String> _cityImages = {
    'İstanbul': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=300&h=200&fit=crop',
    'Ankara': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
    'İzmir': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
    'Antalya': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
    'Bursa': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
    'Konya': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
    'Adana': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
    'Gaziantep': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
    'Kayseri': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
    'Mersin': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop',
  };

  static const String defaultCityImage = 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop';

  String getCityImage(String cityName) {
    return _cityImages[cityName] ?? defaultCityImage;
  }

  // Görsel yükleme durumu için
  bool isImageLoaded = false;
  String? loadingError;

  void setImageLoaded(bool loaded) {
    isImageLoaded = loaded;
  }

  void setLoadingError(String? error) {
    loadingError = error;
  }
}
