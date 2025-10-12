# Terramind Backend API

Bu proje, Terramind uygulamasının backend API'sidir. Mikroservis mimarisi kullanılarak geliştirilmiştir.

## Özellikler

- **Flask** tabanlı RESTful API
- **JWT** tabanlı kimlik doğrulama
- **SQLAlchemy** ORM ile veritabanı yönetimi
- **Flask-Migrate** ile veritabanı migrasyonları
- **CORS** desteği
- **Rate Limiting** ile API koruması
- **Modüler yapı** (models, routes, services)

## API Endpoints

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

## Kurulum

### Gereksinimler
- Python 3.8+
- pip
- virtualenv (önerilen)

### Adımlar

1. **Repository'yi klonlayın:**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Virtual environment oluşturun:**
   ```bash
   python -m venv venv
   ```

3. **Virtual environment'ı aktifleştirin:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Environment dosyasını oluşturun:**
   ```bash
   cp env_example.txt .env
   ```

6. **Environment değişkenlerini düzenleyin:**
   `.env` dosyasını açın ve gerekli değerleri güncelleyin.

7. **Veritabanını başlatın:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

8. **Uygulamayı çalıştırın:**
   ```bash
   python run.py
   ```

## Geliştirme

### Veritabanı Migrasyonları
```bash
# Yeni migrasyon oluşturma
flask db migrate -m "Migration description"

# Migrasyonu uygulama
flask db upgrade

# Migrasyonu geri alma
flask db downgrade
```

### Test
```bash
# Testleri çalıştırma
python -m pytest

# Coverage raporu
python -m pytest --cov=app
```

## Production Deployment

### Gunicorn ile
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker ile
```bash
docker build -t terramind-backend .
docker run -p 5000:5000 terramind-backend
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `SECRET_KEY` | Flask secret key | - |
| `JWT_SECRET_KEY` | JWT secret key | - |
| `DATABASE_URL` | Database connection string | `sqlite:///terramind.db` |
| `CORS_ORIGIN` | CORS allowed origins | `http://localhost:8080` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `5000` |

## API Documentation

API dokümantasyonu Swagger UI ile `http://localhost:5000/docs` adresinde mevcuttur.

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.