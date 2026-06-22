#!/usr/bin/env python3
"""
ChatGPT Client for PanelPulse
Handles interactions with OpenAI's ChatGPT API
"""

import os
import requests
from typing import Optional
from .base_client import BaseAIClient


class ChatGPTClient(BaseAIClient):
    """Client for OpenAI ChatGPT API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4", **kwargs):
        """
        Initialize ChatGPT client
        
        Args:
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: Model to use (gpt-4, gpt-3.5-turbo, etc.)
            **kwargs: Additional configuration
        """
        super().__init__(api_key, **kwargs)
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError(
                "❌ OpenAI API key not found!\n"
                "   Set OPENAI_API_KEY in .env file or pass api_key parameter\n"
                "   Get your API key from: https://platform.openai.com/api-keys"
            )
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using ChatGPT
        
        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-2.0)
            **kwargs: Additional OpenAI-specific parameters
            
        Returns:
            Generated text
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"❌ ChatGPT API error: {e}\n"
                f"   Please check your OPENAI_API_KEY and internet connection"
            )
    
    def validate_credentials(self) -> bool:
        """
        Validate OpenAI API credentials
        
        Returns:
            True if credentials are valid, False otherwise
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
