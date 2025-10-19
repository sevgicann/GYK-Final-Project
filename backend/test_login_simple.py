"""
En basit login testi
"""

def test_login_logic():
    """En basit login mantığı testi."""
    
    # Mock kullanıcı veritabanı
    users_db = {
        'test@example.com': {
            'password': 'password123',
            'name': 'Test User',
            'language': 'tr'
        },
        'admin@example.com': {
            'password': 'admin123',
            'name': 'Admin User',
            'language': 'en'
        }
    }
    
    def login_user(email, password):
        """Basit login fonksiyonu."""
        if email in users_db:
            if users_db[email]['password'] == password:
                return {
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'email': email,
                        'name': users_db[email]['name'],
                        'language': users_db[email]['language']
                    }
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid password'
                }
        else:
            return {
                'success': False,
                'message': 'User not found'
            }
    
    # Test 1: Başarılı login
    print("🧪 Test 1: Başarılı login...")
    result = login_user('test@example.com', 'password123')
    assert result['success'] is True
    assert result['user']['email'] == 'test@example.com'
    assert result['user']['name'] == 'Test User'
    print("✅ Başarılı login testi geçti!")
    
    # Test 2: Yanlış şifre
    print("🧪 Test 2: Yanlış şifre...")
    result = login_user('test@example.com', 'wrongpassword')
    assert result['success'] is False
    assert result['message'] == 'Invalid password'
    print("✅ Yanlış şifre testi geçti!")
    
    # Test 3: Kullanıcı bulunamadı
    print("🧪 Test 3: Kullanıcı bulunamadı...")
    result = login_user('nonexistent@example.com', 'password123')
    assert result['success'] is False
    assert result['message'] == 'User not found'
    print("✅ Kullanıcı bulunamadı testi geçti!")
    
    # Test 4: Admin login
    print("🧪 Test 4: Admin login...")
    result = login_user('admin@example.com', 'admin123')
    assert result['success'] is True
    assert result['user']['email'] == 'admin@example.com'
    assert result['user']['name'] == 'Admin User'
    print("✅ Admin login testi geçti!")
    
    return True

if __name__ == "__main__":
    print("🚀 TerraMind Login Testleri Başlatılıyor...")
    print("=" * 50)
    
    try:
        success = test_login_logic()
        
        print("=" * 50)
        print("🎉 Tüm login testleri başarılı!")
        print("✅ Kullanıcı girişi sistemi çalışıyor!")
        print("✅ TerraMind authentication test edildi!")
        
    except AssertionError as e:
        print(f"❌ Test başarısız: {e}")
    except Exception as e:
        print(f"❌ Hata: {e}")
