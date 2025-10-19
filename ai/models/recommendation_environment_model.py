# environmental_recommendation_runner.py
import pandas as pd
import numpy as np
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score, classification_report
)
import lightgbm as lgb
import warnings
import sys
import os
 
# Uyarıları gizle
warnings.filterwarnings('ignore')
 
# ===============================================================
# 1. Çevre Önerileri Modeli Sınıfı
# ===============================================================
class EnvironmentalRecommendationModel:
    """Ürün ve konum bilgisine göre çevre önerileri yapan model"""
 
    def __init__(self, model_path="environmental_recommendation_model.pkl"):
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.label_encoders = {}   # Her hedef için ayrı encoder
        self.classes = {}          # Her hedef için sınıflar
        self.preprocessor = None
        self.models = {}           # Her hedef için ayrı model
        self.model_path = model_path
 
        # Weather condition mapping (TR->EN)
        self.weather_mapping = {
            'Güneşli': 'sunny',
            'Kısmi Gölge': 'cloudy',
            'Gölgeli': 'cloudy',
            'Tam Gölge': 'cloudy',
            'Yağmurlu': 'rainy',
            'Bulutlu': 'cloudy',
            'Rüzgarlı': 'windy'
        }
 
        # Birden fazla hedefi aynı girdiden tahmin ediyoruz:
        self.target_columns = ['fertilizer_type', 'irrigation_method', 'weather_condition', 'soil_type']
 
        # Metrikleri saklamak için
        self.metrics_ = {}
 
    # -----------------------------------------------------------
    def load_data(self, csv_path="./crop_dataset_v_100bin.csv"):
        """CSV dosyasından veri yükle (aynı klasörde beklenir)"""
        print(f"[INFO] Veri yükleniyor: {csv_path}")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(
                f"CSV bulunamadı: {csv_path}\n"
                f"Lütfen dosyayı bu script ile aynı klasöre koyun ve adı 'crop_dataset_v_100bin.csv' olsun "
                f"ya da load_data(csv_path=...) ile doğru yolu verin."
            )
        self.df = pd.read_csv(csv_path)
        print(f"[INFO] Veri yüklendi: {len(self.df)} satır, {len(self.df.columns)} sütun")
        return self.df
 
    # -----------------------------------------------------------
    def prepare_data(self):
        """Veriyi hazırla - sadece gerekli kolonları kullan"""
        # Input features
        feature_columns = [
            'crop', 'region', 'soil_ph', 'nitrogen', 'phosphorus',
            'potassium', 'temperature_celsius', 'moisture', 'rainfall_mm'
        ]
        missing_cols = [c for c in feature_columns + self.target_columns if c not in self.df.columns]
        if missing_cols:
            raise KeyError(f"Verinizde aşağıdaki gerekli kolonlar eksik: {missing_cols}")
 
        self.X = self.df[feature_columns].copy()
        self.y = self.df[self.target_columns].copy()
 
        # Sayısal kolonları numeric'e çevir
        numeric_cols = ['soil_ph', 'nitrogen', 'phosphorus', 'potassium',
                        'temperature_celsius', 'moisture', 'rainfall_mm']
        for col in numeric_cols:
            self.X[col] = pd.to_numeric(self.X[col], errors='coerce')
 
        # Eksik değerleri median ile doldur
        self.X[numeric_cols] = self.X[numeric_cols].fillna(self.X[numeric_cols].median(numeric_only=True))
 
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
 
        print(f"[INFO] Eğitim verisi: {self.X_train.shape} | Test verisi: {self.X_test.shape}")
        return self.X_train, self.X_test, self.y_train, self.y_test
 
    # -----------------------------------------------------------
    def setup_preprocessor(self):
        """Ön işleme pipeline'ı kur (sklearn sürümleriyle uyumlu OHE)"""
        categorical_cols = ['crop', 'region']
        numeric_cols = ['soil_ph', 'nitrogen', 'phosphorus', 'potassium',
                        'temperature_celsius', 'moisture', 'rainfall_mm']
 
        # sklearn>=1.2 için sparse_output, daha eskiler için sparse
        try:
            categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        except TypeError:
            categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse=False)
 
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_cols),
                ('num', 'passthrough', numeric_cols)
            ],
            remainder='drop'
        )
        return self.preprocessor
 
    # -----------------------------------------------------------
    def preprocess_data(self):
        """Veriyi ön işle"""
        print("[INFO] Veri ön işleniyor (fit/transform)...")
        X_train_processed = self.preprocessor.fit_transform(self.X_train)
        X_test_processed = self.preprocessor.transform(self.X_test)
        print(f"[INFO] İşlenmiş eğitim verisi: {X_train_processed.shape} | İşlenmiş test verisi: {X_test_processed.shape}")
        return X_train_processed, X_test_processed
 
    # -----------------------------------------------------------
    def train_models(self, X_train_processed, X_test_processed):
        """Her hedef için ayrı model eğit ve metrikleri yazdır"""
        print("\n[INFO] Modeller eğitiliyor...")
        self.metrics_.clear()
 
        for target in self.target_columns:
            print(f"\n=== {target} ===")
 
            # Label encode
            le = LabelEncoder()
            y_train_encoded = le.fit_transform(self.y_train[target])
            y_test_encoded = le.transform(self.y_test[target])
 
            self.label_encoders[target] = le
            self.classes[target] = le.classes_
 
            # --- MODEL (değiştirmeden koruyoruz: LightGBM) ---
            model = lgb.LGBMClassifier(
                objective='multiclass',
                num_class=len(le.classes_),
                random_state=42,
                n_estimators=1000,
                learning_rate=0.1,
                max_depth=6,
                num_leaves=31,
                verbose=-1
            )
 
            model.fit(X_train_processed, y_train_encoded)
 
            # Tahmin ve değerlendirme
            y_pred = model.predict(X_test_processed)
 
            acc = accuracy_score(y_test_encoded, y_pred)
            f1_w = f1_score(y_test_encoded, y_pred, average='weighted')
            prec_w = precision_score(y_test_encoded, y_pred, average='weighted', zero_division=0)
            rec_w = recall_score(y_test_encoded, y_pred, average='weighted')
 
            print(f"Accuracy           : {acc:.4f}")
            print(f"F1 (weighted)      : {f1_w:.4f}")
            print(f"Precision (weighted): {prec_w:.4f}")
            print(f"Recall (weighted)  : {rec_w:.4f}")
            print(f"Sınıflar           : {list(le.classes_)}")
 
            # İnsan okunur rapor (orijinal etiket isimleri)
            y_true_labels = le.inverse_transform(y_test_encoded)
            y_pred_labels = le.inverse_transform(y_pred)
            print("\n--- Classification Report ---")
            print(classification_report(y_true_labels, y_pred_labels, zero_division=0))
 
            # Kaydet
            self.models[target] = model
            self.metrics_[target] = {
                "accuracy": acc,
                "f1_weighted": f1_w,
                "precision_weighted": prec_w,
                "recall_weighted": rec_w,
                "n_classes": len(le.classes_)
            }
 
        # Kısa özet tablo
        print("\n================ ÖZET METRİK TABLOSU ================")
        df_sum = pd.DataFrame(self.metrics_).T[
            ["n_classes", "accuracy", "f1_weighted", "precision_weighted", "recall_weighted"]
        ].sort_values("f1_weighted", ascending=False)
        print(df_sum.to_string(float_format=lambda x: f"{x:.4f}"))
 
    # -----------------------------------------------------------
    def save_model(self):
        """Modeli kaydet"""
        print(f"\n[INFO] Model kaydediliyor -> {self.model_path}")
        model_bundle = {
            'models': self.models,
            'preprocessor': self.preprocessor,
            'label_encoders': self.label_encoders,
            'classes': self.classes,
            'weather_mapping': self.weather_mapping,
            'target_columns': self.target_columns
        }
        joblib.dump(model_bundle, self.model_path)
        print("[INFO] Model başarıyla kaydedildi.")
 
    # -----------------------------------------------------------
    def load_saved_model(self):
        """Kaydedilmiş modeli yükle"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"{self.model_path} bulunamadı!")
        print(f"[INFO] Model yükleniyor -> {self.model_path}")
        bundle = joblib.load(self.model_path)
        self.models = bundle['models']
        self.preprocessor = bundle['preprocessor']
        self.label_encoders = bundle['label_encoders']
        self.classes = bundle['classes']
        self.weather_mapping = bundle['weather_mapping']
        self.target_columns = bundle['target_columns']
        print("[INFO] Model başarıyla yüklendi.")
        return self
 
    # -----------------------------------------------------------
    def predict_recommendations(self, crop, region, soil_ph=None, nitrogen=None,
                                phosphorus=None, potassium=None, temperature_celsius=None,
                                moisture=None, rainfall_mm=None):
        """Çevre önerileri tahmin et"""
        if not self.models:
            raise ValueError("Model eğitilmedi veya yüklenmedi!")
 
        # Input verisi
        input_data = {
            'crop': crop,
            'region': region,
            'soil_ph': soil_ph if soil_ph is not None else 6.5,
            'nitrogen': nitrogen if nitrogen is not None else 80,
            'phosphorus': phosphorus if phosphorus is not None else 40,
            'potassium': potassium if potassium is not None else 60,
            'temperature_celsius': temperature_celsius if temperature_celsius is not None else 20,
            'moisture': moisture if moisture is not None else 60,
            'rainfall_mm': rainfall_mm if rainfall_mm is not None else 500
        }
 
        input_df = pd.DataFrame([input_data])
        processed = self.preprocessor.transform(input_df)
 
        recommendations = {}
        for target in self.target_columns:
            pred_encoded = self.models[target].predict(processed)
            pred_label = self.label_encoders[target].inverse_transform(pred_encoded)[0]
            recommendations[target] = pred_label
 
        # İngilizce hava durumunu TR karşılığına çevir
        weather_tr = None
        for tr, en in self.weather_mapping.items():
            if en == recommendations['weather_condition']:
                weather_tr = tr
                break
        if weather_tr:
            recommendations['weather_condition_tr'] = weather_tr
 
        return recommendations
 
    # -----------------------------------------------------------
    def run_pipeline(self, csv_path="./crop_dataset_v_100bin.csv"):
        """Tam pipeline'ı çalıştır"""
        self.load_data(csv_path)
        self.prepare_data()
        self.setup_preprocessor()
        X_train_processed, X_test_processed = self.preprocess_data()
        self.train_models(X_train_processed, X_test_processed)
        self.save_model()
 
        # Test amaçlı tek örnek tahmin
        print("\n--- Örnek Tahmin ---")
        sample_recommendations = self.predict_recommendations(
            crop='Salatalık',
            region='Marmara',
            soil_ph=6.5,
            nitrogen=100,
            phosphorus=50,
            potassium=80,
            temperature_celsius=22,
            moisture=70,
            rainfall_mm=600
        )
        print("Örnek öneriler:")
        for k, v in sample_recommendations.items():
            print(f"  {k}: {v}")
 
 
# ===============================================================
# 2. Ana Çalıştırma
# ===============================================================
if __name__ == "__main__":
    print("############################################################")
    print("# EnvironmentalRecommendationModel — Tek Klasör Çalıştırma #")
    print("############################################################\n")
    print("[YOL] Bu dosyayla aynı klasörde 'crop_dataset_v_100bin.csv' olmalı.")
    print("[NOT] sklearn sürümü eskiyse OHE otomatik uyarlanır (sparse_output->sparse).")
 
    model = EnvironmentalRecommendationModel(model_path="environmental_recommendation_model.pkl")
    # Gerekirse alternatif yol ver: model.run_pipeline(csv_path="veri.csv")
    model.run_pipeline(csv_path="./crop_dataset_v_100bin.csv")
 
    # Alternatif: Kaydedilmiş modeli yükleyip tahmin yapmak
    # model = EnvironmentalRecommendationModel().load_saved_model()
    # recs = model.predict_recommendations('Salatalık', 'Marmara')
    # print(recs)