import json
from typing import Dict
from openai import OpenAI
from src.utils.encryption_utils import EncryptionUtils

API_KEYS_PATH = "configs/api_keys.json"

class OpenAIUtils:
    def __init__(self, encryption_key: str):
        """
        This class should be stateless and containing only util functions for interaction with the OpenAI
        """
        self.encryption_key = encryption_key
        self.api_keys = self._load_api_keys()
        
    def _load_api_keys(self) -> Dict:
        with open(API_KEYS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)["openai"]
            
    def setup_openai(self) -> OpenAI:
        encrypted_key = self.api_keys["encrypted_api_key"]
        api_key = EncryptionUtils.decrypt_api_key(encrypted_key, self.encryption_key)
        encrypted_organization = self.api_keys["encrypted_organization"]
        organization = EncryptionUtils.decrypt_api_key(encrypted_organization, self.encryption_key)
        return OpenAI(api_key=api_key, organization=organization)
        
    def create_completion(self, client: OpenAI, conversation_history: list[dict], model_type: str, **kwargs) -> str:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            **kwargs
        )
        
        return response.choices[0].message.content
