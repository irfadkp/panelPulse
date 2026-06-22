#!/usr/bin/env python3
"""
AI Client Factory for PanelPulse
Creates appropriate AI client based on configuration
"""

import os
from typing import Optional
from .base_client import BaseAIClient
from .chatgpt_client import ChatGPTClient
from .gemini_client import GeminiClient


class AIClientFactory:
    """Factory for creating AI clients"""
    
    SUPPORTED_PROVIDERS = {
        'chatgpt': ChatGPTClient,
        'openai': ChatGPTClient,
        'gemini': GeminiClient,
        'google': GeminiClient,
    }
    
    @classmethod
    def create_client(
        cls,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ) -> BaseAIClient:
        """
        Create an AI client based on provider
        
        Args:
            provider: AI provider name (chatgpt, gemini, etc.)
                     If None, reads from AI_PROVIDER env var
            api_key: API key for the provider
                    If None, reads from provider-specific env var
            **kwargs: Additional provider-specific configuration
            
        Returns:
            Configured AI client instance
            
        Raises:
            ValueError: If provider is not supported or not configured
        """
        # Get provider from env if not specified
        if provider is None:
            provider = os.getenv('AI_PROVIDER', 'gemini').lower()
        else:
            provider = provider.lower()
        
        # Validate provider
        if provider not in cls.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"❌ Unsupported AI provider: {provider}\n"
                f"   Supported providers: {', '.join(cls.SUPPORTED_PROVIDERS.keys())}\n"
                f"   Set AI_PROVIDER in .env file to one of the supported providers"
            )
        
        # Get the client class
        client_class = cls.SUPPORTED_PROVIDERS[provider]
        
        # Create and return the client
        try:
            return client_class(api_key=api_key, **kwargs)
        except Exception as e:
            raise RuntimeError(
                f"❌ Failed to initialize {provider} client: {e}\n"
                f"   Please check your configuration in .env file"
            )
    
    @classmethod
    def list_providers(cls) -> list:
        """
        List all supported AI providers
        
        Returns:
            List of supported provider names
        """
        return list(cls.SUPPORTED_PROVIDERS.keys())
    
    @classmethod
    def get_provider_info(cls) -> dict:
        """
        Get information about all supported providers
        
        Returns:
            Dictionary with provider information
        """
        return {
            'chatgpt': {
                'name': 'OpenAI ChatGPT',
                'env_var': 'OPENAI_API_KEY',
                'signup_url': 'https://platform.openai.com/api-keys',
                'models': ['gpt-4', 'gpt-3.5-turbo', 'gpt-4-turbo']
            },
            'gemini': {
                'name': 'Google Gemini',
                'env_var': 'GEMINI_API_KEY',
                'signup_url': 'https://makersuite.google.com/app/apikey',
                'models': ['gemini-pro', 'gemini-pro-vision']
            }
        }
