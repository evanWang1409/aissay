from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.utils.gptzero_utils import GPTZeroUtils

class DetectorAgent(BaseAgent):
    def __init__(self, config_path: str, encryption_key: str):
        super().__init__(config_path, encryption_key)
        self.gptzero = GPTZeroUtils(encryption_key)