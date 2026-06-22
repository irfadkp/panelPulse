#!/usr/bin/env python3
"""
Mock Client for PanelPulse
Simple rule-based responses without external AI service
"""

from typing import Optional
from .base_client import BaseAIClient


class MockClient(BaseAIClient):
    """Mock client that doesn't require external AI service"""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Mock client (no API key needed)
        
        Args:
            api_key: Not used, for compatibility
            **kwargs: Additional configuration
        """
        super().__init__(api_key, **kwargs)
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate simple rule-based response
        
        Args:
            prompt: Input prompt (not used in mock)
            max_tokens: Not used
            temperature: Not used
            **kwargs: Additional parameters (not used)
            
        Returns:
            Simple acknowledgment message
        """
        # Simple rule-based response
        return "Thank you for your answer. Let's move to the next question."
    
    def validate_credentials(self) -> bool:
        """
        Mock validation always succeeds
        
        Returns:
            Always True
        """
        return True
