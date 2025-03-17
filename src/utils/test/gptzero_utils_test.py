"""Test module for GPTZeroUtils class."""
import argparse
from src.utils.gptzero_utils import GPTZeroUtils
import json
import os

PASSWORD = None

def test_gptzero_utils(test_text: str):
    """Test the GPTZeroUtils class with sample text."""
    # Initialize GPTZeroUtils with encryption key and threshold
    gptzero_util = GPTZeroUtils(PASSWORD, 0.5)  # Using same encryption key as other tests
    
    # Test AI-generated text
    result = gptzero_util.analyze_text(test_text)
    print("Detection Result: ", result)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--password', '-p',
                       required=True,
                       help='Password for encryption/decryption')
    PASSWORD = parser.parse_args().password
    test_text = """
    My fascination with economics began with a simple yet powerful lesson in The Wolf of Wall Street—the "sell me this pen" exercise. This sparked my curiosity about supply and demand, leading me to explore the subject independently. I delved into books like The Road to Serfdom, gaining insights into economic systems and government intervention, and supplemented my learning with online courses on market structures and financial principles.

    To build a solid foundation, I took The Individual and the Economy course, where I analyzed economic models, financial planning, and policy impacts. Simultaneously, I participated in the 2023 Future Business Elite Youth Leadership Summit, where I deepened my understanding through advanced coursework in game theory, foreign exchange, and investment risks, winning the gold award in the final quiz competition.

    Eager to further challenge myself, I look forward to UC Berkeley’s Pre-College Program, where I can refine my analytical skills, engage with peers, and expand my economic knowledge in a dynamic academic environment.
    """
    test_gptzero_utils(test_text)