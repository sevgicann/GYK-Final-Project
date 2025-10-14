# 🚀 TERRAMIND - HIZLI BAŞLANGIÇ

## ✅ ÖNEMLİ: Test Kullanıcı Bilgileri

```
Email: test@gmail.com
Şifre: 123456
```

---

## 🎯 UYGULAMAYI BAŞLATMA (TEK TIKLA)

1. Proje klasöründe **`START_HERE.bat`** dosyasına **ÇİFT TIKLAYIN**

2. İki pencere açılacak:
   - **Backend** (http://localhost:5000)
   - **Frontend** (http://localhost:8080)

3. Frontend Chrome'da otomatik açılacak

4. Login sayfasında yukarıdaki bilgilerle giriş yapın

---

## 🐳 DOCKER İLE ÇALIŞTIRMA (Production Ortamı)

Docker Desktop'ı başlatın, sonra:

```powershell
cd C:\Users\sevgi\GYK-Final-Project\backend
docker-compose up -d --build
```

Bu şunları başlatır:
- ✅ Backend API (Port 5000)
- ✅ PostgreSQL Database (Port 5432)
- ✅ Redis Cache (Port 6379)
- ✅ Nginx Proxy (Port 80)

Docker ile çalıştırdığınızda yeni kullanıcı oluşturmanız gerekecek.

---

## 📦 YÜKLENMİŞ PAKETLER

### Backend
✅ Flask 2.3.3
✅ SQLAlchemy 2.0.44
✅ Flask-JWT-Extended
✅ Flask-CORS
✅ bcrypt

### Frontend
✅ Flutter (Web)
✅ HTTP Package
✅ Shared Preferences

---

## 🔧 SORUN GİDERME

### Backend başlamıyor?
```powershell
cd C:\Users\sevgi\GYK-Final-Project\backend
py run.py
```

### Frontend başlamıyor?
```powershell
cd C:\Users\sevgi\GYK-Final-Project\frontend
flutter run -d chrome --web-port=8080
```

### Login çalışmıyor?
- Backend'in çalıştığından emin olun: http://localhost:5000/health
- Test kullanıcı bilgilerini kontrol edin (yukarıda)
- Browser console'da hata var mı kontrol edin (F12)

### Port kullanımda?
Backend için `.env` dosyasında PORT değiştirin
Frontend için `--web-port=8081` gibi farklı port kullanın

---

## 📊 API ENDPOINTS

- **Health Check**: http://localhost:5000/health
- **Login**: POST http://localhost:5000/api/auth/login
- **Register**: POST http://localhost:5000/api/auth/register
- **Products**: GET http://localhost:5000/api/products
- **Recommendations**: GET http://localhost:5000/api/recommendations

---

## 🎮 HIZLI TEST

1. **START_HERE.bat** çalıştırın
2. Frontend açıldığında:
   - Email: `test@gmail.com`
   - Şifre: `123456`
3. Login'e tıklayın
4. Dashboard'a yönlendirileceksiniz

---

## 📝 NOTLAR

- **SQLite** kullanılıyor (development)
- Docker ile **PostgreSQL** kullanılabilir (production)
- Test kullanıcısı backend veritabanında kayıtlı
- CORS tüm origin'ler için açık (development)

---

## 🆘 DESTEK

Sorun yaşarsanız:
1. Backend logs: `backend/logs/`
2. Browser Console (F12)
3. Terminal çıktılarını kontrol edin

---

**Hazırlayan:** AI Assistant
**Tarih:** 2025-10-14
**Versiyon:** 1.0


