"""
Test script for AI Voice Detection API
Run this after starting the server to verify everything works
"""

import requests
import base64
import json

# Configuration
API_URL = "http://localhost:8000"
API_KEY = "buildathon_2024_secret_key"

def create_dummy_audio_base64():
    """Create a small dummy MP3-like data for testing"""
    # This is just dummy data for testing - not a real MP3
    dummy_audio = b"MP3 DUMMY AUDIO DATA FOR TESTING" * 10
    return base64.b64encode(dummy_audio).decode('utf-8')

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check Endpoint")
    print("="*60)
    
    response = requests.get(f"{API_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Health check failed!"
    print("✅ Health check passed!")

def test_detect_valid_request():
    """Test the /detect endpoint with valid data"""
    print("\n" + "="*60)
    print("TEST 2: Valid Detection Request")
    print("="*60)
    
    audio_base64 = create_dummy_audio_base64()
    
    payload = {
        "language": "English",
        "audio_format": "mp3",
        "audio_base64": audio_base64
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{API_URL}/detect", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Valid request failed!"
    
    data = response.json()
    assert "classification" in data
    assert "confidence_score" in data
    assert "language" in data
    assert "explanation" in data
    assert data["classification"] in ["AI_GENERATED", "HUMAN"]
    assert 0.0 <= data["confidence_score"] <= 1.0
    
    print("✅ Valid detection request passed!")

def test_detect_invalid_api_key():
    """Test the /detect endpoint with invalid API key"""
    print("\n" + "="*60)
    print("TEST 3: Invalid API Key")
    print("="*60)
    
    audio_base64 = create_dummy_audio_base64()
    
    payload = {
        "language": "Tamil",
        "audio_format": "mp3",
        "audio_base64": audio_base64
    }
    
    headers = {
        "x-api-key": "wrong_api_key",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{API_URL}/detect", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 401, "Should return 401 for invalid API key!"
    print("✅ Invalid API key test passed!")

def test_detect_missing_api_key():
    """Test the /detect endpoint with missing API key"""
    print("\n" + "="*60)
    print("TEST 4: Missing API Key")
    print("="*60)
    
    audio_base64 = create_dummy_audio_base64()
    
    payload = {
        "language": "Hindi",
        "audio_format": "mp3",
        "audio_base64": audio_base64
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{API_URL}/detect", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 422, "Should return 422 for missing API key!"
    print("✅ Missing API key test passed!")

def test_detect_invalid_language():
    """Test the /detect endpoint with invalid language"""
    print("\n" + "="*60)
    print("TEST 5: Invalid Language")
    print("="*60)
    
    audio_base64 = create_dummy_audio_base64()
    
    payload = {
        "language": "French",  # Not supported
        "audio_format": "mp3",
        "audio_base64": audio_base64
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{API_URL}/detect", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 422, "Should return 422 for invalid language!"
    print("✅ Invalid language test passed!")

def test_detect_invalid_base64():
    """Test the /detect endpoint with invalid base64"""
    print("\n" + "="*60)
    print("TEST 6: Invalid Base64")
    print("="*60)
    
    payload = {
        "language": "Malayalam",
        "audio_format": "mp3",
        "audio_base64": "This is not valid base64!!!"
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{API_URL}/detect", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 422, "Should return 422 for invalid base64!"
    print("✅ Invalid base64 test passed!")

def test_all_languages():
    """Test detection with all supported languages"""
    print("\n" + "="*60)
    print("TEST 7: All Supported Languages")
    print("="*60)
    
    languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    audio_base64 = create_dummy_audio_base64()
    
    for language in languages:
        payload = {
            "language": language,
            "audio_format": "mp3",
            "audio_base64": audio_base64
        }
        
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.post(f"{API_URL}/detect", json=payload, headers=headers)
        print(f"\n{language}: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Classification: {data['classification']}")
            print(f"  Confidence: {data['confidence_score']}")
        
        assert response.status_code == 200, f"Failed for language: {language}"
    
    print("\n✅ All languages test passed!")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI VOICE DETECTION API - TEST SUITE")
    print("="*60)
    print(f"Testing API at: {API_URL}")
    print(f"Using API Key: {API_KEY}")
    
    try:
        test_health_check()
        test_detect_valid_request()
        test_detect_invalid_api_key()
        test_detect_missing_api_key()
        test_detect_invalid_language()
        test_detect_invalid_base64()
        test_all_languages()
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("="*60)
        print("\nYour API is ready for deployment!")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: Could not connect to {API_URL}")
        print("Make sure the server is running:")
        print("  python main.py")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    main()
