#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilities for exception and error handling.
"""

import sys
import traceback
from voice_recognizer.utils.logging_utils import print_error

def handle_keyboard_interrupt(recognition_service=None):
    """
    Handle keyboard interruption (Ctrl+C).
    
    Args:
        recognition_service: The recognition service to stop.
    """
    from voice_recognizer.utils.logging_utils import print_exit
    
    print_exit()
    
    if recognition_service:
        recognition_service.stop_recognition(wait_for_stop=False)
    
    sys.exit(0)

def handle_exception(e, recognition_service=None):
    """
    Handle a generic exception.
    
    Args:
        e: The caught exception.
        recognition_service: The recognition service to stop.
    """
    print_error(f"An error occurred: {e}")
    
    # In debug mode, print the full traceback
    if __debug__:
        traceback.print_exc()
    
    if recognition_service:
        recognition_service.stop_recognition(wait_for_stop=False)
    
    sys.exit(1) 