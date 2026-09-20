# ElevenLabs Voice Demo (Python)

A small, real project built against the ElevenLabs API — the kind of
integration demo a Solutions Engineer builds for customers.

**What's here**

- `tts_demo.py` — CLI script: list voices, convert text to speech, save an MP3.
- `app.py` — FastAPI service wrapping the ElevenLabs API behind your own
  REST endpoints (`GET /voices`, `POST /speak`). This is the classic SE
  pattern: one stable contract for the customer, auth/validation/errors
  handled in one place.

**Setup**

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your key from https://elevenlabs.io
```

**Run**

```bash
python tts_demo.py --list-voices
python tts_demo.py --text "Hello from Toronto" --output hello.mp3

uvicorn app:app --reload
# POST {"text": "Hello"} to http://localhost:8000/speak
```

**Concepts this exercises**

- Python packaging & virtualenvs, `argparse` CLIs, environment-based config
- Iterators/generators: `convert()` streams byte chunks — written and
  proxied chunk-by-chunk instead of buffered in memory
- REST wrapper pattern: request validation with Pydantic, mapping vendor
  failures to clean HTTP status codes (400/502), streaming responses
- Third-party SDK integration: auth via API key, model/voice selection,
  output formats

**Try next**

- Add a `GET /health` endpoint that verifies the API key works
- Accept a `voice_settings` object (stability/similarity) per request
- Stream directly to the browser with chunked transfer and log latency
# elevenlabs-voice-demo
# elevenlabs-voice-demo
# elevenlabs-voice-demo
# elevenlabs-voice-demo
# elevenlabs-voice-demo
# elevenlabs-voice-demo
