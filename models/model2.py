import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from scipy.optimize import differential_evolution
import sys
import os
import pickle

# Config dosyasını import etmek için path ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database_config import load_crop_data

class CropRecommendationModel:
    """Crop öneri modeli - Fonksiyonel sınıf yapısı"""
    
    def __init__(self):
        self.df = None
        self.model = None
        self.encoders = {}
        self.feature_order = None
        self.numeric_features = ['soil_ph','nitrogen','phosphorus','potassium','moisture',
                                'temperature_celsius','rainfall_mm']
        self.categorical_features = ['region','soil_type','fertilizer_type','irrigation_method','weather_condition']
        self.target = 'crop'
    
    def load_data(self):
        """Veriyi yükler"""
        print("Veritabanından veri çekiliyor...")
        self.df = load_crop_data(table_name='crop_dataset_v_100bin')
        
        if self.df is None:
            raise ValueError("Veri yüklenemedi!")
        
        print(f"Veri yüklendi: {len(self.df)} satır")
        return self.df
    
    def suppress_outliers_iqr(self, columns, lower_quantile=0.005, upper_quantile=0.995):
        """Aykırı değerleri baskılar"""
        df_clean = self.df.copy()
        for col in columns:
            q_low = self.df[col].quantile(lower_quantile)
            q_high = self.df[col].quantile(upper_quantile)
            df_clean[col] = np.clip(self.df[col], q_low, q_high)
        self.df = df_clean
        return self.df
    
    def encode_categorical_features(self):
        """Kategorik değişkenleri encode eder"""
        for col in self.categorical_features + [self.target]:
            le = LabelEncoder()
            self.df[col] = le.fit_transform(self.df[col])
            self.encoders[col] = le
        return self.encoders
    
    def train_model(self):
        """Modeli eğitir"""
        X = self.df[self.numeric_features + self.categorical_features]
        y = self.df[self.target]
        
        self.model = XGBClassifier(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        self.model.fit(X, y)
        self.feature_order = X.columns.tolist()
        print("Model eğitimi tamamlandı.")
        return self.model
    
    def suggest_optimal_conditions(self, target_crop, target_region):
        """Optimum koşulları önerir"""
        if self.model is None:
            raise ValueError("Model henüz eğitilmemiş!")
        
        crop_val = self.encoders['crop'].transform([target_crop])[0]
        region_val = self.encoders['region'].transform([target_region])[0]

        bounds = [
            (self.df[col].min(), self.df[col].max()) for col in self.numeric_features
        ] + [
            (self.df[col].min(), self.df[col].max()) for col in ['soil_type','fertilizer_type','irrigation_method','weather_condition']
        ]

        def objective(x):
            values = dict(zip(self.numeric_features + ['soil_type','fertilizer_type','irrigation_method','weather_condition'], x))
            values['region'] = region_val
            X_test = pd.DataFrame([[values[col] for col in self.feature_order]], columns=self.feature_order)
            prob = self.model.predict_proba(X_test)[0, crop_val]
            return -prob

        result = differential_evolution(objective, bounds, maxiter=60, seed=42)
        best_x = result.x

        best_values = dict(zip(self.numeric_features + ['soil_type','fertilizer_type','irrigation_method','weather_condition'], best_x))
        best_df = pd.DataFrame([best_values])

        for col in ['soil_type','fertilizer_type','irrigation_method','weather_condition']:
            best_df[col] = self.encoders[col].inverse_transform(best_df[col].astype(int))

        values_for_prob = {**best_values, 'region': region_val}
        X_best = pd.DataFrame([[values_for_prob[c] for c in self.feature_order]], columns=self.feature_order)
        final_prob = self.model.predict_proba(X_best)[0, crop_val]

        return best_df.round(2), round(final_prob * 100, 2)
    
    def save_model(self, file_path="crop_model.pkl"):
        """Modeli ve encoderları .pkl olarak kaydeder"""
        if self.model is None:
            raise ValueError("Model henüz eğitilmemiş!")
        
        model_data = {
            "model": self.model,
            "encoders": self.encoders,
            "feature_order": self.feature_order,
            "numeric_features": self.numeric_features,
            "categorical_features": self.categorical_features,
            "target": self.target
        }
        
        with open(file_path, "wb") as f:
            pickle.dump(model_data, f)
        
        print(f"Model '{file_path}' olarak kaydedildi.")
    
    def run_pipeline(self, target_crop="wheat", target_region="Aegean"):
        """Tam pipeline'ı çalıştırır"""
        # Veri yükle
        self.load_data()
        
        # Aykırı değerleri baskıla
        self.suppress_outliers_iqr(self.numeric_features)
        
        # Encoding yap
        self.encode_categorical_features()
        
        # Modeli eğit
        self.train_model()
        
        # Optimum koşulları öner
        optimum_df, probability = self.suggest_optimal_conditions(target_crop, target_region)
        
        print(f"\n🌾 '{target_crop}' ürünü için '{target_region}' bölgesinde önerilen optimum koşullar:\n")
        print(optimum_df)
        print(f"\n🔮 Modelin '{target_crop}' ürünü olasılığı: %{probability}")

        # Modeli kaydet
        self.save_model("crop_model.pkl")
        
        return optimum_df, probability

# Ana çalıştırma
if __name__ == "__main__":
    model = CropRecommendationModel()
    model.run_pipeline()
