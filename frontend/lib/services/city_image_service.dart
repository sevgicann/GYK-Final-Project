class CityImageService {
  static const String _basePath = 'assets/images/cities';
  
  // Türkiye'nin 81 ili için fotoğraf yolları
  static const Map<String, String> _cityImages = {
    'Adana': '$_basePath/adana.jpg',
    'Adıyaman': '$_basePath/adiyaman.jpg',
    'Afyonkarahisar': '$_basePath/afyonkarahisar.jpg',
    'Ağrı': '$_basePath/agri.jpg',
    'Amasya': '$_basePath/amasya.jpg',
    'Ankara': '$_basePath/ankara.jpg',
    'Antalya': '$_basePath/antalya.jpg',
    'Artvin': '$_basePath/artvin.jpg',
    'Aydın': '$_basePath/aydin.jpg',
    'Balıkesir': '$_basePath/balikesir.jpg',
    'Bilecik': '$_basePath/bilecik.jpg',
    'Bingöl': '$_basePath/bingol.jpg',
    'Bitlis': '$_basePath/bitlis.jpg',
    'Bolu': '$_basePath/bolu.jpg',
    'Burdur': '$_basePath/burdur.jpg',
    'Bursa': '$_basePath/bursa.jpg',
    'Çanakkale': '$_basePath/canakkale.jpg',
    'Çankırı': '$_basePath/cankiri.jpg',
    'Çorum': '$_basePath/corum.jpg',
    'Denizli': '$_basePath/denizli.jpg',
    'Diyarbakır': '$_basePath/diyarbakir.jpg',
    'Edirne': '$_basePath/edirne.jpg',
    'Elazığ': '$_basePath/elazig.jpg',
    'Erzincan': '$_basePath/erzincan.jpg',
    'Erzurum': '$_basePath/erzurum.jpg',
    'Eskişehir': '$_basePath/eskisehir.jpg',
    'Gaziantep': '$_basePath/gaziantep.jpg',
    'Giresun': '$_basePath/giresun.jpg',
    'Gümüşhane': '$_basePath/gumushane.jpg',
    'Hakkâri': '$_basePath/hakkari.jpg',
    'Hatay': '$_basePath/hatay.jpg',
    'Isparta': '$_basePath/isparta.jpg',
    'Mersin': '$_basePath/mersin.jpg',
    'İstanbul': '$_basePath/istanbul.jpg',
    'İzmir': '$_basePath/izmir.jpg',
    'Kars': '$_basePath/kars.jpg',
    'Kastamonu': '$_basePath/kastamonu.jpg',
    'Kayseri': '$_basePath/kayseri.jpg',
    'Kırklareli': '$_basePath/kirklareli.jpg',
    'Kırşehir': '$_basePath/kirsehir.jpg',
    'Kocaeli': '$_basePath/kocaeli.jpg',
    'Konya': '$_basePath/konya.jpg',
    'Kütahya': '$_basePath/kutahya.jpg',
    'Malatya': '$_basePath/malatya.jpg',
    'Manisa': '$_basePath/manisa.jpg',
    'Kahramanmaraş': '$_basePath/kahramanmaras.jpg',
    'Mardin': '$_basePath/mardin.jpg',
    'Muğla': '$_basePath/mugla.jpg',
    'Muş': '$_basePath/mus.jpg',
    'Nevşehir': '$_basePath/nevsehir.jpg',
    'Niğde': '$_basePath/nigde.jpg',
    'Ordu': '$_basePath/ordu.jpg',
    'Rize': '$_basePath/rize.jpg',
    'Sakarya': '$_basePath/sakarya.jpg',
    'Samsun': '$_basePath/samsun.jpg',
    'Siirt': '$_basePath/siirt.jpg',
    'Sinop': '$_basePath/sinop.jpg',
    'Sivas': '$_basePath/sivas.jpg',
    'Tekirdağ': '$_basePath/tekirdag.jpg',
    'Tokat': '$_basePath/tokat.jpg',
    'Trabzon': '$_basePath/trabzon.jpg',
    'Tunceli': '$_basePath/tunceli.jpg',
    'Şanlıurfa': '$_basePath/sanliurfa.jpg',
    'Uşak': '$_basePath/usak.jpg',
    'Van': '$_basePath/van.jpg',
    'Yozgat': '$_basePath/yozgat.jpg',
    'Zonguldak': '$_basePath/zonguldak.jpg',
    'Aksaray': '$_basePath/aksaray.jpg',
    'Bayburt': '$_basePath/bayburt.jpg',
    'Karaman': '$_basePath/karaman.jpg',
    'Kırıkkale': '$_basePath/kirikkale.jpg',
    'Batman': '$_basePath/batman.jpg',
    'Şırnak': '$_basePath/sirnak.jpg',
    'Bartın': '$_basePath/bartin.jpg',
    'Ardahan': '$_basePath/ardahan.jpg',
    'Iğdır': '$_basePath/igdir.jpg',
    'Yalova': '$_basePath/yalova.jpg',
    'Karabük': '$_basePath/karabuk.jpg',
    'Kilis': '$_basePath/kilis.jpg',
    'Osmaniye': '$_basePath/osmaniye.jpg',
    'Düzce': '$_basePath/duzce.jpg',
  };

  /// Şehir adına göre fotoğraf yolunu döndürür
  static String? getCityImagePath(String cityName) {
    return _cityImages[cityName];
  }

  /// Tüm şehir fotoğraflarının listesini döndürür
  static List<String> getAllCityNames() {
    return _cityImages.keys.toList();
  }

  /// Şehir fotoğrafının var olup olmadığını kontrol eder
  static bool hasCityImage(String cityName) {
    return _cityImages.containsKey(cityName);
  }

  /// Varsayılan şehir fotoğrafı (şehir bulunamadığında)
  static const String defaultCityImage = '$_basePath/default_city.jpg';
}
