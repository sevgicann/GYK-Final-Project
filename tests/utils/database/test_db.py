"""
Test Database Utilities

Bu modül test veritabanı işlemleri için yardımcı fonksiyonları içerir.
"""

import os
import tempfile
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestDatabase:
    """Test veritabanı yönetimi için yardımcı sınıf."""
    
    def __init__(self, app=None):
        self.app = app
        self.db = None
        self.engine = None
        self.Session = None
        self.temp_db_path = None
        
    def setup_test_db(self):
        """Test veritabanını kurar."""
        # Geçici veritabanı dosyası oluştur
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp()
        
        # Test veritabanı URI'si
        test_db_uri = f'sqlite:///{self.temp_db_path}'
        
        # Flask app konfigürasyonu
        if self.app:
            self.app.config['SQLALCHEMY_DATABASE_URI'] = test_db_uri
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            self.app.config['TESTING'] = True
            
            # SQLAlchemy'yi başlat
            from app import db
            self.db = db
            
            with self.app.app_context():
                self.db.create_all()
        
        # SQLAlchemy engine ve session oluştur
        self.engine = create_engine(test_db_uri)
        self.Session = sessionmaker(bind=self.engine)
        
        return self
    
    def cleanup_test_db(self):
        """Test veritabanını temizler."""
        if self.app and self.db:
            with self.app.app_context():
                self.db.drop_all()
        
        if self.engine:
            self.engine.dispose()
        
        # Geçici dosyayı sil
        if self.temp_db_path and os.path.exists(self.temp_db_path):
            os.close(self.temp_db_fd)
            os.unlink(self.temp_db_path)
    
    def get_session(self):
        """Veritabanı session'ı döndürür."""
        return self.Session()
    
    def clear_tables(self):
        """Tüm tabloları temizler."""
        if self.app and self.db:
            with self.app.app_context():
                for table in reversed(self.db.metadata.sorted_tables):
                    self.db.session.execute(table.delete())
                self.db.session.commit()
    
    def insert_test_data(self, model_class, data_list):
        """Test verisi ekler."""
        if self.app and self.db:
            with self.app.app_context():
                for data in data_list:
                    if isinstance(data, dict):
                        instance = model_class(**data)
                    else:
                        instance = data
                    self.db.session.add(instance)
                self.db.session.commit()


def create_test_database():
    """Test veritabanı oluşturur."""
    return TestDatabase()


def with_clean_db(func):
    """Her test öncesi veritabanını temizleyen decorator."""
    def wrapper(*args, **kwargs):
        # Test öncesi temizlik
        test_db = create_test_database()
        test_db.setup_test_db()
        
        try:
            return func(*args, **kwargs)
        finally:
            # Test sonrası temizlik
            test_db.cleanup_test_db()
    
    return wrapper


def with_test_data(model_class, data_list):
    """Test verisi ile çalışan decorator."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            test_db = create_test_database()
            test_db.setup_test_db()
            
            try:
                # Test verisi ekle
                test_db.insert_test_data(model_class, data_list)
                return func(*args, **kwargs)
            finally:
                test_db.cleanup_test_db()
        
        return wrapper
    return decorator


# Database assertion helpers
def assert_record_exists(session, model_class, **filters):
    """Belirtilen kriterlere uygun kayıt olduğunu doğrular."""
    record = session.query(model_class).filter_by(**filters).first()
    assert record is not None, f"Record not found with filters: {filters}"
    return record


def assert_record_not_exists(session, model_class, **filters):
    """Belirtilen kriterlere uygun kayıt olmadığını doğrular."""
    record = session.query(model_class).filter_by(**filters).first()
    assert record is None, f"Record found when it shouldn't exist: {filters}"


def assert_record_count(session, model_class, expected_count, **filters):
    """Belirtilen kriterlere uygun kayıt sayısını doğrular."""
    query = session.query(model_class)
    if filters:
        query = query.filter_by(**filters)
    actual_count = query.count()
    assert actual_count == expected_count, \
        f"Expected {expected_count} records, found {actual_count}"


def get_test_db_uri():
    """Test veritabanı URI'si döndürür."""
    return 'sqlite:///:memory:'


def create_in_memory_db():
    """Bellek içi test veritabanı oluşturur."""
    from app import app, db
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
