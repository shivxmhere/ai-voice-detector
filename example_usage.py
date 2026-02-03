"""
Example usage script for AI Voice Detection API
This demonstrates how to use the API with actual audio files
"""

import base64
import requests
import json
import sys

def encode_audio_file(file_path):
    """
    Encode an audio file to base64
    
    Args:
        file_path: Path to the audio file
    
    Returns:
        Base64 encoded string
    """
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    return audio_base64

def detect_voice(api_url, api_key, language, audio_file_path):
    """
    Send audio file to the API for voice detection
    
    Args:
        api_url: Base URL of the API
        api_key: API authentication key
        language: Language of the audio (Tamil, English, Hindi, Malayalam, Telugu)
        audio_file_path: Path to the MP3 audio file
    
    Returns:
        API response as dictionary
    """
    # Encode the audio file
    print(f"📁 Reading audio file: {audio_file_path}")
    audio_base64 = encode_audio_file(audio_file_path)
    print(f"✅ Audio file encoded ({len(audio_base64)} characters)")
    
    # Prepare the request
    payload = {
        "language": language,
        "audio_format": "mp3",
        "audio_base64": audio_base64
    }
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Send the request
    print(f"\n🚀 Sending request to: {api_url}/detect")
    print(f"🌐 Language: {language}")
    
    response = requests.post(f"{api_url}/detect", json=payload, headers=headers)
    
    return response

def main():
    """Main function to demonstrate API usage"""
    
    # Configuration
    API_URL = "http://localhost:8000"  # Change to your deployed URL
    API_KEY = "buildathon_2024_secret_key"
    
    print("="*70)
    print("AI VOICE DETECTION API - EXAMPLE USAGE")
    print("="*70)
    
    # Check if audio file is provided
    if len(sys.argv) < 3:
        print("\n❌ Usage: python example_usage.py <language> <audio_file.mp3>")
        print("\nExample:")
        print("  python example_usage.py English sample_audio.mp3")
        print("\nSupported languages:")
        print("  - Tamil")
        print("  - English")
        print("  - Hindi")
        print("  - Malayalam")
        print("  - Telugu")
        sys.exit(1)
    
    language = sys.argv[1]
    audio_file = sys.argv[2]
    
    # Validate language
    valid_languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    if language not in valid_languages:
        print(f"\n❌ Invalid language: {language}")
        print(f"Supported languages: {', '.join(valid_languages)}")
        sys.exit(1)
    
    try:
        # Send request to API
        response = detect_voice(API_URL, API_KEY, language, audio_file)
        
        # Display results
        print("\n" + "="*70)
        print("📊 RESULTS")
        print("="*70)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n🎯 Classification: {result['classification']}")
            print(f"📈 Confidence Score: {result['confidence_score']:.4f}")
            print(f"🌐 Language: {result['language']}")
            print(f"💬 Explanation: {result['explanation']}")
            
            # Visual confidence bar
            confidence_percent = result['confidence_score'] * 100
            bar_length = 50
            filled_length = int(bar_length * result['confidence_score'])
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            print(f"\nConfidence: [{bar}] {confidence_percent:.1f}%")
            
            # Verdict
            print("\n" + "="*70)
            if result['classification'] == "AI_GENERATED":
                print("⚠️  VERDICT: This audio is likely AI-GENERATED")
            else:
                print("✅ VERDICT: This audio is likely from a HUMAN speaker")
            print("="*70)
            
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.json())
    
    except FileNotFoundError:
        print(f"\n❌ Error: Audio file not found: {audio_file}")
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to {API_URL}")
        print("Make sure the server is running!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
