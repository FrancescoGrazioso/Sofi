#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Service for microphone management.
"""

import speech_recognition as sr

class MicrophoneService:
    """
    Service for microphone management.
    """
    
    def __init__(self):
        """
        Initialize the microphone service.
        """
        self.microphone = None
        
    def initialize_microphone(self, device_index=None):
        """
        Initialize the microphone with the specified settings.
        
        Args:
            device_index (int, optional): Index of the microphone device to use.
                                         If None, the default microphone will be used.
        
        Returns:
            Microphone: The initialized microphone object.
        """
        self.microphone = sr.Microphone(device_index=device_index)
        return self.microphone
    
    def get_microphone(self):
        """
        Get the current microphone object.
        
        Returns:
            Microphone: The microphone object, or None if it has not been initialized.
        """
        return self.microphone
    
    def list_microphone_devices(self):
        """
        List all microphone devices available in the system.
        
        Returns:
            list: List of available microphone devices.
        """
        mic_list = sr.Microphone.list_microphone_names()
        return [(i, name) for i, name in enumerate(mic_list)]
    
    def print_available_microphones(self):
        """
        Print the list of available microphones.
        """
        devices = self.list_microphone_devices()
        
        print("\nAvailable microphones:")
        for index, name in devices:
            print(f"  [{index}] {name}")
        print("") 