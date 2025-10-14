#!/usr/bin/env python3
"""
Test kullanıcısı oluşturma scripti
"""

from app import app, db
from models.user import User

def create_test_user():
    """Test kullanıcısı oluştur"""
    
    with app.app_context():
        # Veritabanı tablolarını oluştur
        db.create_all()
        
        # Test kullanıcısının email'i
        test_email = 'test@gmail.com'
        
        # Kullanıcı zaten var mı kontrol et
        existing_user = User.query.filter_by(email=test_email).first()
        
        if existing_user:
            print("Test kullanicisi zaten mevcut!")
            print(f"Email: {test_email}")
            print("Sifre: 123456")
            return
        
        # Yeni kullanıcı oluştur
        password = '123456'
        new_user = User(
            name='Test Kullanıcı',
            email=test_email,
            language='tr',
            is_active=True
        )
        
        # Şifreyi set et (otomatik hashler)
        new_user.set_password(password)
        
        # Veritabanına ekle
        db.session.add(new_user)
        db.session.commit()
        
        print("=" * 60)
        print("TEST KULLANICISI OLUSTURULDU!")
        print("=" * 60)
        print(f"Email: {test_email}")
        print(f"Sifre: {password}")
        print("=" * 60)
        print("\nSimdi login sayfasinda bu bilgilerle giris yapabilirsiniz.")

if __name__ == '__main__':
    create_test_user()

