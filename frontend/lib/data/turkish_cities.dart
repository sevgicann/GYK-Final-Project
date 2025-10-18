class TurkishCities {
  static const List<String> cities = [
    'Adana',
    'Adıyaman',
    'Afyonkarahisar',
    'Ağrı',
    'Amasya',
    'Ankara',
    'Antalya',
    'Artvin',
    'Aydın',
    'Balıkesir',
    'Bilecik',
    'Bingöl',
    'Bitlis',
    'Bolu',
    'Burdur',
    'Bursa',
    'Çanakkale',
    'Çankırı',
    'Çorum',
    'Denizli',
    'Diyarbakır',
    'Edirne',
    'Elazığ',
    'Erzincan',
    'Erzurum',
    'Eskişehir',
    'Gaziantep',
    'Giresun',
    'Gümüşhane',
    'Hakkâri',
    'Hatay',
    'Isparta',
    'Mersin',
    'İstanbul',
    'İzmir',
    'Kars',
    'Kastamonu',
    'Kayseri',
    'Kırklareli',
    'Kırşehir',
    'Kocaeli',
    'Konya',
    'Kütahya',
    'Malatya',
    'Manisa',
    'Kahramanmaraş',
    'Mardin',
    'Muğla',
    'Muş',
    'Nevşehir',
    'Niğde',
    'Ordu',
    'Rize',
    'Sakarya',
    'Samsun',
    'Siirt',
    'Sinop',
    'Sivas',
    'Tekirdağ',
    'Tokat',
    'Trabzon',
    'Tunceli',
    'Şanlıurfa',
    'Uşak',
    'Van',
    'Yozgat',
    'Zonguldak',
    'Aksaray',
    'Bayburt',
    'Karaman',
    'Kırıkkale',
    'Batman',
    'Şırnak',
    'Bartın',
    'Ardahan',
    'Iğdır',
    'Yalova',
    'Karabük',
    'Kilis',
    'Osmaniye',
    'Düzce',
  ];

  static List<String> getCitiesByRegion(String region) {
    switch (region) {
      case 'Marmara':
        return ['İstanbul', 'Bursa', 'Kocaeli', 'Sakarya', 'Bilecik', 'Tekirdağ', 'Edirne', 'Kırklareli', 'Balıkesir', 'Çanakkale', 'Yalova'];
      case 'Ege':
        return ['İzmir', 'Manisa', 'Aydın', 'Muğla', 'Denizli', 'Uşak', 'Afyonkarahisar', 'Kütahya'];
      case 'Akdeniz':
        return ['Antalya', 'Mersin', 'Adana', 'Hatay', 'Osmaniye', 'Kahramanmaraş', 'Isparta', 'Burdur'];
      case 'İç Anadolu':
        return ['Ankara', 'Konya', 'Niğde','Kayseri', 'Sivas', 'Eskişehir', 'Çankırı', 'Çorum', 'Yozgat', 'Nevşehir', 'Kırşehir', 'Aksaray', 'Kırıkkale', 'Karaman'];
      case 'Karadeniz':
        return ['Samsun', 'Trabzon', 'Bolu', 'Ordu', 'Giresun', 'Rize', 'Artvin', 'Gümüşhane', 'Bayburt', 'Kastamonu', 'Sinop', 'Çorum', 'Amasya', 'Tokat', 'Zonguldak', 'Bartın', 'Karabük', 'Düzce'];
      case 'Doğu Anadolu':
        return ['Erzurum', 'Erzincan', 'Ağrı', 'Kars', 'Iğdır', 'Ardahan', 'Van', 'Muş', 'Bitlis', 'Hakkâri', 'Malatya', 'Elazığ', 'Bingöl', 'Tunceli'];
      case 'Güneydoğu Anadolu':
        return ['Gaziantep', 'Şanlıurfa', 'Diyarbakır', 'Mardin', 'Batman', 'Siirt', 'Şırnak', 'Adıyaman', 'Kilis'];
      default:
        return cities;
    }
  }

  static String getRegionByCity(String city) {
    final marmaraCities = getCitiesByRegion('Marmara');
    final egeCities = getCitiesByRegion('Ege');
    final akdenizCities = getCitiesByRegion('Akdeniz');
    final icAnadoluCities = getCitiesByRegion('İç Anadolu');
    final karadenizCities = getCitiesByRegion('Karadeniz');
    final doguAnadoluCities = getCitiesByRegion('Doğu Anadolu');
    final guneydoguAnadoluCities = getCitiesByRegion('Güneydoğu Anadolu');

    if (marmaraCities.contains(city)) return 'Marmara';
    if (egeCities.contains(city)) return 'Ege';
    if (akdenizCities.contains(city)) return 'Akdeniz';
    if (icAnadoluCities.contains(city)) return 'İç Anadolu';
    if (karadenizCities.contains(city)) return 'Karadeniz';
    if (doguAnadoluCities.contains(city)) return 'Doğu Anadolu';
    if (guneydoguAnadoluCities.contains(city)) return 'Güneydoğu Anadolu';
    
    return 'Bilinmeyen';
  }
}
