#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Service for text-to-speech functionality.
"""

import os
import re
import tempfile
from gtts import gTTS
import pygame
from voice_recognizer.utils.logging_utils import print_error, print_info

class TTSService:
    """
    Service for converting text to speech using gTTS (Google Text-to-Speech).
    """
    
    def __init__(self, language="it"):
        """
        Initialize the TTS service.
        
        Args:
            language (str): Language code for TTS synthesis.
        """
        self.language = language
        self.is_speaking = False
        self.temp_file = None
        
        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
        except Exception as e:
            print_error(f"Impossibile inizializzare l'audio per la sintesi vocale: {e}")
    
    def clean_text(self, text):
        """
        Rimuove caratteri speciali dal testo, mantenendo solo lettere, numeri e punteggiatura.
        
        Args:
            text (str): Testo da pulire.
            
        Returns:
            str: Testo pulito.
        """
        if not text:
            return ""
            
        # Mantieni solo lettere, numeri, punteggiatura e spazi
        # La regex conserva: lettere (compresi accenti), numeri, spazi, e punteggiatura comune
        cleaned_text = re.sub(r'[^\w\s.,;:!?"\'\(\)\-–—]', '', text, flags=re.UNICODE)
        return cleaned_text
    
    def speak(self, text):
        """
        Converte il testo in voce e lo riproduce.
        
        Args:
            text (str): Testo da convertire in voce.
            
        Returns:
            bool: True se la conversione e riproduzione hanno avuto successo, False altrimenti.
        """
        if not text or self.is_speaking:
            return False
            
        # Pulisce il testo dai caratteri speciali
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            print_error("Testo vuoto dopo la pulizia, niente da riprodurre.")
            return False
            
        # Crea un file temporaneo per salvare l'audio
        try:
            # Crea il file temporaneo
            fd, self.temp_file = tempfile.mkstemp(suffix='.mp3')
            os.close(fd)  # Chiudi il file descriptor
            
            # Genera il file audio con gTTS
            tts = gTTS(text=cleaned_text, lang=self.language, slow=False)
            tts.save(self.temp_file)
            
            # Riproduci l'audio
            self.is_speaking = True
            print_info("\nRiproduzione risposta vocale...")
            
            pygame.mixer.music.load(self.temp_file)
            pygame.mixer.music.play()
            
            # Attendi che l'audio finisca di riprodursi
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            self.is_speaking = False
            
            # Rimuovi il file temporaneo
            self._cleanup()
            
            return True
            
        except Exception as e:
            print_error(f"Errore durante la sintesi vocale: {e}")
            self.is_speaking = False
            self._cleanup()
            return False
    
    def _cleanup(self):
        """
        Pulisce le risorse temporanee.
        """
        # Rimuovi il file temporaneo se esiste
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
                self.temp_file = None
            except Exception as e:
                print_error(f"Errore durante la pulizia del file temporaneo: {e}") 