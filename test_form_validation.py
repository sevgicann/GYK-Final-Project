"""
Form Validasyon Testleri - TerraMind
"""

import re

class FormValidator:
    """Form validasyon sınıfı"""
    
    @staticmethod
    def validate_email(email):
        """Email validasyonu"""
        if not email:
            return False, "Email boş olamaz"
        
        # Email regex pattern - çift nokta kontrolü ile
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Çift nokta kontrolü
        if '..' in email:
            return False, "Email çift nokta içeremez"
        
        if not re.match(pattern, email):
            return False, "Geçersiz email formatı"
        
        if len(email) > 254:  # RFC 5321 limit
            return False, "Email çok uzun"
        
        return True, "Email geçerli"
    
    @staticmethod
    def validate_password(password):
        """Şifre validasyonu"""
        if not password:
            return False, "Şifre boş olamaz"
        
        if len(password) < 8:
            return False, "Şifre en az 8 karakter olmalı"
        
        if len(password) > 128:
            return False, "Şifre çok uzun"
        
        # Şifre güçlülük kontrolü
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        if not has_upper:
            return False, "Şifre en az bir büyük harf içermeli"
        
        if not has_lower:
            return False, "Şifre en az bir küçük harf içermeli"
        
        if not has_digit:
            return False, "Şifre en az bir rakam içermeli"
        
        if not has_special:
            return False, "Şifre en az bir özel karakter içermeli"
        
        return True, "Şifre geçerli"
    
    @staticmethod
    def validate_username(username):
        """Kullanıcı adı validasyonu"""
        if not username:
            return False, "Kullanıcı adı boş olamaz"
        
        if len(username) < 3:
            return False, "Kullanıcı adı en az 3 karakter olmalı"
        
        if len(username) > 50:
            return False, "Kullanıcı adı çok uzun"
        
        # Sadece harf, rakam, alt çizgi ve tire
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Kullanıcı adı sadece harf, rakam, _ ve - içerebilir"
        
        return True, "Kullanıcı adı geçerli"
    
    @staticmethod
    def validate_name(name, field_name="İsim"):
        """İsim validasyonu"""
        if not name:
            return False, f"{field_name} boş olamaz"
        
        if len(name) < 2:
            return False, f"{field_name} en az 2 karakter olmalı"
        
        if len(name) > 50:
            return False, f"{field_name} çok uzun"
        
        # Sadece harf ve boşluk
        if not re.match(r'^[a-zA-ZğüşıöçĞÜŞİÖÇ\s]+$', name):
            return False, f"{field_name} sadece harf içerebilir"
        
        return True, f"{field_name} geçerli"


def test_email_validation():
    """Email validasyon testleri"""
    print('\n🧪 Testing Email Validation...')
    
    validator = FormValidator()
    
    # Geçerli emailler
    valid_emails = [
        'test@example.com',
        'user.name@domain.co.uk',
        'admin@terramind.com',
        'test123@test.org'
    ]
    
    for email in valid_emails:
        is_valid, message = validator.validate_email(email)
        assert is_valid, f"Email '{email}' geçerli olmalı: {message}"
        print(f'✅ {email}: {message}')
    
    # Geçersiz emailler
    invalid_emails = [
        ('invalid-email', 'Geçersiz format'),
        ('test@', 'Eksik domain'),
        ('@example.com', 'Eksik kullanıcı adı'),
        ('test..test@example.com', 'Çift nokta'),
        ('test@example..com', 'Domain çift nokta'),
        ('', 'Boş email'),
        ('a' * 255 + '@example.com', 'Çok uzun email')
    ]
    
    for email, expected_error in invalid_emails:
        is_valid, message = validator.validate_email(email)
        assert not is_valid, f"Email '{email}' geçersiz olmalı: {message}"
        print(f'✅ {email}: {message}')


def test_password_validation():
    """Şifre validasyon testleri"""
    print('\n🧪 Testing Password Validation...')
    
    validator = FormValidator()
    
    # Geçerli şifreler
    valid_passwords = [
        'StrongPass123!',
        'MyPassword1@',
        'Test123#',
        'SecurePwd9$'
    ]
    
    for password in valid_passwords:
        is_valid, message = validator.validate_password(password)
        assert is_valid, f"Şifre '{password}' geçerli olmalı: {message}"
        print(f'✅ Şifre geçerli: {message}')
    
    # Geçersiz şifreler
    invalid_passwords = [
        ('weak', 'Çok kısa'),
        ('nouppercase123!', 'Büyük harf yok'),
        ('NOLOWERCASE123!', 'Küçük harf yok'),
        ('NoNumbers!', 'Rakam yok'),
        ('NoSpecial123', 'Özel karakter yok'),
        ('', 'Boş şifre'),
        ('a' * 130, 'Çok uzun şifre')
    ]
    
    for password, expected_error in invalid_passwords:
        is_valid, message = validator.validate_password(password)
        assert not is_valid, f"Şifre '{password}' geçersiz olmalı: {message}"
        print(f'✅ {password}: {message}')


def test_username_validation():
    """Kullanıcı adı validasyon testleri"""
    print('\n🧪 Testing Username Validation...')
    
    validator = FormValidator()
    
    # Geçerli kullanıcı adları
    valid_usernames = [
        'testuser',
        'user123',
        'test-user',
        'test_user',
        'admin'
    ]
    
    for username in valid_usernames:
        is_valid, message = validator.validate_username(username)
        assert is_valid, f"Kullanıcı adı '{username}' geçerli olmalı: {message}"
        print(f'✅ {username}: {message}')
    
    # Geçersiz kullanıcı adları
    invalid_usernames = [
        ('ab', 'Çok kısa'),
        ('', 'Boş kullanıcı adı'),
        ('user@name', 'Geçersiz karakter'),
        ('user name', 'Boşluk içeriyor'),
        ('a' * 51, 'Çok uzun')
    ]
    
    for username, expected_error in invalid_usernames:
        is_valid, message = validator.validate_username(username)
        assert not is_valid, f"Kullanıcı adı '{username}' geçersiz olmalı: {message}"
        print(f'✅ {username}: {message}')


def test_name_validation():
    """İsim validasyon testleri"""
    print('\n🧪 Testing Name Validation...')
    
    validator = FormValidator()
    
    # Geçerli isimler
    valid_names = [
        'Ahmet',
        'Mehmet Ali',
        'Ayşe',
        'Zeynep Güneş',
        'Ömer'
    ]
    
    for name in valid_names:
        is_valid, message = validator.validate_name(name)
        assert is_valid, f"İsim '{name}' geçerli olmalı: {message}"
        print(f'✅ {name}: {message}')
    
    # Geçersiz isimler
    invalid_names = [
        ('A', 'Çok kısa'),
        ('', 'Boş isim'),
        ('Ahmet123', 'Rakam içeriyor'),
        ('Ahmet@Ali', 'Geçersiz karakter'),
        ('a' * 51, 'Çok uzun')
    ]
    
    for name, expected_error in invalid_names:
        is_valid, message = validator.validate_name(name)
        assert not is_valid, f"İsim '{name}' geçersiz olmalı: {message}"
        print(f'✅ {name}: {message}')


def main():
    """Ana test fonksiyonu"""
    print('🚀 TerraMind Form Validation Tests Starting...')
    print('=' * 60)
    
    try:
        test_email_validation()
        test_password_validation()
        test_username_validation()
        test_name_validation()
        
        print('\n' + '=' * 60)
        print('🎉 All form validation tests passed!')
        print('✅ Email validation working correctly!')
        print('✅ Password validation working correctly!')
        print('✅ Username validation working correctly!')
        print('✅ Name validation working correctly!')
        print('✅ TerraMind form validation system is functional!')
        
    except AssertionError as e:
        print(f'❌ Test failed: {e}')
    except Exception as e:
        print(f'❌ Error: {e}')


if __name__ == '__main__':
    main()
