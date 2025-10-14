# i18n (Internationalization) Kullanım Rehberi

## Mimari Özet

Modelin "kanonik dili" **İngilizce**'dir. TR/EN dil desteği, backend'de iki adaptör katmanı ile sağlanır:

```
Frontend (TR) → Request Adaptör → Model (EN) → Response Adaptör → Frontend (TR)
```

## Dosya Yapısı

- **`backend/utils/i18n.py`** - i18n adaptör modülü
- **Entegrasyon**: `backend/routes/recommendations.py`

---

## API Kullanımı

### 1. Field Options (Dropdown Seçenekleri)

**Endpoint**: `GET /api/recommendations/field-options`

**Query Parameters**:
- `field`: crop, region, soil_type, fertilizer_type, irrigation_method, weather_condition
- `language`: tr veya en (default: tr)

**Örnek**:
```bash
# Türkçe ürünler
curl "http://localhost:5000/api/recommendations/field-options?field=crop&language=tr"

# Response:
{
  "success": true,
  "data": {
    "field": "crop",
    "language": "tr",
    "options": ["armut", "arpa", "bugday", "domates", "elma", ...]
  }
}
```

---

### 2. Environment Data (Otomatik Çeviri)

**Endpoint**: `POST /api/recommendations/environment-data`

**Request Body**:
```json
{
  "bolge": "ege",
  "toprak_tipi": "kumlu",
  "gubre_tipi": "organik",
  "sulama_yontemi": "damla",
  "hava_durumu": "gunesli",
  "language": "tr"
}
```

**Nasıl Çalışır**:
1. Backend Türkçe field adlarını algılar (`bolge`, `toprak_tipi`)
2. Kategorik değerleri İngilizce'ye çevirir (`ege` → `Aegean`, `kumlu` → `sandy`)
3. Model canonical English veriyi görür
4. Response target dilde döner

**Response**:
```json
{
  "success": true,
  "message": "Çevre bilgileri başarıyla kaydedildi",
  "data": {
    "region": "ege",              // Türkçe'ye geri çevrildi
    "soil_type": "kumlu",
    "fertilizer_type": "organik",
    "irrigation_method": "damla",
    "weather_condition": "gunesli",
    "saved_at": "2025-10-14T...",
    "canonical_format": {          // Debug için canonical format
      "region": "Aegean",
      "soil_type": "sandy",
      "fertilizer_type": "organic",
      "irrigation_method": "drip",
      "weather_condition": "sunny"
    }
  }
}
```

---

## Desteklenen Çeviriler

### Field Names (TR → EN)

| Türkçe | İngilizce |
|--------|-----------|
| toprak_ph | soil_ph |
| azot | nitrogen |
| fosfor | phosphorus |
| potasyum | potassium |
| nem | moisture |
| sicaklik | temperature_celsius |
| yagis | rainfall_mm |
| bolge | region |
| toprak_tipi | soil_type |
| gubre_tipi | fertilizer_type |
| sulama_yontemi | irrigation_method |
| hava_durumu | weather_condition |
| urun | crop |

### Categorical Values

#### Crops (Ürünler)
```
bugday → wheat        arpa → barley         misir → maize
pirinc → rice         patates → potato      domates → tomato
biber → pepper        patlican → eggplant   salatalik → cucumber
kabak → pumpkin       kavun → melon         karpuz → watermelon
uzum → grapes         elma → apple          armut → pear
kiraz → cherry
```

#### Regions (Bölgeler)
```
marmara → Marmara
ege → Aegean
akdeniz → Mediterranean
karadeniz → Black Sea
ic anadolu → Central Anatolia
dogu anadolu → Eastern Anatolia
guneydogu anadolu → Southeastern Anatolia
```

#### Soil Types (Toprak Tipleri)
```
kumlu → sandy
killi → clayey
tinli → loamy
siltli → silty
```

#### Fertilizer Types (Gübre Tipleri)
```
azotlu → nitrogenous
fosforlu → phosphatic
potasyumlu → potassic
organik → organic
kimyasal → chemical
yok → none
```

#### Irrigation Methods (Sulama Yöntemleri)
```
damla → drip
yagmurlama → sprinkler
salma → flood
yok → none
```

#### Weather Conditions (Hava Durumu)
```
gunesli → sunny
bulutlu → cloudy
yagmurlu → rainy
```

---

## Python API (Backend)

### Fonksiyonlar

```python
from utils.i18n import adapt_request, adapt_response, get_field_options, detect_language

# 1. Request adaptörü (TR → EN)
turkish_data = {'bolge': 'ege', 'toprak_tipi': 'kumlu'}
canonical = adapt_request(turkish_data, source_lang='tr')
# → {'region': 'Aegean', 'soil_type': 'sandy'}

# 2. Response adaptörü (EN → TR)
english_data = {'crop': 'wheat', 'region': 'Aegean'}
localized = adapt_response(english_data, target_lang='tr')
# → {'crop': 'bugday', 'region': 'ege'}

# 3. Field seçenekleri
crops_tr = get_field_options('crop', language='tr')
# → ['armut', 'arpa', 'bugday', ...]

crops_en = get_field_options('crop', language='en')
# → ['apple', 'barley', 'wheat', ...]

# 4. Dil algılama
lang = detect_language({'bolge': 'ege'})
# → 'tr'
```

---

## Frontend Kullanımı (Flutter/Dart)

```dart
// 1. Dropdown seçenekleri getir
final response = await http.get(
  Uri.parse('http://localhost:5000/api/recommendations/field-options?field=crop&language=tr'),
);
final options = jsonDecode(response.body)['data']['options'];
// → ['armut', 'arpa', 'bugday', ...]

// 2. Türkçe veri gönder
final envData = {
  'bolge': 'ege',
  'toprak_tipi': 'kumlu',
  'gubre_tipi': 'organik',
  'sulama_yontemi': 'damla',
  'hava_durumu': 'gunesli',
  'language': 'tr', // Response dilini belirt
};

final response = await http.post(
  Uri.parse('http://localhost:5000/api/recommendations/environment-data'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode(envData),
);

// Backend otomatik olarak çeviri yapar, model İngilizce görür
```

---

## Avantajlar

1. **Model Bağımsız**: Model kodu hiç değişmez, her zaman İngilizce görür
2. **Tek Kaynak**: Tüm çeviriler `i18n.py` dosyasında
3. **Otomatik**: Adaptör katmanı otomatik algılar ve çevirir
4. **Esneklik**: İstediğiniz dilde request gönder, istediğiniz dilde response al
5. **Debug Friendly**: `canonical_format` ile hangi veriyi gördüğünü görebilirsiniz

---

## Yeni Dil/Kategori Ekleme

### Yeni kategori eklemek:
```python
# backend/utils/i18n.py içinde
CATEGORIES = {
    'crop': {...},
    'yeni_kategori': {  # Yeni ekle
        'tr_deger1': 'en_value1',
        'tr_deger2': 'en_value2',
    }
}
```

### Yeni dil eklemek (örn. Arapça):
```python
CATEGORIES_AR_TO_EN = {
    'crop': {
        'قمح': 'wheat',
        'شعير': 'barley',
    }
}

def adapt_request_ar(data, source_lang='ar'):
    # Arapça → İngilizce adaptör
    pass
```

---

## Test

```bash
# 1. Field options test
curl "http://localhost:5000/api/recommendations/field-options?field=crop&language=tr"

# 2. Environment data test (Türkçe)
curl -X POST http://localhost:5000/api/recommendations/environment-data \
  -H "Content-Type: application/json" \
  -d @test_request.json

# 3. Logs kontrol
docker-compose logs backend --tail=20
```

**Test dosyası** (`test_request.json`):
```json
{
  "bolge": "ege",
  "toprak_tipi": "kumlu",
  "gubre_tipi": "organik",
  "sulama_yontemi": "damla",
  "hava_durumu": "gunesli",
  "language": "tr"
}
```

---

**Hazırlayan**: Terramind Development Team  
**Tarih**: 2025-10-14  
**Versiyon**: 1.0.0

