from src.agents.writer_agent import WriterAgent
from src.agents.revisor_agent import RevisorAgent
from src.utils.gptzero_utils import GPTZeroUtils
from src.session import EssaySession

WRITER_AGENT_CONFIG = "configs/agents/writer_agent.json"
DETECTOR_AGENT_CONFIG = "configs/agents/detector_agent.json"
REVISOR_AGENT_CONFIG = "configs/agents/revisor_agent.json"

class EssayFlow:
    def __init__(self, session: EssaySession, PASSWORD: str = None):
        self.session = session
        
    def initialize_session(self, init_context: dict):
        # Initialize Session Inputs
        self.session.set_student_context(init_context["student_context"])
        self.session.set_essay_prompt(init_context["essay_prompt"])
        self.session.set_style_preference(init_context["style_preference"])
        if "initial_ideas" in init_context:
            self.session.set_initial_ideas(init_context["initial_ideas"])
        if "prompt_context" in init_context:
            self.session.set_prompt_context(init_context["prompt_context"])
            
        # Initialize Agents
        # self.session.initialize_agents() -- TODO: support multi-agents later
        self.session.writer = WriterAgent(WRITER_AGENT_CONFIG, self.session.encryption_key)
        self.session.writer.set_writing_context(init_context)
        self.session.detector = GPTZeroUtils(self.session.encryption_key, 0.8)
        self.session.revisor = RevisorAgent(REVISOR_AGENT_CONFIG, self.session.encryption_key)
        self.session.revisor.initialize_context(avoid_ai_vocab=False)
        
        
    def execute_flow(self):
        # Generate Initial Essay Outline
        # self.session.generate_outline() 
        
        # Write Essay
        initial_essay = self.session.write_essay()
        
        # Evaluate Essay
        # TODO: To be implemented
        
        # Check AI Detection
        # detection = self.session.detector.analyze_text(essay)
        # sentences_prob = self.session.detector.get_sentence_ai_probabilities(detection)
        
        # Revision with writer agent
        # revised_essay = self.session.writer.revise_by_sentences()
        
        # Revision with revisor agent for more human-like text
        sentences_to_revise = self.session.writer.random_sentence_selection(initial_essay)
        revised_essay = self.session.revise_essay_with_revisor(initial_essay, sentences_to_revise)
        
        # If still detecting AI, try full revision
        final_detection = self.session.detector.analyze_text(revised_essay)
        # if final_detection.get("completely_ai_probability", 0) > 0.7:
        #     final_essay = self.session.revise_essay_with_revisor(final_essay)
        sentences_prob = self.session.detector.get_sentence_ai_probabilities(final_detection)
        
        print("-"*100, "\n")
        print(f"Initila Essay: {initial_essay}")
        print("="*100, "\n")
        print(f"Final Essay: {revised_essay}")
        print("="*100, "\n")
        print(final_detection)
        print("="*100, "\n")
        print("Sentences Pred: ", sentences_prob)
        print("-"*100, "\n")
        
        self.session.writer.dump_conversation_history('writer')
        self.session.revisor.dump_conversation_history('revisor')
        self.session.detector.dump_result(final_detection)