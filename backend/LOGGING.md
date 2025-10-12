# Terramind Backend Logging System

Bu dokümantasyon, Terramind Backend API'sinde kullanılan kapsamlı logging sistemini açıklar.

## 🎯 Amaç

Logging sistemi, uygulamanın tüm fonksiyonlarını, API çağrılarını, veritabanı işlemlerini ve hataları detaylı bir şekilde takip etmek için tasarlanmıştır. Bu sayede:

- **Debugging**: Hataları kolayca tespit edebilirsiniz
- **Performance Monitoring**: Fonksiyon çalışma sürelerini takip edebilirsiniz
- **API Tracking**: Tüm API çağrılarını izleyebilirsiniz
- **Security**: Şüpheli aktiviteleri tespit edebilirsiniz

## 📁 Log Dosyaları

Loglar `backend/logs/` klasöründe saklanır:

- **`terramind.log`**: Tüm loglar (10MB'a kadar, 5 backup)
- **`errors.log`**: Sadece hata logları (5MB'a kadar, 3 backup)

## 🔧 Konfigürasyon

### Environment Variables

```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Log Seviyeleri

- **DEBUG**: Detaylı bilgi (geliştirme için)
- **INFO**: Genel bilgi (varsayılan)
- **WARNING**: Uyarılar
- **ERROR**: Hatalar
- **CRITICAL**: Kritik hatalar

## 🎨 Log Formatı

### Console Output
```
2025-10-12 13:57:38 | INFO | terramind.test.basic | [INFO] Testing basic logging functionality
```

### File Output
```
2025-10-12 13:57:38,159 | INFO | terramind.test.basic | <module>       :1    | [INFO] Testing basic logging functionality
```

## 🛠️ Kullanım

### 1. Temel Logging

```python
from utils.logger import get_logger, log_info, log_error, log_success

# Logger instance oluşturma
logger = get_logger('my_module')

# Temel log mesajları
log_info("İşlem başlatıldı")
log_success("İşlem tamamlandı")
log_error("Hata oluştu")
```

### 2. Fonksiyon Logging Decorator

```python
from utils.logger import log_function_call

@log_function_call
def my_function(param1, param2):
    """Bu fonksiyon otomatik olarak loglanacak"""
    return param1 + param2
```

**Çıktı:**
```
[ENTER] my_module.my_function
[ARGS] ['value1', 'value2']
[EXIT] my_module.my_function (took 0.003s)
```

### 3. API Endpoint Logging

```python
from utils.logger import log_api_call

@log_api_call
@app.route('/api/users', methods=['GET'])
def get_users():
    """API endpoint otomatik olarak loglanacak"""
    return jsonify(users)
```

**Çıktı:**
```
[API] GET /api/users from 127.0.0.1
[USER-AGENT] Mozilla/5.0...
[ENTER] routes.users.get_users
[EXIT] routes.users.get_users (took 0.045s)
```

### 4. Veritabanı İşlemleri

```python
from utils.logger import log_database_operation

@log_database_operation
def find_user_by_email(email):
    """Veritabanı sorgusu otomatik olarak loglanacak"""
    return User.query.filter_by(email=email).first()
```

**Çıktı:**
```
[DB] find_user_by_email
[ENTER] models.user.find_user_by_email
[EXIT] models.user.find_user_by_email (took 0.012s)
```

### 5. Business Logic

```python
from utils.logger import log_business_logic

@log_business_logic
def calculate_recommendations(environment_data):
    """İş mantığı otomatik olarak loglanacak"""
    return process_data(environment_data)
```

**Çıktı:**
```
[BUSINESS] calculate_recommendations
[ENTER] services.recommendation.calculate_recommendations
[EXIT] services.recommendation.calculate_recommendations (took 0.156s)
```

### 6. Performance Monitoring

```python
from utils.logger import log_performance
import time

def slow_operation():
    start_time = time.time()
    
    # Yavaş işlem
    time.sleep(2)
    
    duration = time.time() - start_time
    log_performance("slow_operation", duration)
```

**Çıktı:**
```
[PERFORMANCE] slow_operation took 2.000s
```

## 🔒 Güvenlik

### Hassas Veri Koruması

Logging sistemi otomatik olarak hassas verileri korur:

```python
@log_function_call
def login_user(email, password):
    # password parametresi otomatik olarak "***" olarak loglanır
    pass
```

**Korumalı alanlar:**
- `password`
- `token`
- `secret`
- `key`
- `auth`

## 📊 Log Analizi

### Log Dosyalarını İnceleme

```bash
# Son 100 satırı görüntüle
tail -n 100 logs/terramind.log

# Hata loglarını filtrele
grep "ERROR" logs/terramind.log

# Belirli bir modülü filtrele
grep "terramind.api" logs/terramind.log

# Performance loglarını filtrele
grep "PERFORMANCE" logs/terramind.log
```

### Log Rotation

Log dosyaları otomatik olarak döndürülür:
- **terramind.log**: 10MB'a ulaştığında yeni dosya oluşturur
- **errors.log**: 5MB'a ulaştığında yeni dosya oluşturur
- Eski dosyalar `.1`, `.2` gibi uzantılarla saklanır

## 🎯 Best Practices

### 1. Logger İsimlendirme

```python
# Modül bazında logger kullanın
logger = get_logger('models.user')
logger = get_logger('routes.auth')
logger = get_logger('services.recommendation')
```

### 2. Log Seviyelerini Doğru Kullanın

```python
# DEBUG: Geliştirme sırasında detaylı bilgi
logger.debug(f"Processing item: {item}")

# INFO: Normal işlem akışı
logger.info("User logged in successfully")

# WARNING: Potansiyel sorunlar
logger.warning("Rate limit approaching")

# ERROR: Hatalar
logger.error("Database connection failed")
```

### 3. Decorator Kullanımı

```python
# Fonksiyonlar için
@log_function_call
def process_data(data):
    pass

# API endpoint'leri için
@log_api_call
@app.route('/api/data', methods=['POST'])
def create_data():
    pass

# Veritabanı işlemleri için
@log_database_operation
def save_user(user_data):
    pass
```

### 4. Performance Monitoring

```python
import time

def expensive_operation():
    start_time = time.time()
    
    # İşlem
    result = do_work()
    
    # Performance log
    duration = time.time() - start_time
    if duration > 1.0:  # 1 saniyeden uzun süren işlemler
        log_performance("expensive_operation", duration)
    
    return result
```

## 🚀 Production Kullanımı

### Environment Variables

```bash
# Production için
LOG_LEVEL=WARNING
FLASK_ENV=production
```

### Log Monitoring

Production ortamında log dosyalarını izlemek için:

```bash
# Real-time log monitoring
tail -f logs/terramind.log

# Error monitoring
tail -f logs/errors.log

# Performance monitoring
grep "PERFORMANCE" logs/terramind.log | tail -20
```

### Log Aggregation

Büyük ölçekli uygulamalar için log aggregation araçları kullanın:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Fluentd**
- **Splunk**

## 🔧 Troubleshooting

### Yaygın Sorunlar

1. **Log dosyaları oluşmuyor**
   - `logs/` klasörünün yazma izni olduğundan emin olun
   - Disk alanını kontrol edin

2. **Çok fazla log**
   - `LOG_LEVEL`'ı `WARNING` veya `ERROR`'a ayarlayın
   - Gereksiz `DEBUG` loglarını kaldırın

3. **Performance sorunları**
   - Log dosyalarının boyutunu kontrol edin
   - Log rotation ayarlarını optimize edin

## 📈 Monitoring ve Alerting

### Kritik Hatalar için Alerting

```python
# Kritik hatalar için özel handling
try:
    critical_operation()
except Exception as e:
    logger.critical(f"Critical error: {e}")
    # Alerting sistemi buraya eklenebilir
    send_alert(f"Critical error in production: {e}")
```

### Performance Thresholds

```python
# Yavaş işlemler için alerting
@log_function_call
def slow_operation():
    start_time = time.time()
    result = do_work()
    duration = time.time() - start_time
    
    if duration > 5.0:  # 5 saniyeden uzun
        logger.warning(f"Slow operation detected: {duration:.2f}s")
        # Alerting sistemi buraya eklenebilir
    
    return result
```

---

## 📝 Özet

Terramind logging sistemi:

✅ **Kapsamlı**: Tüm fonksiyonları, API'leri ve veritabanı işlemlerini loglar  
✅ **Performans**: Çalışma sürelerini takip eder  
✅ **Güvenli**: Hassas verileri korur  
✅ **Esnek**: Farklı log seviyeleri ve formatları  
✅ **Production Ready**: Log rotation ve monitoring desteği  

Bu sistem sayesinde uygulamanızın her detayını takip edebilir, hataları hızlıca tespit edebilir ve performans sorunlarını çözebilirsiniz.
