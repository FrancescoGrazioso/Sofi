#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilities for log and system message management.
"""

import sys
from voice_recognizer.config.settings import DISPLAY_SETTINGS, KEYWORD_SETTINGS

def print_progress():
    """
    Print a progress indicator on the same line.
    """
    print(DISPLAY_SETTINGS["progress_indicator"], end="", flush=True)

def print_recognized_text(text):
    """
    Print the recognized text with formatting.
    
    Args:
        text (str): The recognized text.
    """
    if text:
        print(f"{DISPLAY_SETTINGS['text_prefix']}{text}")

def print_buffering_text(text):
    """
    Print the text being buffered with formatting to indicate it's waiting.
    
    Args:
        text (str): The text being buffered.
    """
    if text:
        print(f"{DISPLAY_SETTINGS['buffer_prefix']}{text} [...]", end="", flush=True)

def print_countdown(seconds):
    """
    Print a countdown before sending the text to the API.
    
    Args:
        seconds (int): Remaining seconds before sending.
    """
    print(DISPLAY_SETTINGS["buffer_countdown"] % seconds, end="", flush=True)

def print_keyword_detected():
    """
    Print a message indicating that the wake word has been detected.
    """
    print(DISPLAY_SETTINGS["keyword_detected_message"])

def print_info(message):
    """
    Print an informational message.
    
    Args:
        message (str): The message to print.
    """
    print(message)

def print_error(message):
    """
    Print an error message.
    
    Args:
        message (str): The error message to print.
    """
    print(f"\nError: {message}", file=sys.stderr)

def print_api_response(text):
    """
    Print the response received from the API.
    
    Args:
        text (str): The response text from the API.
    """
    if text:
        print(f"\nRisposta API: {text}")

def print_welcome():
    """
    Print the welcome message at application startup.
    """
    print("Continuous voice recorder initialized.")
    print("Speak into the microphone (press Ctrl+C to exit)...")
    print(f"Use the wake word '{KEYWORD_SETTINGS['keyword'].capitalize()}' to activate the assistant.")
    
def print_calibration_start():
    """
    Print the calibration start message.
    """
    print("\nCalibrating for ambient noise...")
    
def print_calibration_complete():
    """
    Print the calibration complete message.
    """
    print("Calibration complete. Start speaking!")
    
def print_exit():
    """
    Print the exit message.
    """
    print("\nRecording terminated.") 