# 🧪 TerraMind ML API Test Komutları

## 📋 Test Hazırlığı

Backend Docker container'ı çalışıyor. Artık test edebilirsiniz!

```bash
# Container durumunu kontrol et
docker-compose ps

# Backend loglarını izle (ayrı bir terminal'de)
docker-compose logs -f backend
```

---

## 1️⃣ Health Check (Genel Sağlık Kontrolü)

### PowerShell:
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/health" | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### CMD (curl varsa):
```cmd
curl http://localhost:5000/health
```

**Beklenen Yanıt:**
```json
{
  "status": "OK",
  "message": "Terramind API is running",
  "version": "1.0.0",
  "environment": "production",
  "ml_service": {
    "status": "healthy",
    "models": {
      "xgboost": true,
      "lightgbm": true
    }
  }
}
```

---

## 2️⃣ ML Service Health Check

### PowerShell:
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/ml/health" | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**Beklenen Yanıt:**
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
    "initialized": true
  }
}
```

---

## 3️⃣ Ürün Tahmini (Çevre → Ürün) - Türkçe Input

### PowerShell:
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

$response = Invoke-WebRequest -Uri "http://localhost:5000/api/ml/predict-crop" -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**Beklenen Yanıt:**
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
    "model_used": "lightgbm"
  }
}
```

---

## 4️⃣ Ürün Tahmini - İngilizce Input

### PowerShell:
```powershell
$body = @{
    region = "Aegean"
    soil_type = "Loamy"
    soil_ph = 7.0
    nitrogen = 120
    phosphorus = 45
    potassium = 50
    moisture = 70
    temperature_celsius = 28
    rainfall_mm = 800
    fertilizer_type = "Nitrogenous"
    irrigation_method = "Drip Irrigation"
    weather_condition = "sunny"
    model_type = "xgboost"
    language = "en"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/api/ml/predict-crop" -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 5️⃣ Çevre Optimizasyonu (Ürün → Çevre) - Türkçe

### PowerShell:
```powershell
$body = @{
    crop = "buğday"
    region = "Marmara"
    language = "tr"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/api/ml/optimize-environment" -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**Beklenen Yanıt:**
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
    "model_used": "lightgbm"
  }
}
```

**⏱️ NOT:** Bu işlem 2-5 saniye sürebilir (optimizasyon çalışıyor)

---

## 6️⃣ Çevre Optimizasyonu - İngilizce

### PowerShell:
```powershell
$body = @{
    crop = "corn"
    region = "Aegean"
    model_type = "lightgbm"
    language = "en"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:5000/api/ml/optimize-environment" -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 7️⃣ Model Bilgisi Al

### PowerShell (LightGBM):
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/ml/model-info?model_type=lightgbm" | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### PowerShell (XGBoost):
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/ml/model-info?model_type=xgboost" | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 8️⃣ Farklı Ürünler İçin Test

### Mısır (Corn):
```powershell
$body = @{
    crop = "mısır"
    region = "Marmara"
    language = "tr"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/ml/optimize-environment" -Method POST -Body $body -ContentType "application/json" | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Pirinç (Rice):
```powershell
$body = @{
    crop = "pirinç"
    region = "Marmara"
    language = "tr"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/ml/optimize-environment" -Method POST -Body $body -ContentType "application/json" | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Pamuk (Cotton):
```powershell
$body = @{
    crop = "pamuk"
    region = "Ege"
    language = "tr"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/ml/optimize-environment" -Method POST -Body $body -ContentType "application/json" | Select-Object -Expand Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 9️⃣ Hata Senaryoları

### Eksik Parametre Hatası:
```powershell
$body = @{
    region = "Marmara"
    soil_type = "Killi Toprak"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/ml/predict-crop" -Method POST -Body $body -ContentType "application/json"
```

**Beklenen:** HTTP 400 - Missing required features hatası

### Bilinmeyen Ürün Hatası:
```powershell
$body = @{
    crop = "BİLİNMEYEN_ÜRÜN"
    region = "Marmara"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/ml/optimize-environment" -Method POST -Body $body -ContentType "application/json"
```

**Beklenen:** HTTP 500 - Unknown crop hatası

---

## 🔍 Backend Loglarını İzleme

Ayrı bir PowerShell terminali açın ve şunu çalıştırın:

```powershell
cd backend
docker-compose logs -f backend
```

Bu terminal'de şu logları göreceksiniz:

```
🌾 ML CROP PREDICTION REQUEST (Environment → Crop)
  Source Language: tr
  Model: lightgbm
  Input Features:
    soil_ph: 6.5
    nitrogen: 90
    ...
✅ PREDICTION RESULT:
  Predicted Crop: corn
  Confidence: 85.23%
  Model Used: lightgbm
```

---

## 📊 Performans Test

### Hızlı Tahmin (100-300ms):
```powershell
Measure-Command {
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
    } | ConvertTo-Json
    
    Invoke-WebRequest -Uri "http://localhost:5000/api/ml/predict-crop" -Method POST -Body $body -ContentType "application/json"
}
```

### Yavaş Optimizasyon (2-5 saniye):
```powershell
Measure-Command {
    $body = @{
        crop = "buğday"
        region = "Marmara"
    } | ConvertTo-Json
    
    Invoke-WebRequest -Uri "http://localhost:5000/api/ml/optimize-environment" -Method POST -Body $body -ContentType "application/json"
}
```

---

## 🛠️ Sorun Giderme

### Container çalışmıyorsa:
```powershell
cd backend
docker-compose ps
docker-compose logs backend
docker-compose restart backend
```

### ML modeli yüklenmediyse:
```powershell
# Logları kontrol et
docker-compose logs backend | Select-String "ML"

# Container içine gir
docker-compose exec backend bash

# Model dosyalarını kontrol et
ls -la models/
```

### Port zaten kullanılıyorsa:
```powershell
# 5000 portunu kullanan process'i bul
Get-NetTCPConnection -LocalPort 5000

# Container'ı farklı portla çalıştır (docker-compose.yml'de değiştir)
```

---

## ✅ Başarı Kriterleri

- [ ] `/health` endpoint'i `ml_service.status: "healthy"` döndürüyor
- [ ] `/api/ml/health` endpoint'i her iki model için `true` döndürüyor
- [ ] Türkçe input → Türkçe output çalışıyor
- [ ] İngilizce input → İngilizce output çalışıyor
- [ ] Ürün tahmini 300ms altında tamamlanıyor
- [ ] Çevre optimizasyonu 5 saniye içinde tamamlanıyor
- [ ] Backend loglarında ML işlemleri görünüyor
- [ ] Hata durumları düzgün handle ediliyor

---

**Hazır! Şimdi bu komutları PowerShell'de çalıştırabilirsiniz!** 🚀

