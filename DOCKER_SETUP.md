# Terramind Docker Setup

## 🚀 Full Stack Docker Configuration

Bu proje artık tamamen Docker üzerinden çalışacak şekilde yapılandırılmıştır. Backend, Frontend, Veritabanı ve Nginx reverse proxy tümü Docker container'larında çalışır.

## 📋 Gereksinimler

- Docker Desktop (Windows/Mac) veya Docker Engine (Linux)
- Docker Compose v2.0+
- En az 4GB RAM
- En az 10GB disk alanı

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
                    │   Nginx Proxy   │
                    │   Port: 80      │
                    └─────────────────┘
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
.\start_full_stack.ps1

# Veya Batch ile
start_full_stack.bat
```

### Linux/Mac
```bash
cd backend
docker-compose up -d
```

## 📁 Servisler

### 1. Frontend (Flutter Web)
- **Port**: 3000
- **URL**: http://localhost:3000
- **Dockerfile**: `frontend/Dockerfile`
- **Nginx Config**: `frontend/nginx.conf`

### 2. Backend (Flask API)
- **Port**: 5000
- **URL**: http://localhost:5000
- **Dockerfile**: `backend/Dockerfile`
- **Dependencies**: PostgreSQL, Redis

### 3. Database (PostgreSQL)
- **Port**: 5432
- **Database**: terramind_db
- **User**: postgres
- **Password**: pass.123
- **Optimizations**: Performance tuning, Turkish locale

### 4. Cache (Redis)
- **Port**: 6379
- **Memory**: 256MB
- **Persistence**: RDB + AOF
- **Config**: `backend/redis.conf`

### 5. Reverse Proxy (Nginx)
- **Port**: 80
- **URL**: http://localhost
- **Config**: `backend/nginx.conf`
- **Features**: Load balancing, CORS, Gzip, Security headers

## 🔧 Konfigürasyon

### Environment Variables

#### Backend
```bash
FLASK_ENV=production
DATABASE_URL=postgresql://postgres:pass.123@db:5432/terramind_db
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

#### Frontend
```bash
API_BASE_URL=http://backend:5000
```

### Database Configuration
- **Encoding**: UTF-8 with Turkish locale
- **Extensions**: UUID, pg_stat_statements, unaccent
- **Performance**: Optimized for 200 max connections
- **Memory**: 256MB shared buffers

### Redis Configuration
- **Memory Limit**: 256MB with LRU eviction
- **Persistence**: RDB + AOF for durability
- **Performance**: Optimized for caching

## 🧪 Test Etme

### Full Stack Test
```bash
python test_full_stack.py
```

### Individual Service Tests
```bash
# Backend test
curl http://localhost:5000/health

# Frontend test
curl http://localhost:3000/health

# Nginx proxy test
curl http://localhost/health
```

## 📊 Monitoring

### Container Status
```bash
cd backend
docker-compose ps
```

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Resource Usage
```bash
docker stats
```

## 🔄 Development Workflow

### 1. Code Changes
```bash
# Backend changes
cd backend
docker-compose restart backend

# Frontend changes
cd backend
docker-compose restart frontend
```

### 2. Database Migrations
```bash
cd backend
python migrate_database.py upgrade
```

### 3. Rebuild Images
```bash
cd backend
docker-compose build --no-cache
docker-compose up -d
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

#### 2. Database Connection Failed
```bash
# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### 3. Frontend Build Failed
```bash
# Check Flutter installation in container
docker-compose exec frontend flutter --version

# Rebuild frontend
docker-compose build --no-cache frontend
```

#### 4. CORS Issues
- Check nginx configuration
- Verify API_BASE_URL environment variable
- Check browser developer tools for CORS errors

### Reset Everything
```bash
cd backend
docker-compose down -v
docker-compose up -d
```

## 📈 Performance Optimization

### Database
- Connection pooling enabled
- Query optimization
- Index optimization
- Statistics collection

### Redis
- Memory optimization
- Persistence tuning
- Connection pooling

### Nginx
- Gzip compression
- Static file caching
- Load balancing
- Security headers

## 🔒 Security

### Headers
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

### CORS
- Configured for localhost:3000
- Credentials enabled
- Preflight requests handled

### Rate Limiting
- API: 10 requests/second
- Auth: 5 requests/second
- Burst handling enabled

## 📝 Logs

### Application Logs
- Backend: `backend/logs/`
- Frontend: Container logs
- Database: Container logs
- Nginx: Container logs

### Log Rotation
- Automatic log rotation configured
- Old logs cleaned up after 90 days
- Error logs separated from info logs

## 🚀 Production Deployment

### Environment Variables
```bash
# Set production environment variables
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:pass@host:5432/db
export REDIS_URL=redis://host:6379/0
export SECRET_KEY=your-production-secret
export JWT_SECRET_KEY=your-production-jwt-secret
```

### SSL/TLS
- Add SSL certificates to `backend/ssl/`
- Update nginx configuration for HTTPS
- Configure Let's Encrypt for automatic certificates

### Monitoring
- Set up health checks
- Configure log aggregation
- Set up alerting
- Monitor resource usage

## 📞 Support

Herhangi bir sorun yaşarsanız:

1. Logları kontrol edin
2. Container durumunu kontrol edin
3. Port çakışmalarını kontrol edin
4. Environment variable'ları kontrol edin
5. Docker ve Docker Compose versiyonlarını kontrol edin

## 🎯 Next Steps

- [ ] SSL/TLS configuration
- [ ] CI/CD pipeline setup
- [ ] Monitoring and alerting
- [ ] Backup and recovery procedures
- [ ] Load testing
- [ ] Security audit
