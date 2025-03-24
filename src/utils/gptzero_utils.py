import json, requests, os
from datetime import datetime
from typing import Dict, List
from src.utils.encryption_utils import EncryptionUtils

LOG_FILE_DIR = "logs"

class GPTZeroUtils:
    def __init__(self, encryption_key: str, threshold: float):
        self.encryption_key = encryption_key
        self.ai_probability_threshold = threshold
        encrypted_key = self._load_api_key()["encrypted_api_key"]
        self.api_key = EncryptionUtils.decrypt_api_key(encrypted_key, self.encryption_key)
        
        
    def _load_api_key(self) -> Dict:
        with open('configs/api_keys.json', 'r', encoding='utf-8') as f:
            return json.load(f)["gptzero"]

            
    def analyze_text(self, text: str) -> Dict:
        """Perform comprehensive AI detection analysis on the input text"""
        url = "https://api.gptzero.me/v2/predict/text"
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Api-Key": self.api_key
        }
        
        payload = {
            "document": text
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise exception for non-200 status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling GPTZero API: {str(e)}")
        
    def get_sentence_ai_probabilities(self, result):
        """Get AI probabilities for each sentence in the text"""
        sentences_pred = result["documents"][0]["sentences"]
        probabilities = []
        probabilities.extend(pred["generated_prob"] for pred in sentences_pred)
        return probabilities
    
    def dump_result(self, result):
        file_name = f"gptzero_result_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        log_file_path = os.path.join(LOG_FILE_DIR, file_name)
        with open(log_file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)
