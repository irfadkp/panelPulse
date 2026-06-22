#!/usr/bin/env python3
"""
Base AI Client for PanelPulse
Abstract base class for all AI provider implementations
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseAIClient(ABC):
    """Abstract base class for AI clients"""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize AI client
        
        Args:
            api_key: API key for the AI service
            **kwargs: Additional provider-specific configuration
        """
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using the AI service
        
        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def validate_credentials(self) -> bool:
        """
        Validate API credentials
        
        Returns:
            True if credentials are valid, False otherwise
        """
        pass
