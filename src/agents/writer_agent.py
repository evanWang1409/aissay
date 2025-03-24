from typing import Dict, List, Optional
from src.agents.base_agent import BaseAgent
import json
import math

class WriterAgent(BaseAgent):
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
        self.writing_context = {}
        self.actions = self.config.get("actions", [])
        
    def set_writing_context(self, context: Dict):
        """Set the writing context for the agent"""
        init_context = self.config["init_context"]
        self.conversation_history.append({"role": "system", "content": self.unify_prompts(init_context)})
        
        writing_context = self.config["writing_context"]
        writing_context_prompts = [
            writing_context["student_context"].format(student_context=context.get("student_context", "")),
            writing_context["essay_prompt"].format(essay_prompt=context.get("essay_prompt", "")),
        ]
        if "essay_context" in context and context["essay_context"] is not None:
            writing_context_prompts.append(writing_context["essay_context"].format(essay_context=context.get("essay_context", "")))
        if "style_preference" in context and context["style_preference"] is not None:
            writing_context_prompts.append(writing_context["style_preference"].format(style_preference=context.get("style_preference", "")))
        if "initial_ideas" in context and context["initial_ideas"] is not None:
            writing_context_prompts.append(writing_context["initial_ideas"].format(initial_ideas=context.get("initial_ideas", "")))
        
        # ai_vocab_prompt = self.config["ai_vocab_prompt"].format(ai_vocab=self.config.get("ai_vocab", []))
        # writing_context_prompts.append(ai_vocab_prompt)
        
        unified_prompt = self.unify_prompts(writing_context_prompts)
        self.conversation_history.append({"role": "user", "content": unified_prompt})
        self.latest_prompt = unified_prompt
    
    def random_sentence_selection(self, essay: str) -> List[str]:
        sentences = essay.split('.')
        sentences_clean = [s.strip() for s in sentences if s.strip() != ""]
        res = []
        # Select every 3 sentences
        for i in range(math.floor(len(sentences_clean)/3)):
            res.append(sentences_clean[i*3])
        return res

    def revise_by_sentences(self):
        """Revise the essay by selecting sentences"""
        prompt = "Please revise the essay by rewriting the following sentences in the essay to be more human and avoid common ai writing patterns and phrases.\n"
        sentences = self.random_sentence_selection(self.latest_response)
        prompt += "Here are the sentences:\n"
        for sentence in sentences:
            prompt += f"{sentence}.\n"
        prompt += "Only show the full revised essay."
        return self.generate_response(prompt)
        
    def revise_essay_by_sentences(self, essay: str, sentences: List[str]) -> str:
        """Rewrite sentences selected sentences in essay"""
        prompt = "Please revise the essay by rephrasing the following sentences in the essay to be more human and avoid common ai writing patterns and phrases.\n"
        prompt += f"Original Essay:\n{essay}\n"
        prompt += "Here are the sentences to rephrase:\n"
        for sentence in sentences:
            prompt += f"{sentence}.\n"
        prompt += "Only show the full revised essay."
        return self.generate_response(prompt)
        
        
    def get_action_prompt(self, action_name: str) -> str:
        """Get the prompt for a specific action"""
        for action in self.actions:
            if action["name"] == action_name:
                return action["prompts"]
        raise ValueError(f"Action {action_name} not found in actions")
    
    
    def execute_action(self, action_name: str, **kwargs) -> str:
        """Execute a specific action based on the agent's configuration"""
        prompt = self.get_action_prompt(action_name)
        return self.generate_response(prompt)
    
        
    def revise_outline(self, current_outline: str, feedback: str) -> str:
        """Revise the essay outline based on feedback"""
        prompt = f"""
        Please revise the following essay outline based on the feedback provided:
        
        Current Outline:
        {current_outline}
        
        Feedback:
        {feedback}
        
        Please provide an improved outline that addresses the feedback while maintaining a clear structure.
        """
        return self.generate_response(prompt)
    
    def dump_conversation_history(self, agent_type: str = 'writer') -> List[Dict]:
        return super().dump_conversation_history(agent_type)