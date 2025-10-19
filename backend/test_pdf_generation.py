#!/usr/bin/env python3
"""
Test script for PDF generation functionality
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.pdf_service import get_pdf_service

def test_environment_pdf_generation():
    """Test environment recommendation PDF generation"""
    print("🧪 Testing Environment PDF Generation...")
    
    try:
        pdf_service = get_pdf_service()
        
        # Test data
        test_data = {
            'crop': 'Domates',
            'location': 'Amasya',
            'region': 'Karadeniz',
            'soil_type': 'Kumlu Toprak',
            'irrigation_method': 'Damla Sulama',
            'fertilizer_type': 'Amonyum Sülfat',
            'sunlight': 'Güneşli'
        }
        
        print(f"📊 Test Data: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
        
        # Generate PDF
        result = pdf_service.generate_environment_recommendation_pdf(**test_data)
        
        if result['success']:
            print("✅ Environment PDF generated successfully!")
            print(f"📁 File path: {result['file_path']}")
            print(f"📄 Content preview: {result['content'][:200]}...")
            
            # Clean up
            pdf_service.cleanup_pdf_file(result['file_path'])
            print("🗑️ Test file cleaned up")
            
            return True
        else:
            print(f"❌ Environment PDF generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        return False

def test_crop_pdf_generation():
    """Test crop recommendation PDF generation"""
    print("\n🧪 Testing Crop PDF Generation...")
    
    try:
        pdf_service = get_pdf_service()
        
        # Test data
        test_data = {
            'location': 'Amasya',
            'region': 'Karadeniz',
            'soil_type': 'Kumlu Toprak',
            'sunlight': 'Güneşli',
            'irrigation_method': 'Damla Sulama',
            'fertilizer': 'Kompost',
            'ph': 6.5,
            'nitrogen': 120.0,
            'phosphorus': 60.0,
            'potassium': 225.0,
            'humidity': 26.0,
            'temperature': 23.0,
            'rainfall': 850.0,
            'top_3_predictions': [
                ['Domates', 0.8],
                ['Mısır', 0.7],
                ['Buğday', 0.6]
            ]
        }
        
        print(f"📊 Test Data: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
        
        # Generate PDF
        result = pdf_service.generate_crop_recommendation_pdf(**test_data)
        
        if result['success']:
            print("✅ Crop PDF generated successfully!")
            print(f"📁 File path: {result['file_path']}")
            print(f"📄 Content preview: {result['content'][:200]}...")
            
            # Clean up
            pdf_service.cleanup_pdf_file(result['file_path'])
            print("🗑️ Test file cleaned up")
            
            return True
        else:
            print(f"❌ Crop PDF generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting PDF Generation Tests...")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is available
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please set GOOGLE_API_KEY in your .env file")
        return
    
    print(f"🔑 API Key found: {api_key[:10]}...")
    
    # Run tests
    env_test_passed = test_environment_pdf_generation()
    crop_test_passed = test_crop_pdf_generation()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"  Environment PDF: {'✅ PASSED' if env_test_passed else '❌ FAILED'}")
    print(f"  Crop PDF: {'✅ PASSED' if crop_test_passed else '❌ FAILED'}")
    
    if env_test_passed and crop_test_passed:
        print("\n🎉 All tests passed! PDF generation is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
