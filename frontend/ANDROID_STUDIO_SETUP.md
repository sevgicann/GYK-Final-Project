# Android Studio Kurulum Rehberi

## 📱 TerraMind Uygulamasını Android Studio'da Çalıştırma

### 1. Gereksinimler
- **Android Studio** (en son sürüm)
- **Android SDK** (API 21+)
- **Flutter SDK** (kurulu olmalı)
- **Java Development Kit (JDK)** 11+

### 2. Android Studio Kurulumu
1. [Android Studio'yu indirin](https://developer.android.com/studio)
2. Kurulum sırasında **Android SDK**'yı da kurun
3. Android Studio'yu açın

### 3. Flutter Plugin Kurulumu
1. **File > Settings > Plugins**
2. **"Flutter"** arayın ve kurun
3. **"Dart"** plugin'ini de kurun
4. Android Studio'yu yeniden başlatın

### 4. Projeyi Açma
1. Android Studio'yu açın
2. **"Open an existing Android Studio project"** seçin
3. `C:\Users\sevgi\GYK-Final-Project\frontend` klasörünü seçin
4. **"Open"** tıklayın

### 5. Flutter SDK Yolu Ayarlama
1. **File > Settings > Languages & Frameworks > Flutter**
2. Flutter SDK path'ini ayarlayın (örn: `C:\flutter`)
3. **"Apply"** ve **"OK"** tıklayın

### 6. Android Emülatör Oluşturma
1. **Tools > AVD Manager**
2. **"Create Virtual Device"** tıklayın
3. **Phone** kategorisinden bir cihaz seçin (örn: Pixel 4)
4. **System Image** seçin (API 30 veya üzeri)
5. **"Next"** ve **"Finish"** tıklayın
6. Emülatörü başlatın

### 7. Uygulamayı Çalıştırma
1. Android Studio'da **Run** butonuna basın
2. Veya terminal'de:
   ```bash
   cd frontend
   flutter run
   ```

## 🌐 Web'de Çalıştırma
```bash
cd frontend
flutter run -d chrome
```

## 📱 Gerçek Android Cihazda Çalıştırma
1. Android cihazınızda **Geliştirici Seçenekleri**'ni açın
2. **USB Hata Ayıklama**'yı etkinleştirin
3. USB kablosu ile bilgisayara bağlayın
4. `flutter run` komutunu çalıştırın

## 🔧 Sorun Giderme
- **Flutter doctor** çalıştırarak sistem durumunu kontrol edin
- **Android SDK** kurulu olduğundan emin olun
- **Emülatör** çalışır durumda olduğundan emin olun

## ✅ Özellikler
- ✅ Web tarayıcısında çalışır
- ✅ Android emülatörde çalışır
- ✅ Gerçek Android cihazda çalışır
- ✅ GPS konum özelliği
- ✅ İnternet bağlantısı
- ✅ Yerel veri saklama
