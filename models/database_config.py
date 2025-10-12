"""
Database configuration file for TerraMind project
Bu dosya tüm modeller için veritabanı bağlantı ayarlarını içerir.
"""

import psycopg2
import pandas as pd
from typing import Optional, Dict, Any
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Veritabanı bağlantı ayarları ve yönetimi"""
    
    # Ana veritabanı bağlantı bilgileri (her iki model için aynı)
    DB_CONFIG = {
        'data100k': {
            'dbname': 'data100k',
            'user': 'postgres',
            'password': '12345',
            'host': 'localhost',
            'port': '5432'
        }
    }
    
    @classmethod
    def get_connection(cls, db_name: str = 'data100k') -> Optional[psycopg2.extensions.connection]:
        """
        Veritabanı bağlantısı oluşturur
        
        Args:
            db_name (str): Kullanılacak veritabanı adı
            
        Returns:
            psycopg2.extensions.connection: Bağlantı nesnesi veya None
        """
        if db_name not in cls.DB_CONFIG:
            logger.error(f"Veritabanı '{db_name}' bulunamadı. Mevcut veritabanları: {list(cls.DB_CONFIG.keys())}")
            return None
            
        config = cls.DB_CONFIG[db_name]
        
        try:
            conn = psycopg2.connect(**config)
            logger.info(f"'{db_name}' veritabanına başarıyla bağlanıldı.")
            return conn
        except Exception as e:
            logger.error(f"Veritabanı bağlantı hatası ({db_name}): {e}")
            return None
    
    @classmethod
    def load_data(cls, query: str, db_name: str = 'data100k') -> Optional[pd.DataFrame]:
        """
        Veritabanından veri çeker
        
        Args:
            query (str): SQL sorgusu
            db_name (str): Kullanılacak veritabanı adı
            
        Returns:
            pd.DataFrame: Çekilen veri veya None
        """
        conn = cls.get_connection(db_name)
        if conn is None:
            return None
            
        try:
            df = pd.read_sql_query(query, conn)
            logger.info(f"Veritabanından {len(df)} satır veri çekildi.")
            return df
        except Exception as e:
            logger.error(f"Veri çekme hatası: {e}")
            return None
        finally:
            if conn is not None:
                conn.close()
                logger.info("Veritabanı bağlantısı kapatıldı.")
    
    @classmethod
    def execute_query(cls, query: str, db_name: str = 'data100k', fetch: bool = True) -> Optional[Any]:
        """
        SQL sorgusu çalıştırır
        
        Args:
            query (str): SQL sorgusu
            db_name (str): Kullanılacak veritabanı adı
            fetch (bool): Sonuçları getirip getirmeyeceği
            
        Returns:
            Any: Sorgu sonucu veya None
        """
        conn = cls.get_connection(db_name)
        if conn is None:
            return None
            
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                conn.commit()
                cursor.close()
                return True
                
        except Exception as e:
            logger.error(f"Sorgu çalıştırma hatası: {e}")
            return None
        finally:
            if conn is not None:
                conn.close()
                logger.info("Veritabanı bağlantısı kapatıldı.")

# Veri tipi dönüşüm fonksiyonu
def convert_postgres_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    PostgreSQL'den çekilen dataframe'deki sütunları uygun Python tiplerine dönüştürür.
    
    Args:
        df (pd.DataFrame): Dönüştürülecek dataframe
    
    Returns:
        pd.DataFrame: Tip dönüşümü yapılmış dataframe
    """
    df_converted = df.copy()
    for col in df_converted.columns:
        try:
            df_converted[col] = pd.to_numeric(df_converted[col], errors='raise')
        except:
            df_converted[col] = df_converted[col].astype(str).str.strip()
    return df_converted

# Kolay kullanım için fonksiyonlar
def load_crop_data(table_name: str = 'crop_dataset_v_100bin') -> Optional[pd.DataFrame]:
    """
    Crop verilerini yükler ve tip dönüşümü uygular - Her iki model için aynı veritabanından
    
    Args:
        table_name (str): Tablo adı (varsayılan: crop_dataset_v_100bin)
    
    Returns:
        pd.DataFrame: Çekilen ve dönüştürülmüş veri veya None
    """
    query = f"SELECT * FROM {table_name};"
    df = DatabaseConfig.load_data(query, 'data100k')
    
    if df is not None:
        df = convert_postgres_dtypes(df)
        logger.info("Veri tipi dönüşümü uygulandı.")
    
    return df

def get_database_connection():
    """
    Doğrudan veritabanı bağlantısı döndürür
    
    Returns:
        psycopg2.extensions.connection: Bağlantı nesnesi veya None
    """
    return DatabaseConfig.get_connection('data100k')
