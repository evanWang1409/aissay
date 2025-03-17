from src.session import EssaySession

class EssayFlow:
    def __init__(self, session: EssaySession):
        self.session = session
        
    def execute_flow(self):
        self.session.initialize_agents()
        self.session.generate_outline()
        self.session.write_essay()
        self.session.evaluate_essay()
        self.session.check_ai_detection()
        self.session.revise_essay()
