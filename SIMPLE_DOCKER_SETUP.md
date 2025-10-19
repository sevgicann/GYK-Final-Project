# Terramind Simple Docker Setup

## 🚀 Basit Docker Konfigürasyonu

Bu setup, Flutter web uygulamasını development modunda çalıştırır - tıpkı `flutter run -d chrome` komutu gibi!

## 📋 Gereksinimler

- Docker Desktop
- En az 2GB RAM
- En az 5GB disk alanı

## 🏗️ Mimari

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Flutter Web) │    │   (Flask API)   │    │   (PostgreSQL)  │
│   Port: 3000    │    │   Port: 5000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Redis Cache   │
                    │   Port: 6379    │
                    └─────────────────┘
```

## 🚀 Hızlı Başlangıç

### Windows
```bash
# PowerShell ile
.\start_simple.ps1

# Veya Batch ile
start_simple.bat
```

### Linux/Mac
```bash
cd backend
docker-compose up -d
```

## 📁 Servisler

### 1. Frontend (Flutter Web Development Server)
- **Port**: 3000
- **URL**: http://localhost:3000
- **Mode**: Development (hot reload enabled)
- **Responsive**: Mobile ve desktop için optimize edilmiş

### 2. Backend (Flask API)
- **Port**: 5000
- **URL**: http://localhost:5000
- **Database**: PostgreSQL
- **Cache**: Redis

### 3. Database (PostgreSQL)
- **Port**: 5432
- **Database**: terramind_db
- **User**: postgres
- **Password**: pass.123

### 4. Cache (Redis)
- **Port**: 6379
- **Memory**: 256MB

## 🔧 Özellikler

### Frontend
- ✅ Flutter web development server
- ✅ Hot reload (kod değişikliklerinde otomatik yenileme)
- ✅ Responsive design (mobil + desktop)
- ✅ Chrome DevTools desteği
- ✅ Source maps (debugging için)

### Backend
- ✅ Flask API server
- ✅ PostgreSQL database
- ✅ Redis caching
- ✅ JWT authentication
- ✅ CORS enabled

## 🧪 Test Etme

### Frontend
```bash
# Browser'da aç
http://localhost:3000
```

### Backend API
```bash
# Health check
curl http://localhost:5000/health

# API test
curl http://localhost:5000/api/products
```

## 🔄 Development Workflow

### 1. Code Changes
```bash
# Frontend değişiklikleri otomatik olarak yenilenir (hot reload)
# Backend değişiklikleri için:
cd backend
docker-compose restart backend
```

### 2. View Logs
```bash
# Frontend logs
docker-compose logs -f frontend

# Backend logs
docker-compose logs -f backend

# All logs
docker-compose logs -f
```

### 3. Stop Services
```bash
cd backend
docker-compose down
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using the port
netstat -ano | findstr :3000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F
```

#### 2. Frontend Not Loading
```bash
# Check frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend
```

#### 3. Backend Connection Failed
```bash
# Check backend logs
docker-compose logs backend

# Check database
docker-compose logs db
```

### Reset Everything
```bash
cd backend
docker-compose down -v
docker-compose up -d
```

## 📊 Monitoring

### Container Status
```bash
cd backend
docker-compose ps
```

### Resource Usage
```bash
docker stats
```

## 🎯 Avantajlar

1. **Basit**: Karmaşık nginx konfigürasyonu yok
2. **Hızlı**: Flutter development server çok hızlı
3. **Responsive**: Mobil ve desktop için optimize
4. **Hot Reload**: Kod değişikliklerinde otomatik yenileme
5. **Debugging**: Chrome DevTools tam desteği
6. **Lightweight**: Minimal resource kullanımı

## 🚀 Production için

Production'da nginx kullanmak isterseniz, `frontend/Dockerfile` dosyasını production build için güncelleyebilirsiniz:

```dockerfile
# Production build
RUN flutter build web --release
# ... nginx setup
```

Ama development için bu basit setup mükemmel! 🎉
