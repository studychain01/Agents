"""
LLM Configuration and Client Classes

This module contains the configuration settings and client implementation
for interacting with NVIDIA's API endpoints.
"""
import os
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv


class LLMConfig:
    """Configuration settings for the LLM."""
    base_url: str = "https://integrate.api.nvidia.com/v1"
    model: str = "mistralai/mixtral-8x7b-instruct-v0.1"
    max_tokens: int = 1024 
    default_temp: float = 0.5 


class NeMoLLaMa:
    """
    A class to interact with NVIDIA's API through their endpoints.
    This implementation uses AsyncOpenAI client for asynchronous operations.
    """

    def __init__(self, api_key: str):
        """Initialize NeMoLLaMa with API key.

        Args: 
            api_key (str): NVIDIA API authentication key
        """
        self.config = LLMConfig()
        self.client = AsyncOpenAI(
            base_url=self.config.base_url,
            api_key=api_key
        )
        self._is_authenticated = False 
    
    async def check_auth(self) -> bool:
        """Verify API authentication with test request. 
        
        Returns:
            bool: Authentication status

        Example:
            >>> is_valid = await llm.check_auth()
            >>> print(f"Authenticated: {is_valid}")
        """
        test_message = [{"role": "user", "content": "test"}]
        try:
            await self.agenerate(test_message, temperature=0.1)
            self._is_authenticated = True 
            return True 
        except Exception as e: 
            print(f"❌ Authentication failed: {str(e)}")
            return False

    async def agenerate(
        self,
        messages: List[Dict],
        temperature: Optional[float] = None
    ) -> str:
        """Generate text using the configured LLM model.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0, default from config)

        Returns:
            str: Generated text response

        Example:
            >>> messages = [
            ...     {"role": "system", "content": "You are a helpful assistant"},
            ...     {"role": "user", "content": "Plan my study schedule"}
            ... ]
            >>> response = await llm.agenerate(messages, temperature=0.7)
        """
        completion = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=temperature or self.config.default_temp,
            max_tokens=self.config.max_tokens,
            stream=False
        )
        return completion.choices[0].message.content


def configure_api_keys():
    """Configure and verify API keys for LLM services."""
    load_dotenv()
    api_key = os.getenv("NEMOTRON_4_340B_INSTRUCT_KEY")

    os.environ["NEMOTRON_4_340B_INSTRUCT_KEY"] = api_key

    is_configured = bool(os.getenv("NEMOTRON_4_340B_INSTRUCT_KEY"))
    print(f"API Key Configured: {is_configured}")
    return is_configured


def get_llm_instance():
    """Get a configured LLM instance."""
    api_key = os.getenv("NEMOTRON_4_340B_INSTRUCT_KEY")
    if not api_key:
        raise ValueError("NEMOTRON_4_340B_INSTRUCT_KEY not found in environment")
    return NeMoLLaMa(api_key)
