from typing import Dict, List, Optional
import json
import math
import random
from src.agents.base_agent import BaseAgent

class RevisorAgent(BaseAgent):
    def __init__(self, config_path: str, encryption_key: str, provider: str = None):
        # Load config first to get provider if not explicitly provided
        self.config_path = config_path
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Use provider from config if not explicitly provided
        config_provider = config.get("provider", "openai")
        provider = provider if provider is not None else config_provider
        
        # Initialize the base agent with the determined provider
        super().__init__(config_path, encryption_key, provider)
        
    def initialize_context(self, avoid_ai_vocab: bool = False):
        """Initialize the agent with its system context"""
        init_context = self.config.get("init_context", [])
        if avoid_ai_vocab:
            ai_vocab_prompt = self.config.get("ai_vocab_prompt", "").format(ai_vocab=self.config.get("ai_vocab", []))
            system_prompts = init_context + [ai_vocab_prompt]
        else:
            system_prompts = init_context
        
        unified_prompt = self.unify_prompts(system_prompts)
        self.conversation_history.append({"role": "system", "content": unified_prompt})
    
    def select_sentences_for_revision(self, sentences: List[str], percentage: float = 0.3) -> List[int]:
        """Select a percentage of sentences for revision"""
        num_to_select = max(1, int(len(sentences) * percentage))
        return random.sample(range(len(sentences)), num_to_select)
    
    def revise_by_sentences(self, essay: str, sentences_to_revise: List[str]) -> str:
        """Revise specified sentences in an essay"""
        
        sentences_prompt = '\n'.join(sentences_to_revise)

        prompt = (
            "Please revise the following essay by rephrasing only the specified sentences to sound more natural and human-like.\n"
            + "Maintain the original meaning and flow of the essay while avoiding common AI writing patterns and phrases.\n"
            + "Original Essay:\n"
            + essay
            + "\n"
            + "Sentences to revise (numbered as they appear in the essay):\n"
            + sentences_prompt
            + "\n"
            + "Provide only the complete revised essay itself. Do not include any other text such as 'Revised Essay:' or 'Original Essay:' or 'Sentences to revise:'."
        )

        return self.generate_response(prompt)
    
    def dump_conversation_history(self, agent_type: str = 'revisor') -> List[Dict]:
        return super().dump_conversation_history(agent_type)
    
    def revise_entire_essay(self, essay: str) -> str:
        """Revise an entire essay to make it sound more natural and human-like"""
        # Initialize context if not already done
        if not self.conversation_history:
            self.initialize_context()
            
        prompt = f"""
        Revise the following essay to sound more natural and human-like. 
        Maintain the original meaning and flow while avoiding common AI writing patterns and phrases.
        
        Original Essay:
        {essay}
        
        Provide only the complete revised essay itself. Do not include any other text such as "Revised Essay:" or "Original Essay:" or "Sentences to revise:".
        """
        
        return self.generate_response(prompt) 