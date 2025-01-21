# Ambrosio Voice Assistant Implementation

## Project Overview
Build a SOLID-compliant voice assistant named "Ambrosio" to control a smart home via voice commands in Portuguese.

---

## Requirements

### Core Features
1. Wake word detection ("Ambrosio" in Portuguese) using Porcupine.
2. Real-time Portuguese voice processing via OpenAI's Realtime API.
3. Control Home Assistant devices (lights, thermostats).
4. macOS/Raspberry Pi compatibility.
5. Extensible architecture for future tools (ElevenLabs, Koko AI, etc.).

### Technical Constraints
- Python 3.8+
- Strict SOLID principles compliance
- Production-grade error handling

---

## Code Implementation

### Directory Structure
```bash
ambrosio/
├── .env                    # API keys and config
├── requirements.txt        # Python dependencies
├── main.py                 # Entry point
├── core/
│   ├── interfaces.py       # Abstract base classes
│   └── di.py               # Dependency injection
├── integrations/
│   ├── voice_processing/
│   │   └── openai_realtime.py
│   ├── wake_word/
│   │   └── porcupine.py
│   └── smart_home/
│       └── home_assistant.py
├── utils/
│   ├── audio.py
│   └── logger.py
└── config/
    ├── system_prompt.txt   # Portuguese instructions
    └── settings.py         # Config validation
   