"""Test module for OpenAIUtils class."""
import argparse
from src.utils.deepseek_utils import DeepSeekUtils

PASSWORD = None

test_config_path = "configs/test/test_input.json"

def test_deepseek_utils():
    deepseek_util = DeepSeekUtils(PASSWORD)
    client = deepseek_util.setup_deepseek()
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Reply yes"},
    ]
    print(deepseek_util.create_completion(client, conversation_history))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--password', '-p',
                       required=True,
                       help='Password for encryption/decryption')
    PASSWORD = parser.parse_args().password
    test_deepseek_utils()