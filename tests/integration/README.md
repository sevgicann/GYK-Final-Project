# TerraMind Integration Tests

Bu klasör TerraMind projesinin entegrasyon testlerini içerir. Bu testler mobil ve web platformları arasındaki entegrasyonu, API entegrasyonunu, ML model entegrasyonunu ve veritabanı entegrasyonunu test eder.

## 📁 Klasör Yapısı

```
tests/integration/
├── backend/                          # Backend entegrasyon testleri
│   ├── test_api_integration.py      # API entegrasyon testleri
│   ├── test_ml_integration.py       # ML model entegrasyon testleri
│   └── test_database_integration.py # Veritabanı entegrasyon testleri
├── frontend/                         # Frontend entegrasyon testleri
│   └── test_flutter_backend_integration.dart # Flutter-Backend entegrasyon testleri
├── cross_platform/                   # Cross-platform entegrasyon testleri
│   └── test_cross_platform_integration.py # Cross-platform entegrasyon testleri
├── run_integration_tests.py         # Entegrasyon test runner
└── README.md                        # Bu dosya
```

## 🧪 Test Kategorileri

### 1. **Backend Integration Tests**

#### API Integration Tests (`test_api_integration.py`)
- **Authentication Integration**: Kullanıcı kayıt, giriş, token yenileme akışları
- **Product Integration**: Ürün CRUD işlemleri, arama ve filtreleme
- **Environment Integration**: Çevre verisi yönetimi
- **ML Integration**: ML modeli ile API entegrasyonu
- **Recommendation Integration**: Öneri sistemi entegrasyonu
- **Data Flow Integration**: Tam kullanıcı yolculuğu
- **Error Handling Integration**: API hata yönetimi
- **Performance Integration**: API performans testleri
- **Security Integration**: API güvenlik testleri

#### ML Integration Tests (`test_ml_integration.py`)
- **ML Service Integration**: ML servis entegrasyonu
- **XGBoost Integration**: XGBoost model entegrasyonu
- **LightGBM Integration**: LightGBM model entegrasyonu
- **Bi-directional Prediction**: Çift yönlü tahmin entegrasyonu
- **ML Data Integration**: ML veri ön işleme entegrasyonu
- **ML Performance Integration**: ML performans testleri
- **ML Error Handling**: ML hata yönetimi
- **Model Comparison**: Model karşılaştırma testleri

#### Database Integration Tests (`test_database_integration.py`)
- **Database Connection**: Veritabanı bağlantı testleri
- **Model Integration**: Model entegrasyon testleri
- **Query Integration**: Karmaşık sorgu entegrasyonu
- **Migration Integration**: Veritabanı migrasyon testleri
- **Performance Integration**: Veritabanı performans testleri
- **Error Handling**: Veritabanı hata yönetimi
- **Backup Integration**: Veritabanı yedekleme testleri

### 2. **Frontend Integration Tests**

#### Flutter-Backend Integration (`test_flutter_backend_integration.dart`)
- **API Integration**: Flutter-Backend API entegrasyonu
- **Product Service Integration**: Ürün servisi entegrasyonu
- **User Service Integration**: Kullanıcı servisi entegrasyonu
- **ML Service Integration**: ML servis entegrasyonu
- **Environment Service Integration**: Çevre servisi entegrasyonu
- **Recommendation Service Integration**: Öneri servisi entegrasyonu
- **Cross-Platform Integration**: Cross-platform entegrasyon
- **Performance Integration**: Performans entegrasyon testleri
- **Error Handling Integration**: Hata yönetimi entegrasyonu

### 3. **Cross-Platform Integration Tests**

#### Cross-Platform Integration (`test_cross_platform_integration.py`)
- **Data Consistency**: Cross-platform veri tutarlılığı
- **API Compatibility**: API uyumluluğu
- **ML Integration**: Cross-platform ML entegrasyonu
- **Authentication**: Cross-platform kimlik doğrulama
- **Data Synchronization**: Veri senkronizasyonu
- **Performance**: Cross-platform performans
- **Security**: Cross-platform güvenlik
- **Error Handling**: Cross-platform hata yönetimi
- **Data Migration**: Veri migrasyonu

## 🚀 Test Çalıştırma

### Tüm Entegrasyon Testlerini Çalıştırma
```bash
python tests/integration/run_integration_tests.py
```

### Belirli Test Kategorilerini Çalıştırma
```bash
# API entegrasyon testleri
python tests/integration/run_integration_tests.py --type api

# ML entegrasyon testleri
python tests/integration/run_integration_tests.py --type ml

# Veritabanı entegrasyon testleri
python tests/integration/run_integration_tests.py --type database

# Cross-platform entegrasyon testleri
python tests/integration/run_integration_tests.py --type cross_platform
```

### Sadece Backend Testleri
```bash
python tests/integration/run_integration_tests.py --backend-only
```

### Sadece Frontend Testleri
```bash
python tests/integration/run_integration_tests.py --frontend-only
```

### Coverage Raporu ile
```bash
python tests/integration/run_integration_tests.py --coverage
```

### Verbose Çıktı ile
```bash
python tests/integration/run_integration_tests.py --verbose
```

### Test Raporu Oluşturma
```bash
python tests/integration/run_integration_tests.py --report
```

## 📊 Test Markers

Entegrasyon testleri şu marker'ları kullanır:

- `@pytest.mark.integration`: Tüm entegrasyon testleri
- `@pytest.mark.api`: API entegrasyon testleri
- `@pytest.mark.ml`: ML entegrasyon testleri
- `@pytest.mark.database`: Veritabanı entegrasyon testleri
- `@pytest.mark.cross_platform`: Cross-platform entegrasyon testleri
- `@pytest.markoth`: Kimlik doğrulama entegrasyon testleri
- `@pytest.mark.products`: Ürün entegrasyon testleri
- `@pytest.mark.environments`: Çevre entegrasyon testleri
- `@pytest.mark.recommendations`: Öneri entegrasyon testleri
- `@pytest.mark.data_flow`: Veri akışı entegrasyon testleri
- `@pytest.mark.error_handling`: Hata yönetimi entegrasyon testleri
- `@pytest.mark.performance`: Performans entegrasyon testleri
- `@pytest.mark.security`: Güvenlik entegrasyon testleri

## 🔧 Test Konfigürasyonu

### Backend Test Konfigürasyonu
- **Test Database**: SQLite in-memory database
- **Test Client**: Flask test client
- **Mocking**: ML servisleri için mock'lar
- **Fixtures**: Test verileri için factory'ler

### Frontend Test Konfigürasyonu
- **Test Framework**: Flutter test framework
- **HTTP Mocking**: API çağrıları için mock'lar
- **Service Testing**: Servis katmanı testleri
- **Widget Testing**: Widget entegrasyon testleri

## 📈 Test Metrikleri

### Coverage Hedefleri
- **Backend API Coverage**: %90+
- **ML Integration Coverage**: %85+
- **Database Integration Coverage**: %90+
- **Frontend Integration Coverage**: %85+

### Performans Hedefleri
- **API Response Time**: < 2 saniye
- **ML Prediction Time**: < 5 saniye
- **Database Query Time**: < 1 saniye
- **Frontend Load Time**: < 3 saniye

## 🐛 Hata Yönetimi

Entegrasyon testleri şu hata senaryolarını test eder:

- **Network Errors**: Ağ hataları
- **API Errors**: API hataları
- **Database Errors**: Veritabanı hataları
- **ML Model Errors**: ML model hataları
- **Authentication Errors**: Kimlik doğrulama hataları
- **Data Validation Errors**: Veri doğrulama hataları

## 🔒 Güvenlik Testleri

Entegrasyon testleri şu güvenlik konularını test eder:

- **CORS Headers**: Cross-origin resource sharing
- **SQL Injection**: SQL enjeksiyon koruması
- **XSS Protection**: Cross-site scripting koruması
- **Authentication**: Kimlik doğrulama güvenliği
- **Rate Limiting**: Hız sınırlaması
- **Input Validation**: Girdi doğrulama

## 📝 Test Verileri

Entegrasyon testleri şu test verilerini kullanır:

- **Sample Products**: Gerçek crop verileri (wheat, corn, cotton, sunflower, etc.)
- **Sample Users**: Test kullanıcıları
- **Sample Environments**: Test çevre verileri
- **ML Test Data**: ML model test verileri

## 🚀 CI/CD Entegrasyonu

Entegrasyon testleri CI/CD pipeline'ında çalıştırılabilir:

```yaml
# GitHub Actions örneği
- name: Run Integration Tests
  run: |
    python tests/integration/run_integration_tests.py --coverage --report
    
- name: Upload Coverage Reports
  uses: codecov/codecov-action@v3
  with:
    files: backend/coverage.xml,frontend/coverage/lcov.info
```

## 📚 Daha Fazla Bilgi

- [Unit Tests](../unit/README.md)
- [Security Tests](../security/README.md)
- [Accessibility Tests](../accessibility/README.md)
- [Testing Strategy](../../README_TESTING.md)
