# 🧪 GPS Entegrasyonu Test Rehberi

## 🎯 Amaç
Gerçek GPS konumunun doğru alındığını doğrulamak.

---

## 📋 Test Adımları

### 1. Backend'i Başlat
```powershell
cd backend
docker-compose up
```

**Beklenen:** Backend http://localhost:5000 çalışıyor

### 2. Frontend'i Başlat
```powershell
cd frontend
flutter run -d chrome --web-port=8080
```

**Beklenen:** Tarayıcıda uygulama açıldı

### 3. Login Yap
- Email: `test@gmail.com`
- Password: `123456`

**Beklenen:** Ana sayfaya yönlendirildi

---

## 🗺️ GPS Testi

### Test 1: Ürün Seçimi Sayfası

1. **"Ürün Seçiminden Çevre Önerileri"** butonuna tıkla
2. **"GPS Konumunu Kullan"** butonuna tıkla
3. **Tarayıcı izin isteyecek:**
   ```
   [Site] would like to access your location
   [Block] [Allow]
   ```
4. **[Allow] tıkla**

**Beklenen Sonuç:**
```
📍 GPS konumunuz alınıyor...
✅ GPS konumu alındı: [GERÇEK ŞEHRİNİZ] ([GERÇEK BÖLGENİZ])
```

**Örnek:**
```
✅ GPS konumu alındı: Ankara (Central Anatolia)
```

### Test 2: Çevre Önerileri Sayfası

1. **"Çevre Koşullarından Ürün Önerisi"** butonuna tıkla
2. **"GPS Konumu"** butonuna tıkla
3. **İzin ver (eğer tekrar isterse)**

**Beklenen Sonuç:**
```
📍 GPS konumunuz alınıyor...
✅ GPS konumu alındı: [GERÇEK ŞEHRİNİZ] ([GERÇEK BÖLGENİZ])
```

---

## 🔍 Backend Log Kontrolü

Backend loglarında GPS verilerini kontrol et:

```powershell
cd backend
docker-compose logs -f backend
```

**Aranacak Loglar:**
```
📍 Selecting location: [ŞEHİR], [BÖLGE]
🌍 Location Type: gps
🗺️ Coordinates: [LAT], [LNG]
```

**Örnek:**
```
📍 Selecting location: Ankara, Central Anatolia
🌍 Location Type: gps
🗺️ Coordinates: 39.9334, 32.8597
```

---

## 🎯 Doğrulama Kriterleri

### ✅ Başarı Kriterleri
- [ ] GPS izni tarayıcıdan istendi
- [ ] Gerçek koordinatlar alındı
- [ ] Şehir adı doğru gösterildi
- [ ] Bölge adı doğru gösterildi
- [ ] Backend'e koordinatlar gönderildi
- [ ] Başarı mesajı gösterildi

### ❌ Başarısızlık Senaryoları

#### 1. İzin Reddedildi
**Görülen:**
```
❌ Konum izni reddedildi
[Manuel Seç] butonu
```

**Çözüm:**
1. Tarayıcı adres çubuğundaki kilit ikonuna tıkla
2. "Site settings" → "Location" → "Allow"
3. Sayfayı yenile
4. Tekrar dene

#### 2. GPS Kapalı
**Görülen:**
```
❌ GPS servisleri kapalı. Lütfen GPS'i açın.
```

**Çözüm:**
1. Cihaz ayarlarından GPS'i aç
2. Tekrar dene

#### 3. Her Zaman İstanbul Gösteriyor
**Sorun:** Eski simülasyon kodu hala çalışıyor

**Çözüm:**
1. Tarayıcı cache'i temizle
2. Uygulamayı yeniden başlat:
   ```powershell
   # Frontend'i durdur (Ctrl+C)
   flutter clean
   flutter pub get
   flutter run -d chrome --web-port=8080
   ```

#### 4. Geocoding Hatası
**Görülen:**
```
✅ GPS konumu alındı: İstanbul (Marmara)
```
(Koordinatlar alındı ama gerçek şehir bulunamadı, fallback kullanıldı)

**Not:** Bu normal bir durum, koordinat tabanlı bölge tespiti çalışıyor.

---

## 🗺️ Bölge Doğrulama Tablosu

Konumunuzu kontrol edin:

| Gerçek Konumunuz | Beklenen Şehir | Beklenen Bölge |
|------------------|----------------|----------------|
| İstanbul | İstanbul | Marmara |
| Ankara | Ankara | Central Anatolia |
| İzmir | İzmir | Aegean |
| Antalya | Antalya | Mediterranean |
| Samsun | Samsun | Black Sea |
| Erzurum | Erzurum | Eastern Anatolia |
| Gaziantep | Gaziantep | Southeastern Anatolia |
| Bursa | Bursa | Marmara |
| Konya | Konya | Central Anatolia |

---

## 📱 Farklı Tarayıcılar

### Chrome ✅
- GPS desteği: Tam
- İzin sistemi: Çalışıyor
- Performans: Hızlı

### Edge ✅
- GPS desteği: Tam
- İzin sistemi: Çalışıyor
- Performans: Hızlı

### Firefox ✅
- GPS desteği: Tam
- İzin sistemi: Farklı UI
- Performans: İyi

### Safari ⚠️
- macOS: Çalışıyor
- iOS: HTTPS gerekli

---

## 🔧 Debug Modu

Detaylı loglar için browser console'u aç:

1. **F12** veya **Sağ tık → Inspect**
2. **Console** sekmesi
3. GPS butonuna tıkla
4. Logları kontrol et:

```javascript
📍 Checking location permissions...
✅ Location permission granted, getting position...
📍 GPS Coordinates: 39.9334, 32.8597
📍 Placemark: Ankara, Ankara
✅ Detected City: Ankara, Region: Central Anatolia
✅ GPS location sent to backend: Ankara, Central Anatolia
```

---

## 🎬 Test Senaryoları

### Senaryo 1: İlk Kullanım (İzin Yok)
```
1. GPS butonuna tıkla
2. Tarayıcı izin iste
3. [Allow] tıkla
4. ✅ GPS konumu alındı: [ŞEHİR] ([BÖLGE])
```

### Senaryo 2: İkinci Kullanım (İzin Var)
```
1. GPS butonuna tıkla
2. İzin istenmez (cached)
3. ✅ GPS konumu alındı: [ŞEHİR] ([BÖLGE])
```

### Senaryo 3: İzin Reddedilmiş
```
1. GPS butonuna tıkla
2. ❌ Konum izni reddedildi
3. [Manuel Seç] butonu gösterilir
4. Manuel seçim yap
```

### Senaryo 4: Geocoding Başarısız
```
1. GPS butonuna tıkla
2. İzin ver
3. Koordinatlar alındı
4. Geocoding API hatası
5. Fallback: Koordinat → Bölge
6. ✅ GPS konumu alındı: [VARSAYILAN ŞEHİR] ([TAHMİN EDILEN BÖLGE])
```

---

## 📊 Performans Beklentileri

| İşlem | Süre | Durum |
|-------|------|-------|
| İzin isteme | < 2 sn | ✅ |
| GPS konum | 2-5 sn | ✅ |
| Geocoding | 1-2 sn | ✅ |
| Toplam | 3-9 sn | ✅ |

**Daha Yavaşsa:**
- İnternet bağlantınızı kontrol edin
- GPS sinyali zayıf olabilir
- İç mekanda mısınız? (GPS dış mekanda daha iyi)

---

## ✅ Test Sonucu Raporu

Test tamamlandıktan sonra doldurun:

```
Test Tarihi: ______________
Tarayıcı: ______________
İşletim Sistemi: ______________

[ ] GPS izni istendi
[ ] İzin verildi
[ ] Koordinatlar alındı: _______________
[ ] Şehir tespit edildi: _______________
[ ] Bölge tespit edildi: _______________
[ ] Backend'e gönderildi
[ ] Başarı mesajı gösterildi

Notlar:
_______________________________________
_______________________________________
_______________________________________

Sonuç: [ ] BAŞARILI   [ ] BAŞARISIZ
```

---

## 🆘 Yardım

### Sorun: Her zaman İstanbul gösteriyor
**Çözüm:** Cache temizle ve yeniden başlat

### Sorun: İzin veriyorum ama çalışmıyor
**Çözüm:** Browser console'da hata mesajlarını kontrol et

### Sorun: HTTPS hatası
**Çözüm:** Development'ta `localhost` kullan, production'da SSL ekle

### Sorun: Koordinatlar yanlış
**Çözüm:** Cihaz GPS'ini kontrol et, dış mekana çık

---

## 🎉 Başarı!

GPS testi başarılı geçtiyse:

✅ Gerçek konum çalışıyor
✅ İzin sistemi çalışıyor
✅ Backend entegrasyonu tamam
✅ Kullanıma hazır!

**Sonraki Adım:** Production'a deploy et ve SSL sertifikası ekle.

---

**Test Rehberi Versiyonu:** 1.0  
**Tarih:** 14 Ekim 2025  
**Durum:** ✅ Aktif

