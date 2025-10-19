
import pickle
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from scipy.optimize import differential_evolution
from .base_predictor import BasePredictor
from utils.logger import get_logger

logger = get_logger(__name__)


class XGBoostCropPredictor(BasePredictor):
    """
    XGBoost-based bi-directional crop predictor
    - Environment → Crop: Direct prediction
    - Crop → Environment: Optimization using differential evolution
    """
    
    def __init__(self, model_path: str = "ai/models/crop_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.encoders = {}
        self.feature_order = None
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
        """Load model and encoders from pickle file"""
        try:
            logger.info(f"📦 Loading XGBoost model from: {self.model_path}")
            
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.encoders = model_data['encoders']
            self.feature_order = model_data['feature_order']
            
            logger.info("✅ XGBoost model loaded successfully")
            logger.info(f"   Features: {len(self.feature_order)}")
            logger.info(f"   Crops: {len(self.encoders.get('crop', {}).classes_)}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load XGBoost model: {str(e)}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if model is ready"""
        return self.model is not None and self.encoders is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model metadata"""
        if not self.is_loaded():
            return {'status': 'not_loaded'}
        
        return {
            'status': 'loaded',
            'model_type': 'XGBoost',
            'algorithm': 'Gradient Boosting',
            'features': {
                'numeric': self.numeric_features,
                'categorical': self.categorical_features,
                'total': len(self.feature_order)
            },
            'crops': list(self.encoders['crop'].classes_) if 'crop' in self.encoders else [],
            'regions': list(self.encoders['region'].classes_) if 'region' in self.encoders else [],
            'capabilities': ['environment_to_crop', 'crop_to_environment']
        }
    
    def predict_crop_from_environment(self, environment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict best crop from environmental conditions
        Direction: Environment → Crop
        """
        if not self.is_loaded():
            return {'success': False, 'error': 'Model not loaded'}
        
        try:
            logger.info("🌾 Predicting crop from environment (XGBoost)")
            
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
            
            # Encode categorical features
            for col in self.categorical_features:
                if col in df.columns and col in self.encoders:
                    try:
                        df[col] = self.encoders[col].transform(df[col].astype(str))
                    except ValueError as e:
                        logger.warning(f"Unknown category in '{col}': {df[col].iloc[0]}")
                        # Use first class as fallback
                        df[col] = 0
            
            # Ensure numeric types
            for col in self.numeric_features:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Order features correctly
            X = df[self.feature_order]
            
            # Get prediction
            prediction_encoded = self.model.predict(X)[0]
            predicted_crop = self.encoders['crop'].inverse_transform([prediction_encoded])[0]
            
            # Get probabilities
            probabilities = self.model.predict_proba(X)[0]
            crops = self.encoders['crop'].classes_
            
            # Get top 3
            top_indices = np.argsort(probabilities)[::-1][:3]
            top_3 = [
                (crops[idx], float(probabilities[idx]))
                for idx in top_indices
            ]
            
            confidence = float(probabilities[prediction_encoded])
            
            logger.info(f"✅ Predicted crop: {predicted_crop} (confidence: {confidence:.2%})")
            
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
            logger.info(f"🔍 Optimizing environment for crop '{crop}' in region '{region}'")
            
            # Encode target crop and region
            try:
                crop_encoded = self.encoders['crop'].transform([crop])[0]
                region_encoded = self.encoders['region'].transform([region])[0]
            except ValueError as e:
                return {
                    'success': False,
                    'error': f'Unknown crop or region: {str(e)}'
                }
            
            # Define optimization bounds
            # These should ideally come from training data statistics
            bounds = [
                (4.0, 9.0),      # soil_ph
                (0, 150),        # nitrogen
                (0, 150),        # phosphorus
                (0, 220),        # potassium
                (20, 100),       # moisture
                (10, 45),        # temperature_celsius
                (60, 3000),      # rainfall_mm
                (0, len(self.encoders['soil_type'].classes_) - 1),  # soil_type
                (0, len(self.encoders['fertilizer_type'].classes_) - 1),  # fertilizer_type
                (0, len(self.encoders['irrigation_method'].classes_) - 1),  # irrigation_method
                (0, len(self.encoders['weather_condition'].classes_) - 1),  # weather_condition
            ]
            
            # Objective function to maximize crop probability
            def objective(x):
                try:
                    # Build feature vector
                    features = {
                        'soil_ph': x[0],
                        'nitrogen': x[1],
                        'phosphorus': x[2],
                        'potassium': x[3],
                        'moisture': x[4],
                        'temperature_celsius': x[5],
                        'rainfall_mm': x[6],
                        'region': region_encoded,
                        'soil_type': int(round(x[7])),
                        'fertilizer_type': int(round(x[8])),
                        'irrigation_method': int(round(x[9])),
                        'weather_condition': int(round(x[10])),
                    }
                    
                    # Create DataFrame in correct order
                    X_df = pd.DataFrame([[features[col] for col in self.feature_order]], 
                                       columns=self.feature_order)
                    
                    # Get probability for target crop
                    prob = self.model.predict_proba(X_df)[0, crop_encoded]
                    return -prob  # Negative because we minimize
                    
                except Exception as e:
                    logger.debug(f"Optimization iteration error: {e}")
                    return 1.0  # Penalty
            
            # Run optimization
            logger.info("   Running differential evolution optimization...")
            result = differential_evolution(
                objective,
                bounds,
                maxiter=60,
                seed=42,
                workers=1,
                polish=True
            )
            
            # Extract optimal values
            best_x = result.x
            
            optimal_conditions = {
                'soil_ph': round(float(best_x[0]), 2),
                'nitrogen': round(float(best_x[1]), 2),
                'phosphorus': round(float(best_x[2]), 2),
                'potassium': round(float(best_x[3]), 2),
                'moisture': round(float(best_x[4]), 2),
                'temperature_celsius': round(float(best_x[5]), 2),
                'rainfall_mm': round(float(best_x[6]), 2),
                'region': region,
            }
            
            # Decode categorical features
            categorical_encoded = {
                'soil_type': int(round(best_x[7])),
                'fertilizer_type': int(round(best_x[8])),
                'irrigation_method': int(round(best_x[9])),
                'weather_condition': int(round(best_x[10])),
            }
            
            for feature, encoded_value in categorical_encoded.items():
                if feature in self.encoders:
                    try:
                        # Ensure value is within bounds
                        encoded_value = max(0, min(encoded_value, len(self.encoders[feature].classes_) - 1))
                        decoded = self.encoders[feature].inverse_transform([encoded_value])[0]
                        optimal_conditions[feature] = decoded
                    except:
                        optimal_conditions[feature] = "unknown"
            
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

