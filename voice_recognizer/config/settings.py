#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Global configurations for voice recognition.
"""

# Recognition settings
RECOGNITION_SETTINGS = {
    # Recognition language (ISO standard code)
    "language": "it-IT",
    
    # Sensitivity adjustment settings
    "energy_threshold": 300,  # Energy threshold for audio detection
    "dynamic_energy_threshold": True,  # Automatically adjust threshold
    "pause_threshold": 0.3,  # Minimum pause time to consider a phrase completed
    "non_speaking_duration": 0.3,  # Minimum silence duration to consider phrase completed
    
    # Calibration
    "calibration_duration": 1,  # Duration of ambient noise calibration in seconds
    
    # Phrase segmentation
    "phrase_time_limit": 5,  # Maximum time limit for phrase in seconds
    
    # Buffer settings
    "buffer_delay": 2.0,  # Tempo di attesa in secondi prima di inviare il testo all'API
    "buffer_extension_time": 1.0,  # Tempo aggiuntivo di attesa quando viene aggiunto nuovo testo al buffer
    "max_buffer_hold_time": 10.0,  # Tempo massimo di attesa per il buffer prima dell'invio forzato
}

# Display settings
DISPLAY_SETTINGS = {
    "progress_indicator": ".",  # Character used as progress indicator
    "text_prefix": "\nYou said: ",  # Prefix for recognized text
    "keyword_detected_message": "\nWake word detected! Listening...",  # Message when wake word is detected
    "buffer_prefix": "\rTesto in attesa: ",  # Prefix for text being buffered
    "buffer_countdown": "\rInvio fra %d secondi... ",  # Countdown message format
}

# System settings
SYSTEM_SETTINGS = {
    "thread_join_timeout": 1,  # Timeout for thread termination wait
}

# Wake word settings
KEYWORD_SETTINGS = {
    "enabled": True,  # Enable or disable wake word activation
    "keyword": "sofi",  # The wake word that activates the assistant (lowercase)
    "timeout": 10,     # Time in seconds the assistant remains active after hearing the wake word
} 