# 🔍 TerraMind Backend Log İzleme Rehberi

## 🎯 Amaç
UI'dan gelen isteklerin backend'e ulaştığını ve ML modelinin çalıştığını gerçek zamanlı izlemek.

---

## 🚀 Hızlı Başlangıç

### Logları Canlı İzle (Önerilen)
```powershell
cd backend
docker-compose logs -f backend
```

**Açıklama:** 
- `-f` flag'i "follow" demek, yani yeni logları canlı gösterir
- Ctrl+C ile durdurun

---

## 📊 Log Seviyeleri

Backend'de şu log seviyeleri kullanılıyor:

### 🟢 INFO (Normal İşlemler)
```
[INFO] 🚀 Initializing ML Service...
[INFO] 📦 Loading XGBoost model from: models/crop_model.pkl
[INFO] ✅ XGBoost model loaded successfully
```

### 🔵 DEBUG (Detaylı Bilgiler)
```
[DEBUG] ✅ Input validation passed
[DEBUG] Optimization iteration error: ...
```

### 🟡 WARNING (Uyarılar)
```
[WARNING] Unknown category in 'soil_type': xyz
[WARNING] ⚠️ XGBoost predictor failed to initialize
```

### 🔴 ERROR (Hatalar)
```
[ERROR] ❌ Failed to load XGBoost model
[ERROR] ❌ Prediction failed: Missing required features
```

---

## 🎬 Beklenen Log Akışı

### 1. Container Başlatıldığında

```
🚀 Starting Gunicorn server...
   Workers: 5
   Bind: 0.0.0.0:5000
Worker spawned (pid: 8)
Worker spawned (pid: 9)
🚀 Initializing ML Service...
📦 Loading XGBoost model from: models/crop_model.pkl
✅ XGBoost model loaded successfully
   Features: 12
   Crops: 50
📦 Loading LightGBM model from: models/sentetik_crop_model.pkl
✅ LightGBM model loaded successfully
   Crops: 50
   Preprocessing: Feature engineering pipeline included
🎉 ML Service initialization complete
✅ ML Service initialized successfully
ML Service initialized for worker (pid: 8)
ML Service initialized for worker (pid: 9)
✅ Gunicorn server is ready to accept connections!
```

---

### 2. UI'dan Ürün Tahmini İsteği Geldiğinde

**UI → Backend Akışı:**

```
[REQUEST] POST /api/ml/predict-crop from 172.18.0.1
[HEADERS] {'Content-Type': 'application/json', ...}
[REQUEST_DATA] {
    'region': 'Marmara',
    'soil_type': 'Killi Toprak',
    'soil_ph': 6.5,
    'nitrogen': 90,
    ...
}

================================================================================
🌾 ML CROP PREDICTION REQUEST (Environment → Crop)
  Source Language: tr
  Model: lightgbm
  Input Features:
    region: Marmara
    soil_type: Killi Toprak
    soil_ph: 6.5
    nitrogen: 90
    phosphorus: 42
    potassium: 43
    moisture: 65
    temperature_celsius: 25
    rainfall_mm: 600
    fertilizer_type: Amonyum Sülfat
    irrigation_method: Damla Sulama
    weather_condition: Güneşli
================================================================================

🌱 Predicting crop from environment (LightGBM + Feature Engineering)

✅ PREDICTION RESULT:
  Predicted Crop: corn
  Confidence: 85.23%
  Model Used: lightgbm
  Top 3: [('corn', '85.2%'), ('wheat', '10.1%'), ('rice', '4.7%')]
================================================================================

[RESPONSE] 200 for POST /api/ml/predict-crop
```

**⏱️ Süre:** 100-300ms

---

### 3. UI'dan Çevre Optimizasyonu İsteği Geldiğinde

**UI → Backend Akışı:**

```
[REQUEST] POST /api/ml/optimize-environment from 172.18.0.1
[REQUEST_DATA] {
    'crop': 'buğday',
    'region': 'Marmara'
}

================================================================================
🔍 ML ENVIRONMENT OPTIMIZATION REQUEST (Crop → Environment)
  Target Crop: wheat
  Target Region: Marmara
  Model: lightgbm
================================================================================

🔍 Optimizing environment for crop 'wheat' in region 'Marmara' (LightGBM)
   Running differential evolution optimization...

✅ OPTIMIZATION RESULT:
  Success Probability: 92.50%
  Model Used: lightgbm
  Optimal Conditions:
    soil_ph: 6.8
    nitrogen: 120
    phosphorus: 45
    potassium: 50
    moisture: 65
    temperature_celsius: 22
    rainfall_mm: 800
    soil_type: Loamy
    fertilizer_type: Nitrogenous
    irrigation_method: Drip Irrigation
    weather_condition: Sunny
================================================================================

[RESPONSE] 200 for POST /api/ml/optimize-environment
```

**⏱️ Süre:** 2-5 saniye (optimizasyon iterasyonları)

---

### 4. I18N Çevirisi Logları

```
🌍 ENVIRONMENT DATA RECEIVED:
  Source Language: tr
🌱 CANONICAL ENVIRONMENT DATA (EN):
  Region: Marmara
  Soil Type: Clay
  Fertilizer: Ammonium Sulphate
  Irrigation: Drip Irrigation
  Weather: sunny
✅ ENVIRONMENT DATA PROCESSED
```

---

## 🔧 Gelişmiş Log İzleme

### Sadece ML İşlemlerini Filtrele
```powershell
docker-compose logs -f backend | Select-String "ML|🌾|🔍|✅|❌"
```

### Sadece ERROR Logları
```powershell
docker-compose logs -f backend | Select-String "ERROR|❌"
```

### Sadece I18N Çevirileri
```powershell
docker-compose logs -f backend | Select-String "I18N|CANONICAL|ENVIRONMENT DATA"
```

### Son 100 Log Satırı
```powershell
docker-compose logs --tail=100 backend
```

### Belirli Bir Zaman Aralığı
```powershell
docker-compose logs --since="2025-10-14T20:00:00" backend
```

---

## 📝 Log Dosyasına Kaydetme

### Logları Dosyaya Yaz
```powershell
docker-compose logs -f backend > backend_logs.txt
```

### Hem Ekranda Göster Hem Dosyaya Yaz
```powershell
docker-compose logs -f backend | Tee-Object -FilePath backend_logs.txt
```

---

## 🎯 İzleme Senaryoları

### Senaryo 1: UI'dan İlk Tahmin
1. Terminalde log izlemeyi başlat:
   ```powershell
   docker-compose logs -f backend
   ```

2. UI'da bir form doldur ve "Tahmin Et" butonuna tıkla

3. Terminalde şunları göreceksin:
   - ✅ Request geldi: `POST /api/ml/predict-crop`
   - ✅ I18N çevirisi yapıldı (Türkçe → İngilizce)
   - ✅ Model çalıştı: `🌱 Predicting crop from environment`
   - ✅ Sonuç döndü: `✅ PREDICTION RESULT`
   - ✅ Response gönderildi: `200 for POST /api/ml/predict-crop`

### Senaryo 2: Çevre Optimizasyonu
1. UI'da bir ürün seç (örn: "Buğday")

2. "Optimal Koşullar" butonuna tıkla

3. Terminalde şunları göreceksin:
   - ✅ Request geldi: `POST /api/ml/optimize-environment`
   - ✅ Optimizasyon başladı: `🔍 Optimizing environment`
   - ⏳ Optimization çalışıyor (2-5 saniye)
   - ✅ Sonuç bulundu: `✅ OPTIMIZATION RESULT`
   - ✅ Response gönderildi

### Senaryo 3: Hatalı Request
1. UI'da eksik bilgi ile form gönder

2. Terminalde şunları göreceksin:
   - ❌ Validation hatası: `Invalid input data: Missing required features`
   - 🔴 Error response: `400 for POST /api/ml/predict-crop`

---

## 🐛 Sorun Giderme Log Kontrolleri

### Model Yüklenme Sorunu
**Kontrol Et:**
```
✅ XGBoost model loaded successfully
✅ LightGBM model loaded successfully
```

**Hata Varsa:**
```
❌ Failed to load XGBoost model: [Errno 2] No such file or directory
```

**Çözüm:**
```powershell
docker-compose exec backend ls -la models/
```

---

### Request UI'dan Gelmiyor
**Kontrol Et:**
```
[REQUEST] POST /api/ml/predict-crop from 172.18.0.1
```

**Gelmediyse:**
- CORS ayarlarını kontrol et
- Network bağlantısını kontrol et
- Browser console'da hata var mı kontrol et

---

### ML Model Çalışmıyor
**Kontrol Et:**
```
🌱 Predicting crop from environment (LightGBM + Feature Engineering)
```

**Çalışmadıysa:**
```
❌ ML service not available
```

**Çözüm:**
```powershell
docker-compose restart backend
docker-compose logs backend | Select-String "ML Service"
```

---

## 📊 Performans İzleme

### Request Süreleri
Logda her request için süre bilgisi:
```
[2025-10-14 20:15:30,123] INFO in app: Health check requested
[2025-10-14 20:15:30,145] INFO in app: Response time: 22ms
```

### ML İşlem Süreleri
```
🌾 ML CROP PREDICTION REQUEST
... (işlemler)
✅ PREDICTION RESULT
Total time: 245ms
```

---

## 🎨 Log Renklendirme (İsteğe Bağlı)

PowerShell'de renkli log görmek için:

```powershell
docker-compose logs -f backend | ForEach-Object {
    if ($_ -match "ERROR|❌") {
        Write-Host $_ -ForegroundColor Red
    }
    elseif ($_ -match "WARNING|⚠️") {
        Write-Host $_ -ForegroundColor Yellow
    }
    elseif ($_ -match "SUCCESS|✅|🎉") {
        Write-Host $_ -ForegroundColor Green
    }
    elseif ($_ -match "🌾|🔍|🌱") {
        Write-Host $_ -ForegroundColor Cyan
    }
    else {
        Write-Host $_
    }
}
```

---

## ✅ Checklist - Log İzleme Başarılı mı?

UI'dan işlem yaparken şunları görmelisin:

- [ ] Request geldi: `[REQUEST] POST /api/ml/...`
- [ ] I18N çalıştı: `Source Language: tr` / `CANONICAL ... (EN)`
- [ ] ML model çalıştı: `🌱 Predicting...` veya `🔍 Optimizing...`
- [ ] Sonuç döndü: `✅ PREDICTION RESULT` veya `✅ OPTIMIZATION RESULT`
- [ ] Response başarılı: `[RESPONSE] 200 for POST ...`
- [ ] Süre makul: Tahmin < 300ms, Optimizasyon < 5s

---

## 🚀 Hızlı Komutlar

```powershell
# Ana log izleme
docker-compose logs -f backend

# Sadece ML işlemleri
docker-compose logs -f backend | Select-String "ML|🌾|🔍"

# Sadece hatalar
docker-compose logs -f backend | Select-String "ERROR|❌"

# Container durumu
docker-compose ps

# Container yeniden başlat
docker-compose restart backend

# Tüm logları temizle ve baştan başla
docker-compose down
docker-compose up -d
docker-compose logs -f backend
```

---

**Artık UI'dan yaptığınız her işlemi backend'de canlı izleyebilirsiniz!** 🎯

Her form gönderdiğinizde, her butona tıkladığınızda terminal'de detaylı loglar akacak.

