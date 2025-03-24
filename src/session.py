from typing import Dict, Tuple, List
from src.agents.writer_agent import WriterAgent
from src.agents.detector_agent import DetectorAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.revisor_agent import RevisorAgent

class EssaySession:
    def __init__(self, encryption_key: str):
        self.encryption_key = encryption_key
        # Required context
        self.student_context = None  # Student background
        self.essay_prompt = None
        # Optional context
        self.prompt_context = None  # Essay context
        self.style_preference = None
        self.initial_ideas = None  # Key ideas for writing essay
        # Agents
        self.writer = None
        self.detector = None
        self.evaluator = None
        self.revisor = None
        # Session state
        self.max_revision_attempts = 10
        self.current_outline = None
        self.current_essay = None
        self.revision_count = 0
        
    def set_student_context(self, context: str):
        """Set student background context"""
        self.student_context = context
        
    def set_essay_prompt(self, prompt: str):
        """Set the main essay prompt"""
        self.essay_prompt = prompt
        
    def set_prompt_context(self, context: str):
        """Set additional context for the essay prompt"""
        self.prompt_context = context
        
    def set_style_preference(self, style: str):
        """Set preferred writing style"""
        self.style_preference = style
        
    def set_initial_ideas(self, ideas: str):
        """Set initial ideas for the essay"""
        self.initial_ideas = ideas
        
    def initialize_agents(self):
        """Initialize all required agents with appropriate context"""
        # self.writer = WriterAgent("configs/agents/writer_agent.json", self.encryption_key)
        # self.detector = DetectorAgent("configs/agents/detector_agent.json", self.encryption_key)
        # self.evaluator = EvaluatorAgent("configs/agents/evaluator_agent.json", self.encryption_key)
        # self.revisor = RevisorAgent("configs/agents/revisor_agent.json", self.encryption_key)
        # TODO: Implement multi-agent support
        
    def get_session_context(self) -> Dict:
        """Get the current session context"""
        return {
            "student_context": self.student_context,
            "essay_prompt": self.essay_prompt,
            "prompt_context": self.prompt_context,
            "style_preference": self.style_preference,
            "initial_ideas": self.initial_ideas
        }
        
    def get_high_probability_sentences(self, sentences_prob: Dict, threshold: float = 0.7) -> List[str]:
        """Extract sentences with high AI probability scores for targeted revision
        
        Args:
            sentences_prob: Dictionary mapping sentence text to AI probability
            threshold: Probability threshold above which sentences are considered highly AI-like
            
        Returns:
            List of sentences that exceed the probability threshold
        """
        high_prob_sentences = []
        for sentence, prob in sentences_prob.items():
            if prob > threshold:
                high_prob_sentences.append(sentence)
        return high_prob_sentences
        
    def generate_outline(self) -> str:
        """Generate initial essay outline"""
        self.writer.execute_action("generate_outline")
        return self.writer.latest_response
    
    def revise_outline(self, feedback: str) -> str:
        """Revise outline based on feedback"""
        if not self.current_outline:
            raise ValueError("No outline exists to revise")
            
        self.current_outline = self.writer.revise_outline(self.current_outline, feedback)
        return self.current_outline
        
    def write_essay(self) -> str:
        """Write essay based on the approved outline"""
        self.writer.execute_action("write")
        return self.writer.latest_response
        
    def evaluate_current_essay(self) -> Tuple[bool, Dict]:
        """Evaluate current essay for quality and relevance"""
        if not self.current_essay:
            raise ValueError("No essay available for evaluation")
            
        evaluation = self.evaluator.evaluate_essay(
            self.current_essay,
            self.get_session_context(),
            self.style_preference
        )
        
        return evaluation["passes_quality"], evaluation
        
    def detect_ai(self) -> Tuple[bool, Dict]:
        """Check essay for AI detection scores"""
        # detection = self.detector.analyze_essay(self.current_essay)
        # return detection["passes_threshold"], detection
        return None, None # TODO: Implement Full AI detection
        
    def revise_essay(self, feedback: Dict) -> str:
        """Revise essay based on feedback"""
        if not self.current_essay:
            raise ValueError("No essay available for revision")
            
        if self.revision_count >= self.max_revision_attempts:
            raise ValueError("Maximum revision attempts reached")
            
        self.current_essay = self.writer.revise_essay(self.current_essay, feedback)
        self.revision_count += 1
        return self.current_essay
        
    def revise_essay_with_revisor(self, essay: str, sentences: List[str]) -> str:
        """Revise essay using the revisor agent to make it more human-like
        
        Args:
            essay: The essay to revise, uses current_essay if not provided
            high_prob_sentences: Specific sentences to target for revision
            
        Returns:
            Revised essay
        """
        revised = self.revisor.revise_by_sentences(essay, sentences)
            
        self.current_essay = revised
        self.revision_count += 1
        return revised
        
    def process_essay(self) -> Dict:
        """Process the current essay through evaluation and AI detection"""
        # Check quality first
        passes_quality, evaluation = self.evaluate_current_essay()
        if not passes_quality:
            return {
                "status": "needs_revision",
                "reason": "quality",
                "feedback": evaluation
            }
            
        # If quality passes, check AI detection
        passes_ai, detection = self.detect_ai()
        if not passes_ai:
            return {
                "status": "needs_revision",
                "reason": "ai_detection",
                "feedback": detection
            }
            
        # Both checks passed
        return {
            "status": "complete",
            "evaluation": evaluation,
            "detection": detection
        }
        
    def can_revise(self) -> bool:
        """Check if more revisions are allowed"""
        return self.revision_count < self.max_revision_attempts
        
    def get_revision_count(self) -> int:
        """Get current number of revisions"""
        return self.revision_count 