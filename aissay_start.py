import argparse
import json
from typing import Optional, Dict
from src.session import EssaySession

def parse_args():
    parser = argparse.ArgumentParser(description='AI Essay Writing Session')
    parser.add_argument('--password', '-p',
                       help='Password for API access',
                       required=True)
    parser.add_argument('--debug', '-d',
                       help='Use debug configuration instead of user input',
                       action='store_true',
                       default=True)  # Always true for now
    return parser.parse_args()

def load_debug_config() -> Dict:
    """Load debug configuration from file"""
    with open('configs/debug_inputs.json', 'r') as f:
        return json.load(f)

def get_required_inputs() -> dict:
    """Get required inputs from debug config"""
    config = load_debug_config()
    print("\n=== Loading Required Information from Debug Config ===")
    for key, value in config["required"].items():
        print(f"{key}: {value}")
    return config["required"]

def get_optional_inputs() -> dict:
    """Get optional inputs from debug config"""
    config = load_debug_config()
    print("\n=== Loading Optional Information from Debug Config ===")
    for key, value in config["optional"].items():
        print(f"{key}: {value}")
    return config["optional"]

def initialize_session(password: str) -> Optional[EssaySession]:
    """Initialize session with debug configuration"""
    # Create and initialize session
    print("\n=== Initializing Essay Writing Session (Debug Mode) ===")
    session = EssaySession(password)
    session.initialize_agents()
    
    # Get and set required inputs
    required = get_required_inputs()
    session.set_user_context(required["user_context"])
    session.set_essay_prompt(required["essay_prompt"])
    
    # Get and set optional inputs
    optional = get_optional_inputs()
    session.set_prompt_context(optional["prompt_context"])
    session.set_style_preference(optional["style_preference"])
    session.set_initial_ideas(optional["initial_ideas"])
        
    print("\n=== Session Initialized Successfully ===")
    return session

def confirm_inputs(session: EssaySession) -> bool:
    """Show current session settings (auto-confirm in debug mode)"""
    print("\n=== Current Session Settings (Debug Mode) ===")
    context = session.get_session_context()
    
    print("\nRequired Information:")
    print(f"Student Background: {context['user_context']}")
    print(f"Essay Prompt: {context['essay_prompt']}")
    
    print("\nOptional Information:")
    print(f"Additional Context: {context['prompt_context']}")
    print(f"Style Preferences: {context['style_preference']}")
    print(f"Key Ideas: {context['initial_ideas']}")
    
    print("\nAuto-confirming settings in debug mode...")
    return True

def main():
    args = parse_args()
    
    # Initialize session with debug config
    session = initialize_session(args.password)
    if not session:
        return
        
    # Auto-confirm in debug mode
    # confirm_inputs(session)
        
    print("\n=== Debug Session Ready ===")
    print("Session initialized successfully with debug configuration.")
    return session

if __name__ == "__main__":
    main() 