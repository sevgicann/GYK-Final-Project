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

  // Şehir görselleri için local assets yolları
  final Map<String, String> _cityImages = {
    'Adana': 'assets/images/cities/adana.jpg',
    'Adıyaman': 'assets/images/cities/adiyaman.jpg',
    'Afyonkarahisar': 'assets/images/cities/afyonkarahisar.jpg',
    'Ağrı': 'assets/images/cities/agri.jpg',
    'Amasya': 'assets/images/cities/amasya.jpg',
    'Ankara': 'assets/images/cities/ankara.jpg',
    'Antalya': 'assets/images/cities/antalya.jpg',
    'Artvin': 'assets/images/cities/artvin.jpg',
    'Aydın': 'assets/images/cities/aydin.jpg',
    'Balıkesir': 'assets/images/cities/balikesir.jpg',
    'Bilecik': 'assets/images/cities/bilecik.jpg',
    'Bingöl': 'assets/images/cities/bingol.jpg',
    'Bitlis': 'assets/images/cities/bitlis.jpg',
    'Bolu': 'assets/images/cities/bolu.jpg',
    'Burdur': 'assets/images/cities/burdur.jpg',
    'Bursa': 'assets/images/cities/bursa.jpg',
    'Çanakkale': 'assets/images/cities/canakkale.jpg',
    'Çankırı': 'assets/images/cities/cankiri.jpg',
    'Çorum': 'assets/images/cities/corum.jpg',
    'Denizli': 'assets/images/cities/denizli.jpg',
    'Diyarbakır': 'assets/images/cities/diyarbakir.jpg',
    'Edirne': 'assets/images/cities/edirne.jpg',
    'Elazığ': 'assets/images/cities/elazig.jpg',
    'Erzincan': 'assets/images/cities/erzincan.jpg',
    'Erzurum': 'assets/images/cities/erzurum.jpg',
    'Eskişehir': 'assets/images/cities/eskisehir.jpg',
    'Gaziantep': 'assets/images/cities/gaziantep.jpg',
    'Giresun': 'assets/images/cities/giresun.jpg',
    'Gümüşhane': 'assets/images/cities/gumushane.jpg',
    'Hakkâri': 'assets/images/cities/hakkari.jpg',
    'Hatay': 'assets/images/cities/hatay.jpg',
    'Isparta': 'assets/images/cities/isparta.jpg',
    'Mersin': 'assets/images/cities/mersin.jpg',
    'İstanbul': 'assets/images/cities/istanbul.jpg',
    'İzmir': 'assets/images/cities/izmir.jpg',
    'Kars': 'assets/images/cities/kars.jpg',
    'Kastamonu': 'assets/images/cities/kastamonu.jpg',
    'Kayseri': 'assets/images/cities/kayseri.jpg',
    'Kırklareli': 'assets/images/cities/kirklareli.jpg',
    'Kırşehir': 'assets/images/cities/kirsehir.jpg',
    'Kocaeli': 'assets/images/cities/kocaeli.jpg',
    'Konya': 'assets/images/cities/konya.jpg',
    'Kütahya': 'assets/images/cities/kutahya.jpg',
    'Malatya': 'assets/images/cities/malatya.jpg',
    'Manisa': 'assets/images/cities/manisa.jpg',
    'Kahramanmaraş': 'assets/images/cities/kahramanmaras.jpg',
    'Mardin': 'assets/images/cities/mardin.jpg',
    'Muğla': 'assets/images/cities/mugla.jpg',
    'Muş': 'assets/images/cities/mus.jpg',
    'Nevşehir': 'assets/images/cities/nevsehir.jpg',
    'Niğde': 'assets/images/cities/nigde.jpg',
    'Ordu': 'assets/images/cities/ordu.jpg',
    'Rize': 'assets/images/cities/rize.jpg',
    'Sakarya': 'assets/images/cities/sakarya.jpg',
    'Samsun': 'assets/images/cities/samsun.jpg',
    'Siirt': 'assets/images/cities/siirt.jpg',
    'Sinop': 'assets/images/cities/sinop.jpg',
    'Sivas': 'assets/images/cities/sivas.jpg',
    'Tekirdağ': 'assets/images/cities/tekirdag.jpg',
    'Tokat': 'assets/images/cities/tokat.jpg',
    'Trabzon': 'assets/images/cities/trabzon.jpg',
    'Tunceli': 'assets/images/cities/tunceli.jpg',
    'Şanlıurfa': 'assets/images/cities/sanliurfa.jpg',
    'Uşak': 'assets/images/cities/usak.jpg',
    'Van': 'assets/images/cities/van.jpg',
    'Yozgat': 'assets/images/cities/yozgat.jpg',
    'Zonguldak': 'assets/images/cities/zonguldak.jpg',
    'Aksaray': 'assets/images/cities/aksaray.jpg',
    'Bayburt': 'assets/images/cities/bayburt.jpg',
    'Karaman': 'assets/images/cities/karaman.jpg',
    'Kırıkkale': 'assets/images/cities/kirikkale.jpg',
    'Batman': 'assets/images/cities/batman.jpg',
    'Şırnak': 'assets/images/cities/sirnak.jpg',
    'Bartın': 'assets/images/cities/bartin.jpg',
    'Ardahan': 'assets/images/cities/ardahan.jpg',
    'Iğdır': 'assets/images/cities/igdir.jpg',
    'Yalova': 'assets/images/cities/yalova.jpg',
    'Karabük': 'assets/images/cities/karabuk.jpg',
    'Kilis': 'assets/images/cities/kilis.jpg',
    'Osmaniye': 'assets/images/cities/osmaniye.jpg',
    'Düzce': 'assets/images/cities/duzce.jpg',
  };

  static const String defaultCityImage = 'assets/images/cities/default_city.jpg';

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
