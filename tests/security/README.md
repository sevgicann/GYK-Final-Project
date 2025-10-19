# TerraMind Security Tests

Bu klasör TerraMind projesinin güvenlik testlerini içerir. Bu testler basit ama etkili güvenlik kontrollerini yapar.

## 📁 Klasör Yapısı

```
tests/security/
├── test_authentication_security.py    # Kimlik doğrulama güvenlik testleri
├── test_api_security.py              # API güvenlik testleri
├── test_data_security.py             # Veri güvenlik testleri
├── test_ml_security.py               # ML güvenlik testleri
├── run_security_tests.py             # Güvenlik test runner
└── README.md                         # Bu dosya
```

## 🛡️ Test Kategorileri

### 1. **Authentication Security Tests** (`test_authentication_security.py`)

#### Kimlik Doğrulama Güvenlik Testleri
- **Weak Password Detection**: Zayıf şifre tespiti
- **Strong Password Acceptance**: Güçlü şifre kabulü
- **Email Validation**: Email doğrulama
- **Duplicate Email Protection**: Duplicate email koruması
- **Brute Force Protection**: Brute force koruması
- **Token Security**: Token güvenliği
- **Session Management**: Oturum yönetimi

#### Girdi Doğrulama Güvenlik Testleri
- **SQL Injection Protection**: SQL enjeksiyon koruması
- **XSS Protection**: XSS koruması
- **Input Length Validation**: Girdi uzunluk doğrulama
- **Special Character Handling**: Özel karakter işleme

### 2. **API Security Tests** (`test_api_security.py`)

#### API Kimlik Doğrulama Güvenlik Testleri
- **Protected Endpoints Require Auth**: Koruma altındaki endpoint'ler için kimlik doğrulama
- **Invalid Token Rejection**: Geçersiz token reddi
- **Token Expiration Handling**: Token süre sonu işleme

#### API Girdi Güvenlik Testleri
- **SQL Injection in API Endpoints**: API endpoint'lerinde SQL enjeksiyon
- **XSS in API Responses**: API yanıtlarında XSS
- **Large Payload Protection**: Büyük payload koruması
- **Malformed JSON Protection**: Bozuk JSON koruması

#### API Hız Sınırlaması Testleri
- **Rate Limiting on Auth Endpoints**: Kimlik doğrulama endpoint'lerinde hız sınırlaması
- **Rate Limiting on General Endpoints**: Genel endpoint'lerde hız sınırlaması
- **Rate Limiting by IP**: IP bazlı hız sınırlaması

#### API Hata Yönetimi Güvenlik Testleri
- **Error Message Security**: Hata mesajı güvenliği
- **Database Error Handling**: Veritabanı hata yönetimi
- **Validation Error Handling**: Doğrulama hata yönetimi

#### API Veri Koruma Testleri
- **Sensitive Data Filtering**: Hassas veri filtreleme
- **Data Encryption in Transit**: Aktarım sırasında veri şifreleme
- **Input Sanitization**: Girdi sanitizasyonu

#### API Erişim Kontrolü Testleri
- **User Data Isolation**: Kullanıcı veri izolasyonu
- **Admin Endpoint Protection**: Admin endpoint koruması
- **Resource Ownership Validation**: Kaynak sahipliği doğrulama

### 3. **Data Security Tests** (`test_data_security.py`)

#### Veri Şifreleme Güvenlik Testleri
- **Password Hashing Security**: Şifre hash güvenliği
- **Token Security**: Token güvenliği
- **Sensitive Data Encryption**: Hassas veri şifreleme

#### Veri Doğrulama Güvenlik Testleri
- **Input Type Validation**: Girdi tip doğrulama
- **Input Length Validation**: Girdi uzunluk doğrulama
- **Email Format Validation**: Email format doğrulama
- **Password Strength Validation**: Şifre güçlülük doğrulama

#### Veri Erişim Güvenlik Testleri
- **User Data Isolation**: Kullanıcı veri izolasyonu
- **Sensitive Data Exposure**: Hassas veri maruz kalma
- **Data Leakage Prevention**: Veri sızıntısı önleme
- **Unauthorized Data Access**: Yetkisiz veri erişimi

#### Veri Bütünlüğü Güvenlik Testleri
- **Data Consistency Validation**: Veri tutarlılık doğrulama
- **Data Corruption Prevention**: Veri bozulması önleme
- **Constraint Violation Handling**: Kısıt ihlali işleme
- **Transaction Rollback Security**: İşlem geri alma güvenliği

#### Veri Yedekleme Güvenlik Testleri
- **Backup Data Encryption**: Yedek veri şifreleme
- **Backup Access Control**: Yedek erişim kontrolü
- **Backup Data Validation**: Yedek veri doğrulama

### 4. **ML Security Tests** (`test_ml_security.py`)

#### ML Girdi Güvenlik Testleri
- **ML Input Validation**: ML girdi doğrulama
- **ML Input Range Validation**: ML girdi aralık doğrulama
- **ML Input SQL Injection**: ML girdi SQL enjeksiyon
- **ML Input XSS Protection**: ML girdi XSS koruması

#### ML Model Güvenlik Testleri
- **ML Model Integrity**: ML model bütünlüğü
- **ML Model Access Control**: ML model erişim kontrolü
- **ML Model Version Security**: ML model versiyon güvenliği

#### ML Çıktı Güvenlik Testleri
- **ML Output Sanitization**: ML çıktı sanitizasyonu
- **ML Output Data Leakage**: ML çıktı veri sızıntısı
- **ML Output Confidence Validation**: ML çıktı güven doğrulama

#### ML Veri Güvenlik Testleri
- **ML Training Data Protection**: ML eğitim verisi koruması
- **ML Model File Protection**: ML model dosya koruması
- **ML Data Encryption**: ML veri şifreleme

#### ML Performans Güvenlik Testleri
- **ML Prediction Rate Limiting**: ML tahmin hız sınırlaması
- **ML Prediction Timeout**: ML tahmin zaman aşımı
- **ML Resource Usage Limits**: ML kaynak kullanım sınırları

#### ML Hata Yönetimi Güvenlik Testleri
- **ML Error Message Security**: ML hata mesajı güvenliği
- **ML Model Error Handling**: ML model hata yönetimi

## 🚀 Test Çalıştırma

### Tüm Güvenlik Testlerini Çalıştırma
```bash
python tests/security/run_security_tests.py
```

### Belirli Güvenlik Test Kategorilerini Çalıştırma
```bash
# Kimlik doğrulama güvenlik testleri
python tests/security/run_security_tests.py --type auth

# Girdi doğrulama güvenlik testleri
python tests/security/run_security_tests.py --type input_validation

# API güvenlik testleri
python tests/security/run_security_tests.py --type api

# Veri güvenlik testleri
python tests/security/run_security_tests.py --type data_encryption

# ML güvenlik testleri
python tests/security/run_security_tests.py --type ml
```

### Coverage Raporu ile
```bash
python tests/security/run_security_tests.py --coverage
```

### Verbose Çıktı ile
```bash
python tests/security/run_security_tests.py --verbose
```

### Güvenlik Test Raporu Oluşturma
```bash
python tests/security/run_security_tests.py --report
```

## 📊 Test Markers

Güvenlik testleri şu marker'ları kullanır:

- `@pytest.mark.security`: Tüm güvenlik testleri
- `@pytest.mark.auth`: Kimlik doğrulama güvenlik testleri
- `@pytest.mark.input_validation`: Girdi doğrulama güvenlik testleri
- `@pytest.mark.api`: API güvenlik testleri
- `@pytest.mark.data_encryption`: Veri şifreleme güvenlik testleri
- `@pytest.mark.data_validation`: Veri doğrulama güvenlik testleri
- `@pytest.mark.data_access`: Veri erişim güvenlik testleri
- `@pytest.mark.data_integrity`: Veri bütünlüğü güvenlik testleri
- `@pytest.mark.data_backup`: Veri yedekleme güvenlik testleri
- `@pytest.mark.ml`: ML güvenlik testleri

## 🔧 Test Konfigürasyonu

### Güvenlik Test Konfigürasyonu
- **Test Database**: SQLite in-memory database
- **Test Client**: Flask test client
- **Mocking**: ML servisleri için mock'lar
- **Fixtures**: Test verileri için factory'ler

## 📈 Güvenlik Test Metrikleri

### Coverage Hedefleri
- **Authentication Security Coverage**: %90+
- **API Security Coverage**: %85+
- **Data Security Coverage**: %90+
- **ML Security Coverage**: %85+

### Güvenlik Hedefleri
- **Password Strength**: Minimum 8 karakter, büyük/küçük harf, sayı, özel karakter
- **Token Security**: JWT token, minimum 20 karakter
- **Rate Limiting**: Maksimum 10 istek/dakika
- **Input Validation**: Tüm girdiler doğrulanmalı

## 🐛 Güvenlik Test Senaryoları

Güvenlik testleri şu güvenlik senaryolarını test eder:

- **SQL Injection**: SQL enjeksiyon saldırıları
- **XSS Attacks**: Cross-site scripting saldırıları
- **CSRF Attacks**: Cross-site request forgery saldırıları
- **Brute Force**: Brute force saldırıları
- **Data Leakage**: Veri sızıntısı
- **Unauthorized Access**: Yetkisiz erişim
- **Input Validation**: Girdi doğrulama
- **Authentication Bypass**: Kimlik doğrulama atlatma

## 🔒 Güvenlik Önlemleri

Güvenlik testleri şu güvenlik önlemlerini test eder:

- **Password Hashing**: Şifre hash'leme
- **Token Encryption**: Token şifreleme
- **Input Sanitization**: Girdi sanitizasyonu
- **Output Encoding**: Çıktı kodlama
- **Rate Limiting**: Hız sınırlaması
- **CORS Protection**: CORS koruması
- **SQL Injection Protection**: SQL enjeksiyon koruması
- **XSS Protection**: XSS koruması

## 📝 Güvenlik Test Verileri

Güvenlik testleri şu test verilerini kullanır:

- **Weak Passwords**: Zayıf şifre örnekleri
- **Strong Passwords**: Güçlü şifre örnekleri
- **Invalid Emails**: Geçersiz email örnekleri
- **SQL Injection Payloads**: SQL enjeksiyon payload'ları
- **XSS Payloads**: XSS payload'ları
- **Large Inputs**: Büyük girdi örnekleri

## 🚀 CI/CD Entegrasyonu

Güvenlik testleri CI/CD pipeline'ında çalıştırılabilir:

```yaml
# GitHub Actions örneği
- name: Run Security Tests
  run: |
    python tests/security/run_security_tests.py --coverage --report
    
- name: Upload Security Coverage
  uses: codecov/codecov-action@v3
  with:
    files: backend/coverage.xml
```

## 📚 Daha Fazla Bilgi

- [Unit Tests](../unit/README.md)
- [Integration Tests](../integration/README.md)
- [Accessibility Tests](../accessibility/README.md)
- [Testing Strategy](../../README_TESTING.md)
