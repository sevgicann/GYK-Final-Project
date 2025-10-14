# TerraMind ML Model Entegrasyonu

## 📋 Genel Bakış

TerraMind projesi, **çift yönlü tahmin** yapabilen iki ML modeli içerir:

1. **XGBoost Model** (`crop_model.pkl`) - Model2.py tabanlı
2. **LightGBM Model** (`sentetik_crop_model.pkl`) - Sentetik_model.py tabanlı, gelişmiş feature engineering ile

### Çift Yönlü Tahmin Özellikleri

#### 1. Çevre → Ürün Tahmini
Kullanıcı çevresel koşulları girer → Sistem en uygun ürünü önerir

#### 2. Ürün → Çevre Optimizasyonu
Kullanıcı yetiştirmek istediği ürünü seçer → Sistem optimal çevresel koşulları hesaplar

---

## 🏗️ Mimari (SOLID Prensiplerine Uygun)

### Katmanlar

```
backend/
├── services/                    # ML Servis Katmanı
│   ├── __init__.py
│   ├── base_predictor.py       # Interface Segregation (I)
│   ├── xgboost_predictor.py    # Single Responsibility (S)
│   ├── lightgbm_predictor.py   # Single Responsibility (S)
│   └── ml_service.py           # Singleton + Dependency Injection
├── routes/
│   └── ml_endpoints.py         # API Endpoints
└── models/                     # Model Dosyaları
    ├── crop_model.pkl          # XGBoost
    └── sentetik_crop_model.pkl # LightGBM
```

### SOLID Prensipleri

- **S**ingle Responsibility: Her predictor sınıfı tek bir model tipinden sorumlu
- **O**pen/Closed: Yeni model eklemek için mevcut kodu değiştirmeden `BasePredictor` extend edilir
- **L**iskov Substitution: Tüm predictor'lar `BasePredictor` interface'ini implement eder
- **I**nterface Segregation: `BasePredictor` sadece gerekli methodları tanımlar
- **D**ependency Inversion: `MLService` soyut `BasePredictor`'a bağımlı, konkret implementasyonlara değil

---

## 🔌 API Endpoints

### Base URL: `/api/ml`

### 1. Health Check
```http
GET /api/ml/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "models": {
      "xgboost": true,
      "lightgbm": true
    },
    "default_model": "lightgbm",
    "capabilities": {
      "environment_to_crop": true,
      "crop_to_environment": true
    }
  }
}
```

---

### 2. Ürün Tahmini (Çevre → Ürün)
```http
POST /api/ml/predict-crop
```

**Request (Türkçe veya İngilizce):**
```json
{
  "region": "Marmara",
  "soil_type": "Killi Toprak",
  "soil_ph": 6.5,
  "nitrogen": 90,
  "phosphorus": 42,
  "potassium": 43,
  "moisture": 65,
  "temperature_celsius": 25,
  "rainfall_mm": 600,
  "fertilizer_type": "Amonyum Sülfat",
  "irrigation_method": "Damla Sulama",
  "weather_condition": "Güneşli",
  "model_type": "lightgbm",
  "language": "tr"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "predicted_crop": "mısır",
    "confidence": 0.85,
    "top_3_predictions": [
      ["mısır", 0.85],
      ["buğday", 0.10],
      ["pirinç", 0.05]
    ],
    "model_used": "lightgbm",
    "direction": "environment_to_crop"
  }
}
```

---

### 3. Çevre Optimizasyonu (Ürün → Çevre)
```http
POST /api/ml/optimize-environment
```

**Request:**
```json
{
  "crop": "buğday",
  "region": "Marmara",
  "model_type": "lightgbm",
  "language": "tr"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "crop": "buğday",
    "region": "Marmara",
    "optimal_conditions": {
      "soil_ph": 6.8,
      "nitrogen": 120,
      "phosphorus": 45,
      "potassium": 50,
      "moisture": 65,
      "temperature_celsius": 22,
      "rainfall_mm": 800,
      "soil_type": "Loamy",
      "fertilizer_type": "Nitrogenous",
      "irrigation_method": "Drip Irrigation",
      "weather_condition": "Sunny"
    },
    "success_probability": 92.5,
    "model_used": "lightgbm",
    "direction": "crop_to_environment"
  }
}
```

---

### 4. Model Bilgisi
```http
GET /api/ml/model-info?model_type=lightgbm
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "loaded",
    "model_type": "LightGBM",
    "algorithm": "Gradient Boosting Decision Tree",
    "features": {
      "numeric": ["soil_ph", "nitrogen", ...],
      "categorical": ["region", "soil_type", ...],
      "engineered": true
    },
    "crops": ["wheat", "rice", "corn", ...],
    "capabilities": ["environment_to_crop", "crop_to_environment"]
  }
}
```

---

## 🐳 Docker Kurulum

### Model Dosyalarını Hazırlama
```bash
# Model dosyaları backend/models/ klasöründe olmalı
backend/models/
├── crop_model.pkl           # XGBoost model
└── sentetik_crop_model.pkl  # LightGBM model
```

### Docker Build
```bash
cd backend
docker-compose build
```

### Docker Run
```bash
docker-compose up -d
```

### Logları Kontrol Etme
```bash
docker-compose logs -f backend
```

Başarılı başlatmada şu logları görmelisiniz:
```
🚀 Initializing ML Service...
📦 Loading XGBoost model from: models/crop_model.pkl
✅ XGBoost model loaded successfully
📦 Loading LightGBM model from: models/sentetik_crop_model.pkl
✅ LightGBM model loaded successfully
🎉 ML Service initialization complete
✅ ML Service initialized successfully
```

---

## 🧪 Test Senaryoları

### 1. Health Check
```bash
curl http://localhost:5000/api/ml/health
```

### 2. Ürün Tahmini (PowerShell)
```powershell
$body = @{
    region = "Marmara"
    soil_type = "Killi Toprak"
    soil_ph = 6.5
    nitrogen = 90
    phosphorus = 42
    potassium = 43
    moisture = 65
    temperature_celsius = 25
    rainfall_mm = 600
    fertilizer_type = "Amonyum Sülfat"
    irrigation_method = "Damla Sulama"
    weather_condition = "Güneşli"
    language = "tr"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/ml/predict-crop" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

### 3. Çevre Optimizasyonu (PowerShell)
```powershell
$body = @{
    crop = "buğday"
    region = "Marmara"
    language = "tr"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/ml/optimize-environment" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

---

## 🌍 I18N Desteği

Tüm endpoint'ler Türkçe ve İngilizce girdiyi otomatik algılar ve dönüştürür.

### Otomatik Dönüşümler

**Türkçe → İngilizce (İşleme):**
- "Killi Toprak" → "Clay"
- "Amonyum Sülfat" → "Ammonium Sulphate"
- "Damla Sulama" → "Drip Irrigation"
- "Güneşli" → "sunny"

**İngilizce → Türkçe (Yanıt):**
- `language: "tr"` parametresi ile yanıt Türkçe döner
- `language: "en"` veya boş bırakılırsa İngilizce döner

---

## 🔍 Model Detayları

### XGBoost Model (crop_model.pkl)
- **Algoritma:** Gradient Boosting
- **Özellikler:** 12 feature (7 numeric, 5 categorical)
- **Optimizasyon:** Differential Evolution (scipy)
- **Kullanım:** Daha hızlı tahmin, basit deployment

### LightGBM Model (sentetik_crop_model.pkl)
- **Algoritma:** Gradient Boosting Decision Tree
- **Özellikler:** 12 temel + 10 engineered feature
- **Optimizasyon:** Differential Evolution + Feature Engineering
- **Kullanım:** Daha yüksek accuracy, gelişmiş tahmin
- **Varsayılan:** ✅ Default model

### Feature Engineering (LightGBM)
1. N/P oranı
2. N/K oranı
3. pH kategorisi
4. Yağış + sulama etkisi
5. Sulama yoğunluğu
6. Gübre tipi nitrojenli mi?
7. Sıcaklık-nem etkileşimi
8. Evapotranspirasyon proxy
9. Toprak dokusu skoru
10. Genel yetişme indeksi

---

## 📊 Performans

### Beklenen Yanıt Süreleri
- Health Check: < 50ms
- Ürün Tahmini: 100-300ms
- Çevre Optimizasyonu: 2-5 saniye (optimizasyon iterasyonları nedeniyle)

### Optimizasyon Parametreleri
- **Differential Evolution Iterations:** 60-80
- **Worker Threads:** 1 (deterministic sonuçlar için)
- **Seed:** 42 (reproducibility için)

---

## 🚨 Hata Yönetimi

### Model Yükleme Hatası
```json
{
  "success": false,
  "status": "unavailable",
  "message": "ML service not initialized"
}
```

**Çözüm:**
1. Model dosyalarının `backend/models/` klasöründe olduğunu kontrol edin
2. Docker loglarını kontrol edin: `docker-compose logs backend`
3. Model dosyalarının bozuk olmadığını doğrulayın

### Eksik Feature Hatası
```json
{
  "success": false,
  "error": "Missing required features: soil_ph, nitrogen"
}
```

**Çözüm:** Tüm gerekli özelliklerin request'te bulunduğundan emin olun

### Bilinmeyen Crop/Region Hatası
```json
{
  "success": false,
  "error": "Unknown crop or region: xyz"
}
```

**Çözüm:** Geçerli crop/region isimleri için `/api/ml/model-info` endpoint'ini kullanın

---

## 📝 Geliştirme Notları

### Yeni Model Ekleme

1. `BasePredictor` interface'ini implement eden yeni sınıf oluşturun
2. `MLService`'e yeni modeli ekleyin
3. `ml_endpoints.py`'de yeni model tipini destekleyin

### Model Güncelleme

1. Yeni model dosyasını `backend/models/` klasörüne ekleyin
2. Docker image'ı rebuild edin: `docker-compose build`
3. Container'ı restart edin: `docker-compose restart backend`

---

## ✅ Checklist

- [x] SOLID prensiplerine uygun servis mimarisi
- [x] XGBoost predictor implementasyonu
- [x] LightGBM predictor implementasyonu
- [x] Çift yönlü tahmin (Environment ↔ Crop)
- [x] RESTful API endpoints
- [x] I18N desteği (TR/EN)
- [x] Docker entegrasyonu
- [x] Health check endpoint
- [x] Error handling
- [x] Logging
- [x] Dokümantasyon

---

## 🎯 Sonraki Adımlar

1. **Frontend Entegrasyonu:** Flutter UI'dan ML endpoint'leri çağırma
2. **Model Monitoring:** Tahmin performansını izleme
3. **A/B Testing:** XGBoost vs LightGBM karşılaştırması
4. **Cache:** Sık kullanılan tahminler için Redis cache
5. **Rate Limiting:** API endpoint'leri için rate limiting
6. **Batch Prediction:** Toplu tahmin endpoint'i

---

**Son Güncelleme:** 14 Ekim 2025  
**Versiyon:** 1.0.0  
**Durum:** ✅ Production Ready

