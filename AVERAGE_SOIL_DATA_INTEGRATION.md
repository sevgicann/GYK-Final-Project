# Ortalama Toprak Verileri Entegrasyonu

Bu dokümantasyon, ortalama toprak parametrelerini veritabanından dinamik olarak almak için yapılan entegrasyonu açıklar.

## 🎯 Amaç

Ortam koşullarından ürün tahmini sayfasında, ortalama toprak parametrelerini sabit kodlanmış değerler yerine veritabanından dinamik olarak almak.

## 🏗️ Mimari

### Backend
- **Model**: `AverageSoilData` - Ortalama toprak verilerini tutan master tablo
- **Endpoint**: `/api/recommendations/average-soil-data` - Ortalama verileri çeken API
- **Fallback Logic**: Eşleşme bulunamazsa varsayılan değerler döner

### Frontend
- **Service**: `RecommendationService.getAverageSoilData()` - Backend'den veri çeken servis
- **Page**: `EnvironmentRecommendationPage` - Dinamik veri yükleme ile güncellenmiş sayfa
- **Auto-refresh**: Çevre koşulları değiştiğinde otomatik veri yenileme

## 📊 Veri Yapısı

### AverageSoilData Tablosu
```sql
CREATE TABLE average_soil_data (
    id VARCHAR(36) PRIMARY KEY,
    soil_type VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    fertilizer_type VARCHAR(50) NOT NULL,
    irrigation_method VARCHAR(50) NOT NULL,
    weather_condition VARCHAR(50) NOT NULL,
    avg_soil_ph NUMERIC(5,2) NOT NULL,
    avg_nitrogen NUMERIC(8,2) NOT NULL,
    avg_phosphorus NUMERIC(8,2) NOT NULL,
    avg_potassium NUMERIC(8,2) NOT NULL,
    avg_moisture NUMERIC(5,2) NOT NULL,
    avg_temperature_celsius NUMERIC(5,2) NOT NULL,
    avg_rainfall_mm NUMERIC(8,2) NOT NULL,
    data_count INTEGER DEFAULT 1,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(soil_type, region, fertilizer_type, irrigation_method, weather_condition)
);
```

## 🚀 Kurulum

### 1. Veritabanı Migration
```bash
cd backend
python migrations/add_average_soil_data_table.py
```

### 2. Backend Restart
```bash
cd backend
python run.py
```

### 3. Frontend Restart
```bash
cd frontend
flutter run
```

## 🔧 API Endpoints

### GET /api/recommendations/average-soil-data
Ortalama toprak verilerini çeker.

**Query Parameters:**
- `soil_type` (optional): Toprak tipi
- `region` (optional): Bölge
- `fertilizer_type` (optional): Gübre tipi
- `irrigation_method` (optional): Sulama yöntemi
- `weather_condition` (optional): Hava durumu

**Response:**
```json
{
  "success": true,
  "data": {
    "environmental_conditions": {
      "soil_type": "Tınlı Toprak",
      "region": "İç Anadolu",
      "fertilizer_type": "Organik Gübre",
      "irrigation_method": "Damla Sulama",
      "weather_condition": "Güneşli"
    },
    "average_values": {
      "ph": 6.5,
      "nitrogen": 120.0,
      "phosphorus": 60.0,
      "potassium": 225.0,
      "moisture": 26.0,
      "temperature_celsius": 23.0,
      "rainfall_mm": 850.0
    },
    "metadata": {
      "data_count": 150,
      "last_updated": "2024-01-15T10:30:00Z",
      "created_at": "2024-01-15T10:30:00Z"
    }
  },
  "message": "Average soil data retrieved successfully"
}
```

### GET /api/recommendations/average-soil-data/all
Tüm ortalama toprak verilerini listeler.

### POST /api/recommendations/average-soil-data/refresh
Ortalama toprak verilerini crop_dataset tablosundan yeniden hesaplar.

## 🎨 Frontend Kullanımı

### Ortalama Değerleri Kullanma
1. Kullanıcı "Ortalama Değerleri Kullan" butonuna tıklar
2. Sistem mevcut çevre koşullarına göre backend'den ortalama değerleri çeker
3. Form alanları dinamik olarak doldurulur
4. Kullanıcıya veri kaynağı hakkında bilgi verilir

### Otomatik Yenileme
- Bölge, toprak tipi, gübre, sulama veya güneş ışığı değiştiğinde
- Ortalama değerler kullanılıyorsa otomatik olarak yeni değerler yüklenir

### Fallback Mekanizması
- Tam eşleşme bulunamazsa kısmi eşleşme aranır
- Hiç eşleşme bulunamazsa varsayılan değerler kullanılır

## 🔍 Fallback Logic

1. **Tam Eşleşme**: Tüm çevre koşulları eşleşir
2. **Bölge + Toprak Tipi**: Bölge ve toprak tipi eşleşir
3. **Sadece Bölge**: Sadece bölge eşleşir
4. **Sadece Toprak Tipi**: Sadece toprak tipi eşleşir
5. **Varsayılan Değerler**: Hiç eşleşme yoksa sabit değerler

## 📈 Performans

- **Caching**: Backend'de veritabanı sorguları optimize edilmiştir
- **Lazy Loading**: Sadece gerektiğinde veri çekilir
- **Fallback**: Hızlı yanıt için fallback mekanizması

## 🐛 Hata Yönetimi

- **Network Errors**: İnternet bağlantısı yoksa varsayılan değerler
- **API Errors**: Backend hatası durumunda varsayılan değerler
- **Data Errors**: Veri formatı hatası durumunda varsayılan değerler

## 🔄 Veri Güncelleme

Ortalama verileri güncellemek için:

```bash
# Backend'de refresh endpoint'ini çağır
curl -X POST http://localhost:5000/api/recommendations/average-soil-data/refresh
```

## 📝 Loglar

Tüm işlemler detaylı olarak loglanır:
- Backend: `logs/terramind.log`
- Frontend: Console output

## 🎯 Gelecek Geliştirmeler

1. **Caching**: Redis ile önbellekleme
2. **Real-time Updates**: WebSocket ile gerçek zamanlı güncellemeler
3. **Machine Learning**: Daha akıllı fallback algoritması
4. **Analytics**: Kullanıcı davranış analizi

## 📞 Destek

Herhangi bir sorun durumunda:
1. Logları kontrol edin
2. API endpoint'lerini test edin
3. Veritabanı bağlantısını kontrol edin
4. Frontend console hatalarını kontrol edin
