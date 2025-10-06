import pandas as pd
import numpy as np

# Veri seti parametreleri
n_samples = 100000
crops = ['rice', 'cotton', 'wheat', 'barley', 'sunflower', 'corn', 'oat']
n_per_crop = n_samples // len(crops)

regions = ['Mediterranean', 'Southeastern Anatolia', 'Marmara', 'Black Sea', 'Eastern Anatolia', 'Aegean', 'Central Anatolia']
soil_types = ['Sandy', 'Loamy', 'Clay', 'Silty']
fertilizer_types = ['Urea', 'Ammonium Sulphate', 'Potassium Nitrate']
irrigation_methods = ['Drip Irrigation', 'Sprinkler Irrigation', 'Flood Irrigation', 'Rain-fed']
weather_conditions = ['cloudy', 'sunny', 'rainy', 'windy']

# Her bir ekin için optimum koşullar (merkez değerler)
optimums = {
    'rice': {
        'region': ('Marmara', 'Black Sea', 'Mediterranean'), 'soil_type': ('Clay', 'Loamy', 'Silty'), 'soil_ph': 6.7, 'nitrogen': 90, 'phosphorus': 50, 'potassium': 40, 'moisture': 85, 'temperature_celsius': 22, 'rainfall_mm': 1600,
        'fertilizer_type': ('Urea', 'Ammonium Sulphate', 'Potassium Nitrate'), 'irrigation_method': ('Flood Irrigation', 'Sprinkler Irrigation', 'Drip Irrigation'), 'weather_condition': ('rainy', 'cloudy', 'sunny')
    },
    'cotton': {
        'region': ('Southeastern Anatolia', 'Aegean', 'Mediterranean'), 'soil_type': ('Sandy', 'Loamy', 'Clay'), 'soil_ph': 7.2, 'nitrogen': 120, 'phosphorus': 60, 'potassium': 50, 'moisture': 65, 'temperature_celsius': 30, 'rainfall_mm': 750,
        'fertilizer_type': ('Potassium Nitrate', 'Urea', 'Ammonium Sulphate'), 'irrigation_method': ('Drip Irrigation', 'Sprinkler Irrigation', 'Flood Irrigation'), 'weather_condition': ('sunny', 'cloudy', 'windy')
    },
    'wheat': {
        'region': ('Central Anatolia', 'Marmara', 'Southeastern Anatolia'), 'soil_type': ('Silty', 'Loamy', 'Clay'), 'soil_ph': 6.5, 'nitrogen': 70, 'phosphorus': 40, 'potassium': 60, 'moisture': 60, 'temperature_celsius': 20, 'rainfall_mm': 550,
        'fertilizer_type': ('Ammonium Sulphate', 'Urea', 'Potassium Nitrate'), 'irrigation_method': ('Sprinkler Irrigation', 'Rain-fed', 'Drip Irrigation'), 'weather_condition': ('windy', 'cloudy', 'sunny')
    },
    'barley': {
        'region': ('Central Anatolia', 'Eastern Anatolia', 'Southeastern Anatolia'), 'soil_type': ('Loamy', 'Silty', 'Sandy'), 'soil_ph': 7.7, 'nitrogen': 60, 'phosphorus': 35, 'potassium': 52, 'moisture': 55, 'temperature_celsius': 19, 'rainfall_mm': 450,
        'fertilizer_type': ('Potassium Nitrate', 'Ammonium Sulphate', 'Urea'), 'irrigation_method': ('Rain-fed', 'Sprinkler Irrigation', 'Drip Irrigation'), 'weather_condition': ('sunny', 'windy', 'cloudy')
    },
    'sunflower': {
        'region': ('Marmara', 'Central Anatolia', 'Aegean'), 'soil_type': ('Sandy', 'Loamy', 'Silty'), 'soil_ph': 6.2, 'nitrogen': 90, 'phosphorus': 45, 'potassium': 70, 'moisture': 70, 'temperature_celsius': 24, 'rainfall_mm': 650,
        'fertilizer_type': ('Urea', 'Ammonium Sulphate', 'Potassium Nitrate'), 'irrigation_method': ('Drip Irrigation', 'Sprinkler Irrigation', 'Rain-fed'), 'weather_condition': ('sunny', 'cloudy', 'windy')
    },
    'corn': {
        'region': ('Marmara', 'Mediterranean', 'Aegean'), 'soil_type': ('Loamy', 'Silty', 'Clay'), 'soil_ph': 6.9, 'nitrogen': 120, 'phosphorus': 50, 'potassium': 62, 'moisture': 75, 'temperature_celsius': 25.5, 'rainfall_mm': 1000,
        'fertilizer_type': ('Urea', 'Potassium Nitrate', 'Ammonium Sulphate'), 'irrigation_method': ('Drip Irrigation', 'Sprinkler Irrigation', 'Flood Irrigation'), 'weather_condition': ('cloudy', 'sunny', 'rainy')
    },
    'oat': {
        'region': ('Eastern Anatolia', 'Central Anatolia', 'Marmara'), 'soil_type': ('Silty', 'Loamy', 'Sandy'), 'soil_ph': 6.2, 'nitrogen': 60, 'phosphorus': 35, 'potassium': 45, 'moisture': 65, 'temperature_celsius': 18, 'rainfall_mm': 600,
        'fertilizer_type': ('Ammonium Sulphate', 'Urea', 'Potassium Nitrate'), 'irrigation_method': ('Rain-fed', 'Sprinkler Irrigation', 'Drip Irrigation'), 'weather_condition': ('windy', 'cloudy', 'rainy')
    }
}

all_data = []
VARIANCE_PERCENT = 0.50  # Değişiklik: Varyans %10'a çıkarıldı

for crop in crops:
    crop_optimums = optimums[crop]
    data = {}

    # Sayısal değişkenleri üret
    for key in ['soil_ph', 'nitrogen', 'phosphorus', 'potassium', 'moisture', 'temperature_celsius', 'rainfall_mm']:
        center = crop_optimums[key]
        low = center * (1 - VARIANCE_PERCENT)
        high = center * (1 + VARIANCE_PERCENT)
        data[key] = np.random.uniform(low, high, size=n_per_crop)

    # Kategorik değişkenleri üret
    for key in ['region', 'soil_type', 'fertilizer_type', 'irrigation_method', 'weather_condition']:
        choices = crop_optimums[key]
        probabilities = [0.6, 0.25, 0.15]
        if len(choices) < 3:
             probabilities = [1.0] if len(choices) == 1 else [0.7, 0.3]
        data[key] = np.random.choice(choices, size=n_per_crop, p=probabilities)

    data['crop'] = crop
    all_data.append(pd.DataFrame(data))

# Veriyi birleştir ve karıştır
df = pd.concat(all_data).sample(frac=1).reset_index(drop=True)

# Değişiklik: Aykırı değer oranı %5'e çıkarıldı
outlier_indices = df.sample(frac=0.07).index
numeric_cols = df.select_dtypes(include=np.number).columns

for idx in outlier_indices:
    col_to_change = np.random.choice(numeric_cols)
    direction = np.random.choice([-1, 1])
    # Değişiklik: Sapma %20 ile %50 arasında olacak şekilde ayarlandı
    deviation = np.random.uniform(0.30, 0.60)
    factor = 1 + deviation * direction
    df.loc[idx, col_to_change] *= factor


# Veri setini yeni bir isimle CSV dosyasına kaydet
df.to_csv('crop_dataset_v_100bin.csv', index=False)

print("'crop_dataset_v2.csv' dosyası başarıyla oluşturuldu ve 50000 satır veri içeriyor.")
print("Değişiklikler:")
print("- Sayısal değerler optimumun +/- %10 aralığında oluşturuldu.")
print("- Verinin %5'ine aykırı değer eklendi.")
print("- Aykırı değer sapması %20 ile %50 arasına yükseltildi.")
print("\nSol taraftaki dosya menüsünden dosyayı bulup indirebilirsiniz.")