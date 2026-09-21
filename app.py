Minimal voice service wrapping the ElevenLabs API.

A classic Solutions Engineer pattern: put a vendor API behind your own REST
service so a customer's app talks to one stable contract, and you control
auth, validation, and error mapping in one place.

Run:
    uvicorn app:app --reload

Endpoints:
    GET  /voices   -> [{"voice_id": ..., "name": ...}]
    POST /speak     -> audio/mpeg bytes   body: {"text": "...", "voice_id": "..."}
"""

import os

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Voice demo service")


def get_client() -> ElevenLabs:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY is not configured")
    return ElevenLabs(api_key=api_key)


class SpeakRequest(BaseModel):
    text: str
    voice_id: str = "cjVigY5qzO86Huf0OWal"
    model_id: str = "eleven_multilingual_v2"


@app.get("/voices")
def list_voices():
    client = get_client()
    try:
        response = client.voices.get_all()
    except Exception as e:  # surface vendor failures as a clean 502
        raise HTTPException(status_code=502, detail=f"ElevenLabs API error: {e}")
    return [{"voice_id": v.voice_id, "name": v.name} for v in response.voices]


@app.post("/speak")
def speak(req: SpeakRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text must not be empty")
    client = get_client()
    try:
        audio_stream = client.text_to_speech.convert(
            voice_id=req.voice_id,
            text=req.text,
            model_id=req.model_id,
            output_format="mp3_44100_128",
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"ElevenLabs API error: {e}")
    # Stream the vendor's byte iterator straight to the caller —
    # no buffering the whole file in memory.
    return StreamingResponse(audio_stream, media_type="audio/mpeg")
