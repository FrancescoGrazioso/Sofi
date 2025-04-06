#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main module for real-time voice recognition.
"""

import time

from voice_recognizer.services.microphone_service import MicrophoneService
from voice_recognizer.services.recognition_service import RecognitionService
from voice_recognizer.utils.logging_utils import (
    print_welcome,
    print_calibration_start,
    print_calibration_complete
)
from voice_recognizer.utils.exception_utils import (
    handle_keyboard_interrupt,
    handle_exception
)

def main():
    """
    Main function that starts voice recognition.
    """
    # Initialize services
    mic_service = MicrophoneService()
    recognition_service = RecognitionService()
    
    try:
        # Print welcome message
        print_welcome()
        
        # Initialize microphone
        microphone = mic_service.initialize_microphone()
        
        # Calibrate for ambient noise
        print_calibration_start()
        recognition_service.calibrate_for_ambient_noise(microphone)
        print_calibration_complete()
        
        # Start voice recognition
        recognition_service.start_recognition(microphone)
        
        # Keep the program running until Ctrl+C
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        handle_keyboard_interrupt(recognition_service)
    except Exception as e:
        handle_exception(e, recognition_service)

if __name__ == "__main__":
    main() 