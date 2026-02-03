# AI-Generated Voice Detection API

## India AI Impact Buildathon Submission

A FastAPI-based REST API for detecting AI-generated voices in audio files across multiple Indian languages.

---

## Features

✅ **Multi-language Support**: Tamil, English, Hindi, Malayalam, Telugu  
✅ **Secure Authentication**: API key-based authentication via headers  
✅ **Base64 Audio Processing**: Accepts MP3 audio as base64 encoded strings  
✅ **Structured JSON Response**: Consistent response format with classification, confidence, and explanation  
✅ **Production Ready**: Includes error handling, validation, and proper status codes  
✅ **Easy Deployment**: Ready to deploy on Render.com  

---

## API Endpoint

### `POST /detect`

Detects whether an audio file contains AI-generated or human voice.

**Headers:**
```
x-api-key: buildathon_2024_secret_key
Content-Type: application/json
```

**Request Body:**
```json
{
  "language": "English",
  "audio_format": "mp3",
  "audio_base64": "BASE64_ENCODED_AUDIO_DATA_HERE"
}
```

**Response:**
```json
{
  "classification": "AI_GENERATED",
  "confidence_score": 0.8234,
  "language": "English",
  "explanation": "High confidence AI-generated English voice detected with synthetic speech patterns."
}
```

---

## Supported Values

**Languages:** `Tamil`, `English`, `Hindi`, `Malayalam`, `Telugu`  
**Audio Formats:** `mp3`  
**Classification:** `AI_GENERATED` or `HUMAN`  
**Confidence Score:** 0.0 to 1.0  

---

## Local Development

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 3. Test the API

**Health Check:**
```bash
curl http://localhost:8000/
```

**Voice Detection:**
```bash
curl -X POST http://localhost:8000/detect \
  -H "x-api-key: buildathon_2024_secret_key" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "English",
    "audio_format": "mp3",
    "audio_base64": "//uQxAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAACAAADhAC..."
  }'
```

---

## Deploying to Render.com

### Step 1: Create a New Web Service

1. Go to [Render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository or use "Deploy from Git URL"

### Step 2: Configure the Service

- **Name:** `ai-voice-detection-api`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** (Leave empty, Procfile will be used automatically)
- **Plan:** Free or paid tier

### Step 3: Environment Variables (Optional)

You can set the API key as an environment variable:

- Key: `API_KEY`
- Value: Your secure API key

Then modify `main.py` to read from environment:
```python
import os
VALID_API_KEY = os.getenv("API_KEY", "buildathon_2024_secret_key")
```

### Step 4: Deploy

Click **"Create Web Service"** and Render will automatically:
- Install dependencies from `requirements.txt`
- Use the `Procfile` to start the server
- Assign a public URL like `https://ai-voice-detection-api.onrender.com`

---

## Testing with Real Audio

### Convert MP3 to Base64

**Using Python:**
```python
import base64

with open("audio.mp3", "rb") as audio_file:
    audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
    print(audio_base64)
```

**Using Command Line (Linux/Mac):**
```bash
base64 -i audio.mp3 -o audio_base64.txt
```

**Using Command Line (Windows):**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("audio.mp3"))
```

---

## API Documentation

Once deployed, visit:
- **Interactive Docs:** `https://your-api-url.onrender.com/docs`
- **ReDoc:** `https://your-api-url.onrender.com/redoc`

---

## Adding Real AI Model (Future Enhancement)

Replace the `simulate_ai_detection()` function in `main.py` with your actual ML model:

```python
def simulate_ai_detection(audio_bytes: bytes, language: str) -> float:
    # Load your trained model
    model = load_your_model(language)
    
    # Extract features from audio
    features = extract_audio_features(audio_bytes)
    
    # Run inference
    prediction = model.predict(features)
    confidence_score = float(prediction[0])
    
    return confidence_score
```

---

## Security Notes

⚠️ **Change the API Key:** Update `VALID_API_KEY` in `main.py` to a secure value before production deployment.

⚠️ **Use Environment Variables:** Store sensitive data like API keys in environment variables, not in code.

⚠️ **Rate Limiting:** Consider adding rate limiting for production use (e.g., using `slowapi`).

---

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK:** Successful detection
- **400 Bad Request:** Invalid input data
- **401 Unauthorized:** Invalid or missing API key
- **500 Internal Server Error:** Server-side error

---

## Project Structure

```
.
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Procfile            # Render.com deployment config
└── README.md           # This file
```

---

## Support

For issues or questions about the buildathon submission, contact your team lead or refer to the buildathon documentation.

---

## License

This project is created for the India AI Impact Buildathon.

---

**Good luck with your buildathon! 🚀**
