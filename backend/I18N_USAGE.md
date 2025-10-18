# i18n Adaptör - Dil Desteği

## Mimari

Model her zaman **İngilizce** görür. TR ↔ EN çevirisi otomatik yapılır.

```
Frontend (TR) → i18n Adaptör → Model (EN) → i18n Adaptör → Frontend (TR)
```

---

## Dosyalar

- `backend/utils/i18n.py` - Adaptör modülü
- `backend/routes/recommendations.py` - API entegrasyonu (line 10, 122-183)

---

## API Kullanımı

### Endpoint: `/api/recommendations/environment-data`

**Request** (Türkçe):
```json
{
  "region": "İç Anadolu",
  "soil_type": "Killi Toprak",
  "fertilizer": "Amonyum Sülfat",
  "irrigation": "Damla Sulama",
  "sunlight": "Güneşli"
}
```

**Backend'e giden** (İngilizce - otomatik):
```json
{
  "region": "Central Anatolia",
  "soil_type": "Clay",
  "fertilizer_type": "Ammonium Sulphate",
  "irrigation_method": "Drip Irrigation",
  "weather_condition": "sunny"
}
```

---

## Mapping Tablosu

### Frontend Field Names → Canonical
| Frontend | Canonical (Model) |
|----------|-------------------|
| region | region |
| soil_type | soil_type |
| **fertilizer** | **fertilizer_type** |
| **irrigation** | **irrigation_method** |
| **sunlight** | **weather_condition** |

### Bölgeler (Regions)
| Türkçe | English |
|--------|---------|
| İç Anadolu | Central Anatolia |
| Marmara | Marmara |
| Ege | Aegean |
| Akdeniz | Mediterranean |
| Karadeniz | Black Sea |
| Doğu Anadolu | Eastern Anatolia |
| Güneydoğu Anadolu | Southeastern Anatolia |

### Toprak Tipleri (Soil Types)
| Türkçe | English |
|--------|---------|
| Killi Toprak | Clay |
| Kumlu Toprak | Sandy |
| Tınlı Toprak | Loamy |
| Siltli Toprak | Silty |
| Kireçli Toprak* | Loamy* |
| Asitli Toprak* | Sandy* |

*Veri setinde yok, fallback mapping

### Gübre Tipleri (Fertilizer Types)
| Türkçe | English |
|--------|---------|
| Potasyum Nitrat | Potassium Nitrate |
| Amonyum Sülfat | Ammonium Sulphate |
| Üre | Urea |
| Kompost* | Urea* |
| Organik Gübre* | Urea* |

*Veri setinde yok, fallback mapping

### Sulama Yöntemleri (Irrigation Methods)
| Türkçe | English |
|--------|---------|
| Salma Sulama | Flood Irrigation |
| Damla Sulama | Drip Irrigation |
| Yağmurlama | Sprinkler Irrigation |
| Sprinkler | Sprinkler Irrigation |
| Mikro Sulama | Drip Irrigation |

### Güneş Işığı / Hava Durumu (Weather Condition)
| Türkçe | English |
|--------|---------|
| Güneşli | sunny |
| Kısmi Gölge | cloudy |
| Gölgeli | cloudy |
| Tam Gölge | cloudy |
| Yağmurlu | rainy |
| Bulutlu | cloudy |
| Rüzgarlı | windy |

### Ürünler (Crops)
| Türkçe | English |
|--------|---------|
| Buğday | wheat |
| Arpa | barley |
| Mısır | corn |
| Pirinç | rice |
| Yulaf | oat |
| Pamuk | cotton |
| Ayçiçeği | sunflower |
| Domates | tomato |

---

## Veri Kaynakları

- **Frontend**: `frontend/lib/pages/environment_recommendation_page.dart` (lines 365, 384, 403, 429, 448)
- **Dataset**: `res/csv_files/crop_dataset_v_100bin.csv`

---

**Versiyon**: 1.0 | **Tarih**: 2025-10-14
