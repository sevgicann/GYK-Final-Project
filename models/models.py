
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
import sys



# -----------------------------
# Ön İşleme
# -----------------------------
def preprocess_data(df, target_col="crop"):
    """Sayısal dönüşüm + One-Hot Encoding + LabelEncoder for y"""
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Sayısal kolonlar
    num_cols = [
        "nitrogen", "phosphorus", "potassium", "temperature_celsius",
        "humidity", "ph", "rainfall_mm", "days_to_harvest",
        "yield_tons_per_hectare", "moisture"
    ]

    # Sayısalları numeric'e çevir
    for col in num_cols:
        if col in X.columns:
            X[col] = pd.to_numeric(X[col], errors="coerce")

    # Eksik değerleri median ile doldur
    X[num_cols] = X[num_cols].fillna(X[num_cols].median())

    # Kategorik kolonlar
    cat_cols = X.select_dtypes(include=["object"]).columns

    # One-Hot Encoding
    ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    if len(cat_cols) > 0:
        X_cat = ohe.fit_transform(X[cat_cols])
        cat_feature_names = ohe.get_feature_names_out(cat_cols)
    else:
        X_cat = np.empty((len(X), 0))
        cat_feature_names = []

    # Final X
    X_final = pd.concat([
        X[num_cols].reset_index(drop=True),
        pd.DataFrame(X_cat, columns=cat_feature_names, index=X.index)
    ], axis=1)

    # Target encoding
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X_final, y_encoded, ohe, le

# -----------------------------
# XGBoost Modeli
# -----------------------------
def train_xgboost(X, y):
    """XGBoost modeli + metrikler"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Basit XGBoost modeli (optimizasyonsuz)
    model = xgb.XGBClassifier(
        objective='multi:softmax',
        num_class=len(np.unique(y)),
        eval_metric='mlogloss',
        random_state=42
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Performans metrikleri
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="macro")
    rec = recall_score(y_test, y_pred, average="macro")
    f1 = f1_score(y_test, y_pred, average="macro")

    print("Accuracy:", acc)
    print("Precision:", prec)
    print("Recall:", rec)
    print("F1 Score:", f1)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues")
    plt.title("Confusion Matrix")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.show()

    # Feature Importance
    feature_importances = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    plt.figure(figsize=(10,6))
    sns.barplot(x="Importance", y="Feature", data=feature_importances)
    plt.title("Feature Importance (XGBoost)")
    plt.show()

    return model, feature_importances


def create_connection():
    query = "SELECT * FROM real_data TABLESAMPLE SYSTEM (10);"

    conn = None
    try:
        conn = psycopg2.connect(
            dbname="terramind_db",
            user="postgres",
            password="new.pass3",
            host="localhost",
            port="5432"
        )

        cur = conn.cursor()
        print("Executing query...")
        cur.execute(query)

        print("Fetching the data...")
        data = cur.fetchall() 
        
        colnames = [desc[0] for desc in cur.description]

        dataframe = pd.DataFrame(data, columns=colnames)
        
        print(f"Length of random data is {len(dataframe)}")
        print("DataFrame head:")
        print(dataframe.head())

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"DB error: {error}", file=sys.stderr)
        return None
    finally:
        if conn is not None:
            conn.close()
            print("DB connection was closed.")
        
    return dataframe

# -----------------------------
# Çalıştırma
# -----------------------------
if __name__ == "__main__":
    df = create_connection()
    X, y, ohe, le = preprocess_data(df)
    model, feat_imp = train_xgboost(X, y)