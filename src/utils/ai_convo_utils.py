import json
from typing import Dict, Literal
from openai import OpenAI
from src.utils.encryption_utils import EncryptionUtils

API_KEYS_PATH = "configs/api_keys.json"

class AIConvoUtils:
    def __init__(self, encryption_key: str):
        """
        A unified class for interacting with AI conversation APIs (OpenAI and DeepSeek).
        This class should be stateless and contain only utility functions for API interactions.
        
        Args:
            encryption_key: The key used to decrypt API credentials
        """
        self.encryption_key = encryption_key
        self.api_keys = self._load_api_keys()
        
    def _load_api_keys(self) -> Dict:
        """Load API keys from the configuration file"""
        with open(API_KEYS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def setup_client(self, provider: Literal["openai", "deepseek"]) -> OpenAI:
        """
        Set up the client for the specified AI provider
        
        Args:
            provider: The AI provider to use ("openai" or "deepseek")
            
        Returns:
            An OpenAI client configured for the specified provider
        
        Raises:
            ValueError: If an invalid provider is specified
        """
        if provider not in ["openai", "deepseek"]:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai' or 'deepseek'")
            
        if provider == "openai":
            encrypted_key = self.api_keys["openai"]["encrypted_api_key"]
            api_key = EncryptionUtils.decrypt_api_key(encrypted_key, self.encryption_key)
            encrypted_organization = self.api_keys["openai"]["encrypted_organization"]
            organization = EncryptionUtils.decrypt_api_key(encrypted_organization, self.encryption_key)
            return OpenAI(api_key=api_key, organization=organization)
        else:  # provider == "deepseek"
            encrypted_key = self.api_keys["deepseek"]["encrypted_api_key"]
            api_key = EncryptionUtils.decrypt_api_key(encrypted_key, self.encryption_key)
            return OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com/v1"
            )
        
    def create_completion(self, 
                         client: OpenAI, 
                         conversation_history: list[dict], 
                         provider: Literal["openai", "deepseek"],
                         model_type: str = None,
                         **kwargs) -> str:
        """
        Create a completion using the specified AI provider
        
        Args:
            client: The OpenAI client configured for the specified provider
            conversation_history: List of message dictionaries with role and content
            provider: The AI provider to use ("openai" or "deepseek")
            model_type: Model to use (defaults to provider-specific default if None)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The content of the completion
            
        Raises:
            ValueError: If an invalid provider is specified
        """
        if provider not in ["openai", "deepseek"]:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai' or 'deepseek'")
            
        # Set default model based on provider if not specified
        if model_type is None:
            model_type = "gpt-4o-mini" if provider == "openai" else "deepseek-chat"
            
        response = client.chat.completions.create(
            model=model_type,
            messages=conversation_history,
            **kwargs
        )
        
        return response.choices[0].message.content 