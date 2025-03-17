#!/usr/bin/env python3
import argparse
from src.session import EssaySession
from src.agents.writer_agent import WriterAgent
from src.agents.detector_agent import DetectorAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.utils.openai_utils import OpenAIUtils
from src.utils.gptzero_utils import GPTZeroUtils
from src.utils.encryption_utils import EncryptionUtils

PASSWORD = None


def setup_debug_env():
    """Setup debug environment with all components"""
    
    # Initialize utilities
    encryption = EncryptionUtils
    openai = OpenAIUtils(PASSWORD)
    gptzero = GPTZeroUtils(PASSWORD)
    
    # Initialize agents
    writer = WriterAgent("configs/agents/writer_agent.json", PASSWORD)
    detector = DetectorAgent("configs/agents/detector_agent.json", PASSWORD)
    evaluator = EvaluatorAgent("configs/agents/evaluator_agent.json", PASSWORD)
    
    # Initialize session
    essay_session = EssaySession(PASSWORD)
    essay_session.initialize_agents()
    
    return {
        "utils": {
            "encryption": encryption,
            "openai": openai,
            "gptzero": gptzero
        },
        "agents": {
            "writer": writer,
            "detector": detector,
            "evaluator": evaluator
        },
        "session": essay_session
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--password', '-p',
                       required=True,
                       help='Password for encryption/decryption')
    PASSWORD = parser.parse_args().password
    debug_env = setup_debug_env()
    print("\n=== Debug Environment Ready ===")
    print("Available components:")
    print("- debug_env['utils']: encryption, openai, gptzero")
    print("- debug_env['agents']: writer, detector, evaluator")
    print("- debug_env['session']: EssaySession instance")
    
    # Keep variables in global scope for interactive use
    utils = debug_env["utils"]
    agents = debug_env["agents"]
    session = debug_env["session"]
    
    print("\nComponents also available directly as: utils, agents, session") 