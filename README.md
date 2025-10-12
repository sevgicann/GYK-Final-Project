# Terramind - Akıllı Tarım Çözümleri

Bu proje, akıllı tarım çözümleri için geliştirilmiş mikroservis mimarisine sahip bir uygulamadır.

## 🏗️ Proje Yapısı

```
GYK-Final-Project/
├── backend/                    # Backend API (Flask)
│   ├── app.py                 # Ana Flask uygulaması
│   ├── config.py              # Konfigürasyon
│   ├── run.py                 # Uygulama başlatıcı
│   ├── requirements.txt       # Python bağımlılıkları
│   ├── Dockerfile             # Docker konfigürasyonu
│   ├── docker-compose.yml     # Docker Compose
│   ├── nginx.conf             # Nginx proxy konfigürasyonu
│   ├── models/                # Veritabanı modelleri
│   ├── routes/                # API endpoint'leri
│   └── venv/                  # Virtual environment
├── GYK_UI/                    # Frontend (Flutter)
│   ├── lib/
│   │   ├── core/config/       # API konfigürasyonu
│   │   ├── services/          # API servisleri
│   │   ├── models/            # Veri modelleri
│   │   ├── pages/             # UI sayfaları
│   │   └── widgets/           # UI bileşenleri
│   ├── pubspec.yaml           # Flutter bağımlılıkları
│   └── ...
├── models/                    # ML modelleri
├── res/                       # Kaynak dosyalar
└── utilis/                    # Yardımcı araçlar
```

## 🚀 Hızlı Başlangıç

### Backend (API)

#### Geliştirme Ortamı
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python run.py
```

#### Docker ile
```bash
cd backend
docker-compose up -d
```

### Frontend (Flutter)

```bash
cd GYK_UI
flutter pub get
flutter run
```

## 🌐 API Endpoints

### Health Check
- `GET /health` - API durumu

### Authentication
- `POST /api/auth/register` - Kullanıcı kaydı
- `POST /api/auth/login` - Kullanıcı girişi
- `POST /api/auth/refresh` - Token yenileme
- `POST /api/auth/logout` - Çıkış

### Users
- `GET /api/users/profile` - Kullanıcı profili
- `PUT /api/users/profile` - Profil güncelleme
- `DELETE /api/users/profile` - Hesap silme

### Products
- `GET /api/products` - Ürün listesi
- `GET /api/products/{id}` - Ürün detayı
- `POST /api/products` - Yeni ürün ekleme
- `PUT /api/products/{id}` - Ürün güncelleme
- `DELETE /api/products/{id}` - Ürün silme

### Environments
- `GET /api/environments` - Çevre verileri
- `POST /api/environments` - Yeni çevre verisi
- `GET /api/environments/{id}` - Çevre detayı

### Recommendations
- `GET /api/recommendations` - Öneriler
- `POST /api/recommendations` - Yeni öneri oluşturma
- `GET /api/recommendations/{id}` - Öneri detayı

## 🐳 Docker Servisleri

### Backend API
- **Port**: 5000
- **Image**: backend-backend
- **Health Check**: `/health`

### PostgreSQL Database
- **Port**: 5432
- **Image**: postgres:15-alpine
- **Database**: terramind_db
- **User**: postgres
- **Password**: pass.123

### Redis Cache
- **Port**: 6379
- **Image**: redis:7-alpine

### Nginx Proxy
- **Port**: 80, 443
- **Image**: nginx:alpine
- **Features**: Rate limiting, CORS, Security headers

## 🔧 Konfigürasyon

### Environment Variables

#### Backend
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://postgres:pass.123@db:5432/terramind_db
CORS_ORIGIN=http://localhost:8080
REDIS_URL=redis://redis:6379/0
```

#### Frontend
```dart
// lib/core/config/api_config.dart
static const String baseUrl = 'http://localhost:5000';
```

## 📱 Frontend Özellikleri

- **Flutter** tabanlı cross-platform uygulama
- **Material Design** UI
- **JWT** tabanlı kimlik doğrulama
- **HTTP** API entegrasyonu
- **Shared Preferences** ile veri saklama
- **Responsive** tasarım

## 🔒 Güvenlik

- **JWT** token tabanlı kimlik doğrulama
- **CORS** koruması
- **Rate Limiting** (Nginx)
- **Security Headers** (X-Frame-Options, X-XSS-Protection)
- **Input Validation**
- **SQL Injection** koruması (SQLAlchemy ORM)

## 🧪 Test

### Backend Test
```bash
cd backend
python -c "from app import app; print('Backend OK')"
```

### API Test
```bash
curl http://localhost:5000/health
curl http://localhost/
```

### Docker Test
```bash
docker-compose ps
docker-compose logs backend
```

## 📊 Monitoring

### Health Checks
- Backend: `http://localhost:5000/health`
- Nginx: `http://localhost/`

### Logs
```bash
docker-compose logs -f backend
docker-compose logs -f db
docker-compose logs -f redis
docker-compose logs -f nginx
```

## 🚀 Production Deployment

### Docker Compose
```bash
cd backend
docker-compose -f docker-compose.yml up -d
```

### Environment Setup
1. `.env` dosyasını oluşturun
2. Production değerlerini ayarlayın
3. SSL sertifikalarını ekleyin
4. Database backup stratejisi oluşturun

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

- **Proje**: Terramind - Akıllı Tarım Çözümleri
- **Versiyon**: 1.0.0
- **Mimari**: Mikroservis (Frontend + Backend)

---

## 🎯 Sonraki Adımlar

1. **Frontend-Backend Entegrasyonu**: API servislerini test edin
2. **Database Migration**: Veritabanı şemasını oluşturun
3. **Authentication**: Kullanıcı kayıt/giriş sistemini test edin
4. **ML Integration**: Makine öğrenmesi modellerini entegre edin
5. **Production**: Production ortamına deploy edin

**Not**: Bu proje mikroservis mimarisi kullanılarak geliştirilmiştir. Frontend ve backend tamamen ayrı servisler olarak çalışabilir ve bağımsız olarak geliştirilebilir.
