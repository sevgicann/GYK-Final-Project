import pandas as pd
import numpy as np
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
import lightgbm as lgb
import optuna
import warnings
import sys
import os

# Uyarıları gizle
warnings.filterwarnings('ignore')

# Modül yolu ekleme (örnek olarak)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database_config import load_crop_data


# ===============================================================
# 1. Feature Engineering Sınıfı
# ===============================================================
class CustomFeatureEngineer(BaseEstimator, TransformerMixin):
    """Kullanıcı tanımlı 10 özellik üretimi."""

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df = X.copy()

        num_cols = ['nitrogen', 'phosphorus', 'potassium', 'soil_ph',
                    'temperature_celsius', 'moisture', 'rainfall_mm']
        for col in num_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 1. N/P oranı
        df["n_to_p_ratio"] = df["nitrogen"] / (df["phosphorus"] + 1e-6)

        # 2. N/K oranı
        df["n_to_k_ratio"] = df["nitrogen"] / (df["potassium"] + 1e-6)

        # 3. pH kategorisi
        def categorize_ph(ph):
            if ph < 6.5: return "acidic"
            elif ph <= 7.5: return "neutral"
            else: return "alkaline"
        df["soil_ph_category"] = df["soil_ph"].apply(categorize_ph)

        # 4. Yağış + sulama etkisi
        irrigation_bonus = {"drip": 40, "sprinkler": 25, "flood": 10, "none": 0, "unknown": 0}
        df["rainfall_plus_irrigation"] = df["rainfall_mm"] + df["irrigation_method"].map(irrigation_bonus).fillna(0)

        # 5. Sulama yoğunluğu (ordinal)
        irrigation_intensity_map = {"none": 0, "flood": 1, "sprinkler": 2, "drip": 3}
        df["irrigation_intensity"] = df["irrigation_method"].map(irrigation_intensity_map).fillna(0)

        # 6. Gübre tipi nitrojenli mi?
        df["fertilizer_is_nitrogenous"] = (df["fertilizer_type"].str.lower() == "nitrogenous").astype(int)

        # 7. Sıcaklık-nem etkileşimi
        df["temp_moisture_interaction"] = df["temperature_celsius"] * (df["moisture"] / 100)

        # 8. Evapotranspirasyon proxy
        df["evapotranspiration_proxy"] = df["temperature_celsius"] * (1 - df["moisture"] / 100) + np.maximum(0, df["temperature_celsius"] - 20)

        # 9. Toprak dokusu skoru
        soil_texture_score = {"sandy": 1, "loamy": 2, "clayey": 3, "silty": 1.5}
        df["soil_texture_score"] = df["soil_type"].map(soil_texture_score).fillna(0)

        # 10. Genel yetişme indeksi
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


# ===============================================================
# 2. Ana Model Sınıfı
# ===============================================================
class SentetikCropModel:
    """Sentetik Crop Modeli"""

    def __init__(self, model_path="sentetik_crop_model.pkl"):
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.label_encoder = None
        self.classes = None
        self.preprocessor = None
        self.final_model = None
        self.best_params = None
        self.model_path = model_path

    # -----------------------------------------------------------
    def load_data(self):
        print("Veritabanından veri çekiliyor...")
        self.df = load_crop_data(table_name='crop_dataset_v_100bin')
        if self.df is None:
            raise ValueError("Veri yüklenemedi!")
        print(f"Veri yüklendi: {len(self.df)} satır")
        return self.df

    # -----------------------------------------------------------
    def prepare_data(self):
        self.X = self.df.drop('crop', axis=1)
        self.y = self.df['crop']
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(self.y)
        self.classes = self.label_encoder.classes_

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )

        print(f"Tespit edilen sınıflar: {self.classes}")
        return self.X_train, self.X_test, self.y_train, self.y_test

    # -----------------------------------------------------------
    def setup_preprocessor(self):
        categorical_cols = ['region', 'soil_type', 'fertilizer_type', 'irrigation_method',
                            'weather_condition', 'soil_ph_category']

        categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

        self.preprocessor = Pipeline(steps=[
            ('feature_engineering', CustomFeatureEngineer()),
            ('encoding', ColumnTransformer(
                transformers=[('cat', categorical_transformer, categorical_cols)],
                remainder='passthrough'
            ))
        ])
        return self.preprocessor

    # -----------------------------------------------------------
    def preprocess_data(self):
        print("Ön işleme pipeline'ı uygulanıyor...")
        X_train_processed = self.preprocessor.fit_transform(self.X_train)
        X_test_processed = self.preprocessor.transform(self.X_test)
        print(f"İşlenmiş Eğitim Verisi: {X_train_processed.shape}")
        return X_train_processed, X_test_processed

    # -----------------------------------------------------------
    def optimize_hyperparameters(self, X_train_processed, y_train, n_trials=20):
        print("\nOptuna hiperparametre araması başlatıldı...")

        X_train_opt, X_val_opt, y_train_opt, y_val_opt = train_test_split(
            X_train_processed, y_train, test_size=0.2, random_state=42, stratify=y_train
        )

        def objective(trial):
            param = {
                'objective': 'multiclass',
                'metric': 'multi_logloss',
                'num_class': len(self.classes),
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

            model.fit(X_train_opt, y_train_opt, eval_set=[(X_val_opt, y_val_opt)], callbacks=callbacks)

            preds = model.predict(X_val_opt)
            return accuracy_score(y_val_opt, preds)

        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

        self.best_params = study.best_trial.params
        print("\nEn iyi parametreler:")
        for k, v in self.best_params.items():
            print(f"{k}: {v}")
        return self.best_params

    # -----------------------------------------------------------
    def train_final_model(self, X_train_processed, X_test_processed, y_train, y_test):
        print("\nFinal model eğitiliyor...")

        params = self.best_params.copy()
        params.update({
            'objective': 'multiclass',
            'num_class': len(self.classes),
            'random_state': 42,
            'n_estimators': 2000
        })

        self.final_model = lgb.LGBMClassifier(**params)
        callbacks = [lgb.early_stopping(stopping_rounds=30), lgb.log_evaluation(period=0)]

        self.final_model.fit(X_train_processed, y_train, eval_set=[(X_test_processed, y_test)], callbacks=callbacks)

        preds = self.final_model.predict(X_test_processed)
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, average='weighted')
        rec = recall_score(y_test, preds, average='weighted')
        f1 = f1_score(y_test, preds, average='weighted')

        print(f"\nAccuracy : {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall   : {rec:.4f}")
        print(f"F1-score : {f1:.4f}")

        print("\n--- Detaylı Rapor ---")
        print(classification_report(self.label_encoder.inverse_transform(y_test),
                                    self.label_encoder.inverse_transform(preds)))

        # ✅ Modeli kaydet
        self.save_model()

        return {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1_score': f1}

    # -----------------------------------------------------------
    def save_model(self):
        """Model, ön işleme pipeline'ı ve label encoder'ı kaydeder."""
        print(f"\nModel kaydediliyor -> {self.model_path}")
        model_bundle = {
            'model': self.final_model,
            'preprocessor': self.preprocessor,
            'label_encoder': self.label_encoder,
            'classes': self.classes
        }
        joblib.dump(model_bundle, self.model_path)
        print("✅ Model başarıyla kaydedildi.")

    # -----------------------------------------------------------
    def load_saved_model(self):
        """Kaydedilmiş modeli yükler."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"{self.model_path} bulunamadı!")
        print(f"📦 Model yükleniyor -> {self.model_path}")
        bundle = joblib.load(self.model_path)
        self.final_model = bundle['model']
        self.preprocessor = bundle['preprocessor']
        self.label_encoder = bundle['label_encoder']
        self.classes = bundle['classes']
        print("✅ Model başarıyla yüklendi.")
        return self

    # -----------------------------------------------------------
    def predict_new_crop(self, input_data_dict):
        if self.final_model is None:
            raise ValueError("Model eğitilmedi veya yüklenmedi!")
        new_df = pd.DataFrame([input_data_dict])
        processed = self.preprocessor.transform(new_df)
        pred_encoded = self.final_model.predict(processed)
        return self.label_encoder.inverse_transform(pred_encoded)[0]

    # -----------------------------------------------------------
    def run_pipeline(self, n_trials=20):
        self.load_data()
        self.prepare_data()
        self.setup_preprocessor()
        X_train_processed, X_test_processed = self.preprocess_data()
        self.optimize_hyperparameters(X_train_processed, self.y_train, n_trials)
        metrics = self.train_final_model(X_train_processed, X_test_processed, self.y_train, self.y_test)

        print("\n--- Örnek Tahmin ---")
        sample = {
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
        predicted_crop = self.predict_new_crop(sample)
        print(f"Tahmin edilen ürün: {predicted_crop}")
        return metrics


# ===============================================================
# 3. Ana Çalıştırma
# ===============================================================
if __name__ == "__main__":
    model = SentetikCropModel()
    model.run_pipeline()

    # Alternatif: Kaydedilmiş modeli yükleyip tahmin yapmak
    # model = SentetikCropModel().load_saved_model()
    # yeni_ornek = {...}
    # print(model.predict_new_crop(yeni_ornek))
