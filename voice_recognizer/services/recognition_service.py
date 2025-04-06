#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Service for voice recognition management.
"""

import queue
import threading
import time
import speech_recognition as sr

from voice_recognizer.config.settings import RECOGNITION_SETTINGS, KEYWORD_SETTINGS
from voice_recognizer.utils.logging_utils import (
    print_recognized_text, 
    print_error, 
    print_progress,
    print_keyword_detected
)
from voice_recognizer.services.gemini_service import GeminiService

class RecognitionService:
    """
    Service for continuous voice recognition management.
    """
    
    def __init__(self):
        """
        Initialize the voice recognition service.
        """
        self.audio_queue = queue.Queue()
        self.recognizer = sr.Recognizer()
        self.stop_listening_callback = None
        self.worker_thread = None
        self.keyword_active = False
        self.keyword_timer = None
        self.gemini_service = GeminiService()
        self._configure_recognizer()
        
    def _configure_recognizer(self):
        """
        Configure the recognizer with the specified settings.
        """
        self.recognizer.energy_threshold = RECOGNITION_SETTINGS["energy_threshold"]
        self.recognizer.dynamic_energy_threshold = RECOGNITION_SETTINGS["dynamic_energy_threshold"]
        self.recognizer.pause_threshold = RECOGNITION_SETTINGS["pause_threshold"]
        self.recognizer.non_speaking_duration = RECOGNITION_SETTINGS["non_speaking_duration"]
    
    def calibrate_for_ambient_noise(self, microphone, duration=None):
        """
        Calibrate the recognizer for ambient noise.
        
        Args:
            microphone: Microphone object to use for calibration.
            duration (float, optional): Duration of calibration in seconds.
        """
        duration = duration or RECOGNITION_SETTINGS["calibration_duration"]
        
        with microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=duration)
    
    def _audio_callback(self, recognizer, audio):
        """
        Callback called when audio is detected.
        
        Args:
            recognizer: The recognizer that detected the audio.
            audio: The detected audio.
        """
        self.audio_queue.put(audio)
        print_progress()
    
    def _reset_keyword_timer(self):
        """
        Reset the timer for the wake word timeout.
        """
        if self.keyword_timer is not None:
            self.keyword_timer.cancel()
            
        # Create a new timer that deactivates the wake word after timeout
        self.keyword_timer = threading.Timer(
            KEYWORD_SETTINGS["timeout"], 
            self._deactivate_keyword
        )
        self.keyword_timer.daemon = True
        self.keyword_timer.start()
    
    def _activate_keyword(self):
        """
        Activate the wake word mode.
        """
        self.keyword_active = True
        print_keyword_detected()
        self._reset_keyword_timer()
    
    def _deactivate_keyword(self):
        """
        Deactivate the wake word mode.
        """
        self.keyword_active = False
        
    def _check_for_keyword(self, text):
        """
        Check if the text contains the wake word.
        
        Args:
            text (str): The text to check.
            
        Returns:
            bool: True if the wake word is present, False otherwise.
        """
        if not KEYWORD_SETTINGS["enabled"]:
            return True  # If wake word is disabled, always consider active
            
        if self.keyword_active:
            # If already active, reset the timer
            self._reset_keyword_timer()
            return True
            
        # Check if the text contains the wake word
        if KEYWORD_SETTINGS["keyword"].lower() in text.lower():
            self._activate_keyword()
            return True
            
        return False
        
    def _recognition_worker(self):
        """
        Worker thread that performs voice recognition.
        """
        while True:
            audio = self.audio_queue.get()
            
            # Exit signal
            if audio is None:
                break
                
            try:
                # Recognize audio using Google Speech Recognition
                text = self.recognizer.recognize_google(
                    audio, 
                    language=RECOGNITION_SETTINGS["language"]
                )
                
                # Check if the text contains the wake word or if the system is already active
                if self._check_for_keyword(text):
                    # Stampa il testo riconosciuto per il debug
                    print_recognized_text(text)
                    
                    # Invia il testo all'API Gemini invece di stamparlo
                    self.gemini_service.send_text(text)
                
            except sr.UnknownValueError:
                pass  # Ignore unrecognized audio
            except sr.RequestError as e:
                print_error(f"Error during service request: {e}")
            
            self.audio_queue.task_done()
    
    def start_recognition(self, microphone):
        """
        Start continuous voice recognition.
        
        Args:
            microphone: Microphone object to use for recording.
            
        Returns:
            function: Function to stop listening.
        """
        # Start the worker thread
        self.worker_thread = threading.Thread(target=self._recognition_worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        
        # Start listening in the background
        self.stop_listening_callback = self.recognizer.listen_in_background(
            microphone, 
            self._audio_callback, 
            phrase_time_limit=RECOGNITION_SETTINGS["phrase_time_limit"]
        )
        
        return self.stop_listening_callback
    
    def stop_recognition(self, wait_for_stop=False):
        """
        Stop voice recognition.
        
        Args:
            wait_for_stop (bool): If True, wait for listening to stop.
        """
        if self.stop_listening_callback:
            self.stop_listening_callback(wait_for_stop=wait_for_stop)
        
        # Cancel the wake word timer if active
        if self.keyword_timer:
            self.keyword_timer.cancel()
            
        # Send exit signal to worker thread
        self.audio_queue.put(None)
        
        # Wait for worker thread to terminate
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=1) 