import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import KNNImputer

crop_recommendation = pd.read_csv(r"/home/nur/Desktop/GYK-Final-Project/csv_doc/Crop_recommendation.csv")
print(crop_recommendation.head())


crop_yield = pd.read_csv(r"/home/nur/Desktop/GYK-Final-Project/csv_doc/crop_yield.csv")
print(crop_yield.head())


data_core = pd.read_csv(r"/home/nur/Desktop/GYK-Final-Project/csv_doc/data_core.csv")
print(data_core.head())

print(f"crop_recommendation", crop_recommendation.columns)
print(f"crop_yield", crop_yield.columns)
print(f"data_core", data_core.columns)


#kolon isimlerini benzer olacak şekilde değiştir

crop_recommendation = crop_recommendation.rename(
    columns={
        "N": "Nitrogen",
        "P": "Phosphorus",
        "K": "Potassium"
    }
)

data_core = data_core.rename(columns={"Phosphorous": "Phosphorus", "Temparature": "temperature_celsius","Crop Type":"crop"})
crop_recommendation = crop_recommendation.rename(columns={"rainfall": "rainfall_mm",
                                                           "temperature": "temperature_celsius", "label":"crop"})

crop_recommendation.columns = crop_recommendation.columns.str.strip().str.lower().str.replace(" ", "_")
crop_yield.columns = crop_yield.columns.str.strip().str.lower().str.replace(" ", "_")
data_core.columns = data_core.columns.str.strip().str.lower().str.replace(" ", "_")



print(f"crop_recommendation", crop_recommendation.columns)
print(f"crop_yield", crop_yield.columns)
print(f"data_core", data_core.columns)

#print(crop_yield.fertilizer_used)
#print(data_core.fertilizer_name.unique())

#GÖREV
#fertilizer_name sadece data_core da var. df ler birleştikten sonra boş kalan yerleri kmeans ile doldurabilirsin.
#fertilizer_used değişkeni sadece crop_yield da var incele, önemsiz ise sil.


print(crop_recommendation.head())
print(crop_yield.head())
print(data_core.head())


#veri setlerini birleştirelim

df = pd.concat([crop_recommendation, crop_yield, data_core], ignore_index=True)

print(df.head())
print(df.columns)

#eksik verileri inceleyelim
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


check_df(df)

#boşlukları doldurmak için chat e sor

#sayısal kategorik değişken analizi
def grab_col_names(dataframe, cat_th=10,  car_th=20):
    """
    Veri setindeki kategorik, numerik ve kategorik fakat kardinal değişkenlerin isimlerini verir.

    Parameters
    ----------
    dataframe: dataframe
        değişken isimleri alınmak istenen dataframe'dir.
    cat_th: int, float
        numerik fakat kategorik olan değişkenler için sınıf eşik değeri
    car_th: int, float
        kategorik fakat kardinal değişkenler için sınıf eşik değeri

    Returns
    -------
    cat_cols: list
        Kategorik değişken listesi
    num_cols: list
        Numerik değişken listesi
    cat_but_car: list
        Kategorik görünümlü kardinal değişken listesi

    Notes
    ------
    cat_cols + num_cols + cat_but_car = toplam değişken sayısı
    num_but_cat cat_cols'un içerisinde.

    """
    # cat_cols, cat_but_car
    cat_cols = [col for col in df.columns if str(df[col].dtypes) in ["category", "object", "bool"]]

    num_but_cat = [col for col in df.columns if df[col].nunique() < 10 and df[col].dtypes in ["int", "float"]]

    cat_but_car = [col for col in df.columns if
                   df[col].nunique() > 20 and str(df[col].dtypes) in ["category", "object"]]

    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    num_cols = [col for col in df.columns if df[col].dtypes in ["int", "float"]]
    num_cols = [col for col in num_cols if col not in cat_cols]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')

    return cat_cols, num_cols, cat_but_car

cat_cols, num_cols, cat_but_car = grab_col_names(df)

print(f"cat cols", cat_cols)
print(f"num cols", num_cols)
print(f"cat but car", cat_but_car) 

def cat_summary(dataframe, col_name, plot=False):
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
    print("##########################################")

    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show(block=True)

for i in cat_cols:
    cat_summary(df, i)

cat_summary(df, "crop")

# gözlemlerin isimlerini düzenleyelim
df = df.apply(lambda x: x.apply(lambda v: v.lower() if isinstance(v, str) else v) 
              if x.dtype in ["object", "string"] else x)

df['crop'] = df['crop'].replace({
    'ground nuts': 'peanut',
    'paddy': 'rice'
})

df['soil_type'] = df['soil_type'].replace({
    'loamy': 'loam',
    'clayey': 'clay'
})

print(f"İLK BOŞLUKLU DF",df.isna().sum())


#toprak tipi olmayan değişkenleri knn ile dolduralım. iki kez doldurma işlemi yapacağız.
# ilkinde crop değişkeni aynı olanlar arasında, ikincisinde crop u önemsemeden dolduracağız.

#birinci soil_type doldurma adımı
# Belirtilen sütunlarda hiç boşluk olmayan satırları filtrele
cols_for_nn = ['soil_type', 'nitrogen', 'phosphorus', 'potassium', 'temperature_celsius', 'humidity']
df_complete = df.dropna(subset=cols_for_nn)

# Soil_type değeri NaN olan satırları belirle
df_missing_soil = df[df['soil_type'].isna()]

# NaN değerleri doldurmak için döngü
for index, row in df_missing_soil.iterrows():
    current_crop = row['crop']
    
    # Mevcut satırın crop değerine birebir uyan, soil_type'ı dolu olan satırları filtrele
    df_neighbors_candidate = df_complete[df_complete['crop'] == current_crop]
    
    if not df_neighbors_candidate.empty:
        # Komşuluk için kullanılacak özellikler
        features = ['nitrogen', 'phosphorus', 'potassium', 'temperature_celsius', 'humidity']
        
        # NaN olan satırın özellik vektörü
        current_features = row[features].values.reshape(1, -1)
        
        # Komşu adaylarının özellik vektörleri
        neighbor_features = df_neighbors_candidate[features].values
        
        # En yakın 4 komşuyu bulmak için NearestNeighbors modelini kullan
        # n_neighbors, veri boyutuna göre ayarlanabilir. Burada min(4, len(df_neighbors_candidate)) kullanılıyor.
        n_neighbors_to_find = min(4, len(df_neighbors_candidate))
        
        if n_neighbors_to_find > 0:
            nn = NearestNeighbors(n_neighbors=n_neighbors_to_find, metric='euclidean')
            nn.fit(neighbor_features)
            
            distances, indices = nn.kneighbors(current_features)
            
            # En yakın komşuların soil_type değerlerini al
            closest_soil_types = df_neighbors_candidate.iloc[indices[0]]['soil_type'].values
            
            # En sık kullanılan soil_type değerini bul ve atama yap
            if len(closest_soil_types) > 0:
                most_frequent_soil_type = pd.Series(closest_soil_types).mode()[0]
                df.loc[index, 'soil_type'] = most_frequent_soil_type
            else:
                # Hiç komşu bulunamazsa veya uygun soil_type yoksa boş bırak (veya başka bir strateji uygulanabilir)
                pass
        else:
            pass # Uygun komşu adayı yok
    else:
        pass # Mevcut crop değerine sahip soil_type'ı dolu satır yok

print("\nDoldurulmuş DataFrame 1.adım:")
print(df)

print(f"TOPRAK TİPİ DOLDURULMUŞ 1.adım ",df.isna().sum())


#ikinci soil_type doldurma adımı
from sklearn.neighbors import NearestNeighbors
import pandas as pd

# Soil_type ve diğer kolonlarda boşluğu olmayan satırlar
cols_for_nn = ['soil_type', 'nitrogen', 'phosphorus', 'potassium', 'temperature_celsius', 'humidity']
df_complete = df.dropna(subset=cols_for_nn)

# Soil_type değeri NaN olan satırları al
df_missing_soil = df[df['soil_type'].isna()]

# Eksik değerleri doldurma
for index, row in df_missing_soil.iterrows():
    # Komşuluk için kullanılacak özellikler
    features = ['nitrogen', 'phosphorus', 'potassium', 'temperature_celsius', 'humidity']

    # NaN olan satırın özellik vektörü
    current_features = row[features].values.reshape(1, -1)

    # Komşu adaylarının özellik vektörleri (artık crop filtre yok!)
    neighbor_features = df_complete[features].values

    # En yakın komşu sayısı
    n_neighbors_to_find = min(4, len(df_complete))

    if n_neighbors_to_find > 0:
        nn = NearestNeighbors(n_neighbors=n_neighbors_to_find, metric='euclidean')
        nn.fit(neighbor_features)

        distances, indices = nn.kneighbors(current_features)

        # Komşuların soil_type değerlerini al
        closest_soil_types = df_complete.iloc[indices[0]]['soil_type'].values

        # En sık geçen soil_type değerini bul ve ata
        if len(closest_soil_types) > 0:
            most_frequent_soil_type = pd.Series(closest_soil_types).mode()[0]
            df.loc[index, 'soil_type'] = most_frequent_soil_type

print("\n✅ Doldurulmuş DataFrame 2.adım:")
print(df)

print(f"TOPRAK TİPİ DOLDURULMUŞ 2.adım ",df.isna().sum())
##########
for i in cat_cols:
    cat_summary(df, i)

cat_summary(df, "crop")

#crop değişkeninin numerik değişkenler ile analizi
def target_summary_with_num(dataframe, target, numerical_col):
    print(dataframe.groupby(target).agg({numerical_col: "mean"}), end="\n\n\n")


for col in num_cols:
    target_summary_with_num(df, "crop", col)

#crop değişkeninin kategorik değişkenlerile analizi
def target_summary_with_cat(dataframe, target, categorical_col):
    summary = pd.crosstab(dataframe[categorical_col], dataframe[target], normalize="index") * 100
    summary = round(summary, 2)  # yüzde formatında
    print(summary, end="\n\n\n")

for col in cat_cols:
    target_summary_with_cat(df,"crop",col)


# ['rainfall_mm'] boşluğu diğerlerine göre daha az önce onu doldur. ['temperature_celsius', 'humidity', 'soil_type', 'crop','nitrogen',] benzerliklerine göre
#hata verdi, incele
# Kullanılacak özellikler
features = ['temperature_celsius', 'humidity', 'soil_type', 'crop', 'nitrogen']

# Kategorik kolonları sayısal hale getirelim (One-Hot Encoding)
df_features = pd.get_dummies(df[features])

# Eksik değerleri bul
df_missing = df[df['rainfall_mm'].isna()]

for index, row in df_missing.iterrows():
    # Mevcut satırda dolu olan özellikleri seç
    mask = ~row[features].isna()
    available_features = [f for f in features if mask[f]]

    if not available_features:
        continue
    
    df_candidates = df[df['rainfall_mm'].notna()].dropna(subset=available_features)

    if df_candidates.empty:
        continue
    
    candidate_features = pd.get_dummies(df_candidates[available_features]).reindex(columns=df_features.columns, fill_value=0).values

    row_df = pd.DataFrame(row).T
    row_features = pd.get_dummies(row_df[available_features]).reindex(columns=df_features.columns, fill_value=0).values


    # eski versiyon -hatalı kod (düzeltttik :)))
    # # Sayısal ve one-hot özellikler
    # row_features = pd.get_dummies(row[available_features]).reindex(columns=df_features.columns,
    #                                                                fill_value=0).values.reshape(1, -1)

    # # NaN olmayan satırlar
    # df_candidates = df[df['rainfall_mm'].notna()].dropna(subset=features)
    # candidate_features = pd.get_dummies(df_candidates[available_features]).reindex(columns=df_features.columns,
    #                                                                                fill_value=0).values

    # En yakın 3 komşu
    n_neighbors_to_find = min(3, len(df_candidates))

    nn = NearestNeighbors(n_neighbors=n_neighbors_to_find, metric='euclidean')
    nn.fit(candidate_features)
    distances, idx = nn.kneighbors(row_features)

    # Eksik değeri en yakın 3 komşunun ortalaması ile doldur
    nearest_rainfalls = df_candidates.iloc[idx[0]]['rainfall_mm'].values
    df.loc[index, 'rainfall_mm'] = nearest_rainfalls.mean()

print("\n✅rainfall_mm Doldurulmuş DataFrame:")
print(df)

print(f"rainfall_mm doldurulmuş df ",df.isna().sum())


# toprak tipinden sonra ['nitrogen', 'phosphorus', 'potassium', 'humidity', 'ph'] değişkenleri doldur
nan_cols_list = ['nitrogen', 'phosphorus', 'potassium', 'temperature_celsius', 'humidity']

df.to_csv("real_data.csv", index=False)
#['soil_type', 'crop', 'temperature_celsius','rainfall_mm'] değerlerine bakarak nan_cols_list teki boşlukları sırasıyla(tek tek) doldur.
