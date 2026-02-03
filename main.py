"""
AI-Generated Voice Detection API
India AI Impact Buildathon
"""

from fastapi import FastAPI, HTTPException, Header, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Literal
import base64
import random
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="AI Voice Detection API",
    description="API for detecting AI-generated voices in audio files",
    version="1.0.0"
)

# Configuration
VALID_API_KEY = "buildathon_2024_secret_key"  # Change this in production
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
SUPPORTED_FORMATS = ["mp3"]


# Request Model
class VoiceDetectionRequest(BaseModel):
    language: Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"] = Field(
        ...,
        description="Language of the audio file"
    )
    audio_format: Literal["mp3"] = Field(
        ...,
        description="Format of the audio file"
    )
    audio_base64: str = Field(
        ...,
        description="Base64 encoded audio data",
        min_length=1
    )

    @validator('audio_base64')
    def validate_base64(cls, v):
        """Validate that the audio_base64 is valid base64 encoding"""
        try:
            # Attempt to decode to verify it's valid base64
            base64.b64decode(v)
            return v
        except Exception:
            raise ValueError("Invalid base64 encoding for audio_base64")


# Response Model
class VoiceDetectionResponse(BaseModel):
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    language: str
    explanation: str


# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "active",
        "service": "AI Voice Detection API",
        "timestamp": datetime.utcnow().isoformat(),
        "buildathon": "India AI Impact Buildathon"
    }


# Main detection endpoint
@app.post("/detect", response_model=VoiceDetectionResponse)
async def detect_voice(
    request: VoiceDetectionRequest,
    x_api_key: str = Header(..., description="API authentication key")
):
    """
    Detect whether an audio file contains AI-generated or human voice.
    
    Args:
        request: VoiceDetectionRequest containing language, format, and audio data
        x_api_key: API key for authentication (header)
    
    Returns:
        VoiceDetectionResponse with classification, confidence, language, and explanation
    """
    
    # Authentication check
    if x_api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    try:
        # Decode base64 audio to prove we can handle audio data
        audio_bytes = base64.b64decode(request.audio_base64)
        audio_size_kb = len(audio_bytes) / 1024
        
        # Validate audio data is not empty
        if len(audio_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audio data is empty"
            )
        
        # TODO: Replace this with actual AI model inference
        # Placeholder logic for demonstration
        confidence_score = simulate_ai_detection(audio_bytes, request.language)
        
        # Determine classification based on confidence threshold
        classification = "AI_GENERATED" if confidence_score > 0.5 else "HUMAN"
        
        # Generate explanation based on result
        explanation = generate_explanation(
            classification, 
            confidence_score, 
            request.language,
            audio_size_kb
        )
        
        # Return structured response
        return VoiceDetectionResponse(
            classification=classification,
            confidence_score=round(confidence_score, 4),
            language=request.language,
            explanation=explanation
        )
    
    except base64.binascii.Error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid base64 encoding in audio_base64"
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


def simulate_ai_detection(audio_bytes: bytes, language: str) -> float:
    """
    Placeholder function to simulate AI voice detection.
    Replace this with actual ML model inference.
    
    Args:
        audio_bytes: Decoded audio data
        language: Language of the audio
    
    Returns:
        Confidence score between 0.0 and 1.0
    """
    # Use audio characteristics for deterministic randomness
    audio_hash = hash(audio_bytes[:min(1000, len(audio_bytes))])
    language_hash = hash(language)
    
    # Generate pseudo-random but consistent score
    random.seed(audio_hash + language_hash)
    base_score = random.uniform(0.1, 0.95)
    
    # Add small variation based on audio size
    size_variation = (len(audio_bytes) % 100) / 1000
    confidence_score = min(0.99, max(0.01, base_score + size_variation))
    
    return confidence_score


def generate_explanation(
    classification: str, 
    confidence: float, 
    language: str,
    audio_size_kb: float
) -> str:
    """
    Generate a human-readable explanation for the detection result.
    
    Args:
        classification: AI_GENERATED or HUMAN
        confidence: Confidence score
        language: Audio language
        audio_size_kb: Audio file size in KB
    
    Returns:
        Explanation string
    """
    if classification == "AI_GENERATED":
        if confidence > 0.85:
            return f"High confidence AI-generated {language} voice detected with synthetic speech patterns."
        elif confidence > 0.65:
            return f"Moderate confidence AI-generated {language} voice detected with some synthetic characteristics."
        else:
            return f"Low confidence AI-generated {language} voice detected, showing minor synthetic indicators."
    else:  # HUMAN
        if confidence < 0.35:
            return f"High confidence human {language} voice detected with natural speech characteristics."
        elif confidence < 0.5:
            return f"Moderate confidence human {language} voice detected with authentic vocal patterns."
        else:
            return f"Low confidence human {language} voice detected, showing mostly natural characteristics."


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
