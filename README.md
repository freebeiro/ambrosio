# Ambrosio - Intelligent Voice Assistant

An intelligent voice assistant for smart home control, designed to interact with users in real-time voice conversations in European Portuguese (pt-PT). Ambrosio integrates with Home Assistant to manage and control smart home devices.

## Features

- **Wake Word Detection**: Utilizes Picovoice Porcupine for wake word detection, configured to respond to "Ambrosio" in European Portuguese.
- **Real-Time Voice Interaction**: Implements real-time voice recognition using OpenAI's API, ensuring low-latency responses and seamless user experience.
- **WebRTC Audio Streaming**: Provides low-latency audio streaming using WebRTC technology with STUN/TURN servers for NAT traversal and DTLS encryption for secure communication. Uses @roamhq/wrtc package for WebRTC implementation.
- **Smart Home Control**: Integrates with Home Assistant API to control smart devices, supporting operations like turning devices on/off and adjusting settings.
- **Language Support**: Focused on European Portuguese, handling common phrases and variations.
- **Extensible Architecture**: Modular components for voice processing, command parsing, and device control, allowing easy addition of new features.
- **Fuzzy Matching**: Implements fuzzy matching for device names and commands to enhance recognition accuracy.
- **Contextual Understanding**: Automatically selects devices based on room context.
- **Comprehensive Testing**: Includes a test suite for command validation and reliability.

## Requirements

- **Programming Language**: Python 3.9+
- **Voice Recognition**: OpenAI's real-time API
- **Wake Word Detection**: Picovoice Porcupine
- **Smart Home Integration**: Home Assistant API
- **Dependencies**:
  - `websocket-client` library
  - `picovoice` SDK
  - OpenAI API client (`openai` library)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/ambrosio.git
   cd ambrosio
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create and Configure `.env` File**:

   - Copy the example environment file:

     ```bash
     cp .env.example .env
     ```

   - Open `.env` and fill in your credentials:

     ```env
     PICOVOICE_ACCESS_KEY=your_picovoice_access_key
     OPENAI_API_KEY=your_openai_api_key
     HOME_ASSISTANT_URL=http://your-home-assistant:8123
     HOME_ASSISTANT_TOKEN=your_home_assistant_token
     ```

## Usage

Run the assistant:

```bash
python run_ambrosio.py
```

1. Say "Ambrósio" to activate the assistant.
2. The assistant will process your voice commands in real-time using OpenAI's API.

## Valid Commands

### Turn ON commands (use any of these words):

- "liga" or "ligar"
- "acende" or "acender"
- "ativa" or "ativar"

### Turn OFF commands (use any of these words):

- "desliga" or "desligar"
- "apaga" or "apagar"
- "desativa" or "desativar"

### Device/Location Commands:

1. **Living Room (Sala)**:
   - "luz do teto" or "luz do tecto" (ceiling light)
   - "luz da tv" or "luz da televisão" (TV wall light)
   - "luz do sofá" or "luz do sofa" (sofa lamp)
   - "luzes da sala" (all living room lights)
   - "zona da tv" (TV area lights - TV wall light + sofa lamp)

2. **Office (Escritório)**:
   - "luz do escritório" (office light)

3. **Entrance (Entrada)**:
   - "luz da entrada" (entrance light)

4. **Bathroom (Casa de Banho)**:
   - "luz principal da casa de banho" (main bathroom light)
   - "luz auxiliar da casa de banho" (auxiliary bathroom light)

5. **Master Bathroom (Casa de Banho Principal)**:
   - "luz principal da casa de banho principal" (main master bathroom light)
   - "luz auxiliar da casa de banho principal" (auxiliary master bathroom light)

6. **Kitchen (Cozinha)**:
   - "luz da cozinha"

## Project Structure

- **ambrosio/**: Root directory of the project.
  - `README.md`: Project documentation.
  - `CONTEXT.md`: Current project context and development tasks.
  - `.env`: Environment variables for sensitive credentials.
  - `requirements.txt`: List of all required Python packages.
  - `run_ambrosio.py`: Main script to run the assistant.
  - **src/**: Source code directory.
    - `voice_interface.py`: Handles voice input and output.
    - `wake_word.py`: Implements wake word detection using Picovoice.
    - `home_assistant_control.py`: Manages communication with Home Assistant.
    - `command_parser.py`: Parses and handles voice commands.
    - `text_to_speech.py`: Converts text responses to speech output.
    - `utils.py`: Utility functions.

## Additional Notes

- **Security**: Ensure that all API keys and tokens are kept secure. Do not commit the `.env` file to version control.
- **Privacy**: The assistant should prioritize user privacy and handle all voice data responsibly.
- **Collaboration**: Contributions are welcome. Please adhere to the coding standards and guidelines outlined in `CONTRIBUTING.md` (to be created).
- **Documentation**: Maintain comprehensive documentation for each module to assist future developers and AI workers.
- **Version Control**: Regularly commit changes with clear and descriptive messages.
