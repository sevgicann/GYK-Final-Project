"""
Custom Feature Engineering for LightGBM Model
This file contains the CustomFeatureEngineer class used during model training
"""
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class CustomFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom feature engineering transformer for crop prediction
    Creates 10 engineered features from base features
    """

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
            if ph < 6.5:
                return "acidic"
            elif ph <= 7.5:
                return "neutral"
            else:
                return "alkaline"
        df["soil_ph_category"] = df["soil_ph"].apply(categorize_ph)

        # 4. Yağış + sulama etkisi
        irrigation_bonus = {
            "drip": 40, "Drip Irrigation": 40,
            "sprinkler": 25, "Sprinkler": 25,
            "flood": 10, "Flood Irrigation": 10,
            "none": 0, "None": 0, "Rain-fed": 0,
            "unknown": 0
        }
        df["rainfall_plus_irrigation"] = df["rainfall_mm"] + df["irrigation_method"].map(irrigation_bonus).fillna(0)

        # 5. Sulama yoğunluğu (ordinal)
        irrigation_intensity_map = {
            "none": 0, "None": 0, "Rain-fed": 0,
            "flood": 1, "Flood Irrigation": 1,
            "sprinkler": 2, "Sprinkler": 2,
            "drip": 3, "Drip Irrigation": 3
        }
        df["irrigation_intensity"] = df["irrigation_method"].map(irrigation_intensity_map).fillna(0)

        # 6. Gübre tipi nitrojenli mi?
        nitrogenous_fertilizers = [
            "nitrogenous", "Nitrogenous",
            "urea", "Urea",
            "ammonium", "Ammonium Sulphate",
            "potassium nitrate", "Potassium Nitrate"
        ]
        df["fertilizer_is_nitrogenous"] = df["fertilizer_type"].apply(
            lambda x: 1 if any(nit.lower() in str(x).lower() for nit in nitrogenous_fertilizers) else 0
        )

        # 7. Sıcaklık-nem etkileşimi
        df["temp_moisture_interaction"] = df["temperature_celsius"] * (df["moisture"] / 100)

        # 8. Evapotranspirasyon proxy
        df["evapotranspiration_proxy"] = df["temperature_celsius"] * (1 - df["moisture"] / 100) + np.maximum(0, df["temperature_celsius"] - 20)

        # 9. Toprak dokusu skoru
        soil_texture_score = {
            "sandy": 1, "Sandy": 1,
            "loamy": 2, "Loamy": 2,
            "clayey": 3, "Clayey": 3, "Clay": 3,
            "silty": 1.5, "Silty": 1.5
        }
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

