from typing import Dict, List, Optional
from src.agents.base_agent import BaseAgent
from src.utils.openai_utils import OpenAIUtils

class EvaluatorAgent(BaseAgent):
    def __init__(self, config_path: str, encryption_key: str):
        super().__init__(config_path, encryption_key)
        self.openai = OpenAIUtils(encryption_key)
        
    def evaluate_essay(self, essay: str, context: Dict, style_reference: Optional[str] = None) -> Dict:
        """Evaluate essay quality, factual correctness, and relevance"""
        evaluation_prompt = f"""
        Please evaluate the following essay based on these criteria:
        1. Factual correctness
        2. Relevance to the prompt
        3. Coherence and flow
        4. Argument strength
        5. Style matching (if reference provided)
        
        Essay Prompt: {context['essay_prompt']}
        Context: {context.get('prompt_context', 'None provided')}
        Student Background: {context['user_context']}
        
        Essay:
        {essay}
        
        {f'Style Reference: {style_reference}' if style_reference else ''}
        
        Provide a structured evaluation with specific examples and suggestions for improvement.
        Focus on both strengths and areas needing improvement.
        """
        
        evaluation = self.openai.create_completion(evaluation_prompt, temperature=0.3)
        
        # Generate specific improvement suggestions
        suggestions = self.generate_improvement_suggestions(essay, evaluation)
        
        # Check factual accuracy
        factual_check = self.check_factual_accuracy(essay, context)
        
        return {
            "evaluation": evaluation,
            "suggestions": suggestions,
            "factual_check": factual_check,
            "passes_quality": self._assess_quality_pass(evaluation, factual_check)
        }
        
    def check_factual_accuracy(self, essay: str, context: Dict) -> Dict:
        """Check the factual accuracy of claims made in the essay"""
        prompt = f"""
        Conduct a thorough fact-check of the following essay:
        1. Identify all factual claims
        2. Verify accuracy of each claim
        3. Note any misrepresentations or inaccuracies
        4. Suggest corrections if needed
        
        Essay:
        {essay}
        
        Context:
        {context.get('prompt_context', 'None provided')}
        
        Provide a structured analysis of factual accuracy with specific examples.
        """
        
        fact_check = self.openai.create_completion(prompt, temperature=0.2)
        return {
            "analysis": fact_check,
            "passes_fact_check": "inaccurate" not in fact_check.lower() and "incorrect" not in fact_check.lower()
        }
        
    def generate_improvement_suggestions(self, essay: str, evaluation: str) -> List[Dict]:
        """Generate specific suggestions for improving the essay"""
        prompt = f"""
        Based on the following evaluation, generate specific, actionable suggestions for improving the essay:
        
        Evaluation:
        {evaluation}
        
        Please provide suggestions in these categories:
        1. Content and Arguments
        2. Structure and Organization
        3. Style and Language
        4. Evidence and Support
        
        For each category, provide specific examples and clear recommendations.
        """
        
        suggestions_text = self.openai.create_completion(prompt, temperature=0.5)
        
        return [
            {
                "category": "improvements",
                "suggestions": suggestions_text
            }
        ]
        
    def _assess_quality_pass(self, evaluation: str, factual_check: Dict) -> bool:
        """Determine if the essay passes the quality threshold"""
        # Check for critical issues in evaluation
        critical_issues = [
            "major issues",
            "significant problems",
            "fails to address",
            "off-topic",
            "incoherent"
        ]
        
        has_critical_issues = any(issue in evaluation.lower() for issue in critical_issues)
        passes_fact_check = factual_check.get("passes_fact_check", False)
        
        return not has_critical_issues and passes_fact_check
        
    def execute_action(self, action_name: str, **kwargs) -> str:
        """Execute a specific action based on the agent's configuration"""
        if action_name == "evaluate_essay":
            return self.evaluate_essay(
                kwargs.get("essay", ""),
                kwargs.get("context", {}),
                kwargs.get("style_reference", None)
            )
        elif action_name == "check_facts":
            return self.check_factual_accuracy(
                kwargs.get("essay", ""),
                kwargs.get("context", {})
            )
        elif action_name == "generate_suggestions":
            return self.generate_improvement_suggestions(
                kwargs.get("essay", ""),
                kwargs.get("evaluation", "")
            ) 