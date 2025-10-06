import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
import lightgbm as lgb
import optuna
import warnings

# Uyarıları gizleyelim (özellikle pandas slice uyarıları vb. için)
warnings.filterwarnings('ignore')

# =============================================================================
# 1. ADIM: VERİ YÜKLEME VE İSTENEN DEĞİŞKENLERİ GÜNCELLEME
# =============================================================================
df = pd.read_csv(r"C:\Users\Mehdiye\Desktop\TURKCELL PROJE\TerraMind\GYK-Final-Project\crop_dataset_v_100bin.csv")

# =============================================================================
# YENİ EKLENEN KISIM: Belirtilen değişkenleri 2 ile çarpma
# =============================================================================
#columns_to_multiply = ['soil_ph', 'moisture', 'temperature_celsius', 'rainfall_mm']
#for col in columns_to_multiply:
#    df[col] = df[col] * 2

#print("soil_ph, moisture, temperature_celsius, rainfall_mm değişkenleri 2 ile çarpıldı.\n")
# =============================================================================


# Veri setini X (özellikler) ve y (hedef) olarak ayıralım
X = df.drop('crop', axis=1)
y = df['crop']

# Hedef değişkeni encode edelim (String -> Sayı)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
classes = label_encoder.classes_
print(f"Tespit edilen sınıflar: {classes}\n")

# Eğitim ve Test seti ayrımı (%80 Eğitim, %20 Test)
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

# =============================================================================
# 2. ADIM: ÖZEL FEATURE ENGINEERING TRANSFORMER'I
# =============================================================================
class CustomFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Kullanıcının belirttiği 10 feature engineering adımını uygulayan sınıf.
    Pipeline içine entegre edilebilir.
    """
    def __init__(self):
        self.stats = {}

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df = X.copy()
        
        # Güvenlik kontrolü: Sayısal sütunların tipini garantiye alalım
        num_cols = ['nitrogen', 'phosphorus', 'potassium', 'soil_ph', 
                    'temperature_celsius', 'moisture', 'rainfall_mm']
        for col in num_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # --- Kullanıcının İstediği Özellikler ---
        
        # 1. N/P oranı
        df["n_to_p_ratio"] = df["nitrogen"] / (df["phosphorus"] + 1e-6)

        # 2. N/K oranı
        df["n_to_k_ratio"] = df["nitrogen"] / (df["potassium"] + 1e-6)

        # 3. Toprak pH kategorisi
        def categorize_ph(ph):
            if ph < 6.5: return "acidic"
            elif ph <= 7.5: return "neutral"
            else: return "alkaline"
        df["soil_ph_category"] = df["soil_ph"].apply(categorize_ph)

        # 4. Yağış + sulama etkisi (mm eşdeğeri)
        irrigation_bonus = {"drip": 40, "sprinkler": 25, "flood": 10, "none": 0, "unknown": 0}
        df["rainfall_plus_irrigation"] = df["rainfall_mm"] + df["irrigation_method"].map(irrigation_bonus).fillna(0)

        # 5. Sulama yoğunluğu (ordinal kodlama)
        irrigation_intensity_map = {"none": 0, "flood": 1, "sprinkler": 2, "drip": 3}
        df["irrigation_intensity"] = df["irrigation_method"].map(irrigation_intensity_map).fillna(0)

        # 6. Gübre tipi - nitrojenli mi?
        df["fertilizer_is_nitrogenous"] = (df["fertilizer_type"].str.lower() == "nitrogenous").astype(int)

        # 7. Sıcaklık-nem etkileşimi
        df["temp_moisture_interaction"] = df["temperature_celsius"] * (df["moisture"] / 100)

        # 8. Basit evapotranspirasyon proxy'si
        df["evapotranspiration_proxy"] = df["temperature_celsius"] * (1 - df["moisture"] / 100) + np.maximum(0, df["temperature_celsius"] - 20)

        # 9. Toprak dokusu skoru (ordinal)
        soil_texture_score = {"sandy": 1, "loamy": 2, "clayey": 3, "silty": 1.5}
        df["soil_texture_score"] = df["soil_type"].map(soil_texture_score).fillna(0)

        # 10. Genel yetişme koşulları indeksi (growing condition index)
        def min_max_norm(series):
            return (series - series.min()) / (series.max() - series.min() + 1e-9)

        rain_irrig_norm = min_max_norm(df["rainfall_plus_irrigation"])
        moisture_norm = min_max_norm(df["moisture"])
        temp_optimal = -np.abs(df["temperature_celsius"] - 25)
        temp_norm = min_max_norm(temp_optimal)
        ph_optimal = 1 - np.abs(df["soil_ph"] - 6.8) / (df["soil_ph"].max() - df["soil_ph"].min() + 1e-9)
        ph_norm = min_max_norm(ph_optimal)

        df["growing_condition_index"] = (
            0.35 * rain_irrig_norm +
            0.25 * moisture_norm +
            0.15 * temp_norm +
            0.25 * ph_norm
        )
        
        return df

# =============================================================================
# 3. ADIM: PREPROCESSING PIPELINE (FE + ONE-HOT ENCODING)
# =============================================================================

categorical_cols = ['region', 'soil_type', 'fertilizer_type', 'irrigation_method', 
                    'weather_condition', 'soil_ph_category']
categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

preprocessor = Pipeline(steps=[
    ('feature_engineering', CustomFeatureEngineer()),
    ('encoding', ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_cols)
        ],
        remainder='passthrough'
    ))
])

print("Ön işleme pipeline'ı veriye uygulanıyor (Optuna öncesi)...")
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)
print(f"İşlenmiş Eğitim Verisi Boyutu: {X_train_processed.shape}")

# =============================================================================
# 4. ADIM: HİPERPARAMETRE OPTİMİZASYONU (OPTUNA & EARLY STOPPING)
# =============================================================================
print("\nHiperparametre optimizasyonu başlıyor (Optuna)...")

X_train_opt, X_val_opt, y_train_opt, y_val_opt = train_test_split(
    X_train_processed, y_train, test_size=0.2, random_state=42, stratify=y_train
)

def objective(trial):
    param = {
        'objective': 'multiclass',
        'metric': 'multi_logloss',
        'num_class': len(classes),
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'random_state': 42,
        'n_estimators': 1000,
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'num_leaves': trial.suggest_int('num_leaves', 20, 150),
        'max_depth': trial.suggest_int('max_depth', -1, 15),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 10.0),
        'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 10.0),
    }

    model = lgb.LGBMClassifier(**param)
    callbacks = [lgb.early_stopping(stopping_rounds=30, verbose=False)]
    
    model.fit(
        X_train_opt, y_train_opt,
        eval_set=[(X_val_opt, y_val_opt)],
        callbacks=callbacks
    )
    
    preds = model.predict(X_val_opt)
    accuracy = accuracy_score(y_val_opt, preds)
    return accuracy

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=20, show_progress_bar=True)

print("\nEn iyi deneme:")
best_trial = study.best_trial
print(f"  Değer (Accuracy): {best_trial.value:.4f}")
print("  Parametreler: ")
for key, value in best_trial.params.items():
    print(f"    {key}: {value}")

# =============================================================================
# 5. ADIM: FİNAL MODEL EĞİTİMİ VE DEĞERLENDİRME
# =============================================================================
print("\nFinal model en iyi parametrelerle eğitiliyor...")

best_params = best_trial.params
best_params['objective'] = 'multiclass'
best_params['num_class'] = len(classes)
best_params['random_state'] = 42
best_params['n_estimators'] = 2000

final_model = lgb.LGBMClassifier(**best_params)
callbacks_final = [lgb.early_stopping(stopping_rounds=30), lgb.log_evaluation(period=0)]

final_model.fit(
    X_train_processed, y_train,
    eval_set=[(X_test_processed, y_test)],
    callbacks=callbacks_final
)

# Test seti üzerinde tahminler
print("\nModel Değerlendirme Sonuçları:")
y_pred_encoded = final_model.predict(X_test_processed)

acc = accuracy_score(y_test, y_pred_encoded)
f1 = f1_score(y_test, y_pred_encoded, average='weighted')
prec = precision_score(y_test, y_pred_encoded, average='weighted')
rec = recall_score(y_test, y_pred_encoded, average='weighted')

print(f"Accuracy : {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall   : {rec:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nDetaylı Sınıflandırma Raporu:")
print(classification_report(label_encoder.inverse_transform(y_test), 
                            label_encoder.inverse_transform(y_pred_encoded)))

# =============================================================================
# 6. ADIM: SON ÜRÜN PİPELİNE VE TAHMİN FONKSİYONU
# =============================================================================

def predict_new_crop(input_data_dict):
    """
    Sözlük formatında tek bir veri noktası alır, işler ve tahmin edilen ürünü döndürür.
    """
    new_df = pd.DataFrame([input_data_dict])
    processed_data = preprocessor.transform(new_df)
    prediction_encoded = final_model.predict(processed_data)
    prediction_str = label_encoder.inverse_transform(prediction_encoded)
    return prediction_str[0]

# --- Fonksiyonu Test Edelim ---
print("\n--- Yeni Veri İle Tahmin Testi ---")
sample_input = {
    'region': 'Aegean',
    'soil_type': 'loamy',
    'soil_ph': 6.8,
    'nitrogen': 120,
    'phosphorus': 40,
    'potassium': 80,
    'moisture': 45,
    'temperature_celsius': 28,
    'rainfall_mm': 500,
    'fertilizer_type': 'Nitrogenous',
    'irrigation_method': 'drip',
    'weather_condition': 'Sunny'
}

# Önemli Not: Test fonksiyonuna girdiğimiz veriler, 2 ile çarpma işleminden
# ÖNCEKİ orijinal ölçekte olmalıdır. Kod, bu ham girdiyi alıp pipeline içinde
# kendisi işleyecektir. Ancak df'i en başta 2 ile çarptığımız için model artık
# bu çarpılmış değerlere göre eğitilmiştir. Bu yüzden test girdisini de 
# fonksiyona göndermeden önce çarpmamız gerekir.
sample_input['soil_ph'] *= 2
sample_input['moisture'] *= 2
sample_input['temperature_celsius'] *= 2
sample_input['rainfall_mm'] *= 2

predicted_crop = predict_new_crop(sample_input)
print(f"Girilen veriler için tahmin edilen ürün: {predicted_crop}")