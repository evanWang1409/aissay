import json
from typing import Dict, List, Optional
from src.utils.ai_convo_utils import AIConvoUtils

class BaseAgent:
    def __init__(self, config_path: str, encryption_key: str, provider: str = "openai"):
        self.encryption_key = encryption_key
        self.config = self._load_config(config_path)
        
        # Use provider from parameter or fall back to config
        self.provider = provider or self.config.get("provider", "openai")
        
        # Initialize AI Client
        self.ai_utils = AIConvoUtils(self.encryption_key)
        self.model_type = self.config.get("model_type", None)  # Will use default model if None
        self.client = self.ai_utils.setup_client(provider=self.provider)
        
        # Initialize Agent Context
        self.context = self.config.get("init_context", "")
        self.actions = self.config.get("actions", [])
        self.conversation_history = []
        
        # State Tracking
        self.latest_prompt = None
        self.latest_response = None
        
        
    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
        
        
    def unify_prompts(self, prompts: List[str]) -> str:
        """Unify a list of prompts into a single prompt"""
        return "\n".join(prompts) + "\n"
        
        
    def initialize(self):
        """
        Initialize the agent with the given context and actions
        """
        self.conversation_history.append({"role": "system", "content": self.context})
        
    def generate_response(self, new_user_input: str) -> str:
        """
        Generate a response from the AI Client from a new user input
        """
        self.conversation_history.append({"role": "user", "content": new_user_input})
        response = self.ai_utils.create_completion(
            client=self.client, 
            conversation_history=self.conversation_history, 
            provider=self.provider,
            model_type=self.model_type
        )
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Track State
        self.latest_prompt = new_user_input
        self.latest_response = response
        return response
            
    # def execute_action(self, action_name: str, **kwargs) -> str:
    #     action_config = next(
    #         (action for action in self.actions if action["name"] == action_name),
    #         None
    #     )
    #     if not action_config:
    #         raise ValueError(f"Action {action_name} not found")
            
    #     # Implementation will be provided by specific agents
    #     raise NotImplementedError 