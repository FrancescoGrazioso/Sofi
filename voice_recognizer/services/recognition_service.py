#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Service for voice recognition management.
"""

import queue
import threading
import time
import speech_recognition as sr

from voice_recognizer.config.settings import RECOGNITION_SETTINGS, KEYWORD_SETTINGS, DISPLAY_SETTINGS
from voice_recognizer.utils.logging_utils import (
    print_recognized_text, 
    print_error, 
    print_progress,
    print_keyword_detected,
    print_buffering_text,
    print_countdown
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
        
        # Buffer per accumulare il testo prima di inviarlo
        self.text_buffer = ""
        self.buffer_timer = None
        self.buffer_lock = threading.Lock()
        self.countdown_timer = None
        self.forced_send_timer = None
        
        # Timestamp dell'ultimo testo aggiunto al buffer
        self.last_text_time = 0
        
        # Flag che indica se il countdown è visibile
        self.countdown_active = False
        
        # Configurazione del buffer
        self.buffer_delay = RECOGNITION_SETTINGS["buffer_delay"]
        self.buffer_extension = RECOGNITION_SETTINGS["buffer_extension_time"]
        self.max_buffer_hold_time = RECOGNITION_SETTINGS["max_buffer_hold_time"]
        
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
        self._force_send_buffer()  # Invia il buffer rimanente quando si disattiva la keyword
        
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
    
    def _force_send_buffer(self):
        """
        Forza l'invio del buffer corrente all'API, annullando qualsiasi timer attivo.
        """
        # Annulla tutti i timer attivi
        self._cancel_timers()
        
        # Invia il buffer all'API
        self._send_buffer_to_api()
    
    def _cancel_timers(self):
        """
        Annulla tutti i timer attivi relativi al buffer.
        """
        # Annulla il timer del buffer principale
        if self.buffer_timer is not None:
            self.buffer_timer.cancel()
            self.buffer_timer = None
        
        # Annulla il timer del countdown
        if self.countdown_timer is not None:
            self.countdown_timer.cancel()
            self.countdown_timer = None
            
        # Annulla il timer di invio forzato
        if self.forced_send_timer is not None:
            self.forced_send_timer.cancel()
            self.forced_send_timer = None
            
        # Resetta il flag del countdown
        self.countdown_active = False
    
    def _send_buffer_to_api(self):
        """
        Invia il buffer di testo corrente all'API Gemini e pulisce il buffer.
        """
        with self.buffer_lock:
            if self.text_buffer:
                # Stampa un messaggio che indica l'invio del testo buffered
                print_recognized_text(self.text_buffer + " (invio)")
                
                # Invia il testo all'API Gemini
                self.gemini_service.send_text(self.text_buffer)
                
                # Pulisce il buffer
                self.text_buffer = ""
                
                # Resetta il timestamp dell'ultimo testo
                self.last_text_time = 0
    
    def _start_countdown(self, seconds):
        """
        Avvia un countdown visibile per l'utente prima dell'invio del testo.
        
        Args:
            seconds (int): Secondi iniziali del countdown.
        """
        # Imposta il flag del countdown
        self.countdown_active = True
        
        def _countdown_step(remaining):
            """Step del countdown."""
            if remaining <= 0:
                # Se il countdown è terminato, invia il buffer
                self._send_buffer_to_api()
                self.countdown_active = False
                return
                
            # Stampa il countdown
            print_countdown(remaining)
                
            # Programma il prossimo step del countdown
            self.countdown_timer = threading.Timer(1.0, _countdown_step, [remaining - 1])
            self.countdown_timer.daemon = True
            self.countdown_timer.start()
        
        # Avvia il countdown
        _countdown_step(int(seconds))
    
    def _schedule_buffer_send(self):
        """
        Pianifica l'invio del buffer all'API dopo un ritardo.
        """
        # Annulla i timer precedenti
        self._cancel_timers()
        
        # Calcola il tempo passato dall'ultima aggiunta di testo
        time_since_last_text = time.time() - self.last_text_time
        
        # Se è passato troppo tempo, invia subito
        if time_since_last_text > self.buffer_delay and self.last_text_time > 0:
            self._send_buffer_to_api()
            return
            
        # Imposta il timer per l'avvio del countdown
        self.buffer_timer = threading.Timer(
            self.buffer_delay - 3.0 if self.buffer_delay > 3.0 else 0.1,  # Lascia almeno 3 secondi per il countdown o 0.1 se il buffer_delay è troppo piccolo
            self._start_countdown,
            [3]  # Countdown di 3 secondi
        )
        self.buffer_timer.daemon = True
        self.buffer_timer.start()
        
        # Imposta un timer di sicurezza per l'invio forzato dopo il tempo massimo
        if self.max_buffer_hold_time > 0:
            self.forced_send_timer = threading.Timer(
                self.max_buffer_hold_time,
                self._force_send_buffer
            )
            self.forced_send_timer.daemon = True
            self.forced_send_timer.start()
            
        # Mostra il testo buffered con indicazione visiva
        with self.buffer_lock:
            if self.text_buffer:
                print_buffering_text(self.text_buffer)
    
    def _add_to_buffer(self, text):
        """
        Aggiunge testo al buffer e pianifica l'invio.
        
        Args:
            text (str): Testo da aggiungere al buffer.
        """
        with self.buffer_lock:
            if self.text_buffer:
                # Se c'è già del testo nel buffer, aggiungi uno spazio prima del nuovo testo
                self.text_buffer += " " + text
            else:
                # Altrimenti, imposta il buffer al nuovo testo
                self.text_buffer = text
                
            # Aggiorna il timestamp dell'ultimo testo aggiunto
            self.last_text_time = time.time()
            
            # Mostra il testo buffered con indicazione visiva
            print_buffering_text(self.text_buffer)
            
        # Se il countdown è attivo, annulla tutto e riprogramma
        if self.countdown_active:
            self._cancel_timers()
            
        # Pianifica l'invio del buffer
        self._schedule_buffer_send()
        
    def _recognition_worker(self):
        """
        Worker thread that performs voice recognition.
        """
        while True:
            audio = self.audio_queue.get()
            
            # Exit signal
            if audio is None:
                # Invia il buffer rimanente prima di uscire
                self._force_send_buffer()
                break
                
            try:
                # Recognize audio using Google Speech Recognition
                text = self.recognizer.recognize_google(
                    audio, 
                    language=RECOGNITION_SETTINGS["language"]
                )
                
                # Check if the text contains the wake word or if the system is already active
                if self._check_for_keyword(text):
                    # Se contiene la parola chiave, rimuovila dal testo prima di bufferizzarlo
                    if KEYWORD_SETTINGS["keyword"].lower() in text.lower():
                        # Rimuovi solo la prima occorrenza della parola chiave (case insensitive)
                        keyword = KEYWORD_SETTINGS["keyword"].lower()
                        text_lower = text.lower()
                        start_index = text_lower.find(keyword)
                        if start_index != -1:
                            text = text[:start_index] + text[start_index + len(keyword):]
                            text = text.strip()
                    
                    # Aggiungi il testo al buffer solo se non è vuoto dopo la rimozione della keyword
                    if text:
                        self._add_to_buffer(text)
                
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
            
        # Cancel all buffer timers if active
        self._cancel_timers()
            
        # Send exit signal to worker thread
        self.audio_queue.put(None)
        
        # Wait for worker thread to terminate
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=1) 