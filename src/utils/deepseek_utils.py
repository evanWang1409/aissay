import json
from typing import Dict
from openai import OpenAI
from src.utils.encryption_utils import EncryptionUtils

API_KEYS_PATH = "configs/api_keys.json"

class DeepSeekUtils:
    def __init__(self, encryption_key: str):
        """
        This class should be stateless and containing only util functions for interaction with the DeepSeek API
        """
        self.encryption_key = encryption_key
        self.api_keys = self._load_api_keys()
        
    def _load_api_keys(self) -> Dict:
        with open(API_KEYS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)["deepseek"]
            
    def setup_deepseek(self) -> OpenAI:
        """
        Set up the DeepSeek client using the OpenAI SDK with DeepSeek's base URL
        """
        encrypted_key = self.api_keys["encrypted_api_key"]
        api_key = EncryptionUtils.decrypt_api_key(encrypted_key, self.encryption_key)
        
        # DeepSeek uses the OpenAI SDK with a different base URL
        return OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
    def create_completion(self, client: OpenAI, conversation_history: list[dict], model_type: str = "deepseek-chat", **kwargs) -> str:
        """
        Create a completion using the DeepSeek API
        
        Args:
            client: The DeepSeek client
            conversation_history: List of message dictionaries with role and content
            model_type: DeepSeek model to use (default: "deepseek-chat" which is DeepSeek-V3)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The content of the completion
        """
        response = client.chat.completions.create(
            model=model_type,
            messages=conversation_history,
            **kwargs
        )
        
        return response.choices[0].message.content 