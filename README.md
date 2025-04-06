# Sofi - Real-time Voice Recognition Assistant

Sofi is a real-time voice recognition system that continuously listens for a wake word and transcribes speech to text once activated.

## Features

- Continuous real-time voice recognition
- Wake word activation ("Sofi")
- Automatic microphone detection
- Cross-platform support (Windows, macOS, Linux)
- Customizable configuration
- Automatic ambient noise calibration

## Project Structure

```
.
├── voice_recognizer/           # Main package
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # Entry point for direct execution
│   ├── main.py                 # Main application file
│   ├── config/                 # Configurations
│   │   └── settings.py         # Application settings
│   ├── services/               # Services
│   │   ├── __init__.py
│   │   ├── microphone_service.py  # Microphone management
│   │   └── recognition_service.py # Voice recognition management
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── logging_utils.py    # Message handling utilities
│       └── exception_utils.py  # Error handling utilities
├── run.py                      # Launch script
├── requirements.txt            # Dependencies
└── README.md                   # Documentation
```

## Requirements

- Python 3.7+
- Required libraries (installable via requirements.txt):
  - SpeechRecognition
  - PyAudio
  - pydub

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

The program will listen through your default microphone and wait for the wake word "Sofi". Once activated, it will transcribe your speech to text and display it in the console for 10 seconds after the last detected speech.

### How It Works

1. The system continuously listens for the wake word "Sofi"
2. When "Sofi" is detected, the assistant is activated for 10 seconds
3. During this active period, all recognized speech is transcribed and displayed
4. Each new recognized phrase extends the active period
5. After 10 seconds of silence, the system returns to wake word detection mode

## Customization

The voice recognition settings can be modified in the `voice_recognizer/config/settings.py` file:

- Change the wake word
- Adjust the active listening timeout
- Modify sensitivity settings
- Change the language for recognition

## License

MIT

## Acknowledgments

This project uses Google's Speech Recognition API for speech-to-text conversion. 