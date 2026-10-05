# 👁️ VisioMate AI

An intelligent **voice-based assistant for visually impaired people**. Talk to it in English or Tamil/Tanglish
and it can describe surroundings, read text, identify currency, guide you to a place, remind you of medicines,
and send an emergency alert with your location.

## Features

| Feature | How it works | Say (examples) |
|---|---|---|
| 🎙️ Voice assistant | SpeechRecognition (STT) + pyttsx3 (offline TTS), keyword intent router | "help", "what time is it" |
| 🧭 Navigation | OpenStreetMap Nominatim + OSRM walking routes, turn-by-turn voice | "navigate to Gandhipuram bus stand", "next step" |
| 📦 Object detection | YOLOv8, reports object + left/front/right + distance (near/far) | "what is in front of me" |
| 🆘 Emergency SOS | Twilio SMS / Telegram with Google Maps link, 5s cancel window | "emergency", "kaapathunga" |
| 💵 Currency recognition | Custom YOLOv8 model for INR notes, adds up the total | "what note is this" |
| 💊 Medicine reminder | SQLite + background scheduler, spoken alerts | "remind me to take BP tablet at 8:30 pm" |
| 📖 OCR | Tesseract (English + Tamil) with image pre-processing | "read this text" |

## Project structure

```
visiomate-ai/
├── main.py                 # entry point
├── config.yaml             # language, models, SOS contacts
├── visiomate/
│   ├── assistant.py        # ties every feature together
│   ├── intents.py          # EN + Tamil/Tanglish command routing
│   ├── voice.py            # speech in/out
│   ├── navigation.py       # geocoding + routing
│   ├── sos.py              # emergency alerts
│   ├── reminders.py        # medicine reminders
│   └── vision/             # object_detection.py, currency.py, ocr.py
├── models/                 # put inr_currency.pt here
└── tests/
```

## Setup

```bash
git clone https://github.com/<your-username>/visiomate-ai.git
cd visiomate-ai
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

System dependencies:
- **Tesseract OCR**: `sudo apt install tesseract-ocr tesseract-ocr-tam` (Windows: UB-Mannheim installer)
- **PortAudio** (for PyAudio): `sudo apt install portaudio19-dev`

### Configure
1. Edit `config.yaml`: set `sos.contacts`, `language` (`en-IN` / `ta-IN`).
2. Set secrets as environment variables (never commit them):
```bash
export TWILIO_SID=... TWILIO_TOKEN=... TWILIO_FROM=+1...
export TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=...
```

### Run
```bash
python main.py          # voice mode
python main.py --text   # keyboard mode (testing without mic/speaker)
pytest                  # run tests
```

## Training the currency model
1. Collect/annotate INR note photos (both sides, different lighting) in YOLO format. Classes: `10, 20, 50, 100, 200, 500, 2000`.
2. Train: `yolo detect train data=currency.yaml model=yolov8n.pt epochs=60 imgsz=640`
3. Copy `runs/detect/train/weights/best.pt` to `models/inr_currency.pt`.

## ⚠️ Safety notes
- This is an **assistive aid, not a replacement** for a white cane or guide. Do not rely on it alone for safety-critical decisions.
- Default location is **IP-based (city-level only)**. For real navigation/SOS use a GPS module (e.g. `gpsd` on Raspberry Pi) or set `navigation.lat/lon`.
- Speech recognition (Google) and routing need internet. Object detection, OCR, reminders and TTS run offline.

## Roadmap
- [ ] Hardware SOS button (Raspberry Pi GPIO) + wearable camera
- [ ] Continuous obstacle warnings while walking
- [ ] Offline STT (Vosk / Whisper) and Tamil TTS
- [ ] Face recognition for known people
- [ ] Android app

## License
MIT
