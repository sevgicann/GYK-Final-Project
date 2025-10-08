import pandas as pd

df = pd.read_csv(r"C:\Users\Mehdiye\Desktop\TURKCELL PROJE\TerraMind\GYK-Final-Project\crop_dataset_v4.csv")

print(df.columns)
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from scipy.optimize import differential_evolution

# === 1. Veri yükleme ===
df = pd.read_csv(r"C:\Users\Mehdiye\Desktop\TURKCELL PROJE\TerraMind\GYK-Final-Project\crop_dataset_v4.csv")

numeric_features = ['soil_ph','nitrogen','phosphorus','potassium','moisture',
                    'temperature_celsius','rainfall_mm']
categorical_features = ['region','soil_type','fertilizer_type','irrigation_method','weather_condition']
target = 'crop'

# === 2. Aykırı değer baskılama (IQR yöntemiyle winsorization) ===
def suppress_outliers_iqr(df, columns, lower_quantile=0.005, upper_quantile=0.995):
    """
    Nümerik değişkenlerde aykırı değerleri IQR yerine quantile tabanlı olarak baskılar.
    Örn: 0.01 ve 0.99 quantile aralığının dışında kalan değerleri bu sınırlarla değiştirir.
    """
    df_clean = df.copy()
    for col in columns:
        q_low = df[col].quantile(lower_quantile)
        q_high = df[col].quantile(upper_quantile)
        df_clean[col] = np.clip(df[col], q_low, q_high)
    return df_clean

df = suppress_outliers_iqr(df, numeric_features)

# === 3. Encoding ===
encoders = {}
for col in categorical_features + [target]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# === 4. Model eğitimi ===
X = df[numeric_features + categorical_features]
y = df[target]

model = XGBClassifier(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
model.fit(X, y)

feature_order = X.columns.tolist()

# === 5. Optimum koşul bulma ===
def suggest_optimal_conditions(target_crop, target_region):
    crop_val = encoders['crop'].transform([target_crop])[0]
    region_val = encoders['region'].transform([target_region])[0]

    bounds = [
        (df[col].min(), df[col].max()) for col in numeric_features
    ] + [
        (df[col].min(), df[col].max()) for col in ['soil_type','fertilizer_type','irrigation_method','weather_condition']
    ]

    def objective(x):
        values = dict(zip(numeric_features + ['soil_type','fertilizer_type','irrigation_method','weather_condition'], x))
        values['region'] = region_val
        X_test = pd.DataFrame([[values[col] for col in feature_order]], columns=feature_order)
        prob = model.predict_proba(X_test)[0, crop_val]
        return -prob

    result = differential_evolution(objective, bounds, maxiter=60, seed=42)
    best_x = result.x

    best_values = dict(zip(numeric_features + ['soil_type','fertilizer_type','irrigation_method','weather_condition'], best_x))
    best_df = pd.DataFrame([best_values])

    for col in ['soil_type','fertilizer_type','irrigation_method','weather_condition']:
        best_df[col] = encoders[col].inverse_transform(best_df[col].astype(int))

    values_for_prob = {**best_values, 'region': region_val}
    X_best = pd.DataFrame([[values_for_prob[c] for c in feature_order]], columns=feature_order)
    final_prob = model.predict_proba(X_best)[0, crop_val]

    return best_df.round(2), round(final_prob * 100, 2)

# === 6. Kullanıcı girdisi ===
target_crop = "wheat"
target_region = "Aegean"

optimum_df, probability = suggest_optimal_conditions(target_crop, target_region)

print(f"\n🌾 '{target_crop}' ürünü için '{target_region}' bölgesinde önerilen optimum koşullar:\n")
print(optimum_df)
print(f"\n🔮 Modelin '{target_crop}' ürünü olasılığı: %{probability}")
