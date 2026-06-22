#!/usr/bin/env python3
"""
Gemini Client for PanelPulse
Handles interactions with Google's Gemini API
"""

import os
import requests
from typing import Optional
from .base_client import BaseAIClient


class GeminiClient(BaseAIClient):
    """Client for Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro", **kwargs):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google API key (or set GEMINI_API_KEY env var)
            model: Model to use (gemini-pro, gemini-pro-vision, etc.)
            **kwargs: Additional configuration
        """
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = model
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
        if not self.api_key:
            raise ValueError(
                "❌ Gemini API key not found!\n"
                "   Set GEMINI_API_KEY in .env file or pass api_key parameter\n"
                "   Get your API key from: https://makersuite.google.com/app/apikey"
            )
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using Gemini
        
        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional Gemini-specific parameters
            
        Returns:
            Generated text
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": kwargs.get('top_p', 0.95),
                "topK": kwargs.get('top_k', 40),
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                raise RuntimeError("No response generated from Gemini")
                
        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"❌ Gemini API error: {e}\n"
                f"   Please check your GEMINI_API_KEY and internet connection"
            )
    
    def validate_credentials(self) -> bool:
        """
        Validate Gemini API credentials
        
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            # Try a simple generation to validate
            test_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}?key={self.api_key}"
            response = requests.get(test_url, timeout=10)
            return response.status_code == 200
        except:
            return False
