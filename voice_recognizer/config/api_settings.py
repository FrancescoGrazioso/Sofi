#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API configurations for external services.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API settings
GEMINI_API_SETTINGS = {
    "api_key": os.getenv("GEMINI_API_KEY"),
    "model": "gemini-2.0-flash",
    "api_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
    "timeout": 10,  # Timeout for API requests in seconds
    "enabled": True,  # Enable or disable Gemini API integration
} 