"""
LightGBM Bi-Directional Predictor
Based on models/sentetik_model.py - Implements advanced feature engineering
"""
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from scipy.optimize import differential_evolution
from .base_predictor import BasePredictor
from utils.logger import get_logger

logger = get_logger(__name__)


class LightGBMCropPredictor(BasePredictor):
    """
    LightGBM-based bi-directional crop predictor with feature engineering
    - Environment → Crop: Direct prediction with preprocessing pipeline
    - Crop → Environment: Optimization considering engineered features
    """
    
    def __init__(self, model_path: str = "models/sentetik_crop_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.preprocessor = None
        self.label_encoder = None
        self.classes = None
        self.numeric_features = [
            'soil_ph', 'nitrogen', 'phosphorus', 'potassium',
            'moisture', 'temperature_celsius', 'rainfall_mm'
        ]
        self.categorical_features = [
            'region', 'soil_type', 'fertilizer_type',
            'irrigation_method', 'weather_condition'
        ]
        self._load_model()
    
    def _load_model(self):
        """Load model bundle from joblib file"""
        try:
            logger.info(f"📦 Loading LightGBM model from: {self.model_path}")
            
            model_bundle = joblib.load(self.model_path)
            
            self.model = model_bundle['model']
            self.preprocessor = model_bundle['preprocessor']
            self.label_encoder = model_bundle['label_encoder']
            self.classes = model_bundle['classes']
            
            logger.info("✅ LightGBM model loaded successfully")
            logger.info(f"   Crops: {len(self.classes)}")
            logger.info(f"   Preprocessing: Feature engineering pipeline included")
            
        except Exception as e:
            logger.error(f"❌ Failed to load LightGBM model: {str(e)}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is ready"""
        return self.model is not None and self.preprocessor is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model metadata"""
        if not self.is_loaded():
            return {'status': 'not_loaded'}
        
        return {
            'status': 'loaded',
            'model_type': 'LightGBM',
            'algorithm': 'Gradient Boosting Decision Tree',
            'features': {
                'numeric': self.numeric_features,
                'categorical': self.categorical_features,
                'engineered': True
            },
            'crops': list(self.classes),
            'capabilities': ['environment_to_crop', 'crop_to_environment'],
            'preprocessing': 'Advanced feature engineering pipeline'
        }
    
    def predict_crop_from_environment(self, environment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict best crop from environmental conditions
        Direction: Environment → Crop
        Uses preprocessing pipeline with feature engineering
        """
        if not self.is_loaded():
            return {'success': False, 'error': 'Model not loaded'}
        
        try:
            logger.info("🌱 Predicting crop from environment (LightGBM + Feature Engineering)")
            
            # Validate required features
            missing_features = []
            for feature in self.numeric_features + self.categorical_features:
                if feature not in environment_data:
                    missing_features.append(feature)
            
            if missing_features:
                return {
                    'success': False,
                    'error': f'Missing required features: {", ".join(missing_features)}'
                }
            
            # Create DataFrame
            df = pd.DataFrame([environment_data])
            
            # Ensure numeric types
            for col in self.numeric_features:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Ensure categorical types
            for col in self.categorical_features:
                if col in df.columns:
                    df[col] = df[col].astype(str)
            
            # Apply preprocessing pipeline (includes feature engineering)
            X_processed = self.preprocessor.transform(df)
            
            # Get prediction
            prediction_encoded = self.model.predict(X_processed)[0]
            predicted_crop = self.label_encoder.inverse_transform([prediction_encoded])[0]
            
            # Get probabilities
            probabilities = self.model.predict_proba(X_processed)[0]
            
            # Get top 3
            top_indices = np.argsort(probabilities)[::-1][:3]
            top_3 = [
                (self.classes[idx], float(probabilities[idx]))
                for idx in top_indices
            ]
            
            confidence = float(probabilities[prediction_encoded])
            
            logger.info(f"✅ Predicted crop: {predicted_crop} (confidence: {confidence:.2%})")
            logger.info(f"   Top 3: {[(c, f'{p:.1%}') for c, p in top_3]}")
            
            return {
                'success': True,
                'predicted_crop': predicted_crop,
                'confidence': confidence,
                'top_3_predictions': top_3
            }
            
        except Exception as e:
            logger.error(f"❌ Crop prediction failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_environment_from_crop(self, crop: str, region: str) -> Dict[str, Any]:
        """
        Predict optimal environmental conditions for a target crop
        Direction: Crop → Environment (using optimization)
        """
        if not self.is_loaded():
            return {'success': False, 'error': 'Model not loaded'}
        
        try:
            logger.info(f"🔍 Optimizing environment for crop '{crop}' in region '{region}' (LightGBM)")
            
            # Encode target crop
            try:
                crop_encoded = self.label_encoder.transform([crop])[0]
            except ValueError:
                return {
                    'success': False,
                    'error': f'Unknown crop: {crop}'
                }
            
            # Define optimization bounds
            bounds = [
                (4.0, 9.0),      # soil_ph
                (0, 150),        # nitrogen
                (0, 150),        # phosphorus
                (0, 220),        # potassium
                (20, 100),       # moisture
                (10, 45),        # temperature_celsius
                (60, 3000),      # rainfall_mm
            ]
            
            # Categorical options (we'll sample from these)
            categorical_options = {
                'soil_type': ['Sandy', 'Loamy', 'Clayey', 'Silty'],
                'fertilizer_type': ['Nitrogenous', 'Phosphatic', 'Potassic', 'Organic', 'Compound'],
                'irrigation_method': ['Drip Irrigation', 'Sprinkler', 'Flood Irrigation', 'None'],
                'weather_condition': ['Sunny', 'Rainy', 'Cloudy']
            }
            
            # Objective function to maximize crop probability
            def objective(x):
                try:
                    # Sample categorical values (deterministic based on x values)
                    soil_type_idx = int(x[0] * 10) % len(categorical_options['soil_type'])
                    fertilizer_idx = int(x[1] * 10) % len(categorical_options['fertilizer_type'])
                    irrigation_idx = int(x[2] * 10) % len(categorical_options['irrigation_method'])
                    weather_idx = int(x[3] * 10) % len(categorical_options['weather_condition'])
                    
                    features = {
                        'soil_ph': x[4],
                        'nitrogen': x[5],
                        'phosphorus': x[6],
                        'potassium': x[7],
                        'moisture': x[8],
                        'temperature_celsius': x[9],
                        'rainfall_mm': x[10],
                        'region': region,
                        'soil_type': categorical_options['soil_type'][soil_type_idx],
                        'fertilizer_type': categorical_options['fertilizer_type'][fertilizer_idx],
                        'irrigation_method': categorical_options['irrigation_method'][irrigation_idx],
                        'weather_condition': categorical_options['weather_condition'][weather_idx],
                    }
                    
                    # Create DataFrame
                    df = pd.DataFrame([features])
                    
                    # Apply preprocessing pipeline
                    X_processed = self.preprocessor.transform(df)
                    
                    # Get probability for target crop
                    prob = self.model.predict_proba(X_processed)[0, crop_encoded]
                    return -prob  # Negative because we minimize
                    
                except Exception as e:
                    logger.debug(f"Optimization iteration error: {e}")
                    return 1.0  # Penalty
            
            # Extended bounds to include categorical sampling parameters
            extended_bounds = [
                (0, 1),  # soil_type selector
                (0, 1),  # fertilizer_type selector
                (0, 1),  # irrigation_method selector
                (0, 1),  # weather_condition selector
            ] + bounds
            
            # Run optimization
            logger.info("   Running differential evolution optimization...")
            result = differential_evolution(
                objective,
                extended_bounds,
                maxiter=80,
                seed=42,
                workers=1,
                polish=True
            )
            
            # Extract optimal values
            best_x = result.x
            
            # Decode categorical features
            soil_type_idx = int(best_x[0] * 10) % len(categorical_options['soil_type'])
            fertilizer_idx = int(best_x[1] * 10) % len(categorical_options['fertilizer_type'])
            irrigation_idx = int(best_x[2] * 10) % len(categorical_options['irrigation_method'])
            weather_idx = int(best_x[3] * 10) % len(categorical_options['weather_condition'])
            
            optimal_conditions = {
                'soil_ph': round(float(best_x[4]), 2),
                'nitrogen': round(float(best_x[5]), 2),
                'phosphorus': round(float(best_x[6]), 2),
                'potassium': round(float(best_x[7]), 2),
                'moisture': round(float(best_x[8]), 2),
                'temperature_celsius': round(float(best_x[9]), 2),
                'rainfall_mm': round(float(best_x[10]), 2),
                'region': region,
                'soil_type': categorical_options['soil_type'][soil_type_idx],
                'fertilizer_type': categorical_options['fertilizer_type'][fertilizer_idx],
                'irrigation_method': categorical_options['irrigation_method'][irrigation_idx],
                'weather_condition': categorical_options['weather_condition'][weather_idx],
            }
            
            # Calculate final probability
            success_probability = float(-result.fun * 100)  # Convert to percentage
            
            logger.info(f"✅ Optimization complete. Success probability: {success_probability:.2f}%")
            
            return {
                'success': True,
                'crop': crop,
                'region': region,
                'optimal_conditions': optimal_conditions,
                'success_probability': success_probability
            }
            
        except Exception as e:
            logger.error(f"❌ Environment optimization failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

