# Sofi - Real-time Voice Recognition Assistant

Sofi is a real-time voice recognition system that continuously listens for a wake word and transcribes speech to text once activated, sending it to the Gemini API to generate responses that are then played through text-to-speech synthesis.

## Features

- Continuous real-time voice recognition
- Wake word activation ("Sofi")
- Automatic microphone detection
- Cross-platform support (Windows, macOS, Linux)
- Customizable configuration
- Automatic ambient noise calibration
- Integration with Gemini API for AI response generation
- Automatic cleaning of special characters from responses
- Voice playback of responses via text-to-speech
- Smart buffer system with countdown for recognized text

## Project Structure

```
.
├── voice_recognizer/           # Main package
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # Entry point for direct execution
│   ├── main.py                 # Main application file
│   ├── config/                 # Configurations
│   │   ├── settings.py         # Application settings
│   │   └── api_settings.py     # API settings
│   ├── services/               # Services
│   │   ├── __init__.py
│   │   ├── microphone_service.py  # Microphone management
│   │   ├── recognition_service.py # Voice recognition management
│   │   ├── gemini_service.py      # Gemini API service
│   │   └── tts_service.py         # Text-to-speech service
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── logging_utils.py    # Message handling utilities
│       └── exception_utils.py  # Error handling utilities
├── run.py                      # Launch script
├── requirements.txt            # Dependencies
├── .env.example                # Environment file example
└── README.md                   # Documentation
```

## Requirements

- Python 3.7+
- Required libraries (installable via requirements.txt):
  - SpeechRecognition
  - PyAudio
  - pydub
  - requests
  - python-dotenv
  - gTTS (Google Text-to-Speech)
  - pygame

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Sofi.git
   cd Sofi
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy the `.env.example` file to `.env`
   - Edit the `.env` file by adding your Gemini API key

## Usage

### Quick Start

Run the main script:

```bash
python run.py
```

Or run the module directly:

```bash
python -m voice_recognizer
```

The program will listen through your default microphone and wait for the wake word "Sofi". Once activated, it will transcribe your speech to text, send it to the Gemini API, and play back the response via speech synthesis.

### How It Works

1. The system continuously listens for the wake word "Sofi"
2. When "Sofi" is detected, the assistant is activated for 10 seconds
3. During this active period, all recognized speech is collected in a buffer
4. After a brief pause (configurable), the system displays a countdown
5. If no new speech is detected during the countdown, the text is sent to the Gemini API
6. The API response is cleaned of special characters and displayed in the console
7. The response is played back through speech synthesis
8. Each new recognized phrase extends the active period
9. After 10 seconds of silence, the system returns to wake word detection mode

## Customization

Voice recognition settings can be modified in the `voice_recognizer/config/settings.py` file:

- Change the wake word
- Adjust the active listening timeout
- Modify sensitivity settings
- Change the language for recognition
- Configure buffer and countdown timings

Gemini API settings can be modified in the `voice_recognizer/config/api_settings.py` file.

## License

MIT

## Acknowledgments

This project uses:
- Google's Speech Recognition API for speech-to-text conversion
- Gemini API for AI response generation
- gTTS (Google Text-to-Speech) for speech synthesis 