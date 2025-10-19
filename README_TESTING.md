# TerraMind Test Suite

Bu dokümantasyon TerraMind projesinin test yapısını ve nasıl test çalıştırılacağını açıklar.

## 📋 Test Yapısı

### Test Klasör Organizasyonu

```
tests/
├── __init__.py
├── unit/                          # Birim testler
│   ├── backend/                   # Backend birim testleri
│   │   ├── models/                # Model testleri
│   │   ├── services/              # Servis testleri
│   │   └── routes/                # API route testleri
│   └── frontend/                  # Frontend birim testleri
│       ├── services/              # Servis testleri
│       ├── widgets/               # Widget testleri
│       └── models/                # Model testleri
├── integration/                   # Entegrasyon testleri
│   ├── api/                       # API entegrasyon testleri
│   ├── database/                  # Veritabanı testleri
│   └── ml/                        # ML model testleri
├── security/                      # Güvenlik testleri
│   ├── auth/                      # Kimlik doğrulama testleri
│   ├── api/                       # API güvenlik testleri
│   └── injection/                 # Injection saldırı testleri
├── fixtures/                      # Test verileri ve yardımcılar
│   ├── data/                      # Örnek test verileri
│   ├── factories/                 # Test veri üreticileri
│   └── mocks/                     # Mock objeler
└── utils/                         # Test yardımcı araçları
    ├── database/                  # Veritabanı test yardımcıları
    ├── api/                       # API test yardımcıları
    └── ml/                        # ML test yardımcıları
```

## 🚀 Test Çalıştırma

### Gereksinimler

#### Backend Test Gereksinimleri
```bash
cd backend
pip install -r requirements-dev.txt
```

#### Frontend Test Gereksinimleri
```bash
cd frontend
flutter pub get
```

### Test Çalıştırma Komutları

#### Tüm Testleri Çalıştırma
```bash
# Python test runner ile
python tests/run_tests.py

# Manuel olarak
python tests/run_tests.py --type all --coverage --verbose
```

#### Sadece Birim Testleri
```bash
python tests/run_tests.py --type unit
```

#### Sadece Entegrasyon Testleri
```bash
python tests/run_tests.py --type integration
```

#### Sadece Güvenlik Testleri
```bash
python tests/run_tests.py --type security
```

#### Sadece Backend Testleri
```bash
python tests/run_tests.py --backend-only
```

#### Sadece Frontend Testleri
```bash
python tests/run_tests.py --frontend-only
```

### Manuel Test Çalıştırma

#### Backend Testleri
```bash
cd backend
pytest ../tests/unit/backend/ -v --cov=. --cov-report=html
```

#### Frontend Testleri
```bash
cd frontend
flutter test test/unit/
```

## 🧪 Test Kategorileri

### Unit Tests (Birim Testler)

Birim testler, uygulamanın en küçük bileşenlerini (fonksiyonlar, sınıflar, modüller) test eder.

#### Backend Unit Tests
- **Models**: Veritabanı modelleri testleri
  - `test_user_model.py` - User modeli testleri
  - `test_product_model.py` - Product modeli testleri
  - `test_environment_model.py` - Environment modeli testleri

- **Services**: İş mantığı servisleri testleri
  - `test_ml_service.py` - ML Service testleri

- **Routes**: API endpoint'leri testleri
  - `test_auth_routes.py` - Authentication route testleri
  - `test_products_routes.py` - Products route testleri

#### Frontend Unit Tests
- **Services**: Servis sınıfları testleri
  - `test_product_service.dart` - ProductService testleri

- **Widgets**: UI bileşenleri testleri
  - `test_custom_button.dart` - CustomButton widget testleri
  - `test_custom_card.dart` - CustomCard widget testleri

- **Models**: Veri modelleri testleri
  - `test_product.dart` - Product model testleri

### Integration Tests (Entegrasyon Testleri)

Entegrasyon testleri, farklı bileşenlerin birlikte nasıl çalıştığını test eder.

- **API Integration**: API endpoint'lerinin gerçek veritabanı ile çalışması
- **Database Integration**: Veritabanı işlemlerinin test edilmesi
- **ML Integration**: ML modellerinin gerçek verilerle test edilmesi

### Security Tests (Güvenlik Testleri)

Güvenlik testleri, uygulamanın güvenlik açıklarını test eder.

- **Authentication**: Kimlik doğrulama güvenliği
- **API Security**: API endpoint'lerinin güvenliği
- **Data Security**: Veri güvenliği testleri
- **Injection Tests**: SQL injection, XSS gibi saldırı testleri

## 🔧 Test Konfigürasyonu

### Backend Test Konfigürasyonu

#### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
addopts = --verbose --cov=. --cov-report=html
markers =
    unit: Unit tests
    integration: Integration tests
    security: Security tests
```

#### conftest.py
- Test fixtures ve konfigürasyonu
- Veritabanı test setup'ı
- Mock servisleri

### Frontend Test Konfigürasyonu

#### test/ klasörü
- `test/unit/` - Birim testleri
- `test/widget_test.dart` - Ana widget testi

## 📊 Test Coverage (Test Kapsamı)

### Coverage Raporları

#### Backend Coverage
```bash
cd backend
pytest --cov=. --cov-report=html --cov-report=term-missing
```

Coverage raporu `htmlcov/` klasöründe oluşturulur.

#### Frontend Coverage
```bash
cd frontend
flutter test --coverage
```

Coverage raporu `coverage/` klasöründe oluşturulur.

### Coverage Hedefleri

- **Unit Tests**: %80+ coverage
- **Integration Tests**: %70+ coverage
- **Critical Paths**: %95+ coverage

## 🛠️ Test Utilities

### Test Fixtures

#### Sample Data
```python
from tests.fixtures.data.sample_data import SAMPLE_USERS, SAMPLE_PRODUCTS
```

#### Factories
```python
from tests.fixtures.factories.user_factory import UserFactory
from tests.fixtures.factories.product_factory import ProductFactory
```

### Test Helpers

#### API Test Client
```python
from tests.utils.api.test_client import APITestClient, APITestAssertions
```

#### ML Test Helpers
```python
from tests.utils.ml.test_ml_helpers import MLTestHelpers
```

#### Database Test Utils
```python
from tests.utils.database.test_db import TestDatabase
```

## 🏷️ Test Markers

### Backend Markers
- `@pytest.mark.unit` - Birim testleri
- `@pytest.mark.integration` - Entegrasyon testleri
- `@pytest.mark.security` - Güvenlik testleri
- `@pytest.mark.database` - Veritabanı testleri
- `@pytest.mark.api` - API testleri
- `@pytest.mark.ml` - ML testleri
- `@pytest.mark.auth` - Kimlik doğrulama testleri

### Frontend Markers
- Flutter test'lerde `group()` fonksiyonu kullanılır

## 🐛 Debugging Tests

### Backend Test Debugging
```bash
cd backend
pytest ../tests/unit/backend/models/test_user_model.py::TestUserModel::test_user_creation -v -s
```

### Frontend Test Debugging
```bash
cd frontend
flutter test test/unit/services/test_product_service.dart --verbose
```

## 📈 Continuous Integration

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Backend Tests
        run: python tests/run_tests.py --backend-only --coverage
      - name: Run Frontend Tests
        run: python tests/run_tests.py --frontend-only --coverage
```

## 🔍 Test Best Practices

### 1. Test İsimlendirme
- Test fonksiyonları `test_` ile başlamalı
- Açıklayıcı isimler kullanılmalı
- Test sınıfları `Test` ile başlamalı

### 2. Test Yapısı
- Arrange, Act, Assert (AAA) pattern kullanılmalı
- Her test tek bir şeyi test etmeli
- Test'ler birbirinden bağımsız olmalı

### 3. Test Verileri
- Factory pattern kullanılmalı
- Test verileri temiz ve tutarlı olmalı
- Edge case'ler test edilmeli

### 4. Mocking
- External dependencies mock'lanmalı
- Database işlemleri mock'lanmalı
- API çağrıları mock'lanmalı

### 5. Assertions
- Açık ve anlaşılır assertion'lar kullanılmalı
- Error message'lar açıklayıcı olmalı
- Edge case'ler için özel assertion'lar yazılmalı

## 📚 Test Dokümantasyonu

### Test Plan
- [ ] Unit test coverage %80+
- [ ] Integration test coverage %70+
- [ ] Security test coverage %90+
- [ ] Performance test coverage %60+

### Test Checklist
- [ ] Tüm public method'lar test edilmeli
- [ ] Edge case'ler test edilmeli
- [ ] Error handling test edilmeli
- [ ] Input validation test edilmeli
- [ ] Authentication test edilmeli
- [ ] Authorization test edilmeli

## 🤝 Contributing to Tests

### Yeni Test Ekleme
1. Uygun klasöre test dosyası ekleyin
2. Test fonksiyonlarını `test_` ile başlatın
3. Uygun marker'ları ekleyin
4. Test'i çalıştırın ve coverage'ı kontrol edin

### Test Güncelleme
1. Mevcut test'leri güncelleyin
2. Yeni edge case'ler ekleyin
3. Coverage'ı kontrol edin
4. CI'da test'lerin geçtiğinden emin olun

## 📞 Destek

Test konularında yardım için:
- GitHub Issues kullanın
- Test dokümantasyonunu inceleyin
- Mevcut test örneklerini inceleyin
