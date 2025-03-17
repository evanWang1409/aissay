"""Test module for OpenAIUtils class."""
import argparse
from src.utils.openai_utils import OpenAIUtils

test_config_path = "configs/test/test_input.json"
PASSWORD = None

def test_openai_utils():
    openai_util = OpenAIUtils(PASSWORD)
    client = openai_util.setup_openai()
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Reply yes"},
    ]
    print(openai_util.create_completion(client, conversation_history, "gpt-4o-mini"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--password', '-p',
                       required=True,
                       help='Password for encryption/decryption')
    PASSWORD = parser.parse_args().password
    test_openai_utils()