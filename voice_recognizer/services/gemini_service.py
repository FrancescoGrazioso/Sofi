#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Service for interacting with Gemini API.
"""

import json
import requests
from voice_recognizer.config.api_settings import GEMINI_API_SETTINGS
from voice_recognizer.utils.logging_utils import print_error, print_api_response

class GeminiService:
    """
    Service for sending text to the Gemini API and processing responses.
    """
    
    def __init__(self):
        """
        Initialize the Gemini API service.
        """
        self.api_key = GEMINI_API_SETTINGS["api_key"]
        self.model = GEMINI_API_SETTINGS["model"]
        self.api_url = GEMINI_API_SETTINGS["api_url"]
        self.timeout = GEMINI_API_SETTINGS["timeout"]
        self.enabled = GEMINI_API_SETTINGS["enabled"]
        
    def is_configured(self):
        """
        Check if the service is properly configured.
        
        Returns:
            bool: True if the API key is set, False otherwise.
        """
        return self.api_key is not None and self.enabled
        
    def send_text(self, text):
        """
        Send text to the Gemini API.
        
        Args:
            text (str): The text to send to the API.
            
        Returns:
            dict: The API response or None if there was an error.
        """
        if not self.is_configured():
            print_error("Gemini API key non configurata o servizio disabilitato.")
            return None
            
        try:
            # Prepare request parameters
            url = f"{self.api_url}?key={self.api_key}"
            
            # Prepare the request payload
            payload = {
                "contents": [{
                    "parts": [{"text": text}]
                }]
            }
            
            # Send the request
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=self.timeout
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                
                # Extract and return the response text
                if "candidates" in response_data and len(response_data["candidates"]) > 0:
                    # Get the text from the first candidate
                    if "content" in response_data["candidates"][0]:
                        content = response_data["candidates"][0]["content"]
                        if "parts" in content and len(content["parts"]) > 0:
                            text = content["parts"][0].get("text", "")
                            print_api_response(text)
                            return response_data
                
                print_error("Struttura di risposta non valida dall'API Gemini.")
                return None
            else:
                print_error(f"Errore API Gemini: Codice {response.status_code}, {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print_error(f"Timeout durante la richiesta all'API Gemini (dopo {self.timeout}s).")
        except requests.exceptions.RequestException as e:
            print_error(f"Errore durante la richiesta all'API Gemini: {e}")
        except json.JSONDecodeError:
            print_error("Errore durante la decodifica della risposta JSON dall'API Gemini.")
        except Exception as e:
            print_error(f"Errore imprevisto durante l'interazione con Gemini API: {e}")
            
        return None 